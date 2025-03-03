# app/filters/utils.py

from sqlalchemy.orm import Session

from app.models import OrderItem
from app.models.cart_item import CartItem
from app.models.product import Product

def calculate_cart_total(db: Session, cart_id: int):
    # Вычисляем сумму через JOIN между CartItem и Product
    total = (
        db.query(CartItem)
        .join(Product, CartItem.product_id == Product.id)
        .filter(CartItem.cart_id == cart_id)
        .with_entities((CartItem.quantity * Product.price).label('total'))
        .all()
    )
    return sum(item.total for item in total)

def calculate_order_total(db: Session, order_id: int):
    # Вычисляем сумму через JOIN между OrderItem и Product
    total = (
        db.query(OrderItem)
        .join(Product, OrderItem.product_id == Product.id)
        .filter(OrderItem.order_id == order_id)
        .with_entities((OrderItem.quantity * Product.price).label('total'))
        .all()
    )
    return sum(item.total for item in total)