from schemes.user import UserCreate, UserUpdate
from db.db_conf import get_db, SessionType
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime
from db.models.user_model import User
from services.auth_service import AuthService
from fastapi import status
from services.auth_service import pwd_context

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/")
async def create_user(user: UserCreate, db: SessionType = Depends(get_db)):
    """
    Создать нового пользователя.
    """

    auth_service = AuthService(db)
    existing_user = auth_service.get_user_by_login(user.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already taken")
    
    new_user = auth_service.create_user(user)
    return new_user

@user_router.get("/{user_id}")
async def read_user(user_id: int, db: SessionType = Depends(get_db)):
    """
    Получить информацию о пользователе по ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "login": user.login,
        "email": user.email,
        "active": user.active,
        "created_at": user.created_at
    }

@user_router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: SessionType = Depends(get_db)):
    """
    Обновить информацию о пользователе.
    """
    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    if user.first_name is not None:
        existing_user.first_name = user.first_name
    if user.last_name is not None:
        existing_user.last_name = user.last_name
    if user.login is not None:
        existing_user.login = user.login
    if user.email is not None:
        existing_user.email = user.email
    if user.password_hash is not None:
        existing_user.password_hash = user.password_hash
    if user.active is not None:
        existing_user.active = user.active

    db.commit()
    db.refresh(existing_user)
    return {
        "id": existing_user.id,
        "first_name": existing_user.first_name,
        "last_name": existing_user.last_name,
        "login": existing_user.login,
        "email": existing_user.email,
        "active": existing_user.active,
        "created_at": existing_user.created_at
    }

@user_router.delete("/{user_id}")
async def delete_user(user_id: int, db: SessionType = Depends(get_db)):
    """
    Удалить пользователя по ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} has been deleted"}

@user_router.patch("/{user_id}/reset-password", status_code=status.HTTP_200_OK)
async def reset_user_password(
    user_id: int, 
    db: SessionType = Depends(get_db)
):
    """
    Reset user password to default 'test' (hashed).
    Requires authentication.
    """
    # Find the user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Hash the default password "test"
    hashed_password = pwd_context.hash("test")
    
    # Update the user's password
    user.password_hash = hashed_password
    db.commit()
    db.refresh(user)
    
    return {"message": f"Password for user {user_id} reset successfully"}