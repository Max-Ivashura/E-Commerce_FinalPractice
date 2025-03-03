from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from datetime import datetime


def create_order(db: Session, user_id: int):
    new_order = Order(user_id=user_id, created_at=datetime.now())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def add_product_to_order(db: Session, order_id: int, product_id: int, quantity: int):
    # Находим заказ
    order = db.query(Order).get(order_id)
    if not order:
        return None  # Заказ не найден

    # Находим товар
    product = db.query(Product).get(product_id)
    if not product or product.quantity < quantity:
        return None  # Товар не найден или недостаточно на складе

    # Создаем новую позицию заказа
    order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
    db.add(order_item)

    # Обновляем количество товара на складе
    product.quantity -= quantity
    db.commit()
    db.refresh(order_item)
    return order_item


def get_orders_by_user(db: Session, user_id: int):
    # Получаем все заказы пользователя
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


def delete_order(db: Session, order_id: int):
    # Находим заказ
    order = db.query(Order).get(order_id)
    if not order:
        return None  # Заказ не найден

    # Возвращаем товары на склад
    for item in order.order_items:
        product = db.query(Product).get(item.product_id)
        if product:
            product.quantity += item.quantity
            db.delete(item)  # Удаляем позицию заказа

    # Удаляем сам заказ
    db.delete(order)
    db.commit()
    return order
