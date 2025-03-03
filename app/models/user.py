# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    orders = relationship(
        'Order',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    cart = relationship(
        'Cart',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"