from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects import mysql

from stock_service.utils.tools import rounded_timestamp
from stock_service.models.take2 import Base
from stock_service.models.take2 import schema


class Take2StockAdjustmentDict(schema.Schema):
    immutable = ["adjustment_id", "product_id"]


class Take2StockAdjustment(Base):
    __tablename__ = "wms2_stock_adjustments"

    adjustment_id = Column(
        "idStockAdjustment", mysql.INTEGER(11), primary_key=True, nullable=False
    )
    product_id = Column("idProduct", mysql.INTEGER(11))
    warehouse_id = Column("idWarehouse", mysql.INTEGER(11), nullable=False)
    adjustment_type = Column("idAdjustmentType", mysql.INTEGER(11), nullable=False)
    quantity = Column("quantity", mysql.INTEGER(11), nullable=False)
    customer_id = Column("idCustomer", mysql.INTEGER(11))
    parent_id = Column("idParent", mysql.INTEGER(11))
    received_at = Column(
        "receivedAt", TIMESTAMP, nullable=False, default=rounded_timestamp
    )

    def to_schema(self) -> Take2StockAdjustmentDict:
        return Take2StockAdjustmentDict(**self.to_dict())
