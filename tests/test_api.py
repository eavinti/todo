from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/?title=Test%20Task&description=Test%20description")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test description"
    assert data["completed"] is False


def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
