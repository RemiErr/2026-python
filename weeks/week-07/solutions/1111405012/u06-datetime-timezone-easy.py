from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


UTC = ZoneInfo("UTC")


def add_minutes_locally(local_dt: datetime, minutes: int) -> datetime:
    return local_dt + timedelta(minutes=minutes)


def add_minutes_via_utc(local_dt: datetime, minutes: int) -> datetime:
    # 記法：先轉 UTC，再算，再轉回來。
    if local_dt.tzinfo is None:
        raise ValueError("local_dt 必須是 aware datetime")

    utc_dt = local_dt.astimezone(UTC)
    return (utc_dt + timedelta(minutes=minutes)).astimezone(local_dt.tzinfo)


def parse_local_to_utc(text: str, tz_name: str) -> datetime:
    local_dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=ZoneInfo(tz_name))
    return local_dt.astimezone(UTC)


def convert_utc_to_timezone(utc_dt: datetime, tz_name: str) -> datetime:
    if utc_dt.tzinfo is None:
        raise ValueError("utc_dt 必須是 aware datetime")
    return utc_dt.astimezone(ZoneInfo(tz_name))
