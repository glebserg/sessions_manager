from typing import Optional

from fastapi import HTTPException,status

from models import UserModel
from repositories.user import UserRepository
from shemes.app import CreateApp
from shemes.user import UserList, UserDetail


class UserService:

    def __init__(self,user_repo: UserRepository):
        self._user_repo = user_repo

    def get_list(self) -> list[UserList]:
        return [UserList.model_validate(item) for item in self._user_repo.get_list()]

    def get_detail(self,user_id: int) -> UserDetail:
        user: Optional[UserModel] = self._user_repo.get_by_id(user_id)
        if user:
            return UserDetail.model_validate(user)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
