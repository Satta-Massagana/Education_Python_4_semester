from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service import AuthService
from schemes.user import UserCreate, UserLogin, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from db.db_conf import get_db
from sqlalchemy.orm import Session
from api.v1.auth_middleware import get_current_user, User

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    existing_user = auth_service.get_user_by_login(user_data.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already taken")
    
    new_user = auth_service.create_user(user_data)
    return new_user

@auth_router.post("/login")
async def login(user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_data.username, user_data.password)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = auth_service.create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/profile")
def get_group(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "login": user.login,
        "email": user.email,
        "active": user.active,
        "created_at": user.created_at
    }