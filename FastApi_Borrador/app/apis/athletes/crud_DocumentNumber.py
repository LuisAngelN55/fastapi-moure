from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from core.security import get_password_hash, verify_password
from apis.crud_base import CRUDBase
from models.master_models import Document_Numbers
from schemas.athletes_schema import AthleteCreate, AthleteUpdate
from schemas.doc_number_schema import DocNumberSchemaIn
import uuid

class CRUDDocumentNumber(CRUDBase[Document_Numbers, AthleteCreate, AthleteUpdate]):
    
    def get_by_id(self, db: Session, *, id: int) -> Optional[Document_Numbers]:
        return db.query(Document_Numbers).filter(Document_Numbers.id == id).first()
    
    def get_by_athlete(self, db: Session, *, athlete_id: uuid.UUID) -> Optional[Document_Numbers]:
        return db.query(Document_Numbers).filter(Document_Numbers.athlete_id == athlete_id).first()
    
    def get_by_doc(self, db: Session, *, doc_type_code: str, doc_number: int ) -> Optional[Document_Numbers]:
        return db.query(Document_Numbers).filter(Document_Numbers.doc_type_code == doc_type_code, Document_Numbers.doc_number == doc_number).first()

    def create(self, db: Session, *, obj_in: DocNumberSchemaIn) -> Document_Numbers:
        
        db_doc_number = Document_Numbers(
            athlete_id       = obj_in.athlete_id,
            fcenter_id       = obj_in.fcenter_id,
            doc_type_code    = obj_in.doc_type_code,
            doc_number       = obj_in.doc_number
        )
        db.add(db_doc_number)
        db.flush()
        # db.commit()
        # db.refresh(db_phone)
        return db_doc_number

    def update(
        self, db: Session, *, db_obj: DocNumberSchemaIn, obj_in: Union[AthleteUpdate, Dict[str, Any]]
    ) -> Document_Numbers:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
    #     # Password in payload
    #     if "password" in update_data:
    #         # Password is not empty
    #         if update_data["password"]:
    #             hashed_password = get_password_hash(update_data["password"])
    #             del update_data["password"]
    #             update_data["hashed_password"] = hashed_password
        
    #     if "is_superuser" in update_data:
    #         del update_data["is_superuser"]
        return super().update(db, db_obj=db_obj, obj_in=update_data)


doc_numbers = CRUDDocumentNumber(Document_Numbers)


