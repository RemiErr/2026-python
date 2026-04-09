from __future__ import annotations

from datetime import datetime, timedelta, timezone, tzinfo


UTC = timezone.utc
TAIPEI = timezone(timedelta(hours=8), name="Asia/Taipei")
_ZERO = timedelta(0)
_ONE_HOUR = timedelta(hours=1)
_CENTRAL_STANDARD_OFFSET = timedelta(hours=-6)


def _first_sunday_on_or_after(value: datetime) -> datetime:
    days_to_go = (6 - value.weekday()) % 7
    return value + timedelta(days=days_to_go)


def _us_central_dst_range(year: int) -> tuple[datetime, datetime]:
    start = _first_sunday_on_or_after(datetime(year, 3, 8, 2, 0, 0))
    end = _first_sunday_on_or_after(datetime(year, 11, 1, 2, 0, 0))
    return start, end


class USCentralTime(tzinfo):
    def utcoffset(self, dt: datetime | None) -> timedelta:
        return _CENTRAL_STANDARD_OFFSET + self.dst(dt)

    def dst(self, dt: datetime | None) -> timedelta:
        if dt is None:
            return _ZERO

        naive = dt.replace(tzinfo=None)
        start, end = _us_central_dst_range(naive.year)
        if start <= naive < end:
            return _ONE_HOUR
        return _ZERO

    def tzname(self, dt: datetime | None) -> str:
        if self.dst(dt):
            return "America/Chicago"
        return "America/Chicago"

    def fromutc(self, dt: datetime) -> datetime:
        if dt.tzinfo is not self:
            raise ValueError("fromutc() requires dt.tzinfo is self")

        standard_time = (dt + _CENTRAL_STANDARD_OFFSET).replace(tzinfo=self)
        daylight_time = (dt + _CENTRAL_STANDARD_OFFSET + _ONE_HOUR).replace(tzinfo=self)
        start, end = _us_central_dst_range(daylight_time.year)

        if start <= daylight_time.replace(tzinfo=None) < end:
            return daylight_time
        return standard_time


CENTRAL = USCentralTime()


def get_timezone(tz_name: str) -> tzinfo:
    mapping = {
        "UTC": UTC,
        "Asia/Taipei": TAIPEI,
        "America/Chicago": CENTRAL,
    }
    try:
        return mapping[tz_name]
    except KeyError as error:
        raise ValueError(f"不支援的時區：{tz_name}") from error
