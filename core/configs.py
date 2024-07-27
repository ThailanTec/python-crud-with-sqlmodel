from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:python@localhost:5432/postgres'

    class Config:
        case_sensitive = True

    

settigns: Settings = Settings()