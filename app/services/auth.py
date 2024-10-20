from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.schemas.auth import UserCreate
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user_by_id(db: Session, user_id: int):
    """
    Retrieve a user from the database by their ID.

    Args:
        db (Session): Database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found, raises 404 if not found.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        db (Session): Database session.
        username (str): The username of the user to retrieve.

    Returns:
        User: The user object if found, raises 404 if not found.
    """
    db_user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token for user authentication.

    Args:
        data (dict): User data to include in the token payload.
        expires_delta (timedelta, optional): Expiration time delta for the
        token.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = (
            datetime.now(timezone.utc) +
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (str): The JWT token from the request.
        db (Session): Database session.

    Returns:
        User: The current user object if valid, raises 401 if invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user


def register_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        user (UserCreate): User data for registration.

    Returns:
        User: The newly created user object, raises 400 if username already
        exists.
    """
    existing_user = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user based on username and password.

    Args:
        db (Session): Database session.
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        User: The authenticated user object, raises 401 if credentials are
        invalid.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
