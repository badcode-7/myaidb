# app/schemas.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict  # v2

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_vip: bool = False
    created_at: datetime
    updated_at: datetime | None = None

    # v2: 代替 orm_mode=True
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    is_vip: Optional[bool] = None

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_vip: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
