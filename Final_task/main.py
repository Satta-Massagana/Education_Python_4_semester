from fastapi import FastAPI
from datetime import datetime
import uvicorn
import csv
from db.models.user_model import User
from db.models.transaction_model import Transaction
from db.db_conf import Base, DATABASE_URL, engine, SessionLocal
from api.v1.users import user_router
from api.v1.transactions import transaction_router

app = FastAPI()
app.include_router(user_router)
app.include_router(transaction_router)

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


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )
