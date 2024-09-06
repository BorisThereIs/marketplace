from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class BaseTimeStampedModel(Base):
    __abstract__ = True
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, onupdate=datetime.now())