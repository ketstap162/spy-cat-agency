from datetime import datetime

from api.core.settings import TimeZone


def get_now():
    """return default now"""
    if TimeZone.IS_ACTIVE:
        return datetime.now(TimeZone.DATETIME_TZ)
    return datetime.now()
