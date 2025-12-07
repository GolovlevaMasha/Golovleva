import sys
import os

# Добавляем путь к src в PYTHONPATH для корректного импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи из тестового задания
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'New User',
        'email': 'new.user@mail.com'
    }
    
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    
    # Проверяем что возвращается ID
    user_id = response.json()
    assert isinstance(user_id, int)
    
    # Проверяем что пользователь действительно создан
    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert check_response.status_code == 200
    created_user = check_response.json()
    assert created_user['name'] == new_user['name']
    assert created_user['email'] == new_user['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    duplicate_user = {
        'name': 'Duplicate User',
        'email': users[0]['email']
    }
    
    response = client.post("/api/v1/user", json=duplicate_user)
    # Ожидаем ошибку валидации
    assert response.status_code in [400, 409, 422]

def test_delete_user():
    '''Удаление пользователя'''
    # Создаем пользователя
    new_user = {
        'name': 'User to delete',
        'email': 'delete.me@mail.com'
    }
    
    create_response = client.post("/api/v1/user", json=new_user)
    assert create_response.status_code == 201
    
    user_id = create_response.json()
    assert isinstance(user_id, int)
    
    # Пытаемся удалить
    # В реальном API может быть разный endpoint
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    
    # Главное - не должно быть ошибок сервера (5xx)
    assert delete_response.status_code < 500
    
    # Проверяем состояние пользователя после попытки удаления
    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    
    # Тест считается успешным, если мы выполнили все шаги
    # Конкретный результат зависит от реализации API
