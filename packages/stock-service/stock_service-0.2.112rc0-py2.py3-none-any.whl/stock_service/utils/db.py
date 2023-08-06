"""
stock-service mysql db api
"""
from enum import Enum
from sqlalchemy.orm.exc import NoResultFound
from stock_service.config import OldConfig
from stock_service.models.take2 import Base


DEADLOCK_MAX_RETRIES = 3
DEADLOCK_RETRY_DELAY_SECONDS = 0.5


class ConnectionType(Enum):
    WRITE = "master"
    READ = "slave"


def query(sql_query: str, *params, role=ConnectionType.WRITE.value):
    """
    runs sql query statement and returns alchemy results cursor
    example usage:
        >>> results = query("SELECT * FROM products WHERE idProduct = %(product)", {"product": 1})
        >>> results.fetchone()
    """

    if isinstance(role, ConnectionType):
        role = role.value

    client = OldConfig.get_db_client()
    with client.get_connection(role) as conn:
        return conn.execute(sql_query, *params)


def get(model: Base, filter_by: dict, read_for_update=False):
    """
    Fetch a unique instance of `model` that matches `kwargs`.

    :param read_for_update: read from master if True
    :param filter_by: dictionary to filter by
    :returns: Instance of the model
    """
    client = OldConfig.get_db_client()
    context = ConnectionType.WRITE if read_for_update else ConnectionType.READ

    with client.get_session_context(context) as session:
        results = session.query(model).filter_by(**filter_by).one_or_none()
        if results is not None:
            return results
    raise NoResultFound(f"results not found for {filter_by}")


def create(instance):
    """
    Insert a new row given a model instance. Return the instance
    that has been updated with its id.

    :param instance: A model instance that will be inserted
    :return: Instance of the model containing the id
    """
    client = OldConfig.get_db_client()

    with client.get_session_context(ConnectionType.WRITE.value) as session:
        session.expire_on_commit = False
        session.add(instance)
        session.commit()
    return instance


def update(model, get_by: dict, values: dict):
    """
    update db using orm instance

    :param model: orm object class
    :param get_by: dictionary representing the primary key to filter by
    :param values: dictionary of values to update
    """
    client = OldConfig.get_db_client()
    with client.get_session_context(ConnectionType.WRITE.value) as session:
        row = session.query(model).get(get_by)
        row.update(values)
        session.expire_on_commit = False
        session.commit()
        return row.first()
