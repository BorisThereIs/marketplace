from sqlalchemy.types import String, Numeric, Boolean, DateTime, Integer
from .base import BaseTimeStampedModel, Base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, validates


class OrderStatus(Base):
    __tablename__ = 'order_status'

    status_name = Column(String(25), nullable=False, unique=True)


class TrackingStatus(Base):
    __tablename__ = 'tracking_status'

    status_name = Column(String(25), nullable=False, unique=True)


class Country(BaseTimeStampedModel):
    __tablename__ = 'country'

    name = Column(String(50), nullable=False, unique=True)


class ShippingAddress(BaseTimeStampedModel):
    __tablename__ = 'shipping_address'

    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship(argument='User', back_populates='addresses')
    is_default_address = Column(Boolean, nullable=False)
    country_id = Column(ForeignKey('country.id'), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    postal_code = Column(String(100))
    addressee = Column(String(100), nullable=False)
    address_1 = Column(String, nullable=False)
    address_2 = Column(String)
    orders = relationship(argument='Order', back_populates='shipping_address')


class Order(BaseTimeStampedModel):
    __tablename__ = 'order'

    status_id = Column(ForeignKey('order_status.id'), nullable=False)
    user_id = Column(ForeignKey('user.id'), nullable=False)
    user = relationship(argument='User', back_populates='orders')
    shipping_address_id = Column(ForeignKey('shipping_address.id'), nullable=False)
    shipping_address = relationship(argument='ShippingAddress', back_populates='orders')
    total_value = Column(Numeric(scale=4))
    tracking_number = Column(String)
    tracking_status_id = Column(ForeignKey('tracking_status.id'))
    approve_date = Column(DateTime)
    order_lines = relationship(argument='OrderLine', back_populates='order')


class OrderLine(BaseTimeStampedModel):
    __tablename__ = 'order_line'

    order_id = Column(ForeignKey('order.id'), nullable=False)
    order = relationship(argument='Order', back_populates='order_lines')
    product_id = Column(ForeignKey('product.id'), nullable=False)
    product = relationship(argument='Product')
    quantity = Column(Integer, default=1)
    product_quantity = Column(Integer, default=1)
    value = Column(Numeric(scale=4))

    @validates('quantity', 'product_quantity')
    def validate_quantity(self, attribut_name, quantity):
        if quantity < 1:
            raise ValueError('product quantity should be more or equal 1')
        return quantity
