from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from config import templates
from dependencies.app import get_app_service
from services.app import AppService
from shemes.app import AppDetail, AppList

router = APIRouter(prefix="/apps")


@router.get("")
async def apps_list(request: Request, app_service: Annotated[AppService, Depends(get_app_service)]) -> HTMLResponse:
    """Список приложений."""
    apps: list[AppList] = app_service.get_list()
    return templates.TemplateResponse("app_list.html", {"request": request, "apps": apps})


@router.get("/{pk}")
async def app_detail(
    pk: int,
    request: Request,
    app_service: Annotated[AppService, Depends(get_app_service)],
) -> HTMLResponse:
    """Детали приложения."""
    app: AppDetail = app_service.get_detail(pk)
    return templates.TemplateResponse("app_detail.html", {"request": request, "app": app})
