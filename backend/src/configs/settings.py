from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME : str
    PROJECT_VERSION : float
    PROJECT_IS_DEBUG : bool
    PROJECT_PORT : int

    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASSWORD : str
    DB_NAME : str

    JWT_SECRET : str
    JWT_EXPIRATION : int

    REFRESH_TOKEN_SECRET : str
    REFRESH_TOKEN_EXPIRES_IN : str

    LOG_LEVEL : str
    LOG_FILE : str

    API_BASE_URL : str

def get_settings() -> Settings:
    return Settings()