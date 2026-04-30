import csv
import functools
import io
import json
import time
import xml.etree.ElementTree as ET


def read_csv_raw(data: str):
    """把 CSV 文字交給 DictReader，讀成一串字典。"""
    return list(csv.DictReader(io.StringIO(data)))


def read_json_raw(data: str):
    """JSON 本來就很接近 Python 的 list/dict，所以直接 loads 即可。"""
    return json.loads(data)


def read_xml_raw(data: str):
    """XML 要先 parse，再把每個 row 的屬性拿出來。"""
    root = ET.fromstring(data)
    return [row.attrib for row in root.findall("row")]


def timeit(func):
    """
    這就是裝飾器：
    - 呼叫原本函式前先記錄開始時間
    - 執行完再計算花了多久
    - 最後把原函式的結果照常回傳

    functools.wraps 可以保留原本函式名稱與說明文字。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result

    return wrapper


def main():
    # 先準備 1000 筆測試資料，三種格式都用同一批內容，這樣比較才公平。
    rows = [{"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40} for i in range(1000)]

    # CSV：先寫進記憶體檔案，再取出完整字串。
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["id", "name", "score"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    csv_data = csv_buffer.getvalue()

    # JSON：最直接，整串 list of dict 一次轉成字串。
    json_data = json.dumps(rows, ensure_ascii=False)

    # XML：用字串拼出 <data> 底下很多個 <row .../>。
    xml_data = "<data>" + "".join(
        f'<row id="{row["id"]}" name="{row["name"]}" score="{row["score"]}"/>'
        for row in rows
    ) + "</data>"

    # 套上裝飾器後，呼叫時就會自動印出耗時。
    timed_csv = timeit(read_csv_raw)
    timed_json = timeit(read_json_raw)
    timed_xml = timeit(read_xml_raw)

    timed_csv(csv_data)
    timed_json(json_data)
    timed_xml(xml_data)


if __name__ == "__main__":
    main()
