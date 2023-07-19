from typing import List
from pydantic import BaseSettings, AnyHttpUrl



class Settings(BaseSettings):
    PROJECT_NAME: str = "TryHard_BackEnd"
    admin_email: str = 'lang@zuntrix.com'
    DATABASE_URL: str = 'postgresql://zuntrix:zuntrix@localhost/db_aprendizaje'

    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # JWT Configuration
    JWT_ALGORITHM  : str = "HS256"
    JWT_ACCESS_TOKEN_DURATION : int = 1
    JWT_SECRET  : str = "D86201963E5A3EA328FC093B8F8D6AABC464049810BAE84D6D7C9964319D24AF"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8



settings = Settings()