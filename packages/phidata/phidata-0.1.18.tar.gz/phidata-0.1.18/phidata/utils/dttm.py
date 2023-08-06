import datetime
from typing import Optional


def dttm_str_to_dttm(
    dttm_str: str, dttm_format: str = "%Y-%m-%dT%H:%M:%S.%f"
) -> Optional[datetime.datetime]:
    """Convert a datestamp string to a Date object"""

    if dttm_str and dttm_str != "":
        try:
            datetime_object = datetime.datetime.strptime(dttm_str, dttm_format)
            return datetime_object
        except Exception as e:
            return None
    else:
        return None


def dttm_to_dttm_str(
    dttm: datetime.datetime, dttm_format: str = "%Y-%m-%dT%H:%M:%S"
) -> Optional[str]:
    """Convert a datetime object to formatted string"""

    if dttm and isinstance(dttm, datetime.datetime):
        try:
            dttm_str = datetime.datetime.strftime(dttm, dttm_format)
            return dttm_str
        except Exception as e:
            return None
    else:
        return None


def current_datetime_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def yesterday_datetime() -> datetime.datetime:
    return datetime.datetime.now() - datetime.timedelta(days=1)


def get_today_utc_date_str() -> str:
    today = datetime.datetime.now(datetime.timezone.utc).date()
    return today.strftime("%Y_%m_%d")


def current_datetime_utc_str() -> str:
    return dttm_to_dttm_str(current_datetime_utc())
