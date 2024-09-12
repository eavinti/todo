from typing import List
from src.tasks.core.models import Task
from src.tasks.infrastructure.db.repository import TaskRepository


class TaskManager:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title: str, description: str) -> Task:
        task = Task(title=title, description=description)
        task = self.repository.save(task)
        return task

    def list_tasks(self) -> List[Task]:
        return self.repository.get_all()

    def get_task_by_id(self, task_id: int) -> Task:
        return self.repository.get_by_id(task_id)

    def update_task(
        self, task_id: int, title: str, description: str, completed: bool
    ) -> Task:
        task = self.repository.get_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.completed = completed
            self.repository.save(task)
            return task
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.repository.get_by_id(task_id)
        if task:
            self.repository.delete(task)
            return True
        return False

    def complete_task(self, task_id: int):
        task = self.repository.get_by_id(task_id)
        if task:
            task.mark_as_completed()
            self.repository.save(task)
            return task
        return None
