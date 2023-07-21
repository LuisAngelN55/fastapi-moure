from fastapi import APIRouter, status

from apis.athletes import athletes_endpoint

api_router = APIRouter(prefix="/athlete",
                    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


api_router.include_router(athletes_endpoint.router)