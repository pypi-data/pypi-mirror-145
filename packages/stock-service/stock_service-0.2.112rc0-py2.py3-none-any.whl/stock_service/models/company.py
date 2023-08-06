import sqlalchemy
from sqlalchemy.dialects import mysql
from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel


class Company(Base):
    """Company table"""

    __tablename__ = "company"

    company_id = sqlalchemy.Column("company_id", mysql.INTEGER(11), primary_key=True)
    name = sqlalchemy.Column("name", mysql.VARCHAR(64))
    info = sqlalchemy.Column("info", mysql.VARCHAR(256))
    date_created = sqlalchemy.Column("date_created", mysql.DATETIME())
    date_modified = sqlalchemy.Column("date_modified", mysql.DATETIME())


class CompanyModel(BaseModel):
    """Model for accessing the company table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, Company)

    def get_by_id(self, company_id):
        return super().get_one(company_id=company_id)

    def create(self, name, info):
        return super().create(name=name, info=info)
