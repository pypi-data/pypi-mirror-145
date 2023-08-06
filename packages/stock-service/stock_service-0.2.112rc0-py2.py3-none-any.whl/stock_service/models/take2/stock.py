import datetime

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects import mysql

from stock_service.models.take2 import Base
from stock_service.models.take2 import schema


UPDATABLE_COLUMNS = [
    "on_hand",
    "damaged",
    "discrepancy",
    "expired",
    "in_transit",
    "sellable",
    "available",
    "in_receiving",
    "in_returns",
    "ibt_prep",
]


class Take2StockDict(schema.Schema):
    non_negative_fields = ["on_hand", "damaged", "expired", "in_receiving"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in self.non_negative_fields:
            if item in self:
                self[item] = max(self.get(item, 0), 0)

    def __setitem__(self, item, value):
        if item in self.non_negative_fields:
            value = max(value, 0)
        super().__setitem__(item, value)


class Take2Stock(Base):
    __tablename__ = "wms2_products_stock"

    product_id = Column(
        "idProduct", mysql.INTEGER(11), nullable=False, primary_key=True
    )
    warehouse_id = Column(
        "idWarehouse", mysql.INTEGER(11), nullable=False, primary_key=True
    )
    on_hand = Column("stockOnHand", mysql.INTEGER(11), default=0)
    damaged = Column("stockDamaged", mysql.INTEGER(11), default=0)
    discrepancy = Column("stockDiscrepency", mysql.INTEGER(11), default=0)
    expired = Column("stockExpired", mysql.INTEGER(11), default=0)
    in_transit = Column("stockInTransit", mysql.INTEGER(11), default=0)
    sellable = Column("stockSellable", mysql.INTEGER(11), default=0)
    available = Column("stockAvailable", mysql.INTEGER(11), default=0)
    in_receiving = Column("stockInReceiving", mysql.INTEGER(11), default=0)
    in_returns = Column("stockInReturns", mysql.INTEGER(11), default=0)
    ibt_prep = Column("stockIbtPrep", mysql.INTEGER(11), default=0)
    date_created = Column(
        "DateCreated", TIMESTAMP, nullable=False, default=datetime.datetime.now
    )

    def to_schema(self) -> Take2StockDict:
        _dict = self.to_dict()
        _dict.pop("date_created")
        return Take2StockDict(_dict)
