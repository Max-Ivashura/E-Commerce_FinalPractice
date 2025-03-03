# app/models/cart_item.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Integer, nullable=False)

    # Отношение с Cart
    cart = relationship(
        'Cart',
        back_populates='cart_items'
    )

    # Отношение с Product
    product = relationship(
        'Product',
        back_populates='cart_items'
    )

    def __repr__(self):
        return (f"<CartItem(id={self.id}, cart_id={self.cart_id}, "
                f"product_id={self.product_id}, quantity={self.quantity})>")