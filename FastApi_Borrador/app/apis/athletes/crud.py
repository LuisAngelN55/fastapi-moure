from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from datetime import datetime
from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.athletes_info import Athletes
from schemas.athletes_schema import AthleteCreate, AthleteUpdate

class CRUDAthletes(CRUDBase[Athletes, AthleteCreate, AthleteUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.email == email).first()
    
    def get_by_uuid(self, db: Session, *, uuid: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.uuid == uuid).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.username == username).first()
    

    def create(self, db: Session, *, obj_in: AthleteCreate) -> Athletes:
        db_obj = Athletes(
            email            = obj_in.email,
            hashed_password  = get_password_hash(obj_in.password),
            username         = obj_in.username, 
            display_name     = obj_in.username,
            created_date     = datetime.now(),
            last_connection  = datetime.now(),
            is_active        = True,
            email_verified   = False,
            is_superuser     = False,
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
        
        if "is_superuser" in update_data:
            del update_data["is_superuser"]
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
