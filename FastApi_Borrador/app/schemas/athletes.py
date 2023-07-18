from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from datetime import date, datetime

# Entidad Usuario
class Athlete_SchemaIN(BaseModel):
    username :          str
    email :             str
    first_name :        str | None = None
    last_name :         str | None = None
    display_name :      str | None = None
    birthday :          date | None = None
    password :          str
    photo_url :         str | None = None

    blood_type_id :     str | None = None
    nationality_id :    str | None = None
    phone_id :          int | None = None
    gender_code :       str | None = None
    
    
class Athlete_SchemaOUT(BaseModel):
    id :                str
    username :          str
    email :             str
    first_name :        str | None = None
    last_name :         str | None = None
    display_name :      str | None = None
    birthday :          date | None = None
    photo_url :         str | None = None

    blood_type_id :     str | None = None
    nationality_id :    str | None = None
    phone_id :          int | None = None
    gender_code :       str | None = None


class Athlete_Update_Schema(BaseModel):
    username :          str
    email :             str
    first_name :        str | None = None
    last_name :         str | None = None
    display_name :      str | None = None
    birthday :          date | None = None
    password :          str
    photo_url :         str | None = None

    blood_type_id :     str | None = None
    nationality_id :    str | None = None
    phone_id :          int | None = None
    gender_code :       str | None = None
        