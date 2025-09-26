from database import get_db
from repositories.app import AppRepository
from repositories.limit import LimitRepository
from repositories.limit_counter import LimitCounterRepository
from repositories.user import UserRepository


def get_user_repo() -> UserRepository:
    return UserRepository(db=next(get_db()))

def get_app_repo() -> AppRepository:
    return AppRepository(db=next(get_db()))

def get_limit_repo() -> LimitRepository:
    return LimitRepository(db=next(get_db()))

def get_limit_counter_repo() -> LimitCounterRepository:
    return LimitCounterRepository(db=next(get_db()))