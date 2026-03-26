# R08. 日期範圍與字串轉換（3.14–3.15）
# 繁體中文註解版：說明日期範圍、生成器與日期字串轉換。
# calendar.monthrange / strptime / strftime

from datetime import datetime, date, timedelta
from calendar import monthrange


# ── 3.14 當月日期範圍 ─────────────────────────────────
def get_month_range(start: date | None = None) -> tuple[date, date]:
    # 預設以本月 1 號為起點。
    if start is None:
        start = date.today().replace(day=1)

    # monthrange() 回傳 (星期幾, 當月天數)。
    _, days = monthrange(start.year, start.month)

    # 這裡回傳的是半開區間：[start, end)
    # 也就是 start 含在內，end 不含在內。
    return start, start + timedelta(days=days)


first, last = get_month_range(date(2012, 8, 1))
print(first, "~", last - timedelta(days=1))  # 2012-08-01 ~ 2012-08-31


# 通用日期迭代生成器
def date_range(start: datetime, stop: datetime, step: timedelta):
    # 這是典型 generator 寫法，逐次產生時間點，不一次建整包清單。
    while start < stop:
        yield start
        start += step


for d in date_range(datetime(2012, 9, 1), datetime(2012, 9, 2), timedelta(hours=6)):
    print(d)
# 2012-09-01 00:00:00 / 06:00 / 12:00 / 18:00

# ── 3.15 字串轉換為日期 ───────────────────────────────
text = "2012-09-20"

# strptime() 依照格式字串把文字解析成 datetime。
dt = datetime.strptime(text, "%Y-%m-%d")
print(dt)  # 2012-09-20 00:00:00

# strftime() 則是反向，把 datetime 格式化成字串。
print(datetime.strftime(dt, "%A %B %d, %Y"))  # 'Thursday September 20, 2012'


# 手動解析（比 strptime 快 7 倍）
def parse_ymd(s: str) -> datetime:
    # 已知格式固定時，手動 split 往往更快。
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


print(parse_ymd("2012-09-20"))  # 2012-09-20 00:00:00
