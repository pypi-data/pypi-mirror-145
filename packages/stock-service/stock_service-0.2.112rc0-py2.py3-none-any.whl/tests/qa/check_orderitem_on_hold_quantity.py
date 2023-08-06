from stock_service.config import Config
from stock_service.external.tal.orderitems_status_snapshots import (
    get_orderitem_on_hold_quantity,
    find_orderitems_by_product,
    OrderItemStateEnum,
)


config = Config()
config.configure()


def main():
    with config.db_client.get_connection("take2_replica") as connection:
        rows = connection.execute(
            """SELECT
                                        DISTINCT idProduct
                                     FROM
                                        orderitems
                                     WHERE
                                        Status = %(orderitem_status)s
                                        AND idProduct IS NOT NULL
                                     LIMIT 40
                                """,
            {"orderitem_status": OrderItemStateEnum.ON_HOLD},
        ).fetchall()
        for row in rows:
            (product_id,) = row
            compare_orderitem_on_hold_quantity(product_id)


def compare_orderitem_on_hold_quantity(product_id: int):
    """
    Compare values returned from old and new function
    """
    new_quantity_on_hold = get_orderitem_on_hold_quantity(product_id, True)
    old_quantity_on_hold = find_orderitems_by_product(product_id)["status_breakdown"][
        OrderItemStateEnum.ON_HOLD
    ]
    result = "PASSED" if (new_quantity_on_hold == old_quantity_on_hold) else "FAILED"
    print(
        f"product_id={product_id}, old_quantity_on_hold={old_quantity_on_hold}, "
        f"new_quantity_on_hold={new_quantity_on_hold}, result={result}"
    )


if __name__ == "__main__":
    main()
