"""
controller api for `take2.wms2_stock_adjustments` api
"""
import logging
import datetime
from typing import List

from retry import retry

from sqlalchemy.exc import OperationalError

from stock_service.config import Config
from stock_service.utils import db
from stock_service.utils.stats import profile_with_stats
from stock_service.config import OldConfig
from stock_service.models.take2.stock_adjustment import (
    Take2StockAdjustment,
    Take2StockAdjustmentDict,
)

config = Config()
LOGGER = logging.getLogger()
SQL_CLIENT = OldConfig.get_db_client()


@profile_with_stats(namespace="database.take2")
def get_adjustment_by_id(adjustment_id: int):
    """
    returns the stock adjustment by id

    :param adjustment_id: adjustment id to query
    """
    with SQL_CLIENT.get_session_context(role="master") as session:
        stock_adjustment = (
            session.query(Take2StockAdjustment)
            .filter(Take2StockAdjustment.adjustment_id == adjustment_id)
            .one()
        )
        return stock_adjustment.to_schema()


@profile_with_stats(namespace="database.take2")
@retry(
    exceptions=OperationalError,
    tries=db.DEADLOCK_MAX_RETRIES,
    delay=db.DEADLOCK_RETRY_DELAY_SECONDS,
)
def create_stock_adjustment(adjustment_stock: dict) -> Take2StockAdjustmentDict:
    """
    creates new adjustment entry in wms2_stock_adjustment table
    :param adjustment_stock: adjusted stock object
    :returns: dict of inserted entry
    """
    adjustment = Take2StockAdjustment(**adjustment_stock)
    with SQL_CLIENT.get_session_context(db.ConnectionType.WRITE.value) as session:
        session.expire_on_commit = False
        session.add(adjustment)
        session.commit()
    return adjustment.to_schema()


@profile_with_stats(namespace="database.take2")
def get_stock_on_hand_for_products(
    product_ids: List[int], adjustment_datetime: datetime.datetime
) -> List[dict]:
    """
    returns total stock on hand for product_ids that have adjustments before adjustment_datetime

    :param product_ids: list of product_ids
    :param adjustment_datetime: datetime to filter by
    :param snapshot_controller: snapshot controller used to get stock_on_hand
    :returns: [{'product_id': 1, 'stock_on_hand': 0}, ...]
    """
    products_stock_on_hand = []
    for product_id in product_ids:
        with config.db_client.get_connection(role="take2_primary") as connection:
            total = connection.execute(
                """
                SELECT
                    (SUM(stockOnHand) + SUM(stockInReturns)) as total
                FROM
                    wms2_products_stock_snapshots products_stock_snapshots
                INNER JOIN
                    (
                        SELECT
                            max(idStockAdjustment) idStockAdjustment
                        FROM
                            wms2_stock_adjustments
                        WHERE
                            idProduct = %(product_id)s
                        AND
                            receivedAt <= %(adjustment_datetime)s
                        GROUP BY
                            idWarehouse
                    ) stock_adjustments
                ON stock_adjustments.idStockAdjustment = products_stock_snapshots.idStockAdjustment
            """,
                dict(product_id=product_id, adjustment_datetime=adjustment_datetime),
            ).fetchone()[0]

            total_stock_on_hand = int(total) if total else 0
            products_stock_on_hand.append(
                dict(product_id=product_id, stock_on_hand=total_stock_on_hand)
            )
    return products_stock_on_hand
