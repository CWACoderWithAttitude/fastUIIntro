import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_get_index(client: TestClient):
    response = client.get('/')
    assert response.status_code == 200, response.text
    assert response.text.startswith('<!doctype html>\n')
    #assert response.text == "#data = response.json()"
    #print(data)
    #assert data == {"x": "y"}

def test_get_index(client: TestClient):
    response = client.get('/api')
    assert response.status_code == 200, response.text
    assert response.text == 'abc'
    
def Xtest_post_new_ship(client: TestClient):
    ship_json = {
        "name": "USS PyTest",
        "sign": "NX-0815",
        "classification": "Pytest",
        "speed": "Warp 42"
    }
    response = client.post(
        "/api/ships/add",
        #headers={"X-Token": "coneofsilence"},
        json=ship_json,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }    
