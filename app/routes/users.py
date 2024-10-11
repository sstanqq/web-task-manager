from fastapi import APIRouter

router = APIRouter()


@router.post('/')
def create_user():
    return {'message': 'User created'}


@router.get('/{user_id}')
def get_user(user_id: int):
    return {'message': f'Getting user with id {user_id}'}


@router.put('/{user_id}')
def update_user(user_id: int):
    return {'message': f'Updating user with id {user_id}'}


@router.delete('/{user_id}')
def delete_user(user_id: int):
    return {'message': f'Deleting user with id {user_id}'}
