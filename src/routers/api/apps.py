from typing import Annotated

from fastapi import APIRouter, Depends, status

from dependencies.app import get_app_service
from services.app import AppService
from shemes.app import AppDetail, AppList, CreateApp

router = APIRouter(prefix="/api/v1/apps", tags=["Приложения"])


@router.get("", summary="Список приложений")
async def get_list_apps(
    app_service: Annotated[AppService, Depends(get_app_service)],
) -> list[AppList]:
    """Список приложений."""
    return app_service.get_list()


@router.get("/{pk}", summary="Детали приложения")
async def get_app_detail(pk: int, app_service: Annotated[AppService, Depends(get_app_service)]) -> AppDetail:
    """Детали приложения."""
    return app_service.get_detail(pk)


@router.post("", summary="Добавить приложения")
async def create_app(
    payload: CreateApp,
    app_service: Annotated[AppService, Depends(get_app_service)],
) -> AppDetail:
    """Добавить приложение."""
    return app_service.create(payload)


@router.delete(
    "/{pk}",
    summary="Удалить приложение",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_app(
    pk: int,
    app_service: Annotated[AppService, Depends(get_app_service)],
) -> None:
    """Удалить приложение."""
    return app_service.delete(pk)
