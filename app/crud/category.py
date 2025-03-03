from sqlalchemy.orm import Session

from app.models import Category


# app/crud/category.py

def create_category(db: Session, name: str):
    # Проверяем, существует ли категория с таким именем
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        return None  # Категория уже существует

    # Создаем новую категорию
    new_category = Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).get(category_id)


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def update_category(db: Session, category_id: int, category_name: str):
    category = get_category_by_id(db, category_id)
    if category:
        if category_name != category.name:
            category.name = category_name
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category
