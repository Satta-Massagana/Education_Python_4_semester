import pytest
from fastapi import status

@pytest.fixture
def auth_token(test_app):
    # зарегистрировать нового пользователя
    user_data = {
        "first_name": "Group",
        "last_name": "User",
        "login": "groupuser",
        "email": "group@example.com",
        "password": "grouppassword123",
        "active": True
    }
    test_app.post("/auth/register", json=user_data)
    
    # залогиниться и получить токен
    login_data = {
        "username": "groupuser",
        "password": "grouppassword123"
    }
    response = test_app.post("/auth/login", data=login_data)
    return response.json()["access_token"]

def test_create_group(test_app, auth_token):
    group_data = {
        "name": "Test Group",
        "description": "Group for testing",
        "user_ids": []
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = test_app.post("/groups/", json=group_data, headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Test Group"

def test_get_group(test_app, auth_token):
    # создать группу
    group_data = {
        "name": "Test Group 2",
        "description": "Another test group",
        "user_ids": []
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/groups/", json=group_data, headers=headers)

    print('RESPONSE!!!!!!!')
    print(create_response.json())
    group_id = create_response.json()["id"]
    
    # запросить группу
    response = test_app.get(f"/groups/{group_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == group_id
    assert response.json()["name"] == "Test Group 2"

def test_update_group(test_app, auth_token):
    # создать группу
    group_data = {
        "name": "Old Group Name",
        "description": "Old description",
        "user_ids": []
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/groups/", json=group_data, headers=headers)
    group_id = create_response.json()["id"]
    
    # изменить созданную группу
    update_data = {
        "name": "New Group Name",
        "description": "New description"
    }
    response = test_app.put(f"/groups/{group_id}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "New Group Name"
    assert response.json()["description"] == "New description"

def test_delete_group(test_app, auth_token):
    # создать группу
    group_data = {
        "name": "Group to delete",
        "description": "Will be deleted",
        "user_ids": []
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    create_response = test_app.post("/groups/", json=group_data, headers=headers)
    group_id = create_response.json()["id"]
    
    # удалить группу
    response = test_app.delete(f"/groups/{group_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # убедиться что группа удалена
    get_response = test_app.get(f"/groups/{group_id}", headers=headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND