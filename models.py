from __future__ import annotations

import enum
from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import Column, Enum as SQLAEnum, Index
from sqlmodel import Field, Relationship, SQLModel


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., unique=True)
    color: Optional[str] = None

    tasks: List[Task] = Relationship(back_populates="category")
    projects: List[Project] = Relationship(back_populates="category")
    goals: List[Goal] = Relationship(back_populates="category")


class Project(SQLModel, table=True):
    __tablename__ = "project"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    category: Optional[Category] = Relationship(back_populates="projects")
    tasks: List[Task] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
    __tablename__ = "task"
    __table_args__ = (
        Index("ix_task_due_date", "due_date"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    due_date: Optional[date] = Field(default=None, index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    status: TaskStatus = Field(default=TaskStatus.pending, sa_column=Column(SQLAEnum(TaskStatus)))
    recurrence: Optional[str] = None
    priority: int = Field(default=0)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")

    category: Optional[Category] = Relationship(back_populates="tasks")
    project: Optional[Project] = Relationship(back_populates="tasks")


class Goal(SQLModel, table=True):
    __tablename__ = "goal"
    __table_args__ = (
        Index("ix_goal_start_date", "start_date"),
        Index("ix_goal_end_date", "end_date"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    start_date: date = Field(index=True)
    end_date: date = Field(index=True)
    progress: int = Field(default=0, ge=0, le=100)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

    category: Optional[Category] = Relationship(back_populates="goals")


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(..., unique=True)


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    ts: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    entity: str
    action: str