from fastapi import APIRouter, Depends, Response, status, HTTPException
from typing import Optional
from fastapi_cache.decorator import cache
from services.users import get_current_user
from services.depends import get_statistics_service
from services.statistics import StatisticsService

router = APIRouter(
    prefix="/stat",
    tags=['stat'])


@router.get("/count/")
@cache(expire=60)
async def count(
        month: Optional[int] = None,
        year: Optional[int] = None,
        User = Depends(get_current_user),
        service: StatisticsService = Depends(get_statistics_service),
):
    """Число просмотренных протоколов"""
    return await service.count(month=month, year=year)

@router.get("/")
@cache(expire=60)
async def get_stat(
        month: Optional[int] = None,
        year: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        User = Depends(get_current_user),
        service: StatisticsService = Depends(get_statistics_service),
):
    """Просмотр статистики за месяц"""
    return await service.get_by_date(month=month, year=year, limit=limit, offset=offset)



