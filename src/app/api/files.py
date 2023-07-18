from fastapi import APIRouter, Depends, Response, status, UploadFile
from typing import Optional, List
import sys

from models.files import File
from models.users import User, LicenseLevel
from services.users import get_current_user
from services.depends import get_report_service
from services.reports import ReportsService
from config import configs
from modules.exceptions import exception_right, exception_file_count, exception_file_size

router = APIRouter(
    prefix="/files",
    tags=['files'])

@router.post("/")
async def upload_file(
        report_id: str,
        filename: str,
        file: UploadFile,
        user: User = Depends(get_current_user),
        service: ReportsService = Depends(get_report_service)
):
    """Добавление файла"""
    if user.license_level != LicenseLevel.ENTERPRISE:
        raise exception_right

    report = await service.get(report_id)
    if report.user_id != user.id and not user.is_superuser:
        raise exception_right

    files_count = await service.get_files_count_by_report(report_id=report_id)

    if files_count > configs.file_count:
        raise exception_file_count

    contents = await file.read()
    if sys.getsizeof(contents) / (1024 * 1024) > configs.file_size:
        raise exception_file_size

    format = file.filename.split(".")[-1].lower()

    return await service.create_file(report_id, f"{filename}.{format}", contents)

@router.get("/", response_model=Optional[List[File]])
async def get_files(
        report_id: str,
        user: User = Depends(get_current_user),
        service: ReportsService = Depends(get_report_service)
):
    """Просмотр отчетов по объекту"""
    return await service.get_files(report_id=report_id)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_files(
        report_id: str,
        user: User = Depends(get_current_user),
        service: ReportsService = Depends(get_report_service)
):
    """Удаление всех файлов"""
    report = await service.get(report_id)
    if report.user_id != user.id and not user.is_superuser:
        raise exception_right

    await service.delete_files(report_id=report_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)