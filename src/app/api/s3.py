from fastapi import APIRouter, Depends, Response, status, UploadFile
from fastapi.responses import StreamingResponse
from typing import Optional, List
import sys

from services.depends import get_s3_service
from services.s3 import S3Service
from config import configs

router = APIRouter(
    prefix="/s3",
    tags=['s3'])

@router.get("/")
async def get(
        key: str,
        s3_service: S3Service = Depends(get_s3_service)
):
    '''Получение файлов'''
    file =  await s3_service.get(key)
    return StreamingResponse(file["Body"], media_type="application/pdf")
