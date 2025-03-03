# app/models/product.py

from sqlalchemy import Column, Integer, Float, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

# Промежуточная таблица для Many-to-Many с Category
product_category = Table(
    'product_category', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id', ondelete='CASCADE')),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'))
)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    # Отношение Many-to-Many с Category
    categories = relationship(
        'Category',
        secondary=product_category,
        back_populates='products'
    )

    # Отношение One-to-Many с OrderItem
    order_items = relationship(
        'OrderItem',
        back_populates='product',
        cascade='all, delete-orphan'
    )

    # Отношение One-to-Many с CartItem
    cart_items = relationship(
        'CartItem',
        back_populates='product',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (f"<Product(id={self.id}, name='{self.name}', "
                f"price={self.price}, quantity={self.quantity})>")