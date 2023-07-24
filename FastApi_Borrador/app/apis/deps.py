from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from schemas import athletes_schema, token as tokenSchema
from models import athletes_info
from core import security
from core.config import settings
from db.database import SessionLocal
from apis.athletes import crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_athlete(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> athletes_info.Athletes:
    
    try:
        
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = tokenSchema.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    athlete = crud.athletes.get(db, id=token_data.sub)
    if not athlete:
        raise HTTPException(status_code=404, detail="User not found")
    return athlete


def get_current_active_athlete(
    current_athlete: athletes_info = Depends(get_current_athlete),
) -> athletes_info:
    if not crud.athletes.is_active(current_athlete):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_athlete


def get_current_active_superuser(
    current_athlete: athletes_info = Depends(get_current_athlete),
) -> athletes_info:
    
    if not crud.athletes.is_superuser(current_athlete):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_athlete