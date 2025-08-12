from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, schemas, models, auth
from .database import engine, get_db
from .dependencies import get_current_active_user

app = FastAPI(
    title="用户认证服务",
    description="专注于用户注册、登录和管理的微服务",
    version="1.0.0"
)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")
    
    # 创建新用户
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    return crud.create_new_user(db, user_data)

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: schemas.UserLogin, 
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.username},
        is_admin=user.is_admin
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/users/{user_id}/vip", response_model=schemas.UserResponse)
def update_vip_status(
    user_id: int,
    vip_status: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_admin_user)
):
    updated_user = crud.update_user_vip_status(db, user_id, vip_status.is_vip)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user

@app.get("/admin/users", response_model=List[schemas.AdminUserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_admin_user)
):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(auth.get_current_admin_user)
):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_current_user(current_user: schemas.UserResponse = Depends(get_current_active_user)):
    return current_user

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "user-auth"}
