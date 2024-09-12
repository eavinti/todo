# src/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.tasks.application.task_manager import TaskManager
from src.tasks.infrastructure.db.repository import TaskRepository
from settings.db import get_db

router = APIRouter()


@router.post("/tasks/")
def create_task(title: str, description: str, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    return task_manager.create_task(title, description)


@router.get("/tasks/")
def list_tasks(db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    return task_manager.list_tasks()


@router.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    task = task_manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str,
    description: str,
    completed: bool,
    db: Session = Depends(get_db),
):
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    task = task_manager.update_task(task_id, title, description, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    if not task_manager.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
