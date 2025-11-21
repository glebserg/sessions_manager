from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.user import get_user_service
from services.user import UserService
from shemes.user import UserDetail, UserList

router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


@router.get("", summary="Список пользователей")
async def get_list_users(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserList]:
    """Список пользователей."""
    return user_service.get_list()


@router.get("/{pk}", summary="Детали пользователя")
async def get_user_detail(pk: int, user_service: Annotated[UserService, Depends(get_user_service)]) -> UserDetail:
    """Детали пользователя."""
    return user_service.get_detail(pk)
