from models import UserModel
from repositories import BaseRepository


class UserRepository(BaseRepository):
    """Репозиторий пользователей."""

    model = UserModel
