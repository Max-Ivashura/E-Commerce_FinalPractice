from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from datetime import datetime

def create_cart(db: Session, user_id: int):
    # Создаем новую корзину
    new_cart = Cart(user_id=user_id)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

def get_user_cart(db: Session, user_id: int):
    # Находим корзину пользователя по user_id
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    return cart

def add_product_to_cart(db: Session, cart_id: int, product_id: int, quantity: int):
    cart = db.query(Cart).get(cart_id)
    if not cart:
        return None  # Корзина не найдена

    product = db.query(Product).get(product_id)
    if not product or product.quantity < quantity:
        return None  # Товар не найден или недостаточно на складе

    # Проверяем, существует ли позиция корзины для этого товара
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
        .first()
    )

    if cart_item:
        # Если позиция уже существует, увеличиваем количество
        cart_item.quantity += quantity
    else:
        # Иначе создаем новую позицию корзины
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(cart_item)

    # Обновляем количество товара на складе
    product.quantity -= quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

def clear_cart(db: Session, cart_id: int):
    # Находим корзину
    cart = db.query(Cart).get(cart_id)
    if not cart:
        return None  # Корзина не найдена

    # Возвращаем товары на склад
    for item in cart.cart_items:
        product = db.query(Product).get(item.product_id)
        if product:
            product.quantity += item.quantity
            db.delete(item)  # Удаляем позицию корзины

    db.commit()
    return cart

def checkout_cart(db: Session, cart_id: int):
    # Находим корзину
    cart = db.query(Cart).get(cart_id)
    if not cart or not cart.cart_items:
        return None  # Корзина не найдена или пуста

    # Создаем новый заказ
    new_order = Order(user_id=cart.user_id, created_at=datetime.now())
    db.add(new_order)

    # Переносим позиции корзины в заказ
    for cart_item in cart.cart_items:
        # Создаем новую позицию заказа
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(order_item)

        # Удаляем позицию из корзины
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)
    return new_order