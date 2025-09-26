from typing import Type, Optional

from repositories import BaseRepository
from shemes.user import CreateUser
from models import UserModel


class UserRepository(BaseRepository):

    def get_list(self) -> list[Type[UserModel]]:
        return list(self._db.query(UserModel).all())

    def get_by_id(self, pk: int) -> Optional[UserModel]:
        return self._db.query(UserModel).get(pk)

    def get_by_username(self, username: str) -> Optional[UserModel]:
        return self._db.query(UserModel).filter(UserModel.username == username).first()

    def create(self, payload: CreateUser) -> UserModel:
        new_item = UserModel(**payload.model_dump())
        self._db.add(new_item)
        self._db.commit()
        return new_item

    def delete(self, user_id: int) -> None:
        self._db.query(UserModel).filter_by(id=user_id).delete()
        self._db.commit()
