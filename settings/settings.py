from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo.db"

    class Config:
        env_file = "../.env"  # Leer variables de entorno si es necesario


settings = Settings()
