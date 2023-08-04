from fastapi import APIRouter, status, UploadFile, File, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from core.config import settings
from sqlalchemy.orm import Session
from apis import deps
from apis.athletes.crud import athletes
import pathlib

router = APIRouter(
    # prefix="/athlete",
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
    )




