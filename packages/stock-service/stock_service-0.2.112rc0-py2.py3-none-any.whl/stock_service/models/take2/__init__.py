from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def to_dict(sql_instance):
    """
    This method adds an option to convert ORM object to a dict.
    """
    return {
        column.key: getattr(sql_instance, column.key)
        for column in inspect(sql_instance).mapper.column_attrs
    }


# This adds `to_dict` method to models.
Base.to_dict = to_dict
