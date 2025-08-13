from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, schemas, models, auth
from .database import engine, get_db

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
async def register_user(
    db: Session = Depends(get_db),
    user_info: dict = Depends(auth.logto_client.fetch_user_info)
):
    # 使用Logto用户信息创建本地用户记录
    user_data = {
        "logto_user_id": user_info["sub"],
        "is_vip": False  # 默认非VIP
    }
    return crud.create_new_user(db, user_data)

# 登录交由Logto前端SDK处理

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

# 挂载静态文件 (放在API路由之后)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/", StaticFiles(directory="templates", html=True), name="templates")
