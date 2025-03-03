from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category


def filter_products_by_category(db: Session, category_name: str):
    # Находим категорию по имени
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        return []  # Категория не найдена

    # Возвращаем все товары этой категории
    return category.products


def filter_products_by_price(db: Session, max_price: float):
    # Находим товары с ценой меньше max_price
    return db.query(Product).filter(Product.price <= max_price).all()


def filter_products_in_stock(db: Session):
    # Находим товары с количеством больше 0
    return db.query(Product).filter(Product.quantity > 0).all()
