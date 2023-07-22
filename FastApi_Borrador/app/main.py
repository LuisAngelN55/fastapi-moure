from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apis.api_router import api_router
from fastapi.staticfiles import StaticFiles
from core.config import settings
from db.database import engine, Base
# from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from db import save_mdata

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)




app.mount('/static', StaticFiles(directory='static'), name="static")


# save_mdata.save_language()
