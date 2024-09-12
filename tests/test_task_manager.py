import pytest
from src.tasks.application.task_manager import TaskManager
from src.tasks.core.models import Task


class MockTaskRepository:
    def __init__(self):
        self.tasks = []
        self.next_id = 0

    def save(self, task: Task):
        if not hasattr(task, "id") or task.id is None:
            task.id = self.next_id
            self.next_id += 1
        self.tasks.append(task)
        return task

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def delete(self, task: Task):
        self.tasks = [t for t in self.tasks if t.id != task.id]


@pytest.fixture
def mock_repository():
    return MockTaskRepository()


@pytest.fixture
def task_manager(mock_repository):
    return TaskManager(mock_repository)


def test_create_task(task_manager):
    task = task_manager.create_task("Test Task", "Task description")
    assert task.title == "Test Task"
    assert task.description == "Task description"
    assert task.completed is False


def test_list_tasks(task_manager):
    task_manager.create_task("Task 1", "Description 1")
    task_manager.create_task("Task 2", "Description 2")
    tasks = task_manager.list_tasks()
    assert len(tasks) == 2


def test_get_task_by_id(task_manager):
    task_manager.create_task("Test Task", "Task description")
    retrieved_task = task_manager.get_task_by_id(task_id=0)

    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "Task description"

    non_existent_task = task_manager.get_task_by_id(task_id=999)
    assert non_existent_task is None


def test_update_task(task_manager):
    task_manager.create_task("Test Task", "Task description")
    updated_task = task_manager.update_task(
        task_id=0,
        title="Updated Task",
        description="Updated description",
        completed=True,
    )

    assert updated_task is not None
    assert updated_task.title == "Updated Task"
    assert updated_task.description == "Updated description"
    assert updated_task.completed is True

    non_existent_update = task_manager.update_task(
        task_id=999, title="Non-existent", description="Non-existent", completed=False
    )
    assert non_existent_update is None


def test_delete_task(task_manager):
    task_manager.create_task("Test Task", "Task description")
    delete_result = task_manager.delete_task(task_id=0)
    assert delete_result is True

    tasks = task_manager.list_tasks()
    assert len(tasks) == 0

    non_existent_delete = task_manager.delete_task(task_id=999)
    assert non_existent_delete is False
