from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def get_tasks():
    return {'message': 'Getting all tasks'}


@router.get('/user/{user_id}')
def get_user_tasks(user_id: int):
    return {'message': f'Getting tasks for user with id {user_id}'}


@router.get('/{task_id}')
def get_task(task_id: int):
    return {'message': f'Getting task with id {task_id}'}


@router.post('/')
def create_task():
    return {'message': 'Creating a new task'}


@router.put('/{task_id}')
def update_task(task_id: int):
    return {'message': f'Updating task with id {task_id}'}


@router.delete('/{task_id}')
def delete_task(task_id: int):
    return {'message': f'Deleting task with id {task_id}'}
