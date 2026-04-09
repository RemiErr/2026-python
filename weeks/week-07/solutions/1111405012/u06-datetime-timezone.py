from __future__ import annotations

from datetime import datetime, timedelta

from simple_timezones import UTC, get_timezone


def add_minutes_locally(local_dt: datetime, minutes: int) -> datetime:
    # 直接在本地時間上加減，可能會落到夏令時不存在的時間。
    return local_dt + timedelta(minutes=minutes)


def add_minutes_via_utc(local_dt: datetime, minutes: int) -> datetime:
    # 正確流程：先轉 UTC、計算、再轉回原時區。
    if local_dt.tzinfo is None:
        raise ValueError("local_dt 必須是 aware datetime")

    utc_dt = local_dt.astimezone(UTC)
    moved = utc_dt + timedelta(minutes=minutes)
    return moved.astimezone(local_dt.tzinfo)


def parse_local_to_utc(text: str, tz_name: str) -> datetime:
    # 使用者輸入通常沒有時區，所以要先補上本地時區，再轉成 UTC 儲存。
    naive = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    local_dt = naive.replace(tzinfo=get_timezone(tz_name))
    return local_dt.astimezone(UTC)


def convert_utc_to_timezone(utc_dt: datetime, tz_name: str) -> datetime:
    # 顯示給不同地區使用者時，再從 UTC 轉成目標時區。
    if utc_dt.tzinfo is None:
        raise ValueError("utc_dt 必須是 aware datetime")
    return utc_dt.astimezone(get_timezone(tz_name))
