from typing import Optional

from stock_client.constants import Warehouse
from stock_service.config import Config
from stock_service.controllers.stock_service_controller import StockServiceController
from stock_service.producers import send_stock_update_notify_event
from stock_service.utils.tools import take2_stock_to_local_stock

config = Config()
stock_service_controller = StockServiceController()


def adjust_takealot_stock(
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
):

    config.logger.warning(
        "=====DEPRECATED=====: takealot_stock_management.adjust_takealot_stock"
    )

    adjustment = stock_service_controller.adjust_stock(
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
    )

    send_stock_update_notify_event(
        product_reference=str(product_id),
        location=Warehouse.ID_TO_CODE[warehouse_id],
        update_request={
            "quantity": quantity,
            "previous_adjustment_type_id": old_reason_code,
            "new_adjustment_type_id": new_reason_code,
        },
        stock_levels=take2_stock_to_local_stock(adjustment["adjusted_stock"]),
        additional_data={
            "customer_id": customer_id,
            "instruction_id": instruction_id,
            "license_plate_number": license_plate_number,
            "advanced_shipping_notification": advanced_shipping_notification,
        },
        adjustment_id=adjustment["stock_adjustment"]["adjustment_id"],
        movement_quantity=adjustment["movement_quantity"],
        received_at=adjustment["stock_adjustment"]["received_at"],
        trace_id=trace_id,
    )

    return adjustment
