import datetime
from typing import Annotated
from fastapi import APIRouter, Depends

from dependencies.limit import get_limit_service
from dependencies.limit_counters import get_limit_counter_service
from services.limit import LimitService
from services.limit_counter import LimitCounterService
from shemes.limit import LimitList, CreateLimit, LimitDetail
from shemes.limit_counter import LimitCounterList

router = APIRouter(prefix="/limits", tags=["Ограничения"])


@router.get("", summary="Список ограничений")
async def get_list_limits(
        limit_service: Annotated[LimitService, Depends(get_limit_service)]
) -> list[LimitList]:
    return limit_service.get_list()


@router.get("/{pk}", summary="Детали ограничения")
async def get_limit_detail(
        pk: int,
        limit_service: Annotated[LimitService, Depends(get_limit_service)]
) -> LimitDetail:
    return limit_service.get_detail(pk)


@router.get("/{pk}/counters", summary="Счётчики ограничения")
async def get_limit_counters(
        pk: int,
        limit_counter_service: Annotated[LimitCounterService, Depends(get_limit_counter_service)]
) -> list[LimitCounterList]:
    today = datetime.date.today()
    return limit_counter_service.get_list(limit_id=pk)


@router.post("", summary="Добавить ограничение")
async def create_limit(
        payload: CreateLimit,
        limit_service: Annotated[LimitService, Depends(get_limit_service)]
) -> LimitDetail:
    return limit_service.create(payload)
