from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskOut(TaskBase):
    id: UUID
    status: TaskStatus

    class Config:
        from_attributes = True
