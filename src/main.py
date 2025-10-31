from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from config import app_setting, templates
from constants import UPDATE_COUNTER_RATE, USER_INSPECT_RATE
from database import Base, engine
from dependencies.user import get_user_service
from services.background import counter_updater, access_killer
from dependencies.init_app import create_local_users_to_db, create_base_app
from routers.api import users as api_users
from routers.api import apps as api_apps
from routers.api import limits as api_limits
from routers import users,apps

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.user import UserService
from shemes.user import UserDetail, UserList


@asynccontextmanager
async def lifespan(_: FastAPI):
    """on_startup."""

    Base.metadata.create_all(bind=engine)
    await create_local_users_to_db()
    create_base_app()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(counter_updater, "interval", seconds=UPDATE_COUNTER_RATE, next_run_time=datetime.now())
    scheduler.add_job(access_killer, "interval", seconds=USER_INSPECT_RATE, next_run_time=datetime.now())
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(api_apps.router)
app.include_router(api_limits.router)
app.include_router(api_users.router)
app.include_router(users.router)
app.include_router(apps.router)

@app.get("/")
async def users_list(request: Request, user_service: Annotated[UserService, Depends(get_user_service)]) -> HTMLResponse:
    users_detail: list[UserList] = user_service.get_list()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users_detail})

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=app_setting.PORT,
        reload=app_setting.DEV,
        access_log=app_setting.DEV,
    )
