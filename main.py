from fastapi import FastAPI

from src.tasks.controllers import router as task_router
from settings.db import init_db

app = FastAPI()

# Inicializar la base de datos
init_db()

# Incluir las rutas
app.include_router(task_router)
