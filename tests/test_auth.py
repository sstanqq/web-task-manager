from app.main import app
from fastapi.testclient import TestClient
from app.models import User

client = TestClient(app)


def test_register_user_success(mock_db_session):
    data = {
        'first_name': 'New',
        'last_name': 'User',
        'username': 'user',
        'password': 'password123'
    }

    query = mock_db_session.query.return_value
    filter_result = query.filter.return_value
    filter_result.first.return_value = None

    # Тут имитирую автоинкремент(Потом подумать)
    mock_db_session.add = lambda user: setattr(user, 'id', 1)
    mock_db_session.commit = lambda: None
    mock_db_session.refresh = lambda user: None

    response = client.post('/auth/register/', json=data)
    print(response.json())
    assert response.status_code == 200
    r_json = response.json()
    assert r_json['first_name'] == data['first_name']
    assert r_json['username'] == data['username']


def test_register_user_already_exists(mock_db_session):
    data = {
        'first_name': 'Existing',
        'last_name': 'User',
        'username': 'user',
        'password': 'password123'
    }
    query = mock_db_session.query.return_value
    filter_result = query.filter.return_value
    filter_result.first.return_value = True

    response = client.post('/auth/register/', json=data)

    assert response.status_code == 400
    r_json = response.json()
    assert r_json['detail'] == 'Username already registered'


def test_register_user_invalid_password(mock_db_session):
    data = {
        'first_name': 'New',
        'last_name': 'User',
        'username': 'user',
        'password': '123'  # length < 6
    }
    query = mock_db_session.query.return_value
    filter_result = query.filter.return_value
    filter_result.first.return_value = None

    mock_db_session.add = lambda user: setattr(user, 'id', 1)
    mock_db_session.commit = lambda: None
    mock_db_session.refresh = lambda user: None

    response = client.post('/auth/register/', json=data)
    assert response.status_code == 422
    error = response.json()['detail'][0]
    assert error['msg'] == 'String should have at least 6 characters'
    assert error['input'] == data['password']
    assert error['ctx']['min_length'] == 6


def test_login_user_failure(mock_db_session):
    data = {
        'username': 'user',
        'password': 'password'
    }
    query = mock_db_session.query.return_value
    filter_result = query.filter.return_value
    filter_result.first.return_value = None

    response = client.post('/auth/login/', data=data)
    print(response.json())
    assert response.status_code == 401
    r_json = response.json()
    assert r_json['detail'] == 'Invalid username or password'


def test_login_user_success(mock_db_session):
    data = {
        'username': 'user',
        'password': 'password'
    }

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    mock_user = User(username="user",
                     password=pwd_context.hash(data['password']))
    query = mock_db_session.query.return_value
    filter_result = query.filter.return_value
    filter_result.first.return_value = mock_user

    response = client.post('/auth/login/', data=data)
    assert response.status_code == 200
    print(response.json())
    assert 'access_token' in response.json()
