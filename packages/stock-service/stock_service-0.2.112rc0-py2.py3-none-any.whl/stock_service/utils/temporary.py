from stock_service.ad_hoc.sync_stock_from_take2 import sync_stock_item_from_take2
from stock_service.config import Config
from stock_service.controllers.stock_controller import get_stock_levels_for_warehouses

config = Config()


def compare_take2_to_local(product_id: int, warehouse_id: int):
    config.logger.info("comparing_stock %s %s", product_id, warehouse_id)
    take2_stock = get_stock_levels_for_warehouses(
        product_id=product_id, warehouse_ids=[warehouse_id]
    )
    local_stock = dict()
    with config.db_client.get_connection("stock_replica") as connection:
        rows = connection.execute(
            """
            SELECT
                stock.location_id,
                stock_status.status,
                stock_level.quantity
            FROM
                stock_status
                LEFT JOIN stock_level ON stock_level.stock_status_id = stock_status.stock_status_id
                LEFT JOIN stock ON stock_level.stock_id = stock.stock_id
                LEFT JOIN inventory ON stock.inventory_id = inventory.inventory_id
            WHERE
                inventory.product_reference = %(product_reference)s
        """,
            {"product_reference": str(product_id)},
        ).fetchall()

        for row in rows:
            warehouse_id, status, level = row
            warehouse = local_stock.setdefault(warehouse_id, {})
            warehouse[status] = level

    # Old vs new level names
    compare_list = (
        ("on_hand", "on_hand"),
        ("damaged", "damaged"),
        ("expired", "expired"),
        ("in_returns", "in_returns"),
        ("in_receiving", "pending_putaway"),
        ("sellable", "pickable"),
        ("available", "available"),
    )

    for old_stock in take2_stock:
        warehouse_id = old_stock["warehouse_id"]
        for old_status, new_status in compare_list:
            old_value = old_stock.get(old_status, 0)
            new_value = local_stock.get(warehouse_id, {}).get(new_status, 0)
            if old_value == new_value:
                # We don't want to create a bunch of stats for things that is zero
                if old_value or new_value:
                    config.stats_client.incr(
                        f"internal.take2_stock_comparison.match.{new_status}"
                    )
            else:
                config.stats_client.incr(
                    f"internal.take2_stock_comparison.differ.{new_status}"
                )
                sync_stock_item_from_take2(product_id, warehouse_id)
                if config.log_stock_differences:
                    config.logger.warning(
                        "take2_local_stock_not_matching %s",
                        {
                            "product_id": product_id,
                            "warehouse_id": warehouse_id,
                            "status": new_status,
                            "take2_level": old_value,
                            "local_level": new_value,
                        },
                    )

    return take2_stock
