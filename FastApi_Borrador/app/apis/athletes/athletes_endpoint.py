from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List
from schemas import athletes
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from schemas.athletes import Create_Athlete_SchemaIN, Update_Athlete_SchemaIN, Athlete_SchemaOUT
from sqlalchemy.orm import Session
from apis import deps
from core.config import settings
from core import security
import schemas

from apis.athletes import crud
import models

from jose import jwt




router = APIRouter (prefix="/signup",
                    tags=["basicauth"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})





# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=Athlete_SchemaOUT )
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Athlete_SchemaOUT)
async def create_athlete(
    *,
    db: Session = Depends(deps.get_db),
    athlete_in: Create_Athlete_SchemaIN,
    # current_user: models.athletes_info = Depends(deps.get_current_active_superuser)
    ) -> Any:


    athlete = crud.athletes.get_by_email(db, email= athlete_in.email)
    if athlete:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario con el correo electrónico {athlete_in.email}",
        )

    athlete = crud.athletes.get_by_username(db, username= athlete_in.username)
    if athlete:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario con el nombre de usuario \'{athlete_in.username}\'",
        )
        

    athlete = (crud.athletes.create(db, obj_in=athlete_in))
    athlete_dict = vars(athlete)

    
    return athlete_dict

@router.get('/test')
async def test():
    token = deps.reusable_oauth2
    payload = jwt.decode(
    token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    token_data = schemas.TokenPayload(**payload)
    print(token)
    # print(payload)
    return token



# @router.post('/basicauth')
# async def create_user(form: OAuth2PasswordRequestForm = Depends(), email: str):
#     # if not user_db:
#     #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
#     # user = search_userdb(form.username)
    
#     # if not form.password == user.password:
#     #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
        
#     # return {
#     #     "access_token": user.username,
#     #     "token_type": "bearer"
#     # }
#     return { "msg": form }


# def search_user(field: str, key):

#     try:
#         user = db_client.users.find_one({field: key}) #Encontrar usuario
#         # return User( **user_schema(user) ) #Convierte en diccionario y luego crea el objeto User 
#     except:
#         return {"error": "No se ha encontrado el usuario"}