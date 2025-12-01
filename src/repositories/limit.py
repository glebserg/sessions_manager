from models import LimitModel
from repositories import BaseRepository
from shemes.limit import UpdateLimit


class LimitRepository(BaseRepository):
    """Репозиторий лимитов."""

    model = LimitModel

    def update(self, pk: int, payload: UpdateLimit) -> LimitModel | None:
        """Обновить."""
        item = self.get_by_id(pk)
        if item:
            for field, value in payload.model_dump(exclude_unset=True).items():
                setattr(item, field, value)
            self._db.commit()
        return item
