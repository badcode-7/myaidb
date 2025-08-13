from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from logto import LogtoClient
from .database import get_db
from .config import settings
from . import schemas

logto_client = LogtoClient(
    endpoint=settings.logto_endpoint,
    app_id=settings.logto_app_id,
    app_secret=settings.logto_app_secret
)

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(logto_client.get_access_token)
):
    try:
        user_info = await logto_client.fetch_user_info(token)
        user = db.query(models.User).filter(
            models.User.logto_user_id == user_info["sub"]
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not registered"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

async def get_current_admin_user(
    current_user: schemas.UserResponse = Depends(get_current_user)
):
    user_info = await logto_client.fetch_user_info()
    if "admin" not in user_info.get("roles", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user
