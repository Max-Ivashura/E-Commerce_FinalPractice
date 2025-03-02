from sqlalchemy.orm import Session

from app.models import Category


def create_category(db: Session, category_name: str):
    new_category = Category(name=category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).get(category_id)


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
