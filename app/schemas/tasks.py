from pydantic import BaseModel, ConfigDict, Field
from app.enums import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None
    status: TaskStatus = Field(TaskStatus.NEW)
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(BaseModel):
    title: str | None
    description: str | None
    status: TaskStatus | None

    model_config = ConfigDict(from_attributes=True)


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskFilter(BaseModel):
    status: TaskStatus | None
