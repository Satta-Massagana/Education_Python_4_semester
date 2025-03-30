from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from Final_task.services.auth_service import AuthService
from db.models.user_model import User
from db.db_conf import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    auth_service = AuthService(db)
    user = auth_service.verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user
