# src/infrastructure/db/repository.py
from typing import List
from sqlalchemy.orm import Session
from src.tasks.infrastructure.db.models import TaskORM
from src.tasks.core.models import Task


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, task: Task):
        # Guardar la tarea en la base de datos
        if not task.id:
            db_task = TaskORM(
                title=task.title, description=task.description, completed=task.completed
            )
            self.db_session.add(db_task)
        else:
            db_task = self.db_session.query(TaskORM).filter_by(id=task.id).first()
            db_task.title = task.title
            db_task.description = task.description
            db_task.completed = task.completed

        self.db_session.commit()
        self.db_session.refresh(db_task)
        return self._to_task(db_task)

    def get_all(self) -> List[Task]:
        # Obtener todas las tareas de la base de datos
        return [self._to_task(task) for task in self.db_session.query(TaskORM).all()]

    def get_by_id(self, task_id: int) -> Task:
        # Obtener una tarea por su ID
        task_orm = self.db_session.query(TaskORM).filter_by(id=task_id).first()
        return self._to_task(task_orm) if task_orm else None

    def delete(self, task: Task):
        # Eliminar la tarea de la base de datos
        db_task = self.db_session.query(TaskORM).filter_by(title=task.title).first()
        if db_task:
            self.db_session.delete(db_task)
            self.db_session.commit()

    def _to_task(self, task_orm: TaskORM) -> Task:
        # Convertir el modelo ORM al modelo de dominio
        task_data = {
            "title": task_orm.title,
            "description": task_orm.description,
            "completed": task_orm.completed,
        }

        # Solo incluir el id si no es None
        if task_orm.id is not None:
            task_data["id"] = task_orm.id

        return Task(**task_data)
