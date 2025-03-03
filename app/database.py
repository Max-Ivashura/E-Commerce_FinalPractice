# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./e-commerce.db"

# Создаем движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Для SQLite (необходимо при работе с несколькими потоками)
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
from app.models import Base  # Импортируем Base из models/base.py

# Функция для получения сессии (например, для использования в FastAPI или Flask)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Импортируем все модели, чтобы Alembic их увидел
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from app.models.cart_item import CartItem