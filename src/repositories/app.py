from typing import Type, Optional

from sqlalchemy import desc

from repositories import BaseRepository
from shemes.app import CreateApp
from models import AppModel


class AppRepository(BaseRepository):

    def get_list(self) -> list[Type[AppModel]]:
        return list(self._db.query(AppModel).order_by(desc(AppModel.created_at)).all())

    def get_by_id(self, pk: int) -> Optional[AppModel]:
        return self._db.query(AppModel).get(pk)

    def get_by_name(self, name: str) -> Optional[AppModel]:
        return self._db.query(AppModel).filter(AppModel.name == name).first()

    def create(self, payload: CreateApp) -> AppModel:
        new_item = AppModel(**payload.model_dump())
        self._db.add(new_item)
        self._db.commit()
        return new_item

    def delete(self, app_id: int) -> None:
        self._db.query(AppModel).filter_by(id=app_id).delete()
        self._db.commit()
