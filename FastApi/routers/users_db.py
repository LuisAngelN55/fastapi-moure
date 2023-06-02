from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client


router = APIRouter (prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

## Inicia el servidor uvicorn users:app --reload

# Entidad Usuario


users_list = []

 

@router.get('/')
async def users():
    return users_list


@router.get("/{id}")
async def user (id: int):
    return search_user(id)


@router.get("/")
async def user (id: int):
    return search_user(id)


    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User )
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(status_code=404, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    db_client.local.users.insert_one(user_dict)

    return user
        
@router.put('/')
async def user(user: User):
    
    found = False 
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return {"error": "No se ha encontrado el usuario"}
    
    return user
    
    
@router.delete("/{id}")
async def user (id: int):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if not found:
        return {"error": "No se ha encontrado el usuario"}
 


def search_user(id: int):
    users = filter(lambda user: user.id == id , users_list)
    try:
        return list(users)[0]
    except:
        print('An exception occurred')
        return {"error": "No se ha encontrado el usuario"}
    