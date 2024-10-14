from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserUpdate, UserRead
import app.services.users as service
from app.database import get_db

router = APIRouter()


@router.post('/', response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user)


@router.get('/{username}', response_model=UserRead)
def get_user(username: str, db: Session = Depends(get_db)):
    return service.get_user_by_username(db, username)


@router.put('/{user_id}', response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return service.update_user(db, user_id, user)


@router.delete('/{user_id}', response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service.delete_user(db, user_id)
    return {'detail': 'User deleted successfully'}
