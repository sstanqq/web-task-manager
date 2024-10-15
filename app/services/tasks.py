from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Task
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.enums import TaskStatus


def get_task_by_id(db: Session, task_id: int, user_id: int):
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def get_tasks(db: Session,
              page: int = 1,
              limit: int = 10,
              status: TaskStatus | None = None):
    query = db.query(Task)

    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than or equal to 1"
        )
    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than 0"
        )

    if status:
        query = query.filter(Task.status == status)

    tasks = query.offset((page - 1) * limit).limit(limit).all()
    return tasks


def get_user_tasks(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


def create_task(db: Session, task_data: TaskCreate, user_id: int):
    new_task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session,
                task_id: int,
                task_data: TaskUpdate,
                user_id: int):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()


def mark_task_as_completed(db: Session, task_id: int, user_id: int):
    task = get_task_by_id(db, task_id, user_id)
    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return task
