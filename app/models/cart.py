from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    cart_items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    user = relationship('User', back_populates='cart', uselist=False)

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id})>"
