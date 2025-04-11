import pytest
from fastapi import status

def test_create_user(test_app):
    user_data = {
        "first_name": "New",
        "last_name": "User",
        "login": "newuser",
        "email": "new@example.com",
        "password": "newpassword123",
        "active": True
    }
    response = test_app.post("/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["login"] == "newuser"

def test_get_user(test_app):
    # создать юзера
    user_data = {
        "first_name": "Get",
        "last_name": "User",
        "login": "getuser",
        "email": "get@example.com",
        "password": "getpassword123",
        "active": True
    }
    create_response = test_app.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # получить созданного юзера
    response = test_app.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == user_id
    assert response.json()["login"] == "getuser"

def test_update_user(test_app):
    # создать юзера
    user_data = {
        "first_name": "Update",
        "last_name": "User",
        "login": "updateuser",
        "email": "update@example.com",
        "password": "updatepassword123",
        "active": True
    }
    create_response = test_app.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # изменить созданного юзера
    update_data = {
        "first_name": "Updated",
        "email": "updated@example.com"
    }
    response = test_app.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Updated"
    assert response.json()["email"] == "updated@example.com"

def test_delete_user(test_app):
    # создать юзера
    user_data = {
        "first_name": "Delete",
        "last_name": "User",
        "login": "deleteuser",
        "email": "delete@example.com",
        "password": "deletepassword123",
        "active": True
    }
    create_response = test_app.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # удалить созданного юзера
    response = test_app.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"User with ID {user_id} has been deleted"
    
    # убедиться что юзер больше не существует
    get_response = test_app.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
