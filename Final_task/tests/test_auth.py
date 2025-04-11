import pytest
from fastapi import status

def test_register_user(test_app):
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "login": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "active": True
    }
    response = test_app.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["login"] == "testuser"

def test_register_existing_user(test_app):
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "login": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "active": True
    }
    # первая регистрация должна пройти
    test_app.post("/auth/register", json=user_data)
    # вторая с таким же логином должна упасть
    response = test_app.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Login already taken" in response.json()["detail"]

def test_login_success(test_app):
    # создать юзера
    user_data = {
        "first_name": "Login",
        "last_name": "Test",
        "login": "logintest",
        "email": "login@example.com",
        "password": "loginpassword123",
        "active": True
    }
    test_app.post("/auth/register", json=user_data)
    
    # попробовать залогиниться
    login_data = {
        "username": "logintest",
        "password": "loginpassword123"
    }
    response = test_app.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(test_app):
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = test_app.post("/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in response.json()["detail"]
