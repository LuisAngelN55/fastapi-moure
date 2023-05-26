from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

## Inicia el servidor uvicorn users:app --reload

# Entidad Usuario
class User(BaseModel):
    id :        int
    name:       str
    surname:    str
    url:        str
    age:         int

users_list = [
    User(id= 1, name = "Luis", surname = "Naranjo", url = "https://zuntrix.com", age= 30 ),
    User(id= 2, name = "Angel", surname = "Giraldo", url = "https://tryhard.app", age= 31 ),
    User(id= 3, name = "Andrea", surname = "Jimenez", url = "https://Andrea.com", age= 27 ),
    User(id= 4, name = "Martha", surname = "Muriel", url = "https://Martha.app", age= 55 )
    ]


@router.get("/usersjson")
async def users():
    return [
        {"name": "Luis", "surname": "Naranjo", "url": "https://zuntrix.com", "age": 30},
        {"name": "", "surname": "Giraldo", "url": "https://tryhard.app", "age": 31},
    ]
    

@router.get('/users/')
async def users():
    return users_list


@router.get("/user/{id}")
async def user (id: int):
    return search_user(id)


@router.get("/userquery/")
async def user (id: int):
    return search_user(id)


    
@router.post('/user/', status_code=201, response_model=User )
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")

    users_list.append(user)
    return user
        
@router.put('/user/')
async def user(user: User):
    
    found = False 
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            
    if not found:
        return {"error": "No se ha encontrado el usuario"}
    
    return user
    
    
@router.delete("/user/{id}")
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
    