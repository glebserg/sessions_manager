from datetime import date
from typing import Optional


def get_count_today(limit_id: int, day: date) -> Optional[int]:
    from dependencies.limit_counters import get_limit_counter_service
    service = get_limit_counter_service()
    result = service.get_or_none(limit_id, day)
    return result.count_minutes if result else None
