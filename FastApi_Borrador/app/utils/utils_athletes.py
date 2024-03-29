from schemas.phones_schema import PhoneNumberSchemaIn
from schemas.doc_number_schema import DocNumberSchemaIn
from schemas.athletes_schema import Athlete
import models
from sqlalchemy.orm import Session
import schemas
from apis.athletes import crud_PhoneNumber
from apis.athletes import crud_DocumentNumber
import os
from apis.athletes.crud_PhoneNumber import phones
from apis.athletes.crud_DocumentNumber import doc_numbers
from PIL import Image


def convert_athletedb_athleteout(athletedb: models.Athletes, db: Session) -> schemas.AthleteOut:
    
    if athletedb.phone_id:
        phone = crud_PhoneNumber.phones.get_by_athlete(db=db, athlete_id=str(athletedb.id))
    else: phone = None

    if athletedb.doc_number:
        doc_number = crud_DocumentNumber.doc_numbers.get_by_athlete(db, athlete_id=str(athletedb.id))
    else: doc_number = None
    
    athlete = schemas.AthleteOut(
        id                    = athletedb.id,
        username              = athletedb.username,
        email                 = athletedb.email,

        first_name            = athletedb.first_name,
        last_name             = athletedb.last_name,
        display_name          = athletedb.display_name,
        birthday              = athletedb.birthday,
        photo_url             = athletedb.photo_url,

        phone_number          = phone,
        blood_type            = athletedb.blood_type,
        nationality_code      = athletedb.nationality_code,
        doc_number            = doc_number,
        gender_code           = athletedb.gender_code,

        created_date          = athletedb.created_date,
        last_connection       = athletedb.last_connection,
        email_verified        = athletedb.email_verified,
        is_active             = athletedb.is_active,
        is_superuser          = athletedb.is_superuser,
        google_sub            = athletedb.google_sub,
        facebook_sub          = athletedb.facebook_sub,
    )
    return athlete



def create_update_phone(db: Session, phone_in: PhoneNumberSchemaIn, athlete_db: Athlete) -> models.athletes_info.Phones:
## phone_id: phone_in athlete
    if not athlete_db.phone_id:
        phoneDB = phones.create(db, obj_in= phone_in)
    else:
        phoneDB = phones.get_by_athlete(db, athlete_id=athlete_db.id)
        phones.update(db, db_obj=phoneDB, obj_in=phone_in)

    return phoneDB

def create_update_doc_number(db: Session, phone_in: DocNumberSchemaIn, athlete_db: Athlete) -> models.master_models.Document_Numbers:
## phone_id: phone_in athlete
    if not athlete_db.doc_number_id:
        doc_numberDB = doc_numbers.create(db, obj_in= phone_in)
    else:
        doc_numberDB = doc_numbers.get_by_athlete(db, athlete_id=athlete_db.id)
        phones.update(db, db_obj=doc_numberDB, obj_in=phone_in)

    return doc_numberDB


def resize_profile_image(filename: str, path: str, suffix: str) -> str:
    sizes = [{
        "width": 1280,
        "height": 720
    }, {
        "width": 640,
        "height": 480
    }, {
        "width": 125,
        "height": 125
    }]

    image_path = ''
    # for size in sizes:
    #     size_defined = size["width"], size["height"]
    #     image = Image.open(path + filename, mode="r")
    #     image.thumbnail(size_defined)
    #     image.save(path + str(size["height"]) + "_" + filename)
    
    new_filename: str | None = None
    size_defined = sizes[0].get("width"), sizes[0].get("height")     
    image = Image.open(path + filename, mode="r")
    image.thumbnail(size_defined)

    accepted_suffix = ['.jpg'] # ['.jpg', '.jpeg']
    if suffix not in accepted_suffix:
        image = image.convert('RGB')
        new_filename = filename.replace(suffix, accepted_suffix[0] )
    new_filename = new_filename if new_filename is not None else filename
    image.save(path + str(sizes[0]["height"]) + "_" + new_filename)
    os.remove(path + filename)
    return (path + str(sizes[0]["height"]) + "_" + new_filename)