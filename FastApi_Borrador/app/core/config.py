from typing import List
from pydantic import BaseSettings, AnyHttpUrl



class Settings(BaseSettings):
    PROJECT_NAME: str = "TryHard_BackEnd"
    admin_email: str = 'lang@zuntrix.com'
    DATABASE_URL: str = 'postgresql://zuntrix:zuntrix@localhost/db_aprendizaje'

    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    


settings = Settings()