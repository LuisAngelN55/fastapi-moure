from schemas.phones_schema import PhoneNumberSchemaIn
from schemas.athletes_schema import Athlete
import models
from sqlalchemy.orm import Session
import schemas
from apis.athletes import crud_PhoneNumber
import os
from apis.athletes.crud_PhoneNumber import phones
from PIL import Image


def convert_athletedb_athleteout(athletedb: models.Athletes, db: Session) -> schemas.AthleteOut:
    
    if athletedb.phone_id:
        phone = crud_PhoneNumber.phones.get_by_athlete(db=db, athlete_id=str(athletedb.id))
    else: phone = None
    
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
        blood_type_id         = athletedb.blood_type_id,
        nationality_code      = athletedb.nationality_code,
        document_number_id    = athletedb.document_number_id,
        gender_code           = athletedb.gender_code,

        created_date          = athletedb.created_date,
        last_connection       = athletedb.last_connection,
        email_verified        = athletedb.email_verified,
        is_active             = athletedb.is_active,
        is_superuser          = athletedb.is_superuser,
        google_sub            = athletedb.google_sub,
        facebook_sub          = athletedb.facebook_sub,
    )
    print(athlete)
    return athlete



def create_update_phone(db: Session, phone_in: PhoneNumberSchemaIn, athlete_db: Athlete) -> models.athletes_info.Phones:
## phone_id: phone_in athlete
    if not athlete_db.phone_id:
        phoneDB = phones.create(db, obj_in= phone_in)
    else:
        phoneDB = phones.get_by_athlete(db, athlete_id=athlete_db.id)
        phones.update(db, db_obj=phoneDB, obj_in=phone_in)

    return phoneDB


def resize_profile_image(filename: str, path: str) -> str:
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

    size_defined = sizes[0].get("width"), sizes[0].get("height")     
    image = Image.open(path + filename, mode="r")
    image.thumbnail(size_defined)
    image.save(path + str(sizes[0]["height"]) + "_" + filename)
        
    os.remove(path + filename)
    print("success")
    return (path + str(sizes[0]["height"]) + "_" + filename)