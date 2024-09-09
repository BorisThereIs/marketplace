from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, DateTime, Date
from .base import BaseTimeStampedModel


class UserStatus(BaseTimeStampedModel):
    __tablename__ = 'user_status'
    status_name = Column(String(25), nullable=False, unique=True)


class AbstractBaseUser(BaseTimeStampedModel):
    __abstract__ = True
    password = Column(String)
    last_login = Column(DateTime, nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status_id = Column(ForeignKey('user_status.id', name='user_status_id_fkey'), nullable=False)


class User(AbstractBaseUser):
    __tablename__ = 'user'
    date_of_birth = Column(Date)
    signup_datetime = Column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return f'User, email={self.email}, status={self.status_id}'
