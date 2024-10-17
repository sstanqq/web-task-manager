from unittest.mock import MagicMock
import pytest
from app.main import app
from app.database import get_db
from app.models import User
from app.services.auth import get_current_user

mock_session = MagicMock()
mock_user = User(id=1, username='user', password='password')


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


def override_get_current_user():
    return mock_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def mock_db_session():
    return mock_session


@pytest.fixture
def mock_user_session():
    return mock_user
