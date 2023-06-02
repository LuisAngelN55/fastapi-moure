from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter (prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

## Inicia el servidor uvicorn users:app --reload

# Entidad Usuario

 

@router.get('/', response_model= list[User])
async def users():
    return users_schema(db_client.users.find())
 

@router.get("/{id}", response_model= User) #PATH
async def user (id: str):
    if type(search_user("_id", ObjectId(id))) != User:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return search_user("_id", ObjectId(id))


@router.get("/", response_model= User)  #QUERY PARAMETER
async def user (id: str):
    return search_user("_id", ObjectId(id))


    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User )
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)
        
@router.put('/', response_model= User)
async def user(user: User):
    
    try:
        user_dict = dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace({ "_id": ObjectId(user.id) }, user_dict)
    except:
        return {"error": "No se ha encontrado el usuario"}
        
    
    return search_user("_id", ObjectId(user.id))
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user (id: str):

    found = db_client.users.find_one_and_delete({ "_id": ObjectId(id) })
    
    if not found:
        return {"error": "No se ha encontrado el usuario"}
 

def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key}) #Encontrar usuario
        # return User( **user_schema(user) ) #Convierte en diccionario y luego crea el objeto User 
    except:
        return {"error": "No se ha encontrado el usuario"}
    

    