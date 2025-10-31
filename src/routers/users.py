from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from config import templates
from dependencies.user import get_user_service
from services.user import UserService
from shemes.user import UserDetail

router = APIRouter(prefix="/users")


@router.get("")
async def users_list(request: Request, user_service: Annotated[UserService, Depends(get_user_service)]) -> HTMLResponse:
    users_detail: list[UserDetail] = user_service.get_list()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users_detail})


@router.get("/{pk}")
async def get_user_detail(
        pk: int,
        request: Request, user_service: Annotated[UserService,
        Depends(get_user_service)]
) -> HTMLResponse:
    user_detail: UserDetail = user_service.get_detail(pk)
    return templates.TemplateResponse("user_detail.html", {"request": request, "user": user_detail})
