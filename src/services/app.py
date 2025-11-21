from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from constants import NAME_APP_SYSTEM
from models import AppModel
from repositories.app import AppRepository
from shemes.app import AppDetail, AppList, CreateApp


class AppService:
    """Сервис для работы с приложениями."""

    def __init__(self, app_repo: AppRepository):
        self._app_repo = app_repo

    def get_list(self) -> list[AppList]:
        """Список приложений."""
        return [AppList.model_validate(item) for item in self._app_repo.get_list()]

    def get_detail(self, app_id: int) -> AppDetail:
        """Детали приложения."""
        app: Optional[AppModel] = self._app_repo.get_by_id(app_id)
        if app:
            return AppDetail.model_validate(app)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")

    def create(self, payload: CreateApp) -> AppDetail:
        """Добавить приложение."""
        try:
            new_item: AppModel = self._app_repo.create(payload)
        except IntegrityError as ex:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex).split("\n")[0])
        else:
            return AppDetail.model_validate(new_item)

    def delete(self, app_id: int) -> None:
        """Удалить приложение."""
        app: Optional[AppModel] = self._app_repo.get_by_id(app_id)
        if not app:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="App not found")
        else:
            if app.name == NAME_APP_SYSTEM:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This is a service application, it cannot be deleted",
                )
            return self._app_repo.delete(app_id)
