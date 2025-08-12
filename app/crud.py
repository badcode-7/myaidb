# app/crud.py
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

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

def update_user_vip_status(db: Session, user_id: int, is_vip: bool):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db_user.is_vip = is_vip
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
