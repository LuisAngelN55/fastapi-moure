from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from schemas import athletes_schema, phones_schema
from sqlalchemy.orm import Session
from apis import deps
from core.config import settings
from core import security
import schemas
from apis.athletes.crud_PhoneNumber import phones
from utils.utils import send_new_account_email
import uuid
from apis.athletes.crud_PhoneNumber import phones


from apis.athletes import crud
import models

from jose import jwt




router = APIRouter (prefix="/athletes",
                    tags=["Athletes"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})





# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=Athlete_SchemaOUT )
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=athletes_schema.Athlete)
async def create_athlete(
    *,
    db: Session = Depends(deps.get_db),
    athlete_in: athletes_schema.AthleteCreate,
    # current_user: models.athletes_info = Depends(deps.get_current_active_superuser)
    ) -> Any:

    athlete_in.email = athlete_in.email.lower()
    athlete_in.username = athlete_in.username.lower()

    athlete = crud.athletes.get_by_email(db, email= athlete_in.email)
    if athlete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el correo electrónico {athlete_in.email}",
        )

    athlete = crud.athletes.get_by_username(db, username= athlete_in.username)
    if athlete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el nombre de usuario \'{athlete_in.username}\'",
        )
        

    athlete = (crud.athletes.create(db, obj_in=athlete_in))
    if settings.EMAILS_ENABLED and athlete_in.email:
        send_new_account_email(
            athlete_id=str(athlete.id), email_to=athlete_in.email, username=athlete_in.username, password=athlete_in.password
        )
    
    return athlete


@router.get('/test-phone', response_model=schemas.PhoneNumber)
async def test(
    phone_id : str,
    db: Session = Depends(deps.get_db)):
    # phone = phones.get_by_id(db=db, id=phone_id)
    phone = phones.get_by_athlete(db=db, athlete_id=phone_id )
    
    return phone


@router.post('/test-phone', response_model=schemas.PhoneNumber)
async def create_phone(
    phone_in : schemas.phones_schema.PhoneNumberSchemaIn,
    db: Session = Depends(deps.get_db)):
    # phone = phones.get_by_id(db=db, id=phone_id)
    # phone = phones.get_by_athlete(db=db, athlete_id=phone_id )
    
    phone = phones.create(db, obj_in=phone_in)
    return phone


@router.get("/me", response_model=schemas.Athlete)
def read_athlete_me(
    db: Session = Depends(deps.get_db),
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),
) -> Any:
    """
    Get current user.
    """
    return current_athlete


@router.get("/{athlete_id}", response_model=schemas.Athlete)
def read_athlete_by_id(
    athlete_id: str,
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    athlete = crud.athletes.get(db, id=athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The user doesn't exist"
        )
    if athlete == current_athlete:
        return athlete
    if not crud.athletes.is_superuser(current_athlete):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
        )
    return athlete


@router.put("/{athlete_id}", response_model=schemas.Athlete)
def update_athlete(
    *,
    db: Session = Depends(deps.get_db),
    athlete_id: str,
    athlete_in: schemas.AthleteUpdate,
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),
) -> Any:
    """
    Update a user.
    """
    athlete = crud.athletes.get(db, id=athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
        
    if phones.get_by_number(db, phone_number=athlete_in.phone.phone_number, country_code=athlete_in.phone.country_code_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already in use",
        )
    
    if athlete == current_athlete or crud.athletes.is_superuser(current_athlete):
        athlete = crud.athletes.update(db, db_obj=athlete, obj_in=athlete_in)
        return athlete
    
    raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user doesn't have enough privileges",
    )