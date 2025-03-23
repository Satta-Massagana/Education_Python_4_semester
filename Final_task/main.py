from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Type, Generator
from datetime import datetime
import uvicorn
import csv
from models import Base, User, Transaction
from schemas import UserCreate, UserUpdate, TransactionCreate, TransactionUpdate

app = FastAPI()

# Подключение к PostgreSQL
DATABASE_URL = "postgresql://admin1:ASqw12@localhost:5434/admin1"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц при запуске приложения
Base.metadata.create_all(engine)

SessionType = Type[SessionLocal]

def get_db() -> Generator[SessionType, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_data_from_csv():
    session = SessionLocal()
    
    # Загрузка пользователей
    if session.query(User).first() is None:
        with open('./Final_task/users.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    login=row['login'],
                    email=row['email'],
                    password_hash=row['password_hash'],
                    created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S'),
                    active=row['active'].upper() == 'TRUE'
                )
                session.add(user)
        session.commit()
    
    # Загрузка транзакций
    if session.query(Transaction).first() is None:
        with open('./Final_task/transactions.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = Transaction(
                    category=row['category'],
                    amount=float(row['amount']),
                    currency=row['currency'],
                    description=row['description'],
                    type=row['type'],
                    date=datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'),
                    user_id=int(row['user_id'])
                )
                session.add(transaction)
        session.commit()
    session.close()

# Загрузка данных при старте
@app.on_event("startup")
async def startup_event():
    load_data_from_csv()

# CRUD операции для пользователей
@app.post("/users/")
async def create_user(user: UserCreate, db: SessionType = Depends(get_db)):
    """
    Создать нового пользователя.
    """
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        email=user.email,
        password_hash=user.password_hash,
        created_at=datetime.utcnow(),
        active=user.active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "login": new_user.login,
        "email": new_user.email,
        "active": new_user.active,
        "created_at": new_user.created_at
    }

@app.get("/users/{user_id}")
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

@app.put("/users/{user_id}")
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

@app.delete("/users/{user_id}")
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

# CRUD операции для транзакций
@app.post("/transactions/")
async def create_transaction(transaction: TransactionCreate, db: SessionType = Depends(get_db)):
    """
    Создать новую транзакцию.
    """
    new_transaction = Transaction(
        category=transaction.category,
        amount=transaction.amount,
        currency=transaction.currency,
        description=transaction.description,
        type=transaction.type,
        date=datetime.utcnow(),
        user_id=transaction.user_id
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return {
        "id": new_transaction.id,
        "user_id": new_transaction.user_id,
        "date": new_transaction.date,
        "category": new_transaction.category,
        "amount": new_transaction.amount,
        "currency": new_transaction.currency,
        "description": new_transaction.description,
        "type": new_transaction.type
    }

@app.get("/transactions/{transaction_id}")
async def read_transaction(transaction_id: int, db: SessionType = Depends(get_db)):
    """
    Получить информацию о транзакции по ID.
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {transaction_id} not found")
    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "date": transaction.date,
        "category": transaction.category,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "description": transaction.description,
        "type": transaction.type
    }

@app.put("/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: SessionType = Depends(get_db)):
    """
    Обновить информацию о транзакции.
    """
    existing_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not existing_transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {transaction_id} not found")
    
    if transaction.category is not None:
        existing_transaction.category = transaction.category
    if transaction.amount is not None:
        existing_transaction.amount = transaction.amount
    if transaction.currency is not None:
        existing_transaction.currency = transaction.currency
    if transaction.description is not None:
        existing_transaction.description = transaction.description
    if transaction.type is not None:
        existing_transaction.type = transaction.type
    if transaction.user_id is not None:
        existing_transaction.user_id = transaction.user_id

    db.commit()
    db.refresh(existing_transaction)
    return {
        "id": existing_transaction.id,
        "user_id": existing_transaction.user_id,
        "date": existing_transaction.date,
        "category": existing_transaction.category,
        "amount": existing_transaction.amount,
        "currency": existing_transaction.currency,
        "description": existing_transaction.description,
        "type": existing_transaction.type
    }

@app.delete("/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int, db: SessionType = Depends(get_db)):
    """
    Удалить транзакцию по ID.
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {transaction_id} not found")
    db.delete(transaction)
    db.commit()
    return {"message": f"Transaction with ID {transaction_id} has been deleted"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=444
    )
