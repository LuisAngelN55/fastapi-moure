from typing import Optional

from sqlalchemy.orm import Session
from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.athletes_info import Phones
from schemas.athletes_schema import AthleteCreate, AthleteUpdate
from schemas.phones_schema import PhoneNumberSchemaIn
import uuid

class CRUDPhoneNumber(CRUDBase[Phones, AthleteCreate, AthleteUpdate]):
    
    def get_by_id(self, db: Session, *, id: int) -> Optional[Phones]:
        return db.query(Phones).filter(Phones.id == id).first()
    
    def get_by_athlete(self, db: Session, *, athlete_id: uuid.UUID) -> Optional[Phones]:
        return db.query(Phones).filter(Phones.athlete_id == athlete_id).first()
    
    def get_by_number(self, db: Session, *, phone_number: str, country_code: str ) -> Optional[Phones]:
        return db.query(Phones).filter(Phones.phone_number == phone_number, Phones.country_code_id == country_code).first()

    def create(self, db: Session, *, obj_in: PhoneNumberSchemaIn) -> Phones:
        
        db_phone = Phones(
            athlete_id       = obj_in.athlete_id,
            fcenter_id       = obj_in.fcenter_id,
            country_code_id  = obj_in.country_code_id, 
            phone_number     = obj_in.phone_number
        )
        db.add(db_phone)
        db.flush()
        # db.commit()
        # db.refresh(db_phone)
        return db_phone

    # def update(
    #     self, db: Session, *, db_obj: Athletes, obj_in: Union[AthleteUpdate, Dict[str, Any]]
    # ) -> Athletes:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
        
    #     # Password in payload
    #     if "password" in update_data:
    #         # Password is not empty
    #         if update_data["password"]:
    #             hashed_password = get_password_hash(update_data["password"])
    #             del update_data["password"]
    #             update_data["hashed_password"] = hashed_password
        
    #     if "is_superuser" in update_data:
    #         del update_data["is_superuser"]
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)


phones = CRUDPhoneNumber(Phones)


