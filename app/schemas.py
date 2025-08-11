# app/schemas.py
from datetime import datetime
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
    created_at: datetime
    updated_at: datetime | None = None

    # v2: 代替 orm_mode=True
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
