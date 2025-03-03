# app/models/order_item.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Integer, nullable=False)

    # Отношение с Order
    order = relationship(
        'Order',
        back_populates='order_items'
    )

    # Отношение с Product
    product = relationship(
        'Product',
        back_populates='order_items'
    )

    def __repr__(self):
        return (f"<OrderItem(id={self.id}, order_id={self.order_id}, "
                f"product_id={self.product_id}, quantity={self.quantity})>")