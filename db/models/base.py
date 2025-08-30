from typing import Any, Dict
from typing import List

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import Delete, Select, Update, delete, func, select, update
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from api.core.settings import TimeZone
from db.utils.naming import camel_to_snake
from db.utils.dt import get_now


class BaseRetrieveMixin:
    @classmethod
    def _exists(cls, filters: list = None, **kwargs) -> Select:
        """Build and return exists DB query"""

        base_query = select(func.count(1)).select_from(cls)
        if kwargs:
            base_query = base_query.filter_by(**kwargs)
        if filters:
            base_query = base_query.where(*filters)
        return base_query

    @classmethod
    def _get(cls, filters: list = None, order_by: list = None, **kwargs) -> Select:
        """Build and return DB query for getting one instance"""
        base_query = select(cls)
        if kwargs:
            base_query = base_query.filter_by(**kwargs)
        if filters:
            base_query = base_query.where(*filters)
        if order_by:
            base_query = base_query.order_by(*order_by)
        return base_query


class BaseUpdateMixin:
    @classmethod
    def _update(cls, new_data: Dict, filters: List = None, **kwargs) -> Update:
        """Build and return DB query for updating one instance"""
        base_query = update(cls)
        if kwargs:
            base_query = base_query.filter_by(**kwargs)
        if filters:
            base_query = base_query.where(*filters)
        return base_query.values(**new_data)


class BaseDeleteMixin:
    @classmethod
    def _delete(cls, filters: list = None, **kwargs) -> Delete:
        """Build and return DB query for deleting one instance"""
        base_query = delete(cls)
        if filters:
            base_query = base_query.where(*filters)
        if kwargs:
            base_query = base_query.filter_by(**kwargs)
        return base_query


class BaseCRUD(BaseRetrieveMixin, BaseUpdateMixin, BaseDeleteMixin):
    @classmethod
    def exists(cls, filters: list = None, **kwargs) -> Select:
        """Execute DB query and return Bool val"""
        return super()._exists(filters=filters, **kwargs)

    @classmethod
    def get(cls, filters: list = None, **kwargs) -> Select:
        """Execute DB query and return one instance or None"""
        return super()._get(filters=filters, **kwargs)

    @classmethod
    def update(cls, new_data: Dict, filters: List = None, **kwargs) -> Update:
        """Execute DB query for updating one Instance"""
        return super()._update(filters=filters, new_data=new_data, **kwargs)

    @classmethod
    def delete(cls, filters: list = None, **kwargs) -> Delete:
        """Execute DB query and delete one Instance"""
        return super()._delete(filters=filters, **kwargs)


class BaseModel(BaseCRUD, DeclarativeBase):
    """Base model"""

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        doc="Unique element's ID or PK",
    )

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    created_at = Column(DateTime(timezone=TimeZone.IS_ACTIVE), default=get_now, nullable=False)
    updated_at = Column(DateTime(timezone=TimeZone.IS_ACTIVE), onupdate=get_now, nullable=True)
