import pytest
from fastapi.testclient import TestClient
from main import router

# Создаем клиент для тестирования
client = TestClient(router)

# Тесты для /actors/
def test_get_actors():
    response = client.get("/actors/")
    assert response.status_code == 200
    assert response.json()  

def test_create_actor():
    new_actor = {"name": "John Doe", "age": 40}
    response = client.post("/actors/", json=new_actor)
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_get_actor():
    response = client.get("/actors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_actor():
    updated_actor = {"name": "Jane Doe", "age": 35}
    response = client.put("/actors/1", json=updated_actor)
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"

def test_delete_actor():
    response = client.delete("/actors/1")
    assert response.status_code == 200
    assert response.json() == {}


def test_get_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert response.json()  

def test_create_movie():
    new_movie = {"title": "Test Movie", "release_year": 2022}
    response = client.post("/movies/1", json=new_movie)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Movie"


def test_get_movie():
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_movie():
    response = client.delete("/movies/1")
    assert response.status_code == 200
    assert response.json() == {}
