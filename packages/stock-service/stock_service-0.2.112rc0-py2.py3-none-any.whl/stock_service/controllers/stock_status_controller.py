from functools import lru_cache

from stock_service.config import Config
from stock_service.utils.stats import profile_with_stats

config = Config()


@lru_cache(maxsize=32)
@profile_with_stats(namespace="database.stock")
def get_stock_status_id(stock_status):
    with config.db_client.get_connection("stock_replica") as connection:
        row = connection.execute(
            """
            SELECT
                stock_status_id
            FROM
                stock_status
            WHERE
                status = %s
        """,
            stock_status.lower().strip(),
        ).one()
        return row["stock_status_id"]
