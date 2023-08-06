from typing import List, Optional, Tuple
from retry import retry

from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from stock_service.utils import db
from stock_service.utils.stats import profile_with_stats

from stock_service.external.tal import products
from stock_client.constants import Warehouse
from stock_service.config import Config, OldConfig
from stock_service.models.take2.stock import (
    Take2Stock,
    Take2StockDict,
    UPDATABLE_COLUMNS,
)
from stock_service.models.take2 import warehouse
from stock_service.models.stock_level import StockLevelModel

config = Config()
SQL_CLIENT = OldConfig().get_db_client()
logger = OldConfig.logger
stats_client = OldConfig().get_stats_client()
stockdb_stock_level_model = StockLevelModel(OldConfig().get_db_client())


def get_or_create_stock(product_id, warehouse_id) -> Tuple[Take2StockDict, bool]:
    """
    get stock levels or creates stock if it doesn't exist

    :param product_id: product_id to filter on
    :param warehouse_id: warehouse_id to filter on
    :returns: tuple of (stock data, True if stock is created else False)
    """
    try:
        return get_stock_levels(product_id, warehouse_id, read_for_update=True), False
    except NoResultFound:
        try:
            return (
                create_stock(dict(product_id=product_id, warehouse_id=warehouse_id)),
                True,
            )
        except IntegrityError:
            try:
                return (
                    get_stock_levels(product_id, warehouse_id, read_for_update=True),
                    False,
                )
            except NoResultFound:
                raise


@profile_with_stats(namespace="database.take2")
def get_or_create_take2_stock(product_id, warehouse_id) -> Tuple[Take2StockDict, bool]:
    return get_or_create_stock(product_id=product_id, warehouse_id=warehouse_id)


@profile_with_stats(namespace="database.take2")
def get_stock_levels_for_warehouses(
    product_id: int, warehouse_ids: Optional[List[int]] = None
):
    """
    returns list of products in `warehouse_ids`
    :returns: list of product stock
    """
    warehouses = warehouse_ids if warehouse_ids else Warehouse.IDS
    stocks: List[Take2StockDict] = []
    for warehouse_id in warehouses:
        stock, created = get_or_create_stock(
            product_id=product_id, warehouse_id=int(warehouse_id)
        )
        # additional warehouse info needed
        stock["warehouse"] = warehouse.get_warehouse_by_id(warehouse_id)
        if created:
            products.set_legacy_product(product_id, warehouse_id, 0)
        stocks.append(stock)
    return stocks


@profile_with_stats(namespace="database.take2")
def get_stock_levels(
    product_id: int, warehouse_id: int, read_for_update=False
) -> Take2StockDict:
    """
    returns Take2StockDict from database using product_id and warehouse_id primary keys

    :param product_id: product_id to filter on
    :param warehouse_id: warehouse_id to filter on
    :param read_for_update: reads from master database
    """
    context = db.ConnectionType.WRITE if read_for_update else db.ConnectionType.READ
    with SQL_CLIENT.get_session_context(context.value) as session:
        results = (
            session.query(Take2Stock)
            .filter_by(product_id=product_id, warehouse_id=warehouse_id)
            .one_or_none()
        )
        if results is not None:
            take2_stock = results.to_schema()
            # compare_take2stock_with_stock_levels(take2_stock)
            return take2_stock
    raise NoResultFound(
        f"product_id={product_id}, warehouse_id={warehouse_id} not found in wms2_products_stock"
    )


@profile_with_stats(namespace="database.take2")
@retry(
    exceptions=OperationalError,
    tries=db.DEADLOCK_MAX_RETRIES,
    delay=db.DEADLOCK_RETRY_DELAY_SECONDS,
)
def create_stock(stock: dict) -> Take2StockDict:
    """
    Create new product stock entry in the database

    :param stock_data: dictionary containing values to insert
    :returns: dict object from the db containing inserted values
    """
    if not (stock.get("product_id") and stock.get("warehouse_id")):
        raise ValueError("warehouse_id and product_id are required to create stock")

    row = Take2Stock(**stock)
    with SQL_CLIENT.get_session_context(db.ConnectionType.WRITE.value) as session:
        session.expire_on_commit = False
        session.add(row)
        session.commit()
        return row.to_schema()


