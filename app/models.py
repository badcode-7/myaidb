from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    logto_user_id = Column(String(100), unique=True, index=True, nullable=False)
    is_vip = Column(Boolean, default=False)  # VIP状态保留为业务字段
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
