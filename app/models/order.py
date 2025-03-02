from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    order_items = relationship('OrderItem',
                               back_populates='order',
                               cascade='all, delete')
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return (f"<Order(id={self.id},"
                f" user_id='{self.user_id}',"
                f" created_at={self.created_at})>")
