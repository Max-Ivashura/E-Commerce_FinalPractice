from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.models import Base

product_category = Table(
    'product_category', Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    categories = relationship('Category',
                              secondary=product_category,
                              back_populates='products')

    order_items = relationship('OrderItem', back_populates='product', cascade='all, delete-orphan')
    cart_items = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')

    def __repr__(self):
        return (f"<Product(id={self.id}, name='{self.name},"
                f" price={self.price}, quantity={self.quantity})>")
