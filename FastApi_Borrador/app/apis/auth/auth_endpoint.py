from datetime import timedelta, datetime
from random  import randint
from fastapi_jwt_auth import AuthJWT

from typing import Any
import urllib
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request, responses
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas
from apis import deps
from apis.athletes import crud
from core import security
from core.config import settings, jwt_settings
from core.security import get_password_hash
from utils.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    google_get_tokens,
    google_get_user_info,
    generate_email_verification_token,
    send_confirmation_email,
    generate_random_password
)

router = APIRouter (prefix="/auth",
                    tags=["Auth"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})




## * ------------------- LOGIN Email/Password ------------------- ##
@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
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
    tokens = security.create_tokens(subject=str(athlete.id), Authorize=Authorize)
    crud.athletes.update_connection(db=db, db_obj=athlete)
    return tokens

## * ------------------- Refresh Token ------------------- ##
@router.post('/refresh-token')
def refresh_token(request: Request, Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    refresh_token = request.headers.get('authorization')

    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}



## * ------------------- TEST ------------------- ##
@router.post("/login/test-token", response_model=schemas.Athlete)
def test_token(current_user: models.Athletes = Depends(deps.get_current_athlete)) -> Any:
    """
    Test access token
    """
    return current_user


## * ------------------- Verify Eamil ------------------- ##
@router.get('/verify-email/{token}', response_class=responses.RedirectResponse)
async def verify_email(token: str, db: Session = Depends(deps.get_db)):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    athlete = crud.athletes.get_by_email(db, email=email)
    if not athlete:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    athlete.is_active = True
    athlete.email_verified = True
    db.add(athlete)
    db.commit()
    params = {'username':athlete.username, 'email':athlete.email,}
    quoted_params = urllib.parse.urlencode(params)

    return responses.RedirectResponse(f'{settings.FRONTEND_BASE_URL}auth/email-verified?{quoted_params}', status_code=303)
    
    
    
## * ------------------- Resend Confirmation Email ------------------- ##
@router.get('/resend-confirmation-email/', response_class=responses.Response)
async def resend_confirmation_email(email: str,db: Session = Depends(deps.get_db)):
    athlete = crud.athletes.get_by_email(db, email=email)
    if not athlete:
        raise HTTPException(
        status_code=404,
        detail=f"No hemos encontrado ningún athleta con el correo: {email}",
    )
    send_confirmation_email(athlete_id=str(athlete.id), email_to=email, username=athlete.username)
    return responses.Response('Email de confirmación de correo enviado', status_code=status.HTTP_200_OK)



## * ------------------- Password Recovery ------------------- ##
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



## * ------------------- Reset Password ------------------- ##
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


## * ------------------- Google Social Login ------------------- ##
@router.post('/login-google')
async def google_login(google_code: str | None = None, db: Session = Depends(deps.get_db), Authorize: AuthJWT = Depends()):
    if not google_code:
        raise HTTPException(status_code=400, detail="Google Code not received")
    
    redirect_uri= "http://localhost:5173/auth/social-login"
    tokens = google_get_tokens(code=google_code, redirect_uri=redirect_uri)
    access_token = tokens['access_token']
    
    userdata_from_google = google_get_user_info(access_token = access_token)
    
    athlete_google = crud.athletes.get_by_email(db, email=userdata_from_google['email'])
    
    if not athlete_google:
        athlete_in = schemas.athletes_schema.AthleteCreate(
            email            = userdata_from_google['email'],
            username         = userdata_from_google['email'][ 0 : userdata_from_google['email'].index('@') ] + str(randint(0,999)),
            password         = generate_random_password(),
            google_sub       = userdata_from_google["sub"],
            first_name       = userdata_from_google["name"],
            last_name        = userdata_from_google["family_name"],
            display_name     = userdata_from_google["given_name"],
            photo_url        = userdata_from_google["picture"],
            
            email_verified   = True,
            last_connection  = datetime.now()
        )

        athlete =  crud.athletes.create(db, obj_in=athlete_in)
        tokens = security.create_tokens(subject=str(athlete.id), Authorize=Authorize)
        return tokens
    
    
    if athlete_google and not athlete_google.google_sub:
        athlete_in: models.Athletes = {
            "google_sub"       : userdata_from_google["sub"],
            "first_name"       : userdata_from_google["name"],
            "last_name"        : userdata_from_google["family_name"],
            "display_name"     : userdata_from_google["given_name"],
            "photo_url"        : userdata_from_google["picture"],
        }
        for attr_db, value in athlete_google.__dict__.items():
            if value and attr_db in athlete_in:
                del athlete_in[attr_db] 
        
        athlete_in['email_verified'] = True
        athlete_in['last_connection'] = datetime.now()
        athlete = crud.athletes.update(db, db_obj=athlete_google, obj_in=athlete_in)
        tokens = security.create_tokens(subject=str(athlete.id), Authorize=Authorize)
        
        return tokens
        
        
    tokens = security.create_tokens(subject=str(athlete_google.id), Authorize=Authorize)
    return tokens
        
    return google_code
