from models import AppModel
from repositories import BaseRepository


class AppRepository(BaseRepository):
    """Репозиторий приложений."""

    model = AppModel
