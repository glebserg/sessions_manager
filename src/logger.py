import logging

import uvicorn

from config import app_setting


def set_log_level(log_config: dict, log_level: str) -> None:
    """Назначение уровня логирования."""
    keys = ("uvicorn", "uvicorn.error", "uvicorn.access")
    for key in keys:
        log_config["loggers"][key]["level"] = log_level.upper()


logging.getLogger("apscheduler.scheduler").setLevel(logging.CRITICAL)
logging_config = uvicorn.config.LOGGING_CONFIG
set_log_level(logging_config, app_setting.LOG_LEVEL)
uvicorn_logger = logging.getLogger("uvicorn")
