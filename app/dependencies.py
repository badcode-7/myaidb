from fastapi import Depends
from .database import get_db
from .auth import get_current_user
from .schemas import UserResponse

def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
    db = Depends(get_db)
):
    return current_user