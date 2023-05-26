from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users


app = FastAPI()

#ROUTERS
app.include_router(products.router)
app.include_router(users.router)
app.mount('/static', StaticFiles(directory='static'), name="static")

@app.get("/")
async def root():
    return "¡Hola FastApi!"

@app.get("/url")
async def url():
    return { "url_curso" : "https//mouredev.com/python" }