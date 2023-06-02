from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# JWT Configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "50bea0a82b0716688791817bca1e84fd980fcd7eb742878f5e2b7133bf173f87"

crypt = CryptContext(schemes=["bcrypt"])



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
        "password"  :  "$2a$12$VOT1OJCVY1hRqhH7VIrVzeWdUZJdnfrSM186qlutXqjCqRimltebe"
    },
    "angel": {
        "username"  :  "angel",
        "full_name" :  "Angel Naranjo",
        "email"     :  "angel @gmail.com",
        "disabled"  :  True,
        "password"  :  "$2a$12$do2jmOz03NWTlyGMm.3Z/e9IfI71eZA3azU7hRO.VScqXZxq29bXC"
    }
}


def search_userdb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Creadenciales de autenticación inválidas",
            headers={"WWW-authenticate": "Bearer"}
        )
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
         
    except JWTError:
        raise exception
    
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    
        
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
    
    
    
    if not crypt.verify(form.password, user.password) :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
        
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    access_token = {
        "sub": user.username,
        "exp": expire
    }
    
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    } 
    
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
