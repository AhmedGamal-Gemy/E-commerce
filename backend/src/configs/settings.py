from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME : str
    PROJECT_VERSION : str
    PROJECT_IS_DEBUG : bool
    PROJECT_PORT : int

    API_PREFIX : str

    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASSWORD : str
    DB_NAME : str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REFRESH_TOKEN_SECRET : str

    LOG_LEVEL : str
    LOG_FILE : str

    API_BASE_URL : str

def get_settings() -> Settings:
    return Settings()