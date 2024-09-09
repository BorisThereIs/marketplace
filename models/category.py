from sqlalchemy import ForeignKey
from .base import Base
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'category'
    category = Column(String, nullable=False, unique=True)
    parent_id = Column(ForeignKey('category.id'))
    product = relationship(argument='Product', back_populates='categories')


    def __repr__(self) -> str:
        return f'Category, {self.category}'
    