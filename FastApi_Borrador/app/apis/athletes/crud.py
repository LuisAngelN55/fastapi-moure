from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from datetime import datetime
from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.athletes_info import Athletes
from schemas.athletes import Create_Athlete_SchemaIN, Update_Athlete_SchemaIN, Athlete_SchemaOUT


class CRUDAthletes(CRUDBase[Athletes, Create_Athlete_SchemaIN, Athlete_SchemaOUT]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.email == email).first()
    
    def get_by_id(self, db: Session, *, id: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.id == id).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.username == username).first()
    

    def create(self, db: Session, *, obj_in: Create_Athlete_SchemaIN) -> Athletes:
        db_obj = Athletes(
            email            = obj_in.email,
            password         = get_password_hash(obj_in.password),
            username         = obj_in.username, 
            display_name     = obj_in.username,
            created_date     = datetime.now(),
            last_connection  = datetime.now(),
            is_active        = True,
            email_verified   = False
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Athletes, obj_in: Union[Create_Athlete_SchemaIN, Dict[str, Any]]
    ) -> Athletes:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[Athletes]:
        Athletes = self.get_by_email(db, email=email)
        if not Athletes:
            return None
        if not verify_password(password, Athletes.hashed_password):
            return None
        return Athletes

    def is_active(self, Athletes: Athletes) -> bool:
        return Athletes.is_active

    def is_superuser(self, Athletes: Athletes) -> bool:
        return Athletes.is_superAthletes


athletes = CRUDAthletes(Athletes)
