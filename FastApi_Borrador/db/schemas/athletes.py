from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from datetime import date, datetime

# Entidad Usuario
def Athletes(BaseModel):
    return {
        "id" : str,
        "username" : str,
        "email" : str,
        "first_name" : str,
        "last_name" : str,
        "display_name" : str,
        "birthday" : date,
        "password" : str,
        "photo_url" : str,

        "created_date" : datetime,
        "last_connection" : datetime,
        "email_verified" : bool,
        "is_active"     : bool,

        "blood_type_id" : str,
        "nationality_id" : str,
        "phone_id" : int,
        "gender_code" : str
    }