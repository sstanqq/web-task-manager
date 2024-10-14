from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from app.enums import TaskStatus


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    tasks: Mapped[List['Task']] = relationship(
        back_populates='owner', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return (
            f'User(id={self.id!r}, first_name={self.first_name!r}, '
            f'last_name={self.last_name!r}, user_name={self.username!r})'
        )


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), default=TaskStatus.NEW, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    owner: Mapped['User'] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        return (
            f'Task(id={self.id!r}, title={self.title!r}, '
            f'description={self.description!r}, status={self.status!r})'
        )
