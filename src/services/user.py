from fastapi import HTTPException, status

from models import UserModel
from repositories.user import UserRepository
from shemes.user import UserDetail, UserList


class UserService:
    """Сервис для работы с пользователями."""

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def get_list(self) -> list[UserList]:
        """Возвращает список пользователей."""
        return [UserList.model_validate(item) for item in self._user_repo.get_list()]

    def get_detail(self, user_id: int) -> UserDetail:
        """Возвращает детали пользователя."""
        user: UserModel | None = self._user_repo.get_by_id(user_id)
        if user:
            return UserDetail.model_validate(user)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
