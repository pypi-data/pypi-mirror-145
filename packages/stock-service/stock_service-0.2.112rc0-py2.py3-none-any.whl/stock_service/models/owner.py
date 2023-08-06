from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import IntegrityError
from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel
from stock_service.models.company import CompanyModel


class Owner(Base):
    """Owner table"""

    __tablename__ = "owner"
    __table_args__ = (
        UniqueConstraint("company_id", "merchant_reference", name="uniqueOwner"),
    )

    owner_id = Column("owner_id", mysql.INTEGER(11), primary_key=True)
    company_id = Column(
        "company_id", mysql.INTEGER(11), ForeignKey("company.company_id")
    )
    merchant_reference = Column("merchant_reference", mysql.VARCHAR(64))
    date_created = Column("date_created", mysql.DATETIME())
    date_modified = Column("date_modified", mysql.DATETIME())


class OwnerModel(BaseModel):
    """Model for accessing the owner table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, Owner)
        self.company_model = CompanyModel(client)

    def get_by_id(self, owner_id):
        return super().get_one(owner_id=owner_id)

    def get_by(self, company_id=None, merchant_reference=None):
        kwargs = {
            k: v
            for k, v in {
                "company_id": company_id,
                "merchant_reference": merchant_reference,
            }.items()
            if v is not None
        }
        return super().get_all(**kwargs)

    def create(self, company_id, merchant_reference):
        try:
            return super().create(
                company_id=company_id, merchant_reference=merchant_reference
            )
        except IntegrityError as e:
            if not self.company_model.get_by_id(company_id=company_id):
                raise ReferenceError(f"Cannot find company id {company_id}") from e
            if self.get_by(company_id, merchant_reference):
                raise ValueError(
                    f"Duplicate entry: owner already exists - company: {company_id}, "
                    f"business: {merchant_reference}"
                ) from e
            raise
