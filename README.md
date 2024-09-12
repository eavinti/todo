# ToDo

#### Run black
> python -m black .

#### flake8 
> flake8 

#### Run Tests
> pytest


```bash
docker build -t todo-app .
docker run -d --name fastapi-container -p 8000:8000 todo-app

### Ingresa a
[http://0.0.0.0:8000/tasks/](http://0.0.0.0:8000/tasks/)
