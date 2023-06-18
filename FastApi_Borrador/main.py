from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.models import athletes_info, master_models
from db.database import engine, Base
# from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from db import save_mdata

Base.metadata.create_all(bind=engine)


app = FastAPI()

#ROUTERS
# app.include_router(products.router)
# app.include_router(users.router)
# app.include_router(users_db.router)
# app.include_router(basic_auth_users.router)
# app.include_router(jwt_auth_users.router)

app.mount('/static', StaticFiles(directory='static'), name="static")


# save_mdata.save_language()

@app.get("/")
async def root():
    return "¡Hola FastApi!"

@app.get("/url")
async def url():
    return { "url_curso" : "https//mouredev.com/python" }