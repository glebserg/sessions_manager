from datetime import datetime,date

from sqlalchemy import String, DateTime, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class BaseIDModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UserModel(BaseIDModel):
    __tablename__ = "users"
    __table_args__ = {"comment": "Пользователи"}

    username: Mapped[str] = mapped_column(String(), nullable=False, comment="Имя пользователя")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(), comment="Дата добавления")
    limits = relationship("LimitModel", back_populates="user")

class AppModel(BaseIDModel):
    __tablename__ = "apps"
    __table_args__ = {"comment": "Приложения"}

    name: Mapped[str] = mapped_column(String(), nullable=False, comment="Имя программы/процесса",unique=True)
    limits = relationship("LimitModel", back_populates="app",uselist=True)

class LimitModel(BaseIDModel):
    __tablename__ = "limits"
    __table_args__ = (
        UniqueConstraint('user_id', 'app_id', name='uniq_user_app'),
        {"comment": "Суточные ограничения доступа пользователя"}
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    app_id: Mapped[int] = mapped_column(ForeignKey("apps.id", ondelete="CASCADE"))
    minutes: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(default=True)

    user = relationship("UserModel", back_populates="limits")
    app = relationship("AppModel", back_populates="limits")

class LimitCounterModel(BaseIDModel):
    __tablename__ = "limit_counter"
    __table_args__ = {"comment": "Счётчик лимитов"}

    limit_id: Mapped[int] = mapped_column(ForeignKey("limits.id", ondelete="CASCADE"))
    count_minutes: Mapped[int] = mapped_column(Integer,default=1)
    date: Mapped[date] = mapped_column(Date, comment="Дата", nullable=False)

