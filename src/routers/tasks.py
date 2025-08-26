from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.tables import models
from src.sch import schemas
from src.database.db import get_db

app = FastAPI(title="Task Manager")


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskOut)
async def create_task(task: schemas.TaskCreate, session: AsyncSession = Depends(get_db)):
    new_task = models.Task(title=task.title, description=task.description)
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


@router.get("/{task_id}", response_model=schemas.TaskOut)
async def get_task(task_id: UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[schemas.TaskOut])
async def list_tasks(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Task))
    return result.scalars().all()


@router.put("/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: UUID, task_data: schemas.TaskUpdate, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Task).where(models.Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return {"detail": "Task deleted"}
