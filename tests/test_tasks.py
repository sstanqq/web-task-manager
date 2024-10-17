import pytest
from app.main import app
from fastapi.testclient import TestClient
from app.models import Task

client = TestClient(app)

mock_task = Task(id=1,
                 title="Test Task",
                 description="Task Description",
                 status="New",
                 user_id=1)


@pytest.fixture
def token():
    data = {
        'username': 'user',
        'password': 'password'
    }
    response = client.post('/auth/login/', data=data)
    assert response.status_code == 200
    return response.json()['access_token']


def test_create_task(token):
    data = {
        'title': 'New Task',
        'description': 'Description of the new task',
        'status': 'New'
    }

    response = client.post(
        '/tasks/',
        json=data
    )
    assert response.status_code == 200
    r_json = response.json()
    assert r_json["title"] == data["title"]
    assert r_json["description"] == data["description"]
    assert r_json["status"] == data["status"]


def test_read_task(mock_db_session):

    query = mock_db_session.query.return_value
    query.filter.return_value.first.return_value = mock_task

    response = client.get(
        f'/tasks/{mock_task.id}'
    )
    assert response.status_code == 200
    r_json = response.json()
    assert r_json['title'] == mock_task.title


def test_update_task(mock_db_session):
    updated_data = {
        'title': 'Updated Task',
        'description': 'Updated Description',
        'status': 'In Progress'
    }

    query = mock_db_session.query.return_value
    query.filter.return_value.first.return_value = mock_task

    response = client.put(f'/tasks/{mock_task.id}', json=updated_data)

    assert response.status_code == 200
    r_json = response.json()
    assert r_json['title'] == updated_data['title']
    assert r_json['description'] == updated_data['description']
    assert r_json['status'] == updated_data['status']


def test_update_task_failure(mock_db_session):
    updated_data = {
        'title': 'Updated Task',
        'description': 'Updated Description',
        'status': 'In Progress'
    }

    query = mock_db_session.query.return_value
    query.filter.return_value.first.return_value = None

    response = client.put(f'/tasks/{mock_task.id}', json=updated_data)

    assert response.status_code == 404
    r_json = response.json()
    assert r_json['detail'] == 'Task not found'


def test_delete_task(mock_db_session):
    query = mock_db_session.query.return_value
    query.filter.return_value.first.return_value = mock_task

    mock_db_session.commit = lambda: None

    response = client.delete(f'/tasks/{mock_task.id}')

    assert response.status_code == 200
    assert response.json() == {'detail': 'Task successfully deleted'}


def test_delete_task_failure(mock_db_session):
    query = mock_db_session.query.return_value
    query.filter.return_value.first.return_value = None

    response = client.delete(f'/tasks/{mock_task.id}')

    assert response.status_code == 404
    r_json = response.json()
    assert r_json['detail'] == 'Task not found'
