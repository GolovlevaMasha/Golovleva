import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_get_existed_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}


@pytest.mark.asyncio
async def test_get_nonexistent_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user():
    user_data = {"name": "Alice", "email": "alice@example.com"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/user/", json=user_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
    assert response.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_update_user():
    user_data = {"name": "John Updated", "email": "john.updated@example.com"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/user/1", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"


@pytest.mark.asyncio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/user/1")
    assert response.status_code == 204
    
    # Проверяем, что пользователь удален
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/1")
    assert response.status_code == 404
