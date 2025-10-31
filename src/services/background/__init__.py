from dependencies.limit import get_limit_service
from dependencies.limit_counters import get_limit_counter_service
from services.background.counter_updater import CounterUpdater
from services.background.access_killer import AccessKiller
from services.processes_collector import ProcessesCollector
from services.sessions_collector import SessionsCollector


async def access_killer():
    task = AccessKiller(
        proc_collector=ProcessesCollector(),
        session_collector=SessionsCollector(),
        limit_service=get_limit_service(),
        limit_counter_service=get_limit_counter_service()
    )
    await task()

async def counter_updater():
    task = CounterUpdater(
        proc_collector=ProcessesCollector(),
        session_collector=SessionsCollector(),
        limit_service=get_limit_service(),
        limit_counter_service=get_limit_counter_service()
    )
    await task()