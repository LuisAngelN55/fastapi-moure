from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.athletes_info import Athletes
from schemas.athletes import Athlete_SchemaIN


class CRUDAthletes(CRUDBase[Athletes, Athlete_SchemaIN, Athlete_SchemaIN]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[Athletes]:
        return db.query(Athletes).filter(Athletes.email == email).first()

    def create(self, db: Session, *, obj_in: Athlete_SchemaIN) -> Athletes:
        db_obj = Athletes(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            username=obj_in.username,
            # first_name=obj_in.first_name,
            # is_superAthletes=obj_in.is_superAthletes,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Athletes, obj_in: Union[Athlete_SchemaIN, Dict[str, Any]]
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
