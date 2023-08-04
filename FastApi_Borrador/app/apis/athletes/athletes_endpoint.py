from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File
from typing import Any
from schemas import athletes_schema
from sqlalchemy.orm import Session
from apis import deps
from core.config import settings
import schemas
from apis.athletes.crud_PhoneNumber import phones
from utils.utils import send_new_account_email
from utils.utils_athletes import convert_athletedb_athleteout, resize_profile_image
from apis.athletes.crud_PhoneNumber import phones
from fastapi.responses import JSONResponse
import pathlib
from apis.athletes import crud
import models



router = APIRouter (prefix="/athletes",
                    tags=["Athletes"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})





# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=Athlete_SchemaOUT )
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=athletes_schema.Athlete)
async def create_athlete(
    *,
    db: Session = Depends(deps.get_db),
    athlete_in: athletes_schema.AthleteCreate,
    # current_user: models.athletes_info = Depends(deps.get_current_active_superuser)
    ) -> Any:

    athlete_in.email = athlete_in.email.lower()
    athlete_in.username = athlete_in.username.lower()

    athlete = crud.athletes.get_by_email(db, email= athlete_in.email)
    if athlete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el correo electrónico {athlete_in.email}",
        )

    athlete = crud.athletes.get_by_username(db, username= athlete_in.username)
    if athlete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el nombre de usuario \'{athlete_in.username}\'",
        )
        

    athlete = (crud.athletes.create(db, obj_in=athlete_in))
    if settings.EMAILS_ENABLED and athlete_in.email:
        send_new_account_email(
            athlete_id=str(athlete.id), email_to=athlete_in.email, username=athlete_in.username, password=athlete_in.password
        )
    
    return athlete


@router.get('/test-phone', response_model=schemas.PhoneNumber)
async def test(
    phone_id : str,
    db: Session = Depends(deps.get_db)):
    # phone = phones.get_by_id(db=db, id=phone_id)
    phone = phones.get_by_athlete(db=db, athlete_id=phone_id )
    
    return phone


@router.post('/test-phone', response_model=schemas.PhoneNumber)
async def create_phone(
    phone_in : schemas.phones_schema.PhoneNumberSchemaIn,
    db: Session = Depends(deps.get_db)):
    # phone = phones.get_by_id(db=db, id=phone_id)
    # phone = phones.get_by_athlete(db=db, athlete_id=phone_id )
    
    phone = phones.create(db, obj_in=phone_in)
    return phone


@router.get("/me", response_model=schemas.AthleteOut)
def read_athlete_me(
    db: Session = Depends(deps.get_db),
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete)
) -> schemas.AthleteOut:
    """
    Get current user.
    """
    # athlete = convert_athletedb_athleteout(athletedb=current_athlete, db=db)
    athlete = schemas.AthleteOut(**current_athlete.__dict__)
    if current_athlete.phone_id:
        phone = phones.get_by_athlete(db=db, athlete_id=str(current_athlete.id))
    else: phone = None
    athlete.phone_number = phone
    return athlete


@router.get("/{athlete_id}", response_model=schemas.Athlete)
def read_athlete_by_id(
    athlete_id: str,
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    try:
        athlete = crud.athletes.get(db, id=athlete_id)
    except:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="The user doesn't exist"
        )
    else:
        if athlete == current_athlete:
            return athlete
        if not crud.athletes.is_superuser(current_athlete):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="The user doesn't have enough privileges"
            )
        return athlete


@router.put("/{athlete_id}", response_model=schemas.AthleteOut)
def update_athlete(
    *,
    db: Session = Depends(deps.get_db),
    athlete_id: str,
    athlete_in: schemas.AthleteUpdate,
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),
) -> Any:
    """
    Update a user.
    """
    athlete = crud.athletes.get(db, id=athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    
    if crud.athletes.get_by_username(db, username= athlete_in.username) and athlete_in.username != athlete.username:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'El nombre de usuario "{athlete_in.username}" ya esta en uso',
        )
    
    
    if athlete_in.phone:
        current_phone = phones.get_by_number(db, phone_number=athlete_in.phone.phone_number,country_code=athlete_in.phone.country_code_id)
        if current_phone:
            if current_phone.id != current_athlete.phone_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El número de telefono {current_phone.phone_number} ya está siendo usado",
                )
            else: delattr(athlete_in, "phone")
            
    
    if athlete == current_athlete or crud.athletes.is_superuser(current_athlete):
        athlete_in.first_name = athlete_in.first_name.capitalize()
        athlete_in.last_name = athlete_in.last_name.capitalize()
        athlete = crud.athletes.update(db, db_obj=athlete, obj_in=athlete_in)
        athlete_out = convert_athletedb_athleteout(athletedb=current_athlete, db=db)
        return athlete_out
    
    raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The user doesn't have enough privileges",
    )


@router.post("/{athlete_id}/profile-image")
async def upload_file(
    background_task: BackgroundTasks, athlete_id: str,
    db: Session = Depends(deps.get_db), file: UploadFile = File(...),
    current_athlete: models.Athletes = Depends(deps.get_current_active_athlete),):

    athlete = crud.athletes.get_by_id(db, id=athlete_id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    
    if athlete == current_athlete or crud.athletes.is_superuser(current_athlete):
        image_suffix = pathlib.Path(file.filename).suffix
        profile_images_path = settings.STATIC_FILES_PATH + "profile_images/"
        profile_image_name = athlete_id
        photo_url = profile_images_path + profile_image_name + image_suffix
        with open(photo_url, "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()
        # background_task.add_task(resize_profile_image, filename = profile_image_name+image_suffix, path = profile_images_path)
        image_path = resize_profile_image(filename=profile_image_name+image_suffix, path=profile_images_path, suffix = image_suffix)
        photo_url = f'{settings.SERVER_HOST}/{image_path}'
        data_update_athlete = schemas.AthleteUpdate(**{ "photo_url": photo_url })
        
        athlete = crud.athletes.update(db, db_obj=athlete, obj_in=data_update_athlete)
        return JSONResponse(content={"msg": "success", "path": photo_url})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The user doesn't have enough privileges",
    )