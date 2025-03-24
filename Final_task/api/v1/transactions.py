from schemes.transaction import TransactionCreate, TransactionUpdate
from db.db_conf import get_db, SessionType
from fastapi import Depends, APIRouter, HTTPException
from datetime import datetime

from db.models.transaction_model import Transaction

transaction_router = APIRouter(prefix="/transactions", tags=["transactions"])

# CRUD операции для транзакций
@transaction_router.post("/")
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

@transaction_router.get("/{transaction_id}")
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

@transaction_router.put("/{transaction_id}")
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

@transaction_router.delete("/{transaction_id}")
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
