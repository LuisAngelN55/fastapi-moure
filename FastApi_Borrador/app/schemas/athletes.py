from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from datetime import date, datetime

# Entidad Athleta
class Create_Athlete_SchemaIN(BaseModel):
    username :          str
    email :             str
    password :          str

class Update_Athlete_SchemaIN(BaseModel):
    id                   : str
    username             : str
    email                : str
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
    email_verified       : bool | None = None
    is_active            : bool | None = True
    
class Athlete_SchemaOUT(BaseModel):
    id                   : str
    username             : str
    email                : str
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
    email_verified       : bool | None = None
    is_active            : bool | None = True
