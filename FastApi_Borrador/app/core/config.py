from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, AnyHttpUrl, EmailStr, validator
from pydantic import BaseModel



class Settings(BaseSettings):
    PROJECT_NAME: str = "TryHard"
    admin_email: str = 'lang@zuntrix.com'
    DATABASE_URL: str = 'postgresql://zuntrix:zuntrix@localhost/db_aprendizaje'
    SERVER_NAME: str = "TryHard"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"

    API_V1_STR: str = "/api/v1"
    
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173"]
    FRONTEND_BASE_URL: AnyHttpUrl = "http://localhost:5173/"
    
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
    EMAILS_FROM_NAME: Optional[str] = "TryHard App ⚡️"

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
    
    
    
    
    SOCIAL_AUTH_USER_FIELDS=['email','first_name','username','password']
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "234710864201-7lac6uu9gvebilqdfg4quj2iq8l2upm5.apps.googleusercontent.com"
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
    # Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    ]
    GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
    GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'



class JWT_Settings(BaseModel):
    authjwt_secret_key: str = "D86201963E5A3EA328FC093B8F8D6AABC464049810BAE84D6D7C9964319D24AF"
    authjwt_algorithm: str = "HS256"
    
    # How long an access token should live before it expires.
    # This takes value integer (seconds) or datetime.timedelta, and defaults to 15 minutes.
    # Can be set to False to disable expiration.
    # seg * min
    authjwt_access_token_expires : int = 60 * 0.5
    
    # How long an refresh token should live before it expires.
    # This takes value integer (seconds) or datetime.timedelta, and defaults to 30 days.
    # Can be set to False to disable expiration.
    # seg * min * horas * dias
    authjwt_refresh_token_expires : int = 60 * 60 * 24 * 10
    

settings = Settings()

jwt_settings = JWT_Settings()