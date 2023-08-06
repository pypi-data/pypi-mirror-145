from typing import Optional
import time
import uuid

from stock_client.constants import StockAdjustmentType, Warehouse
from stock_service.config import Config
from stock_service.controllers.adjustment_controller import create_adjustment
from stock_service.controllers.inventory_controller import set_stock_levels
from stock_service.controllers.stock_adjustment_controller import (
    create_stock_adjustment,
)
from stock_service.controllers.stock_controller import (
    get_or_create_take2_stock,
    update_take2_stock,
)
from stock_service.controllers.stock_snapshot_controller import (
    create_take2_stock_snapshot,
)
from stock_service.external.merchant_returns import get_good_stock_on_hold_by_product_id
from stock_service.external.tal import products
from stock_service.external.tal.orderitems_status_snapshots import (
    create_orderitem_snapshot,
    get_orderitem_on_hold_quantity,
)
from stock_service.producers import send_stock_update_notify_event
from stock_service.producers.stock_producer import StockAdjustmentProducer
from stock_service.stock_management.adjustment import adjust_stock_quanities
from stock_service.utils import stats
from stock_service.utils.tools import take2_stock_to_local_stock

DEFAULT_OWNER_ID = 1  # Takealot
config = Config()

legacy_stock_movement_producer = StockAdjustmentProducer(
    topic=config.service_config.get("stock_service.stock_movement_topic")
)


@stats.profile_with_stats(namespace="managers")
def adjust_stock_await(
    product_id: int,
    warehouse_id: int,
    quantity: int,
    old_reason_code: int,
    new_reason_code: int,
    customer_id: Optional[int] = None,
    instruction_id: Optional[int] = None,
    advanced_shipping_notification: Optional[str] = None,
    is_prepaid_voucher: Optional[bool] = False,
    license_plate_number: Optional[str] = None,
    trace_id: Optional[str] = None,
    return_reference_number: Optional[str] = None,
    group_number: Optional[int] = None,
    sequence_number: Optional[int] = None,
):

    start_time = time.perf_counter()

    with config.stats_client.timer(
        "managers.update_stock_managers.adjust_stock_await.do_stock_adjustment"
    ):
        stock_adjustment = do_stock_adjustment(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            old_reason_code=old_reason_code,
            new_reason_code=new_reason_code,
            customer_id=customer_id,
            instruction_id=instruction_id,
            advanced_shipping_notification=advanced_shipping_notification,
            is_prepaid_voucher=is_prepaid_voucher,
            license_plate_number=license_plate_number,
            trace_id=trace_id,
            return_reference_number=return_reference_number,
            group_number=group_number,
            sequence_number=sequence_number,
            asynchronous=False,
        )

    elapsed_time = time.perf_counter() - start_time

    if elapsed_time > 20:
        config.stats_client.incr(
            "managers.update_stock_managers.adjust_stock_await.do_stock_adjustment.timeout"
        )
        config.stats_client.incr(
            "managers.update_stock_managers.adjust_stock_await.do_stock_adjustment.timeout.adjustment_type."
            f"{new_reason_code}"
        )
        config.logger.error(
            "do_stock_adjustment took longer than 20s | elapsed_time=%ss, trace_id=%s, "
            "product_id=%s, warehouse_id=%s, quantity=%s, new_reason_code=%s, group_number=%s, "
            "sequence_number=%s",
            elapsed_time,
            trace_id,
            product_id,
            warehouse_id,
            quantity,
            new_reason_code,
            group_number,
            sequence_number,
        )

    elif elapsed_time > 15:
        config.stats_client.incr(
            "managers.update_stock_managers.adjust_stock_await.do_stock_adjustment.slow_call.adjustment_type."
            f"{new_reason_code}"
        )
        config.logger.warning(
            "do_stock_adjustment took longer than 15s | elapsed_time=%ss, trace_id=%s, "
            "product_id=%s, warehouse_id=%s, quantity=%s, new_reason_code=%s, group_number=%s,"
            "sequence_number=%s",
            elapsed_time,
            trace_id,
            product_id,
            warehouse_id,
            quantity,
            new_reason_code,
            group_number,
            sequence_number,
        )

    return stock_adjustment


