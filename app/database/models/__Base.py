import enum

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql._typing import _ColumnExpressionArgument

from app.errors import AlreadyExistsInDB, NotFoundInDB


class FindableArg(enum.Enum):
    ALL = "ALL"
    SINGLE = "SINGLE"


class Base(DeclarativeBase):
    @classmethod
    def select_where(
        cls, *whereclause: _ColumnExpressionArgument[bool], all=False
    ):
        from .. import session

        stmt = select(cls).where(*whereclause)

        if all:
            return session.scalars(stmt).all()

        item = session.scalars(stmt).first()

        if item == None:
            raise NotFoundInDB(whereclause, cls.__name__)

        return item

    @classmethod
    def exists(cls, *whereclause):
        try:
            cls.select_where(*whereclause)
        except NotFoundInDB:
            pass
        else:
            raise AlreadyExistsInDB(whereclause, cls.__name__)

    def create(self):
        from .. import session

        session.add(self)
        session.commit()

    def delete(self):
        from .. import session

        session.delete(self)
        session.commit()
