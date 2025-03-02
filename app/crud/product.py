from sqlalchemy.orm import Session

from app.models import Product


def create_product(db: Session, name: str, price: float, quantity: int):
    new_product = Product(name=name, price=price, quantity=quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product_by_id(db: Session, id: int):
    return db.query(Product).get(id)


def update_product(db: Session, id: int, name: str, price: float, quantity: int):
    product = get_product_by_id(db, id)
    if product:
        if name:
            product.name = name
        if price:
            product.price = price
        if quantity:
            product.quantity = quantity
        db.commit()
        db.refresh(product)
    return product


def delete_product(db: Session, id: int):
    product = get_product_by_id(db, id)
    if product:
        db.delete(product)
        db.commit()
        db.refresh(product)
    return product
