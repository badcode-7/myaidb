from sqlalchemy.orm import Session
from . import models
from .auth import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_new_user(db: Session, user_data: dict):
    hashed_password = get_password_hash(user_data["password"])
    db_user = models.User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hashed_password
    )
    return create_user(db, db_user)