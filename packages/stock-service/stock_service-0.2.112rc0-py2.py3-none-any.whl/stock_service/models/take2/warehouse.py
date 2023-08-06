from functools import lru_cache

from sqlalchemy import Column
from sqlalchemy.dialects import mysql
from sqlalchemy.orm.exc import NoResultFound

from stock_service.models.take2 import Base
from stock_service.models.take2 import schema
from stock_service.config import OldConfig
from stock_service.utils import db


config = OldConfig()


class WarehouseDict(schema.Schema):
    pass


class Warehouse(Base):
    __tablename__ = "wms2_warehouses"

    idWarehouse = Column(
        "idWarehouse", mysql.TINYINT(4), nullable=False, primary_key=True
    )
    WarehouseName = Column("WarehouseName", mysql.VARCHAR(45), nullable=False)
    Description = Column("Description", mysql.VARCHAR(255), nullable=True)
    Address = Column("Address", mysql.VARCHAR(255), nullable=True)
    StreetNumber = Column("StreetNumber", mysql.VARCHAR(255), nullable=True)
    Street = Column("Street", mysql.VARCHAR(255), nullable=True)
    Suburb = Column("Suburb", mysql.VARCHAR(255), nullable=True)
    City = Column("City", mysql.VARCHAR(255), nullable=True)
    PostalCode = Column("PostalCode", mysql.VARCHAR(255), nullable=True)
    Telephone = Column("Telephone", mysql.VARCHAR(20), nullable=True)
    AltTelephone = Column("AltTelephone", mysql.VARCHAR(20), nullable=True)

    def to_schema(self) -> WarehouseDict:
        return WarehouseDict(self.to_dict())


@lru_cache(maxsize=2)
def get_warehouse_by_id(warehouse_id: int) -> WarehouseDict:
    sql_client = OldConfig.get_db_client()
    with sql_client.get_session_context(db.ConnectionType.READ.value) as session:
        results = (
            session.query(Warehouse).filter_by(idWarehouse=warehouse_id).one_or_none()
        )
        if results is not None:
            return results.to_schema()
    raise NoResultFound(f"warehouse_id={warehouse_id} not found in wms2_warehouses")
