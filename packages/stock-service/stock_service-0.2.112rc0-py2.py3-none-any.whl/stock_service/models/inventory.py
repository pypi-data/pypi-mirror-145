from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel
from stock_service.models.owner import Owner, OwnerModel


class Inventory(Base):
    """Inventory table"""

    __tablename__ = "inventory"
    __table_args__ = (
        UniqueConstraint("product_reference", "owner_id", name="uniqueInventory"),
    )

    inventory_id = Column(
        "inventory_id", mysql.INTEGER(11), primary_key=True, autoincrement=True
    )
    product_reference = Column("product_reference", mysql.VARCHAR(64))
    owner_id = Column("owner_id", mysql.INTEGER(11), ForeignKey("owner.owner_id"))
    owner = relationship("Owner")
    stock = relationship("Stock", back_populates="inventory")
    date_created = Column("date_created", mysql.DATETIME())
    date_modified = Column("date_modified", mysql.DATETIME())


class InventoryModel(BaseModel):
    """Model for accessing the inventory table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, Inventory)
        self.owner_model = OwnerModel(client)

    def get_by_id(self, inventory_id):
        return super().get_one(inventory_id=inventory_id)

    def get_by(self, product_reference=None, owner_id=None):
        kwargs = {
            k: v
            for k, v in {
                "product_reference": product_reference,
                "owner_id": owner_id,
            }.items()
            if v is not None
        }
        return super().get_all(**kwargs)

    def get_by_product_and_company(self, product_reference, company_id):
        with self.client.get_session_context("stock.leader") as session:
            results = (
                session.query(Inventory)
                .join(Owner)
                .filter(
                    Owner.company_id == company_id,
                    Owner.owner_id == Inventory.owner_id,
                    Inventory.product_reference == product_reference,
                )
                .all()
            )
            return [r.to_dict() for r in results] if results else None

    def create(self, product_reference, owner_id):
        try:
            return super().create(
                product_reference=product_reference, owner_id=owner_id
            )
        except IntegrityError as e:
            if not self.owner_model.get_by_id(owner_id):
                raise ReferenceError(f"Cannot find owner id {owner_id}") from e
            if self.get_by(product_reference=product_reference, owner_id=owner_id):
                raise ValueError(
                    f"Duplicate entry: owner already exists - product: {product_reference}, owner: {owner_id}"
                ) from e
            raise
