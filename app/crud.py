# app/crud.py
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from . import models, schemas

def get_user_by_logto_id(db: Session, logto_user_id: str):
    return db.query(models.User).filter(models.User.logto_user_id == logto_user_id).first()

def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_new_user(db: Session, user_data: dict):
    db_user = models.User(
        logto_user_id=user_data["logto_user_id"],
        is_vip=user_data.get("is_vip", False)
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
