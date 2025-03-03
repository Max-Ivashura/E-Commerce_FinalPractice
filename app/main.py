# main.py

from sqlalchemy.orm import sessionmaker
from app.database import engine, Base
from app.models import User, Product, Category, Order, Cart
from app.crud import user, product, category, order, cart
from app.filters.product_filters import filter_products_by_category, filter_products_by_price, filter_products_in_stock
from app.filters.utils import calculate_cart_total, calculate_order_total
from datetime import datetime

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # 1. Создание данных
    print("Создание данных...")

    # Создаем пользователя (если он еще не существует)
    alice = user.get_user_by_email(db, email="alice@example.com")
    if not alice:
        alice = user.create_user(db, username="Alice", email="alice@example.com")
        if alice:
            print(f"  - Пользователь создан: {alice}")
        else:
            print("Ошибка: пользователь не создан.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - Пользователь '{alice.username}' уже существует.")

    # Создаем категорию (если она еще не существует)
    tech_category = category.get_category_by_name(db, name="Technology")
    if not tech_category:
        tech_category = category.create_category(db, name="Technology")
        if tech_category:
            print(f"  - Категория создана: {tech_category}")
        else:
            print("Ошибка: категория не создана.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - Категория '{tech_category.name}' уже существует.")

    # Создаем товар Phone (если он еще не существует)
    phone_product = product.get_product_by_name(db, name="Phone")
    if not phone_product:
        phone_product = product.create_product(
            db,
            name="Phone",
            price=199.99,
            quantity=10,
            category_names=["Technology"]
        )
        if phone_product:
            print(f"  - Товар 'Phone' создан: {phone_product}")
        else:
            print("Ошибка: товар 'Phone' не создан.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - Товар '{phone_product.name}' уже существует.")

    # Создаем товар Laptop (если он еще не существует)
    laptop_product = product.get_product_by_name(db, name="Laptop")
    if not laptop_product:
        laptop_product = product.create_product(
            db,
            name="Laptop",
            price=999.99,
            quantity=5,
            category_names=["Technology"]
        )
        if laptop_product:
            print(f"  - Товар 'Laptop' создан: {laptop_product}")
        else:
            print("Ошибка: товар 'Laptop' не создан.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - Товар '{laptop_product.name}' уже существует.")

    # Создаем заказ (если он еще не существует)
    order1 = order.get_user_orders(db, user_id=alice.id)
    if not order1:
        order1 = order.create_order(db, user_id=alice.id)
        if order1:
            print(f"  - Заказ создан: {order1}")
        else:
            print("Ошибка: заказ не создан.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - У пользователя '{alice.username}' уже есть заказы.")

    # Создаем корзину для пользователя (если она еще не существует)
    cart1 = cart.get_user_cart(db, user_id=alice.id)
    if not cart1:
        cart1 = cart.create_cart(db, user_id=alice.id)
        if cart1:
            print(f"  - Корзина создана: {cart1}")
        else:
            print("Ошибка: корзина не создана.")
            exit(1)  # Прерываем выполнение программы
    else:
        print(f"  - Корзина пользователя '{alice.username}' уже существует.")

    # 2. Чтение данных
    print("\nЧтение данных...")
    print(f"  - Пользователь: {alice}")
    print(f"  - Категория: {tech_category}")
    print("  - Товары:")
    for prod in db.query(Product).all():
        print(f"    - {prod}")

    print(f"  - Заказ: {order1}")
    print(f"  - Корзина: {cart1}")

    # 3. Добавление товаров в корзину
    print("\nДобавление товаров в корзину...")
    cart_item1 = cart.add_product_to_cart(db, cart_id=cart1.id, product_id=phone_product.id, quantity=2)
    if cart_item1:
        print(f"  - Товар '{phone_product.name}' добавлен в корзину: {cart_item1}")
    else:
        print(f"  - Ошибка: товар '{phone_product.name}' не может быть добавлен.")

    cart_item2 = cart.add_product_to_cart(db, cart_id=cart1.id, product_id=laptop_product.id, quantity=1)
    if cart_item2:
        print(f"  - Товар '{laptop_product.name}' добавлен в корзину: {cart_item2}")
    else:
        print(f"  - Ошибка: товар '{laptop_product.name}' не может быть добавлен.")

    # 4. Вычисление общей стоимости корзины
    print("\nОбщая стоимость корзины...")
    try:
        cart_total = calculate_cart_total(db, cart_id=cart1.id)
        print(f"  - Общая стоимость корзины: ${cart_total:.2f}")
    except Exception as e:
        print(f"  - Ошибка при вычислении стоимости корзины: {e}")

    # 5. Создание заказа из корзины
    print("\nПревращение корзины в заказ...")
    try:
        new_order = cart.checkout_cart(db, cart_id=cart1.id)
        if new_order:
            print(f"  - Новый заказ создан: {new_order}")
        else:
            print("  - Ошибка: корзина пуста или не найдена.")
    except Exception as e:
        print(f"  - Ошибка при создании заказа: {e}")

    # 6. Вычисление общей стоимости заказа
    print("\nОбщая стоимость заказа...")
    try:
        if new_order:
            order_total = calculate_order_total(db, order_id=new_order.id)
            print(f"  - Общая стоимость заказа: ${order_total:.2f}")
        else:
            print("  - Нет заказа для расчета стоимости.")
    except Exception as e:
        print(f"  - Ошибка при вычислении стоимости заказа: {e}")

    # 7. Фильтрация товаров
    print("\nФильтрация товаров...")
    try:
        cheap_products = filter_products_by_price(db, max_price=200.0)
        print(f"  - Товары дешевле $200: {[p.name for p in cheap_products]}")

        in_stock_products = filter_products_in_stock(db)
        print(f"  - Товары в наличии: {[p.name for p in in_stock_products]}")

        tech_products = filter_products_by_category(db, category_name="Technology")
        print(f"  - Товары в категории 'Technology': {[p.name for p in tech_products]}")
    except Exception as e:
        print(f"  - Ошибка при фильтрации товаров: {e}")

    # 8. Получение истории заказов пользователя
    print("\nИстория заказов пользователя...")
    try:
        user_orders = order.get_user_orders(db, user_id=alice.id)
        if user_orders:
            for o in user_orders:
                print(f"  - Заказ ID {o.id}, созданный {o.created_at}:")
                order_items = order.get_order_items(db, order_id=o.id)
                for item in order_items:
                    print(f"    - {item['product_name']} x{item['quantity']} = ${item['total']:.2f}")
        else:
            print(f"  - У пользователя '{alice.username}' нет заказов.")
    except Exception as e:
        print(f"  - Ошибка при получении истории заказов: {e}")

    # 9. Очистка корзины
    print("\nОчистка корзины...")
    try:
        cleared_cart = cart.clear_cart(db, cart_id=cart1.id)
        if cleared_cart:
            print(f"  - Корзина очищена: {cleared_cart}")
        else:
            print("  - Ошибка: корзина не найдена.")
    except Exception as e:
        print(f"  - Ошибка при очистке корзины: {e}")
except Exception as e:
    print(f"Критическая ошибка: {e}")
finally:
    db.close()  # Закрываем сессию