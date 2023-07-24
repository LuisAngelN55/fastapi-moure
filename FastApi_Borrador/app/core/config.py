from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, AnyHttpUrl, EmailStr, validator



class Settings(BaseSettings):
    PROJECT_NAME: str = "TryHard"
    admin_email: str = 'lang@zuntrix.com'
    DATABASE_URL: str = 'postgresql://zuntrix:zuntrix@localhost/db_aprendizaje'
    SERVER_NAME: str = "TryHard"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"

    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # JWT Configuration
    JWT_ALGORITHM  : str = "HS256"
    JWT_ACCESS_TOKEN_DURATION : int = 1
    JWT_SECRET  : str = "D86201963E5A3EA328FC093B8F8D6AABC464049810BAE84D6D7C9964319D24AF"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    
    #EMAIL
    SMTP_SSL: bool = True
    SMTP_PORT: Optional[int] = "465"
    SMTP_HOST: Optional[str] = "smtp.hostinger.com"
    SMTP_USER: Optional[str] = "listen@tryhard.app"
    SMTP_PASSWORD: Optional[str] = "Tr-Hd-2022*"
    EMAILS_FROM_EMAIL: Optional[EmailStr] = "listen@tryhard.app"
    EMAILS_FROM_NAME: Optional[str] = "TryHard App"

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "lang@zuntrix.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "lang@zuntrix.com"
    FIRST_SUPERUSER_PASSWORD: str = "123456789"
    USERS_OPEN_REGISTRATION: bool = False



settings = Settings()