# ToDo

> La app esta usando SQLite para almacenar los datos.
>
> El codigo se encuentra en src/, dentro existe el modulo tasks y las rutas inician en controllers.py

#### Formateo de Código:
```bash
python -m black .
```

#### Linter: 
```bash
flake8 
```

#### Para ejecutar las pruebas:
```bash
pytest
```

#### Para ejecutar la aplicación en Docker:
```bash
docker build -t todo-app .
docker run -d --name fastapi-container -p 8000:8000 todo-app
```

#### Ingresa a
[/docs](http://0.0.0.0:8000/docs)
[/tasks/](http://0.0.0.0:8000/tasks/)
