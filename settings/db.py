from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from .settings import settings  # Importamos la configuración

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = settings.database_url
BASE = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función para inicializar la base de datos y crear las tablas
def init_db():
    BASE.metadata.create_all(bind=engine)


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
