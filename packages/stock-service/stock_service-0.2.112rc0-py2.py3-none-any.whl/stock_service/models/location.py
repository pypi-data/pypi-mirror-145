from sqlalchemy import Column
from sqlalchemy.dialects import mysql
from sql_client import SQLClient

from stock_service.models import Base
from stock_service.models.base_model import BaseModel


class Location(Base):
    """Location table"""

    __tablename__ = "location"

    location_id = Column("location_id", mysql.INTEGER(11), primary_key=True)
    name = Column("name", mysql.VARCHAR(64))
    info = Column("info", mysql.VARCHAR(256))
    date_created = Column("date_created", mysql.DATETIME())
    date_modified = Column("date_modified", mysql.DATETIME())


class LocationModel(BaseModel):
    """Model for accessing the location table"""

    def __init__(self, client: SQLClient):
        super().__init__(client, Location)

    def get_by_id(self, location_id):
        return super().get_one(location_id=location_id)

    def get_by(self, name=None):
        return super().get_all(name=name)

    def create(self, name, info):
        return super().create(name=name, info=info)
