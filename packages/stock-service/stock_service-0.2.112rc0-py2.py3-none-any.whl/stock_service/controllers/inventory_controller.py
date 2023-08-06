import datetime

from retry import retry
from sqlalchemy.exc import NoResultFound, OperationalError

from stock_service.config import Config
from stock_service.controllers.stock_status_controller import get_stock_status_id
from stock_service.utils.stats import profile_with_stats

config = Config()


@profile_with_stats(namespace="database.stock")
@retry(exceptions=OperationalError, tries=3, delay=0.1)
def get_or_create_inventory_id(owner_id, product_reference):
    with config.db_client.get_connection("stock_primary") as connection:
        row = connection.execute(
            """
            SELECT
                inventory_id
            FROM
                inventory
            WHERE
                owner_id = %s
                AND product_reference = %s
        """,
            owner_id,
            str(product_reference),
        ).one_or_none()
        if row:
            return row["inventory_id"]

        cursor = connection.execute(
            """
                INSERT INTO inventory
                    (owner_id, product_reference)
                VALUES
                    (%s, %s)
            """,
            owner_id,
            str(product_reference),
        )
        return cursor.lastrowid


@profile_with_stats(namespace="database.stock")
@retry(exceptions=OperationalError, tries=3, delay=0.1)
def get_or_create_stock_id(inventory_id, location_id):
    # Replace with DB Lookup or warehouse API
    if location_id not in (1, 3):
        raise ValueError(f"Invalid location ID ({location_id})")

    with config.db_client.get_connection("stock_primary") as connection:
        row = connection.execute(
            """
            SELECT
                stock_id
            FROM
                stock
            WHERE
                inventory_id = %s
                AND location_id = %s
        """,
            inventory_id,
            location_id,
        ).one_or_none()
        if row:
            return row["stock_id"]

        cursor = connection.execute(
            """
                INSERT INTO stock
                    (inventory_id, location_id)
                VALUES
                    (%s, %s)
            """,
            inventory_id,
            location_id,
        )
        return cursor.lastrowid


@profile_with_stats(namespace="database.stock")
@retry(exceptions=OperationalError, tries=3, delay=0.1)
def set_stock_levels(owner_id, product_reference, location_id, stock_levels):
    saved_levels = list()
    adjustment_time = datetime.datetime.now()
    inventory_id = get_or_create_inventory_id(
        owner_id=owner_id, product_reference=product_reference
    )

    stock_id = get_or_create_stock_id(
        inventory_id=inventory_id, location_id=location_id
    )

    stock_levels.pop("product_id", None)
    stock_levels.pop("warehouse_id", None)

    with config.db_client.get_connection("stock_primary") as connection:
        for status, quantity in stock_levels.items():
            stock_status_id = get_stock_status_id(status)
            if not stock_status_id:
                raise ValueError(f"Invalid stock status ({status})")
            connection.execute(
                """
                INSERT INTO stock_level
                    (stock_id, stock_status_id, quantity)
                VALUES
                    (%(stock_id)s, %(stock_status_id)s, %(quantity)s)
                ON DUPLICATE KEY UPDATE
                    quantity = %(quantity)s,
                    date_modified = %(date_modified)s
            """,
                {
                    "stock_id": stock_id,
                    "stock_status_id": stock_status_id,
                    "quantity": quantity,
                    "date_modified": adjustment_time,
                },
            )
            saved_levels.append({"status": status, "quantity": quantity})
        connection.execute(
            """
            UPDATE
                stock
            SET
                date_modified = %s
            WHERE
                stock_id = %s
        """,
            adjustment_time,
            stock_id,
        )
    return {
        "inventory_id": inventory_id,
        "stock_id": stock_id,
        "levels": saved_levels,
    }


@profile_with_stats(namespace="database.stock")
@retry(exceptions=OperationalError, tries=3, delay=0.1)
def get_stock_levels(owner_id, product_reference, location_id):
    with config.db_client.get_connection("stock_replica") as connection:
        rows = connection.execute(
            """
            SELECT
                stock_status.status,
                stock_level.quantity
            FROM
                stock_status
                LEFT JOIN stock_level ON stock_level.stock_status_id = stock_status.stock_status_id
                LEFT JOIN stock ON stock_level.stock_id = stock.stock_id
                LEFT JOIN inventory ON stock.inventory_id = inventory.inventory_id
            WHERE
                inventory.product_reference = %(product_reference)s
                AND inventory.owner_id = %(owner_id)s
                AND stock.location_id = %(location_id)s
        """,
            {
                "owner_id": owner_id,
                "product_reference": str(product_reference),
                "location_id": location_id,
            },
        ).fetchall()
        if len(rows) == 0:
            raise NoResultFound(
                f"No stock found for owner_id={owner_id} "
                f"product_reference={product_reference} location_id={location_id}"
            )
        levels = (
            {"status": row["status"], "quantity": row["quantity"]} for row in rows
        )
        return list(levels)
