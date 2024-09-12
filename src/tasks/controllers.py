from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.tasks.application.task_manager import TaskManager
from src.tasks.infrastructure.db.repository import TaskRepository
from settings.db import get_db

router = APIRouter()


@router.post(
    "/tasks/",
    response_description="Create a new task",
    summary="Create Task",
    description="Creates a new task with a title, description, and a default 'completed' status of False.",
    responses={
        201: {"description": "Task successfully created"},
        422: {"description": "Validation error"},
    },
)
def create_task(title: str, description: str, db: Session = Depends(get_db)):
    """
    This endpoint creates a new task with the given `title` and `description`.

    - **title**: The title of the task.
    - **description**: A detailed description of the task.
    """
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    return task_manager.create_task(title, description)


@router.get(
    "/tasks/",
    response_description="List all tasks",
    summary="List Tasks",
    description="Returns a list of all tasks, with their titles, descriptions, and statuses.",
)
def list_tasks(db: Session = Depends(get_db)):
    """
    Retrieves a list of all tasks in the system.
    """
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    return task_manager.list_tasks()


@router.get(
    "/tasks/{task_id}",
    response_description="Get task by ID",
    summary="Get Task",
    description="Retrieves a task by its unique ID.",
    responses={
        200: {"description": "Task found"},
        404: {"description": "Task not found"},
    },
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific task by its ID.

    - **task_id**: The ID of the task to retrieve.
    """
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    task = task_manager.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put(
    "/tasks/{task_id}",
    response_description="Update a task by ID",
    summary="Update Task",
    description="Updates an existing task's title, description, and completion status.",
    responses={
        200: {"description": "Task successfully updated"},
        404: {"description": "Task not found"},
    },
)
def update_task(
    task_id: int,
    title: str,
    description: str,
    completed: bool,
    db: Session = Depends(get_db),
):
    """
    Updates the title, description, and completed status of a specific task.

    - **task_id**: The ID of the task to update.
    - **title**: The updated title of the task.
    - **description**: The updated description of the task.
    - **completed**: The updated completion status of the task.
    """
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    task = task_manager.update_task(task_id, title, description, completed)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
    "/tasks/{task_id}",
    response_description="Delete a task by ID",
    summary="Delete Task",
    description="Deletes a specific task by its ID.",
    responses={
        200: {"description": "Task successfully deleted"},
        404: {"description": "Task not found"},
    },
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Deletes a task by its ID.

    - **task_id**: The ID of the task to delete.
    """
    task_repo = TaskRepository(db)
    task_manager = TaskManager(task_repo)
    if not task_manager.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
