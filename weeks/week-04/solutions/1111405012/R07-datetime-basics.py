# R07. 日期時間基本運算（3.12–3.13）
# 繁體中文註解版：補充 timedelta 與 weekday 計算的思路。
# timedelta 加減 / weekday() 計算指定星期

from datetime import datetime, timedelta

# ── 3.12 timedelta 基本運算 ───────────────────────────
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)
c = a + b

# timedelta.days 只看整天數；小時與分鐘會留在秒數部分。
print(c.days)  # 2

# total_seconds() 才能得到完整總秒數，再自行換算成小時。
print(c.total_seconds() / 3600)  # 58.5

dt = datetime(2012, 9, 23)
print(dt + timedelta(days=10))  # 2012-10-03 00:00:00

d1, d2 = datetime(2012, 9, 23), datetime(2012, 12, 21)
print((d2 - d1).days)  # 89

# datetime 會自動處理閏年差異。
print((datetime(2012, 3, 1) - datetime(2012, 2, 28)).days)  # 2（閏年）
print((datetime(2013, 3, 1) - datetime(2013, 2, 28)).days)  # 1（平年）

# ── 3.13 計算指定星期日期 ─────────────────────────────
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_previous_byday(dayname: str, start: datetime | None = None) -> datetime:
    # 若未指定起點，就以今天為基準。
    if start is None:
        start = datetime.today()

    # weekday()：Monday=0 ... Sunday=6
    day_num = start.weekday()
    target = WEEKDAYS.index(dayname)

    # 算出距離上一個目標星期幾有幾天。
    # 若剛好是同一天，就往前推 7 天，取得「上一個」而不是「今天」。
    days_ago = (7 + day_num - target) % 7 or 7
    return start - timedelta(days=days_ago)


base = datetime(2012, 8, 28)  # 週二
print(get_previous_byday("Monday", base))  # 2012-08-27
print(get_previous_byday("Friday", base))  # 2012-08-24
