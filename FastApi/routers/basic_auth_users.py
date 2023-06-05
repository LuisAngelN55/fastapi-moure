from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

router = APIRouter (prefix="/basicauth",
                    tags=["basicauth"],
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Entidad Usuario
class User(BaseModel):
    username :  str
    full_name:  str
    email:      str
    disabled:   bool
    
class UserDB(User):
    password : str
    
users_db = {
    "luisangeln": {
        "username"  :  "luisangeln",
        "full_name" :  "Luis Angel",
        "email"     :  "luis@gmail.com",
        "disabled"  :  False,
        "password"  :  "123456"
    },
    "angel": {
        "username"  :  "angel",
        "full_name" :  "Angel Naranjo",
        "email"     :  "angel @gmail.com",
        "disabled"  :  True,
        "password"  :  "654321"
    }
}


def search_userdb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Creadenciales de autenticación inválidas",
            headers={"WWW-authenticate": "Bearer"}
        )
        
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario Inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no existe")
    
    user = search_userdb(form.username)
    
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
        
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }
    

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
 