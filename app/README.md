# Project 2: E-commerce

## Task: Создание системы электронной коммерции

Цель: Реализовать систему электронной коммерции с использованием SQLAlchemy ORM. Система должна включать модели для товаров, категорий, заказов, пользователей и корзины. Настройте Alembic для управления миграциями и реализуйте основные CRUD-операции.

---

### 1. Требования

#### a) Модели
Создайте следующие модели:

1. User:
   - id: Целое число, первичный ключ.
   - username: Строка, уникальное имя пользователя.
   - email: Строка, уникальный email.
   - orders: Связь с моделью Order (One-to-Many).
   - cart: Связь с моделью Cart (One-to-One).

2. Product:
   - id: Целое число, первичный ключ.
   - name: Строка, название товара (уникальное).
   - price: Число с плавающей точкой, цена товара.
   - quantity: Целое число, количество на складе.
   - categories: Связь с моделью Category через промежуточную таблицу (Many-to-Many).

3. Category:
   - id: Целое число, первичный ключ.
   - name: Строка, название категории (уникальное).
   - products: Связь с моделью Product через промежуточную таблицу (Many-to-Many).

4. Order:
   - id: Целое число, первичный ключ.
   - user_id: Внешний ключ, связанный с таблицей users.
   - created_at: Дата и время создания заказа (по умолчанию текущая дата).
   - order_items: Связь с моделью OrderItem (One-to-Many).

5. OrderItem:
   - id: Целое число, первичный ключ.
   - order_id: Внешний ключ, связанный с таблицей orders.
   - product_id: Внешний ключ, связанный с таблицей products.
   - quantity: Целое число, количество товара в заказе.

6. Cart:
   - id: Целое число, первичный ключ.
   - user_id: Внешний ключ, связанный с таблицей users.
   - cart_items: Связь с моделью CartItem (One-to-Many).

7. CartItem:
   - id: Целое число, первичный ключ.
   - cart_id: Внешний ключ, связанный с таблицей carts.
   - product_id: Внешний ключ, связанный с таблицей products.
   - quantity: Целое число, количество товара в корзине.

---

### 2. Отношения между моделями

1. User ↔ Order: One-to-Many (один пользователь может иметь много заказов).
2. User ↔ Cart: One-to-One (один пользователь имеет одну корзину).
3. Product ↔ Category: Many-to-Many (товар может принадлежать нескольким категориям, а категория может содержать несколько товаров).
4. Order ↔ OrderItem: One-to-Many (в одном заказе может быть много позиций).
5. Cart ↔ CartItem: One-to-Many (в одной корзине может быть много позиций).

---

### 3. Миграции

Настройте Alembic для управления изменениями структуры базы данных. Создайте первую миграцию для всех моделей и примените её.

---

### 4. CRUD-операции

Реализуйте следующие CRUD-функции для каждой модели:

#### a) User
- Создание нового пользователя.
- Получение пользователя по ID.
- Обновление данных пользователя.
- Удаление пользователя.

#### b) Product
- Создание нового товара.
- Получение товара по ID.
- Обновление данных товара (например, цена или количество).
- Удаление товара.

#### c) Category
- Создание новой категории.
- Получение категории по ID.
- Обновление названия категории.
- Удаление категории вместе со всеми товарами (если нужно).

#### d) Order
- Создание нового заказа для пользователя.
- Добавление товаров в заказ.
- Получение всех заказов пользователя.
- Удаление заказа.

#### e) Cart
- Создание корзины для пользователя.
- Добавление товаров в корзину.
- Очистка корзины.
- Превращение корзины в заказ.

---

### 5. Дополнительные функции

1. Фильтрация товаров:
   - По категории.
   - По цене (например, найти все товары cheaper than X).
   - По наличию на складе (только товары с quantity > 0).

2. Вычисление общей стоимости:
   - Для корзины.
   - Для заказа.

3. История заказов:
   - Вывод всех заказов конкретного пользователя.
   - Вывод всех товаров в заказе.

---

### 6. Пример использования

Создайте файл main.py для тестирования вашего кода. Например:

from sqlalchemy.orm import sessionmaker
from app.database import engine, Base
from app.models import User, Product, Category, Order, Cart
from app.crud import user, product, category, order, cart
from datetime import datetime

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# 1. Создание данных
print("Создание данных...")
alice = user.create_user(db, username="Alice", email="alice@example.com")
tech_category = category.create_category(db, name="Technology")
phone_product = product.create_product(db, name="Phone", price=199.99, quantity=10, categories=[tech_category])
order1 = order.create_order(db, user_id=alice.id)
cart1 = cart.create_cart(db, user_id=alice.id)

# 2. Чтение данных
print("\nЧтение данных...")
print(f"Пользователь: {alice}")
print(f"Категория: {tech_category}")
print(f"Товар: {phone_product}")
print(f"Заказ: {order1}")
print(f"Корзина: {cart1}")

# 3. Добавление товара в корзину
cart_item = cart.add_to_cart(db, cart_id=cart1.id, product_id=phone_product.id, quantity=2)
print(f"\nДобавлено в корзину: {cart_item}")

# 4. Создание заказа из корзины
new_order = cart.checkout_cart(db, cart_id=cart1.id)
print(f"\nНовый заказ создан: {new_order}")

# 5. Фильтрация товаров
cheap_products = product.filter_products_by_price(db, max_price=200.0)
print(f"\nТовары дешевле 200: {cheap_products}")

---

### 7. Результат

Ваш проект должен включать:
- Файл models.py с определением всех моделей.
- Файл crud.py с CRUD-операциями для каждой модели.
- Файл filters.py с дополнительными функциями (например, фильтрацией товаров).
- Настроенную систему миграций через Alembic.
- Файл main.py для демонстрации работы всех компонентов.
