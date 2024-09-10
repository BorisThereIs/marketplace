from typing import List

from .shop import Shop
from .base import BaseTimeStampedModel
from .category import Category
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, Numeric, Double
from sqlalchemy.orm import relationship


class Product(BaseTimeStampedModel):
    __tablename__ = 'product'
    name = Column(String(100), nullable=False)
    sku = Column(String(64), nullable=False)
    category_id = Column(ForeignKey(Category.id), nullable=False)
    categories = relationship(argument=List[Category], back_populates='product')
    shop_id = Column(ForeignKey(Shop.id), nullable=False)
    shop = relationship(argument=Shop)
    description = Column(String(250), nullable=True)
    # status = Column()
    price = Column(Numeric(scale=4), nullable=False)
    net_weight = Column(Double(precision=8))
    net_lenght = Column(Numeric(scale=2))
    net_width = Column(Numeric(scale=2))
    net_height = Column(Numeric(scale=2))
    gross_weight = Column(Double(precision=8))
    gross_lenght = Column(Numeric(scale=2))
    gross_width = Column(Numeric(scale=2))
    gross_height = Column(Numeric(scale=2))
    # warehouses = Column()
    image_url = Column(String)
    __table_args__ = (
        UniqueConstraint(*[sku, shop_id]),
    )

    def __repr__(self) -> str:
        return f'Product, sku={self.sku}, name={self.name}, shop={self.shop.name}'
    