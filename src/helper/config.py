from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    
    APP_NAME : str
    APP_VERSION : str
    ALLOWED_FILE_TYPES :list
    ALLOWED_FILE_SIZE: float
    
    FILE_CHUNK_SIZE : int

    MONGO_URL:str
    MONGO_DATABASE:str
    
    
    class config:
        env_file = ".env"


def get_settings():
    return Settings()
