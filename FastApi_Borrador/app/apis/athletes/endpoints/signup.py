from fastapi import APIRouter, Depends, HTTPException, status
from schemas import athletes
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from schemas.athletes import Athlete_SchemaIN, Athlete_SchemaOUT
from sqlalchemy.orm import Session
from apis import deps
from apis.athletes import crud
import models



router = APIRouter (prefix="/signup",
                    tags=["basicauth"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")




# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=Athlete_SchemaOUT )
@router.post('/', status_code=status.HTTP_201_CREATED )
async def create_athlete(*, db: Session = Depends(deps.get_db),
                         athlete: Athlete_SchemaIN,
                         current_user: models.athletes_info = Depends(deps.get_current_active_superuser)):
    # if type(search_user("email", user.email)) == User:
    #     raise HTTPException(status_code=404, detail="El usuario ya existe")

    athlete_dict = dict(athlete)


    # id = db_client.users.insert_one(user_dict).inserted_id

    # new_user = user_schema(db_client.users.find_one({"_id": id}))
    user = crud.athletes.create(db, obj_in=athlete)
    athlete_dict['id'] = 'fesgre'

    return user
    return User(**new_user)



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