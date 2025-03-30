from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models.user_model import User
from db.db_conf import get_db
from schemes.user import UserCreate

SECRET_KEY = "itsmykey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_login(self, login: str) -> Optional[User]:
        return self.db.query(User).filter(User.login == login).first()

    def create_user(self, user_data: UserCreate) -> User:
        password_hash = pwd_context.hash(user_data.password)
        user = User(
           first_name=user_data.first_name,
            last_name=user_data.last_name,
            login=user_data.login,
            email=user_data.email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            active=user_data.active
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, login: str, password: str) -> Optional[User]:
        user = self.get_user_by_login(login)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def create_access_token(self, user_id: int) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user_id), "exp": expires_at}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def verify_token(self, token: str) -> Optional[User]:
        """Decode the JWT token and return the user."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(payload.get("sub"))
            return self.db.query(User).filter(User.id == user_id).first()
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")