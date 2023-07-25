from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from datetime import date, datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid



# Athlete entity - Shared properties
class AthleteBase(BaseModel):
    username             : str | None = None
    email                : EmailStr | None = None
    first_name           : str | None = None
    last_name            : str | None = None
    display_name         : str | None = None
    birthday             : date | None = None
    photo_url            : str | None = None

    blood_type_id        : int | None = None
    nationality_code     : str | None = None
    phone_id             : int | None = None
    document_number_id   : int | None = None    
    gender_code          : str | None = None
    
    created_date         : datetime | None = None    
    last_connection      : datetime | None = None
    email_verified       : bool | None = False
    is_active            : bool | None = True
    is_superuser         : bool | None = False

# class PhoneNumber(BaseModel):
#     athlete_id           : str
#     fcenter_id
#     country_code_id
#     phone_number

# Athlete entity - Properties to receive via API on creation
class AthleteCreate(AthleteBase):
    username             : str
    email                : EmailStr
    password             : str
    
    
# Athlete entity - Properties to receive via API on update
class AthleteUpdate(AthleteBase):
    password             : str | None = None
    
    
class AthleteInDBBase(AthleteBase):
    id                 : uuid.UUID
    class Config:
        orm_mode = True


# Additional properties to return via API
class Athlete(AthleteInDBBase):
    pass


# Additional properties stored in DB
class AthleteInDB(AthleteInDBBase):
    hashed_password: str
