from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserRead
from app.schemas.auth import Token
import app.services.auth as service
from app.database import get_db

router = APIRouter()


@router.post('/register', response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.register_user(db, user)


@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(get_db)):
    user = service.authenticate_user(db,
                                     form_data.username,
                                     password=form_data.password)

    access_token = service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
