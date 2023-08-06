from retry import retry
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from stock_service.utils import db
from stock_service.utils.stats import profile_with_stats
from stock_service.config import OldConfig
from stock_service.models.take2.stock_snapshot import (
    Take2StockSnapshot,
    Take2StockSnapshotDict,
)


SQL_CLIENT = OldConfig.get_db_client()


@profile_with_stats(namespace="database.take2")
def get_stock_snapshot(
    take2_adjustment_id: int, read_for_update=False
) -> Take2StockSnapshotDict:
    """Get product stock snapshot by primary key"""
    context = db.ConnectionType.WRITE if read_for_update else db.ConnectionType.READ
    with SQL_CLIENT.get_session_context(context.value) as session:
        results = (
            session.query(Take2StockSnapshot)
            .filter_by(adjustment_id=take2_adjustment_id)
            .one_or_none()
        )
        if results is not None:
            return results.to_schema()
    raise NoResultFound(
        f"results not found for take2 adjustment_id={take2_adjustment_id}"
    )


@retry(
    exceptions=OperationalError, tries=db.DEADLOCK_MAX_RETRIES, delay=0.1, logger=None
)
def create_stock_snapshot(
    take2_adjustment_id: int, take2_snapshot: dict
) -> Take2StockSnapshotDict:
    """
    Create new product stock snapshot.
    :param take2_adjustment_id: `idAdjustment` from the `wms2_stock_adjustments` table
    :param stock: dict containing product stock values
    """
    take2_snapshot_copy = take2_snapshot.copy()
    keys_to_exclude = ["product_id", "warehouse_id"]
    for key in keys_to_exclude:
        if key in take2_snapshot_copy:
            del take2_snapshot_copy[key]

    take2_snapshot_instance = Take2StockSnapshot(
        adjustment_id=take2_adjustment_id, **take2_snapshot_copy
    )
    with SQL_CLIENT.get_session_context(db.ConnectionType.WRITE.value) as session:
        session.expire_on_commit = False
        session.add(take2_snapshot_instance)
        session.commit()
    return take2_snapshot_instance.to_schema()


@profile_with_stats(namespace="database.take2")
def create_take2_stock_snapshot(
    take2_adjustment_id: int, take2_snapshot: dict
) -> Take2StockSnapshotDict:
    return create_stock_snapshot(
        take2_adjustment_id=take2_adjustment_id, take2_snapshot=take2_snapshot
    )
