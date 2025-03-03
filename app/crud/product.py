# app/crud/product.py

from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category


def create_product(db: Session, name: str, price: float, quantity: int, category_names: list[str] = None):
    if category_names is None:
        category_names = []

    # Находим существующие категории по их именам
    categories = db.query(Category).filter(Category.name.in_(category_names)).all()

    # Создаем новый товар
    new_product = Product(name=name, price=price, quantity=quantity)
    new_product.categories = categories  # Присваиваем категории после создания объекта

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).get(product_id)


def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()


def update_product(db: Session, product_id: int, name: str = None, price: float = None, quantity: int = None,
                   category_names: list[str] = None):
    product = db.query(Product).get(product_id)
    if not product:
        return None  # Товар не найден

    # Обновляем данные
    if name:
        product.name = name
    if price is not None:
        product.price = price
    if quantity is not None:
        product.quantity = quantity

    # Обновляем категории, если указаны новые имена
    if category_names is not None:
        categories = db.query(Category).filter(Category.name.in_(category_names)).all()
        product.categories = categories

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).get(product_id)
    if not product:
        return None  # Товар не найден

    # Удаляем товар
    db.delete(product)
    db.commit()
    return product
