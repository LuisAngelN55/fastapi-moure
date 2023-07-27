from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas
from apis import deps
from apis.athletes import crud
from core import security
from core.config import settings
from core.security import get_password_hash
from utils.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    google_get_tokens,
    google_get_user_info
)

router = APIRouter (prefix="/auth",
                    tags=["Auth"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    athlete = crud.athletes.authenticate(
        db, email=form_data.username.lower(), password=form_data.password
    )
    if not athlete:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.athletes.is_active(athlete):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            athlete.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.Athlete)
def test_token(current_user: models.Athletes = Depends(deps.get_current_athlete)) -> Any:
    """
    Test access token
    """
    return current_user



@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    email = email.lower()
    user = crud.athletes.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, username=user.username, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    athlete = crud.athletes.get_by_email(db, email=email)
    if not athlete:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.athletes.is_active(athlete):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    athlete.hashed_password = hashed_password
    db.add(athlete)
    db.commit()
    return {"msg": "Password updated successfully"}


@router.post('/login-google')
async def google_login(google_code: str | None = None):
    if google_code:
        redirect_uri= "http://localhost:5173/auth/social-login"
        tokens = google_get_tokens(code=google_code, redirect_uri=redirect_uri)
        access_token = tokens['access_token']
        
        userdata_from_google = google_get_user_info(access_token = access_token)
        print(userdata_from_google)
    return google_code
