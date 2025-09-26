from typing import Type, Optional

from repositories import BaseRepository
from models import LimitModel
from shemes.limit import CreateLimit


class LimitRepository(BaseRepository):

    def get_list(self) -> list[Type[LimitModel]]:
        return list(self._db.query(LimitModel).all())

    def get_by_id(self, pk: int) -> Optional[LimitModel]:
        return self._db.query(LimitModel).get(pk)

    def create(self, payload: CreateLimit) -> LimitModel:
        new_item = LimitModel(**payload.model_dump())
        self._db.add(new_item)
        self._db.commit()
        return new_item