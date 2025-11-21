from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import database_settings

engine = create_engine(
    database_settings.DB_URL,
    connect_args={"check_same_thread": False},
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=30,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if database_settings.DB_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_sqlite_fk(dbapi_connection, connection_record):
        """Активация FK."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Для FastAPI зависимостей
def get_db() -> Session:
    """Получить сессию БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
