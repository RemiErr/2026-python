# U02. 正則表達式進階技巧（2.4–2.6）
# 繁體中文註解版：強調效能、回呼替換與保留原大小寫。
# 預編譯效能 / sub 回呼函數 / 大小寫一致替換

import re
import timeit
from calendar import month_abbr

# ── 預編譯效能（2.4）──────────────────────────────────
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")


def using_module():
    # 每次都直接呼叫模組函式，模式可能需要反覆處理。
    return re.findall(r"(\d+)/(\d+)/(\d+)", text)


def using_compiled():
    # 重複使用預編譯好的 regex 物件。
    return datepat.findall(text)


t1 = timeit.timeit(using_module, number=50_000)
t2 = timeit.timeit(using_compiled, number=50_000)
print(f"直接呼叫: {t1:.3f}s  預編譯: {t2:.3f}s")


# ── sub 回呼函數（2.5）────────────────────────────────
def change_date(m: re.Match) -> str:
    # 依照月份數字，到 calendar.month_abbr 找英文縮寫月份。
    mon_name = month_abbr[int(m.group(1))]
    return f"{m.group(2)} {mon_name} {m.group(3)}"


print(datepat.sub(change_date, text))
# 'Today is 27 Nov 2012. PyCon starts 13 Mar 2013.'


# ── 保持大小寫一致的替換（2.6）───────────────────────
def matchcase(word: str):
    # 外層函式回傳真正的 replace 函式，形成 closure。
    def replace(m: re.Match) -> str:
        t = m.group()

        # 依照原字串大小寫型態，決定替換字要轉成哪種形式。
        if t.isupper():
            return word.upper()
        if t.islower():
            return word.lower()
        if t[0].isupper():
            return word.capitalize()
        return word

    return replace


s = "UPPER PYTHON, lower python, Mixed Python"
print(re.sub("python", matchcase("snake"), s, flags=re.IGNORECASE))
# 'UPPER SNAKE, lower snake, Mixed Snake'
