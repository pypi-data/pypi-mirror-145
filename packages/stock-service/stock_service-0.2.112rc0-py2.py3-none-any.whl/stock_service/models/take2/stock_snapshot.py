from sqlalchemy import Column
from sqlalchemy.dialects import mysql
from stock_service.models.take2 import Base
from stock_service.models.take2 import schema


class Take2StockSnapshotDict(schema.Schema):
    immutable = ["adjustment_id"]


class Take2StockSnapshot(Base):
    __tablename__ = "wms2_products_stock_snapshots"

    adjustment_id = Column(
        "idStockAdjustment", mysql.INTEGER(11), nullable=False, primary_key=True
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

    def to_schema(self) -> Take2StockSnapshotDict:
        return Take2StockSnapshotDict(**self.to_dict())
