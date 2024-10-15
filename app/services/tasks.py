from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Task
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.enums import TaskStatus


def get_task_by_id(db: Session, task_id: int, user_id: int):
    """
    Retrieve a task from the database by its ID and associated user ID.

    Args:
        db (Session): Database session.
        task_id (int): The ID of the task to retrieve.
        user_id (int): The ID of the user to validate ownership.

    Returns:
        Task: The task object if found, raises 404 if not found or not owned
        by user.
    """
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
    """
    Retrieve a paginated list of tasks from the database.

    Args:
        db (Session): Database session.
        page (int): The page number for pagination.
        limit (int): The number of tasks per page.
        status (TaskStatus | None): Optional filter for task status.

    Returns:
        List[Task]: A list of task objects.

    Raises:
        HTTPException: If the page is less than 1 or limit is less than or
        equal to 0.
    """
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
    """
    Retrieve all tasks associated with a specific user.

    Args:
        db (Session): Database session.
        user_id (int): The ID of the user whose tasks to retrieve.

    Returns:
        List[Task]: A list of tasks associated with the user.
    """
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


def create_task(db: Session, task_data: TaskCreate, user_id: int):
    """
    Create a new task in the database.

    Args:
        db (Session): Database session.
        task_data (TaskCreate): Task data for the new task.
        user_id (int): The ID of the user creating the task.

    Returns:
        Task: The newly created task object.
    """
    new_task = Task(**task_data.model_dump(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session,
                task_id: int,
                task_data: TaskUpdate,
                user_id: int):
    """
    Update an existing task in the database.

    Args:
        db (Session): Database session.
        task_id (int): The ID of the task to update.
        task_data (TaskUpdate): New data for the task.
        user_id (int): The ID of the user updating the task.

    Returns:
        Task: The updated task object, raises 404 if task not found or not
        owned by user.
    """
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
    """
    Delete an existing task from the database.

    Args:
        db (Session): Database session.
        task_id (int): The ID of the task to delete.
        user_id (int): The ID of the user deleting the task.

    Raises:
        HTTPException: If the task is not found or not owned by user.
    """
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()


def mark_task_as_completed(db: Session, task_id: int, user_id: int):
    """
    Mark a task as completed in the database.

    Args:
        db (Session): Database session for executing the update.
        task_id (int): The ID of the task to be marked as completed.
        user_id (int): The ID of the user who owns the task.

    Returns:
        Task: The updated task object with the new status.

    Raises:
        HTTPException: If the task is not found or does not belong to the user.
    """
    task = get_task_by_id(db, task_id, user_id)
    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return task
