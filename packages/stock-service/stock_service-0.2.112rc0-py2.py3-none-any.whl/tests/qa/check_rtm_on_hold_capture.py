import sys

from sqlalchemy.orm.exc import NoResultFound

from stock_client.constants import StockAdjustmentType
from stock_service.config import Config
from stock_service.controllers.inventory_controller import (
    get_or_create_inventory_id,
    get_or_create_stock_id,
)
from stock_service.managers.update_stock_managers import do_stock_adjustment

config = Config()
config.configure()


def get_test_data():
    """Get sample data: list of (product_id, warehouse_id)
    where stock_level for Return To Merchant On hold does not exist for that specific stock_id
    """
    with config.db_client.get_connection("stock_primary") as connection:
        query = """SELECT
                        inventory.product_reference,
                        stock.location_id
                   FROM
                        inventory, stock
                   WHERE
                        inventory.owner_id = 1
                        AND inventory.inventory_id = stock.inventory_id
                        AND NOT EXISTS (SELECT
                                            stock_id
                                        FROM
                                            stock_level
                                        WHERE
                                            stock.stock_id = stock_level.stock_id
                                            AND stock_level.stock_status_id = 12)
                   LIMIT 10"""
        rows = connection.execute(query).fetchall()
        for row in rows:
            product_id, warehouse_id = row
            print(f"product_id={product_id}, warehouse_id={warehouse_id}")


def get_return_to_merchant_on_hold_value(stock_id: int):
    with config.db_client.get_connection("stock_primary") as connection:
        query = """SELECT
                        quantity
                   FROM
                        stock_level
                   WHERE
                        stock_id = %(stock_id)s
                        AND stock_status_id = %(stock_status_id)s"""
        try:
            (rtm_on_hold_value,) = connection.execute(
                query, {"stock_id": stock_id, "stock_status_id": 12}
            ).fetchone()
        except NoResultFound:
            rtm_on_hold_value = None

    return rtm_on_hold_value


def test_adjust_stock_store_rtm_on_hold(
    product_id: int, warehouse_id: int, quantity: int
):
    # GIVEN: Valid stock adjustment arguments
    owner_id = 1
    product_reference = product_id
    location_id = warehouse_id

    # WHEN: we adjust stock
    do_stock_adjustment(
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
        old_reason_code=StockAdjustmentType.TYPE_GENERAL_RETURN,
        new_reason_code=StockAdjustmentType.TYPE_TRUSTED_RETURN,
        customer_id=None,
        instruction_id=None,
        advanced_shipping_notification=None,
        is_prepaid_voucher=None,
        license_plate_number=None,
        trace_id=None,
        return_reference_number=None,
    )

    inventory_id = get_or_create_inventory_id(owner_id, product_reference)
    stock_id = get_or_create_stock_id(inventory_id, location_id)

    # THEN: Return to merchant On hold value should be captured in the Stock DB
    rtm_on_hold_value = get_return_to_merchant_on_hold_value(stock_id)

    status = "[FAILED]" if rtm_on_hold_value is None else "[PASSED]"
    print(
        f"owner_id={owner_id}, product_reference={product_reference}, location_id={location_id}, "
        f"inventory_id={inventory_id}, stock_id={stock_id}, rtm_on_hold_value={rtm_on_hold_value}, status={status}"
    )


def main():
    get_test_data()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        test_adjust_stock_store_rtm_on_hold(
            product_id=int(sys.argv[1]),
            warehouse_id=int(sys.argv[2]),
            quantity=int(sys.argv[3]),
        )
    else:
        main()
