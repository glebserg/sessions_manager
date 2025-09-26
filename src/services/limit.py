from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models import LimitModel
from repositories.limit import LimitRepository
from shemes.limit import LimitList, LimitDetail, CreateLimit


class LimitService:

    def __init__(self, limit_repo: LimitRepository):
        self._limit_repo = limit_repo

    def get_list(self) -> list[LimitList]:
        return [LimitList.model_validate(item) for item in self._limit_repo.get_list()]

    def get_detail(self, limit_id: int) -> LimitDetail:
        limit: Optional[LimitModel] = self._limit_repo.get_by_id(limit_id)
        if limit:
            return LimitDetail.model_validate(limit)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Limit not found")

    def create(self, payload: CreateLimit) -> LimitDetail:
        try:
            new_limit: LimitModel = self._limit_repo.create(payload)
        except IntegrityError as ex:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex).split("\n")[0])
        return LimitDetail.model_validate(new_limit)
