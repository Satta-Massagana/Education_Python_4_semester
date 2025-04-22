from fastapi import FastAPI
from datetime import datetime
import uvicorn
import csv
from contextlib import asynccontextmanager
from db.models.user_model import User
from db.models.transaction_model import Transaction
from db.models.group_model import Group
from db.db_conf import SessionLocal
from api.v1.users import user_router
from api.v1.transactions import transaction_router
from api.v1.groups import groups_router
from api.v1.auth import auth_router
from api.v1.analytics import analytics_router
from db.db_conf import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Загрузка данных при старте
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data_from_csv()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(groups_router)
app.include_router(auth_router)
app.include_router(analytics_router)

def load_data_from_csv():
    session = SessionLocal()
    Base.metadata.create_all(engine)
    
    # Загрузка пользователей
    if session.query(User).first() is None:
        with open('./users.csv', 'r', encoding='utf-8') as file:
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
        with open('./transactions.csv', 'r', encoding='utf-8') as file:
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

    # Загрузка групп
    if session.query(Group).first() is None:
        with open('./groups.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                group = Group(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S'),
                    owner_id=int(row['owner_id'])
                )
                session.add(group)
        session.commit()

    session.close()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )
