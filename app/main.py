# main.py

from app.database import engine, Base

if __name__ == "__main__":
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")