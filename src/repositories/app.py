from typing import Optional

from models import AppModel
from repositories import BaseRepository


class AppRepository(BaseRepository):
    """Репозиторий приложений."""

    # TODO get_by(**kwargs)
    def get_by_name(self, name: str) -> Optional[AppModel]:
        return self._db.query(AppModel).filter(AppModel.name == name).first()
