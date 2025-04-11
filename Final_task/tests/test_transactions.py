import pytest
from fastapi import status

@pytest.fixture
def auth_token(test_app):
    # Register a user
    user_data = {
        "first_name": "Transaction",
        "last_name": "User",
        "login": "transactionuser",
        "email": "transaction@example.com",
        "password": "transaction123",
        "active": True
    }
    test_app.post("/auth/register", json=user_data)
    
    # Login to get token
    login_data = {
        "username": "transactionuser",
        "password": "transaction123"
    }
    response = test_app.post("/auth/login", data=login_data)
    return response.json()["access_token"]

def test_create_transaction(test_app, auth_token):
    transaction_data = {
        "category": "Food",
        "amount": 10.50,
        "currency": "USD",
        "description": "Lunch",
        "type": "Expense",
        "user_id": 1  # This would be the ID of the user created in the auth_token fixture
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = test_app.post("/transactions/", json=transaction_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["category"] == "Food"
    assert response.json()["amount"] == 10.50

def test_get_transaction(test_app, auth_token):
    # создать транзакцию
    transaction_data = {
        "category": "Transport",
        "amount": 5.75,
        "currency": "USD",
        "description": "Bus ticket",
        "type": "Expense",
        "user_id": 1
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/transactions/", json=transaction_data, headers=headers)
    transaction_id = create_response.json()["id"]
    
    # получить созданную транзакцию
    response = test_app.get(f"/transactions/{transaction_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == transaction_id
    assert response.json()["description"] == "Bus ticket"

def test_update_transaction(test_app, auth_token):
    # создать транзакцию
    transaction_data = {
        "category": "Entertainment",
        "amount": 20.00,
        "currency": "USD",
        "description": "Movie",
        "type": "Expense",
        "user_id": 1
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/transactions/", json=transaction_data, headers=headers)
    transaction_id = create_response.json()["id"]
    
    # изменить созданную транзакцию
    update_data = {
        "amount": 25.00,
        "description": "Movie and snacks"
    }
    response = test_app.put(f"/transactions/{transaction_id}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["amount"] == 25.00
    assert response.json()["description"] == "Movie and snacks"

def test_delete_transaction(test_app, auth_token):
    # создать транзакцию
    transaction_data = {
        "category": "Groceries",
        "amount": 50.00,
        "currency": "USD",
        "description": "Weekly shopping",
        "type": "Expense",
        "user_id": 1
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/transactions/", json=transaction_data, headers=headers)
    transaction_id = create_response.json()["id"]
    
    # удалить созданную транзакцию
    response = test_app.delete(f"/transactions/{transaction_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Transaction with ID {transaction_id} has been deleted"
    
    # убедиться что транзакция удалена
    get_response = test_app.get(f"/transactions/{transaction_id}", headers=headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
