from datetime import datetime
from .shop import Shop
from .base import Base, BaseTimeStampedModel
from .category import Category
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import String, Numeric, Double, DateTime, Integer
from sqlalchemy.orm import relationship, validates


class Product(BaseTimeStampedModel):
    __tablename__ = 'product'

    name = Column(String(100), nullable=False)
    sku = Column(String(64), nullable=False)
    category_id = Column(ForeignKey(Category.id), nullable=False)
    category = relationship(argument=Category, back_populates='products')
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


class Warehouse(BaseTimeStampedModel):
    __tablename__ = 'warehouse'

    name = Column(String(250), nullable=False, unique=True)
    # status = Column()
    # address = Column()
    # timezone = Column()
    # cutoff_time = Column()


class WarehouseProductStock(Base):
    __tablename__ = 'warehouse_product_stock'

    sku = Column(String(64), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    warehouse_id = Column(ForeignKey('warehouse.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    modified_at = Column(DateTime, onupdate=datetime.now())

    __table_args__ = (
        UniqueConstraint(*[product_id, warehouse_id]),
    )

    @validates('quantity')
    def validate_quantity(self, attribute_name, quantity):
        if quantity < 0:
            raise ValueError(f'{attribute_name} should be more or equal to 0')
        return quantity
    