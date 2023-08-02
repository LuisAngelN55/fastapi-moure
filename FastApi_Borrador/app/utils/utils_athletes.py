from schemas.phones_schema import PhoneNumberSchemaIn
from schemas.athletes_schema import Athlete
import models
from sqlalchemy.orm import Session

from apis.athletes.crud_PhoneNumber import phones

def create_update_phone(db: Session, phone_in: PhoneNumberSchemaIn, athlete_db: Athlete) -> models.athletes_info.Phones:
## phone_id: phone_in athlete
    if not athlete_db.phone_id:
        phoneDB = phones.create(db, obj_in= phone_in)
    else:
        phoneDB = phones.get_by_athlete(db, athlete_id=athlete_db.id)
        phones.update(db, db_obj=phoneDB, obj_in=phone_in)

    return phoneDB