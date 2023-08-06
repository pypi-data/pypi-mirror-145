from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel
from stock_service.models.inventory import InventoryModel
from stock_service.models.location import LocationModel


class Stock(Base):
    """Stock table"""

    __tablename__ = "stock"
    __table_args__ = (
        UniqueConstraint("inventory_id", "location_id", name="uniqueStock"),
    )

    stock_id = Column("stock_id", mysql.INTEGER(11), primary_key=True)
    inventory_id = Column(
        "inventory_id", mysql.INTEGER(11), ForeignKey("inventory.inventory_id")
    )
    inventory = relationship("Inventory", back_populates="stock")
    location_id = Column(
        "location_id", mysql.INTEGER(11), ForeignKey("location.location_id")
    )
    location = relationship("Location")
    levels = relationship("StockLevel", back_populates="stock")
    date_created = Column("date_created", mysql.DATETIME())
    date_modified = Column("date_modified", mysql.DATETIME())


class StockModel(BaseModel):
    """Model for accessing the stock table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, Stock)
        self.inventory_model = InventoryModel(client)
        self.location_model = LocationModel(client)

    def get_by_id(self, stock_id):
        return super().get_one(stock_id=stock_id)

    def get_by(self, inventory_id=None, location_id=None):
        kwargs = {
            k: v
            for k, v in {
                "inventory_id": inventory_id,
                "location_id": location_id,
            }.items()
            if v is not None
        }
        return super().get_all(**kwargs)

    def create(self, inventory_id, location_id):
        try:
            return super().create(inventory_id=inventory_id, location_id=location_id)
        except IntegrityError as e:
            if not self.inventory_model.get_by_id(inventory_id=inventory_id):
                raise ReferenceError(f"Cannot find inventory id {inventory_id}") from e
            if not self.location_model.get_by_id(location_id=location_id):
                raise ReferenceError(f"Cannot find location id {location_id}") from e
            if self.get_by(inventory_id=inventory_id, location_id=location_id):
                raise ValueError(
                    f"Duplicate entry: stock already exists - inventory: {inventory_id}, "
                    f"location: {location_id}"
                ) from e
            raise