@retry(
    exceptions=OperationalError,
    tries=db.DEADLOCK_MAX_RETRIES,
    delay=db.DEADLOCK_RETRY_DELAY_SECONDS,
    logger=None,
)
def update_stock(stock: dict) -> Take2StockDict:
    """
    updates the specified columns based on product_id and warehouse_id.

    :param stock_data: Stock dictionary containing product_id, warehouse_id and the columns to be updated
    :return: returns updated results dict from db or empty dict if update is not performed
    """

    if not (stock.get("product_id") and stock.get("warehouse_id")):
        raise ValueError("warehouse_id and product_id are required to create stock")
    product_id, warehouse_id = stock.pop("product_id"), stock.pop("warehouse_id")

    for key in stock.keys():
        if key not in UPDATABLE_COLUMNS:
            raise TypeError

    with SQL_CLIENT.get_session_context(db.ConnectionType.WRITE.value) as session:
        row = (
            session.query(Take2Stock)
            .filter_by(product_id=product_id, warehouse_id=warehouse_id)
            .one_or_none()
        )
        if row:
            for column_name, new_value in stock.items():
                setattr(row, column_name, new_value)
            session.commit()
            return row.to_schema()
    raise NoResultFound(
        f"product_id={product_id}, warehouse_id={warehouse_id} not found in wms2_products_stock"
    )


@profile_with_stats(namespace="database.take2")
def update_take2_stock(stock: dict) -> Take2StockDict:
    return update_stock(stock=stock)


@profile_with_stats(namespace="internal")
def compare_take2stock_with_stock_levels(take2_stock: Take2Stock):
    # read list of stock levels at the specified location:
    levels_list = stockdb_stock_level_model.get_levels_by_location_id(
        product_reference=take2_stock.product_id,
        company_id=1,
        location_id=take2_stock.warehouse_id,
    )

    # convert to dictionary to iterate for comparison with take2
    # using hard coded stock status values because new statuses may be added
    # but won't compare with take2 database anyway:
    # |               1 | damaged         | Damaged         | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               2 | expired         | Expired         | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               3 | in_returns      | In returns      | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               4 | ibt_incoming    | IBT incoming    | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               5 | pending_putaway | Pending putaway | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               6 | pickable        | Pickable        | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               7 | reserved        | Reserved        | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               8 | on_hand         | On hand         | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    # |               9 | available       | Available       | 2021-03-10 13:40:55 | 2021-03-10 13:40:55 |
    level_dict = dict()
    for level in levels_list:
        level_dict[level["status"]] = level["quantity"]

    # calulcate expected values from take2 data:
    take2_stock_dict = dict()
    take2_stock_dict["damaged"] = take2_stock.damaged
    take2_stock_dict["expired"] = take2_stock.expired
    take2_stock_dict["in_returns"] = take2_stock.in_returns
    take2_stock_dict["ibt_incoming"] = take2_stock.in_transit + take2_stock.ibt_prep
    take2_stock_dict["pending_putaway"] = take2_stock.in_receiving
    take2_stock_dict["pickable"] = (
        take2_stock.on_hand
        - take2_stock.damaged
        - take2_stock.expired
        - take2_stock.in_receiving
    )
    take2_stock_dict["reserved"] = take2_stock.sellable - take2_stock.available
    take2_stock_dict["on_hand"] = take2_stock.on_hand
    take2_stock_dict["available"] = take2_stock.available

    # compare each level in take2 with what we found in stock db ...
    for level_name in take2_stock_dict:
        take2_level = take2_stock_dict.get(level_name, 0)
        stock_level = level_dict.get(level_name, 0)
        if take2_level != stock_level:
            stats_client.incr("take2_stock_comparison.level_difference." + level_name)
            logger.debug(
                "product=%s warehouse=%s level=%s: take2(%s) != stock(%s)",
                take2_stock.product_id,
                take2_stock.warehouse_id,
                level_name,
                take2_level,
                stock_level,
            )
        else:
            stats_client.incr("take2_stock_comparison.level_match." + level_name)
