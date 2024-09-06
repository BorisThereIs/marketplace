from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Date
from .base import BaseTimeStampedModel


class UserStatus(BaseTimeStampedModel):
    __tablename__ = 'user_status'
    status_name = Column(String(25), nullable=False, unique=True)


class User(BaseTimeStampedModel):
    __tablename__ = 'user'
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    status = Column(ForeignKey('user_status.id'), nullable=False)
    signup_datetime = Column(DateTime, nullable=False)

