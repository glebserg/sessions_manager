from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI

from config import app_setting
from constants import UPDATE_COUNTER_RATE, USER_INSPECT_RATE
from dependencies.limit import get_limit_service
from dependencies.limit_counters import get_limit_counter_service
from models import LimitCounterModel
from services.background.counter_updater import CounterUpdater
from dependencies.init_app import init_app
from routers import users, apps, limits
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from services.limit import LimitService
from services.limit_counter import LimitCounterService
from services.background.process_killer import ProcessKiller
from services.processes_collector import ProcessesCollector
from shemes.proc import ActiveProcess
from utils.cmd import run_cmd


async def update_counters() -> None:
    limit_counter_service: LimitCounterService = get_limit_counter_service()
    limit_service: LimitService = get_limit_service()
    proc_collector = ProcessesCollector()
    for limit in limit_service.get_list():
        if limit.active:
            coincidence: Optional[ActiveProcess] = proc_collector.get(limit.user.username, limit.app.name)
            if coincidence:
                today = datetime.today()
                limit_counter_service.counter_up(limit.id, today)
                counter: LimitCounterModel = limit_counter_service.get_or_none(limit.id, today)
                if counter.count_minutes >= limit.minutes:
                    await run_cmd(f"kill {coincidence.pid}")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """on_startup."""
    await init_app()

    process_collector = ProcessesCollector()
    limit_service = get_limit_service()
    limit_counter_service = get_limit_counter_service()

    counter_updater = CounterUpdater(
        proc_collector=process_collector,
        limit_service=limit_service,
        limit_counter_service=limit_counter_service
    )

    process_killer = ProcessKiller(
        proc_collector=process_collector,
        limit_service=limit_service,
        limit_counter_service=limit_counter_service
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(counter_updater, "interval", seconds=UPDATE_COUNTER_RATE, next_run_time=datetime.now())
    scheduler.add_job(process_killer, "interval", seconds=USER_INSPECT_RATE, next_run_time=datetime.now())
    scheduler.start()
    yield
    scheduler.shutdown()



app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(apps.router)
app.include_router(limits.router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=app_setting.PORT,
        reload=app_setting.DEV,
        access_log=app_setting.DEV,
    )