def adjust_stock_async(
    product_id: int,
    warehouse_id: int,
    quantity: int,
    old_reason_code: int,
    new_reason_code: int,
    customer_id: Optional[int] = None,
    instruction_id: Optional[int] = None,
    advanced_shipping_notification: Optional[str] = None,
    is_prepaid_voucher: Optional[bool] = False,
    license_plate_number: Optional[str] = None,
    trace_id: Optional[str] = None,
    return_reference_number: Optional[str] = None,
    group_number: Optional[int] = None,
    sequence_number: Optional[int] = None,
):

    return do_stock_adjustment(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
        old_reason_code=old_reason_code,
        new_reason_code=new_reason_code,
        customer_id=customer_id,
        instruction_id=instruction_id,
        advanced_shipping_notification=advanced_shipping_notification,
        is_prepaid_voucher=is_prepaid_voucher,
        license_plate_number=license_plate_number,
        trace_id=trace_id,
        return_reference_number=return_reference_number,
        group_number=group_number,
        sequence_number=sequence_number,
        asynchronous=True,
    )


def do_stock_adjustment(
    product_id: int,
    warehouse_id: int,
    quantity: int,
    old_reason_code: int,
    new_reason_code: int,
    customer_id: Optional[int] = None,
    instruction_id: Optional[int] = None,
    advanced_shipping_notification: Optional[str] = None,
    is_prepaid_voucher: Optional[bool] = False,
    license_plate_number: Optional[str] = None,
    trace_id: Optional[str] = None,
    return_reference_number: Optional[str] = None,
    group_number: Optional[int] = None,
    sequence_number: Optional[int] = None,
    asynchronous: Optional[bool] = False,
):

    if not trace_id:
        trace_id = str(uuid.uuid4())

    config.logger.info(
        'Adjusting stock for: "product_id": %s, "warehouse_id": %s, "quantity": %s, "old_reason_code": %s, '
        '"new_reason_code": %s, "customer_id": %s, "instruction_id": %s, "advanced_shipping_notification: %s", '
        '"is_prepaid_voucher: %s", "license_plate_number: %s", "trace_id: %s", "return_reference_number: %s" '
        '"group_number: %s", "sequence_number: %s", "asynchronous: %s"',
        product_id,
        warehouse_id,
        quantity,
        old_reason_code,
        new_reason_code,
        customer_id,
        instruction_id,
        advanced_shipping_notification,
        is_prepaid_voucher,
        license_plate_number,
        trace_id,
        return_reference_number,
        group_number,
        sequence_number,
        asynchronous,
    )

    # This is because Oracle is currently sending us a '*' in the instruction field for some message types
    # I can't see if this is still true as I can't find this error in the logs.
    if instruction_id:
        try:
            instruction_id = int(instruction_id)
        except (ValueError, TypeError):
            config.logger.warning(
                "invalid_oracle_instruction_id: Error when trying to cast instruction %s to int",
                instruction_id,
            )
            instruction_id = None

    # Create Take2 stock adjustment record
    # We need to create this to get the adjustment ID, which is used to create order item snapshots
    config.logger.info("create_take2_adjustment, trace_id=%s", trace_id)
    adjustment = create_stock_adjustment(
        dict(
            product_id=product_id,
            warehouse_id=warehouse_id,
            quantity=quantity,
            customer_id=customer_id,
            adjustment_type=int(new_reason_code),
        )
    )

    # Get the merchant returns on_hold value
    config.logger.info("get_merchant_returns_on_hold, trace_id=%s", trace_id)
    merchant_returns_on_hold = get_good_stock_on_hold_by_product_id(
        product_id, warehouse_id
    )

    # Get the current on hold quantity for orders
    config.logger.info("get_orderitem_on_hold_quantity, trace_id=%s", trace_id)
    orderitem_on_hold_quantity = get_orderitem_on_hold_quantity(
        adjustment["product_id"], is_prepaid_voucher, adjustment["warehouse_id"]
    )
    create_orderitem_snapshot(adjustment["adjustment_id"], orderitem_on_hold_quantity)

    # Get old stock levels
    config.logger.info("get_take2_stock_levels, trace_id=%s", trace_id)
    old_take2stock, _ = get_or_create_take2_stock(
        product_id=int(product_id), warehouse_id=int(warehouse_id)
    )

    # Calculate new levels based on old and new reason codes
    config.logger.info("calculate_new_stock_levels, trace_id=%s", trace_id)
    updated_take2stock = adjust_stock_quanities(
        take2stock=old_take2stock,
        quantity=quantity,
        old_reason_code=old_reason_code,
        new_reason_code=new_reason_code,
    )

    # Calculate available stock by substracting on_hold (orderitems, merchant_returns) and ibt_prep
    config.logger.info("calculate_available_stock, trace_id=%s", trace_id)
    updated_take2stock["available"] = (
        updated_take2stock["sellable"]
        - orderitem_on_hold_quantity
        - updated_take2stock["ibt_prep"]
        - merchant_returns_on_hold.get("quantity", 0)
    )

    # Write the current take2 stock changes
    config.logger.info("write_take2_stock, trace_id=%s", trace_id)
    adjusted_stock = update_take2_stock(updated_take2stock)

    # Calculate stock difference
    config.logger.info("calculate_stock_difference, trace_id=%s", trace_id)
    movement_quantity = (
        updated_take2stock["on_hand"] + updated_take2stock["in_returns"]
    ) - (old_take2stock["on_hand"] + old_take2stock["in_returns"])

    # Write the stock levels to new DB
    config.logger.info("set_local_stock_levels, trace_id=%s", trace_id)
    stock_service_stock = take2_stock_to_local_stock(adjusted_stock)
    # Store RTM On Hold value
    stock_service_stock["return_to_merchant"] = merchant_returns_on_hold.get(
        "quantity", 0
    )
    stock_service_stock["on_hold"] = orderitem_on_hold_quantity
    stock_v2 = set_stock_levels(
        owner_id=1,
        product_reference=product_id,
        location_id=warehouse_id,
        stock_levels=stock_service_stock,
    )

    # Create stock service adjustment
    adjustment_v2_id = create_adjustment(
        stock_id=stock_v2["stock_id"],
        old_adjustment_type_id=old_reason_code,
        new_adjustment_type_id=new_reason_code,
        quantity=quantity,
        levels=stock_v2["levels"],
        trace_id=trace_id,
        group_number=group_number,
        sequence_number=sequence_number,
    )
    config.logger.info(
        "created_stock_service_adjustment, trace_id=%s adjustment_v2_id=%s",
        trace_id,
        adjustment_v2_id,
    )

    # Create the take2 snapshot
    config.logger.info("create_take2_snapshot, trace_id=%s", trace_id)
    create_take2_stock_snapshot(adjustment["adjustment_id"], adjusted_stock)

    # Update legacy product table with new stock values
    config.logger.info("update_products_table, trace_id=%s", trace_id)
    product = products.get_legacy_product(product_id)
    in_cpt = warehouse_id == Warehouse.CPT_ID
    legacy_stock = product["qtyInStockCpt"] if in_cpt else product["qtyInStockJhb"]
    if legacy_stock != adjusted_stock["available"]:
        available_stock = max(
            min(adjusted_stock["available"], adjusted_stock["sellable"]), 0
        )
        products.set_legacy_product(product_id, warehouse_id, available_stock)

    # Send legacy stock movement event
    config.logger.info("send_legacy_stock_movement_event, trace_id=%s", trace_id)
    legacy_stock_movement_producer.send_stock_movement_event(
        adjusted_stock=adjusted_stock,
        adjustment=adjustment,
        quantity=quantity
        if new_reason_code == StockAdjustmentType.TYPE_TRUSTED_RETURN
        else movement_quantity,
        is_seller_listing=product["IsSellerListing"],
        instruction_id=instruction_id,
        advanced_shipping_notification=advanced_shipping_notification,
    )

    # Send stock update notify event
    config.logger.info("send_stock_update_notify_event, trace_id=%s", trace_id)
    send_stock_update_notify_event(
        product_reference=str(product_id),
        location=Warehouse.ID_TO_CODE[warehouse_id],
        update_request={
            "quantity": quantity,
            "previous_adjustment_type_id": old_reason_code,
            "new_adjustment_type_id": new_reason_code,
        },
        stock_levels=stock_service_stock,
        additional_data={
            "customer_id": customer_id,
            "instruction_id": instruction_id,
            "license_plate_number": license_plate_number,
            "advanced_shipping_notification": advanced_shipping_notification,
        },
        adjustment_id=adjustment["adjustment_id"],
        movement_quantity=movement_quantity,
        received_at=adjustment["received_at"],
        trace_id=trace_id,
    )

    config.logger.info("adjust_stock_completed, trace_id=%s", trace_id)
    return dict(
        stock=old_take2stock,
        adjusted_stock=adjusted_stock,
        stock_adjustment=adjustment,
        movement_quantity=movement_quantity,
    )
