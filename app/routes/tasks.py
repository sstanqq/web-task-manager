from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.schemas.tasks import TaskCreate, TaskUpdate, TaskRead
import app.services.tasks as service
from app.database import get_db
from app.services.auth import get_current_user
from app.schemas.users import UserRead

router = APIRouter()


@router.get('/', response_model=List[TaskRead])
def get_tasks(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 10,
        current_user: UserRead = Depends(get_current_user)
        ):
    return service.get_tasks(db, skip, limit)


@router.get('/user/{user_id}', response_model=List[TaskRead])
def get_user_tasks(user_id: int,
                   db: Session = Depends(get_db),
                   current_user: UserRead = Depends(get_current_user)):
    return service.get_user_tasks(db, user_id)


@router.get('/{task_id}', response_model=TaskRead)
def get_task(task_id: int,
             db: Session = Depends(get_db),
             current_user: UserRead = Depends(get_current_user)):
    return service.get_task_by_id(db, task_id, current_user.id)


@router.post('/', response_model=TaskRead)
def create_task(task_data: TaskCreate,
                current_user: UserRead = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return service.create_task(db, task_data, current_user.id)


@router.put('/{task_id}', response_model=TaskRead)
def update_task(task_id: int,
                task_data: TaskUpdate,
                current_user: UserRead = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return service.update_task(db, task_id, task_data, current_user.id)


@router.delete('/{task_id}', response_model=dict)
def delete_task(task_id: int,
                current_user: UserRead = Depends(get_current_user),
                db: Session = Depends(get_db)):
    service.delete_task(db, task_id, current_user.id)
    return {'detail': 'Task successfully deleted'}
