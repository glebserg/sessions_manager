from typing import Optional

from models import UserModel
from repositories import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий пользователей."""

    model = UserModel

    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Пользователь по username."""
        return self._db.query(UserModel).filter(UserModel.username == username).first()
