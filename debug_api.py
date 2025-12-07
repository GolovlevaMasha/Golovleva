import sys
sys.path.append('.')
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

print("=== Диагностика API ===")

# 1. Проверим GET существующего пользователя
print("\n1. GET существующего пользователя:")
response = client.get("/api/v1/user", params={'email': 'i.i.ivanov@mail.com'})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# 2. Проверим POST создание пользователя
print("\n2. POST создание пользователя:")
test_user = {'name': 'Test User', 'email': 'test.user@mail.com'}
response = client.post("/api/v1/user", json=test_user)
print(f"Status: {response.status_code}")
print(f"Response type: {type(response.json())}")
print(f"Response: {response.json()}")

# 3. Проверим структуру ответа
if response.status_code == 201:
    data = response.json()
    print(f"Response is dict: {isinstance(data, dict)}")
    print(f"Response is int: {isinstance(data, int)}")
    
    # Проверим созданного пользователя
    if isinstance(data, dict) and 'email' in data:
        check_email = data['email']
    elif isinstance(data, int):
        # Если вернулся только ID, проверим по тестовому email
        check_email = test_user['email']
    else:
        check_email = None
    
    if check_email:
        print(f"\n3. Проверка созданного пользователя (email: {check_email}):")
        check_response = client.get("/api/v1/user", params={'email': check_email})
        print(f"Status: {check_response.status_code}")
        if check_response.status_code == 200:
            print(f"User: {check_response.json()}")
