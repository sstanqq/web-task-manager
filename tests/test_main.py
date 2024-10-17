from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_main():
    response = client.get('/')

    assert response.status_code == 200
    r_json = response.json()
    assert r_json['message'] == 'Welcome to the web-task-manager!'
