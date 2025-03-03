# app/models/order.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношение One-to-Many с OrderItem
    order_items = relationship(
        'OrderItem',
        back_populates='order',
        cascade='all, delete-orphan'
    )

    # Отношение с User
    user = relationship(
        'User',
        back_populates='orders'
    )

    def __repr__(self):
        return (f"<Order(id={self.id}, user_id={self.user_id}, "
                f"created_at={self.created_at})>")