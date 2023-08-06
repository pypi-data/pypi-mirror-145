from sqlalchemy import Column
from sqlalchemy.dialects import mysql
from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel


class StockStatus(Base):
    """Stock status table"""

    __tablename__ = "stock_status"

    stock_status_id = Column("stock_status_id", mysql.INTEGER(11), primary_key=True)
    status = Column("status", mysql.VARCHAR(64))
    description = Column("description", mysql.VARCHAR(256))
    date_created = Column("date_created", mysql.DATETIME())
    date_modified = Column("date_modified", mysql.DATETIME())


class StockStatusModel(BaseModel):
    """Model for accessing the stock status table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, StockStatus)

    def get_by_id(self, stock_status_id):
        return super().get_one(stock_status_id=stock_status_id)

    def create(self, status, description):
        return super().create(status=status, description=description)
