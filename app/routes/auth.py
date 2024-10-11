from fastapi import APIRouter

router = APIRouter()


@router.post('/login')
def login():
    return {'message': 'User login'}


@router.post('/logout')
def logout():
    return {'message': 'User logout'}
