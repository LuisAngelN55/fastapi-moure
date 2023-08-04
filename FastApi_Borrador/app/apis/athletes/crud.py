from typing import Any, Dict, Optional, Union
from db.database import SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.athletes_info import Athletes
from schemas.athletes_schema import AthleteCreate, AthleteUpdate
from schemas.phones_schema import PhoneNumberSchemaIn
from apis.athletes.crud_PhoneNumber import phones
from utils.utils_athletes import create_update_phone
from fastapi import HTTPException, status

class CRUDAthletes(CRUDBase[Athletes, AthleteCreate, AthleteUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.email == email).first()
    
    def get_by_id(self, db: Session, *, id: str) -> Optional[Athletes]:
        try:
            athlete =db.query(Athletes).filter(Athletes.id == id).first()
            return athlete
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The user id doesn't exist"
            )
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.username == username).first()
    

    def create(self, db: Session, *, obj_in: AthleteCreate) -> Athletes:
        db_obj = Athletes(
            email            = obj_in.email,
            hashed_password  = get_password_hash(obj_in.password),
            username         = obj_in.username, 
            created_date     = datetime.now(),
            last_connection  = datetime.now(),
            is_active        = True,
            is_superuser     = False,
            
            first_name        = obj_in.first_name or None,
            last_name        = obj_in.last_name or None,
            display_name     = obj_in.display_name or obj_in.username,
            email_verified   = obj_in.email_verified or False,
            google_sub       = obj_in.google_sub or None,
            facebook_sub       = obj_in.facebook_sub or None,
            photo_url        = obj_in.photo_url or None,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Athletes, obj_in: Union[AthleteUpdate, Dict[str, Any]]
    ) -> Athletes:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Password in payload
        if "password" in update_data:
            # Password is not empty
            if update_data["password"]:
                hashed_password = get_password_hash(update_data["password"])
                del update_data["password"]
                update_data["hashed_password"] = hashed_password
        

        if "phone" in update_data:
            phone_in = PhoneNumberSchemaIn(**update_data["phone"])
            phoneDB = create_update_phone(db, phone_in, athlete_db=db_obj)
            update_data["phone_id"] = phoneDB.id
            del update_data["phone"]
            
        
        
        if "is_superuser" in update_data:
            del update_data["is_superuser"]


        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    
    def update_connection(self, db: Session, *, db_obj: Athletes) -> Athletes:
        update_data = { "last_connection" : datetime.now() }
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Athletes]:
        athlete = self.get_by_email(db, email=email)
        if not athlete:
            return None
        if not verify_password(password, athlete.hashed_password):
            return None
        return athlete

    def is_active(self, athlete: Athletes) -> bool:
        return athlete.is_active

    def is_superuser(self, athlete: Athletes) -> bool:
        return athlete.is_superuser


athletes = CRUDAthletes(Athletes)
