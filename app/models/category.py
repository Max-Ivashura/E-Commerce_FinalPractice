# app/models/category.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.product import product_category  # Импортируем промежуточную таблицу

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    products = relationship(
        'Product',
        secondary=product_category,
        back_populates='categories'
    )

    def __repr__(self):
        return f"<Category(name='{self.name}')>"