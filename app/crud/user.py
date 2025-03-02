from sqlalchemy.orm import Session

from app.models import User


def create_user(db: Session, username: str, email: str):
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Обновляем объект после сохранения
    return new_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).get(user_id)


def update_user(db: Session, user_id: int, username: str, email: str):
    user = db.query(User).get(user_id)
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    if user:
        db.delete(user)
        db.commit()
    return user
