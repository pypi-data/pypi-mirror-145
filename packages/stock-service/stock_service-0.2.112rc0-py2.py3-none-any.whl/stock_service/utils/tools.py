import datetime

from stock_service.config import Config

config = Config()


def rounded_timestamp():
    return datetime.datetime.now().replace(microsecond=0)


def take2_stock_to_local_stock(take2_stock):
    stock = {
        "product_id": take2_stock["product_id"],
        "warehouse_id": take2_stock["warehouse_id"],
        "damaged": take2_stock["damaged"],
        "expired": take2_stock["expired"],
        "in_returns": take2_stock["in_returns"],
        "pending_putaway": take2_stock["in_receiving"],
        "pickable": take2_stock["sellable"],
        "ibt_prep": take2_stock["ibt_prep"],
        "reserved": take2_stock["sellable"] - take2_stock["available"],
        "discrepancy": take2_stock["discrepancy"],
    }
    stock["on_hand"] = (
        stock["pickable"]
        + stock["expired"]
        + stock["damaged"]
        + stock["pending_putaway"]
    )
    stock["available"] = stock["pickable"] - stock["reserved"]
    return stock


def local_stock_to_take2_stock(local_stock: dict):
    take2_stock = {
        "product_id": local_stock["product_id"],
        "warehouse_id": local_stock["warehouse_id"],
        "damaged": local_stock["damaged"],
        "expired": local_stock["expired"],
        "in_returns": local_stock["in_returns"],
        "in_receiving": local_stock["pending_putaway"],
        "sellable": local_stock["pickable"],
        "ibt_prep": local_stock["ibt_prep"],
        "discrepancy": local_stock["discrepancy"],
    }
    take2_stock["available"] = local_stock["pickable"] - local_stock["reserved"]
    take2_stock["on_hand"] = (
        local_stock["pickable"]
        + local_stock["expired"]
        + local_stock["damaged"]
        + local_stock["pending_putaway"]
    )
    return take2_stock
