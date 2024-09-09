from typing import List
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import BaseTimeStampedModel, Base
from .user import AbstractBaseUser


class ShopStatus(Base):
    __tablename__ = 'shop_status'
    status_name = Column(String(50), nullable=False, unique=True)


class Shop(BaseTimeStampedModel):
    __tablename__ = 'shop'
    name = Column(String(100), nullable=False)
    status_id = Column(ForeignKey('shop_status.id'), nullable=False)
    managers = relationship(argument='ShopManager', back_populates='shop')
    
    def __repr__(self) -> str:
        return f'Shop, id={self.id}, name={self.name}, status={self.status_id}'


class ShopManager(AbstractBaseUser):
    __tablename__ = 'shop_manager'
    shop_id = Column(ForeignKey(Shop.id), nullable=False)
    shop = relationship(argument='Shop', back_populates='managers')
