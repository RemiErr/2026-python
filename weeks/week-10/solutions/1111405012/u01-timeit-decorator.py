import csv
import functools
import io
import json
import time
import xml.etree.ElementTree as ET


def read_csv_raw(data: str) -> list[dict]:
    """把 CSV 字串讀成 dict 清單。"""
    return list(csv.DictReader(io.StringIO(data)))


def read_json_raw(data: str) -> list[dict]:
    """把 JSON 字串讀成 Python list。"""
    return json.loads(data)


def read_xml_raw(data: str) -> list[dict]:
    """把 XML 字串讀成每列屬性的 dict 清單。"""
    root = ET.fromstring(data)
    return [row.attrib for row in root.findall("row")]


def timeit(func):
    """印出函式名稱與耗時，並保留原本 metadata。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result

    return wrapper


def timeit_silent(func):
    """不印出資訊，只回傳 (結果, 耗時)。"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    return wrapper


def make_sample_data(rows: list[dict]) -> tuple[str, str, str]:
    """用同一批資料同時產生 CSV / JSON / XML 三種格式。"""
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["id", "name", "score"])
    writer.writeheader()

    normalized_rows = []
    xml_rows = []

    for row in rows:
        item = {
            "id": row["id"],
            "name": row["name"],
            "score": row["score"],
        }
        normalized_rows.append(item)
        writer.writerow(item)
        xml_rows.append(
            f'<row id="{item["id"]}" name="{item["name"]}" score="{item["score"]}"/>'
        )

    csv_data = csv_buffer.getvalue()
    json_data = json.dumps(normalized_rows, ensure_ascii=False)
    xml_data = f"<data>{''.join(xml_rows)}</data>"
    return csv_data, json_data, xml_data


def make_student_rows(count: int = 1000) -> list[dict]:
    """建立和課堂範例相同結構的測試資料。"""
    return [
        {"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40}
        for i in range(count)
    ]


def benchmark_formats(csv_data: str, json_data: str, xml_data: str, runs: int = 5) -> dict[str, float]:
    """重複多次量測三種格式的平均讀取耗時。"""
    timed_csv = timeit_silent(read_csv_raw)
    timed_json = timeit_silent(read_json_raw)
    timed_xml = timeit_silent(read_xml_raw)
    total_times = {"CSV": 0.0, "JSON": 0.0, "XML": 0.0}

    for _ in range(runs):
        _, elapsed = timed_csv(csv_data)
        total_times["CSV"] += elapsed

        _, elapsed = timed_json(json_data)
        total_times["JSON"] += elapsed

        _, elapsed = timed_xml(xml_data)
        total_times["XML"] += elapsed

    return {fmt: total / runs for fmt, total in total_times.items()}


def format_report(avg_times: dict[str, float], record_count: int, runs: int) -> str:
    """把平均耗時整理成和課堂範例相近的表格文字。"""
    lines = [
        f"=== 讀取 {record_count} 筆資料，重複 {runs} 次平均 ===",
        "",
        f"{'格式':<6} {'平均耗時':>12}  {'相對 JSON':>10}",
    ]
    base = avg_times["JSON"] if avg_times["JSON"] > 0 else 1e-12

    for fmt in ["CSV", "JSON", "XML"]:
        avg = avg_times[fmt]
        lines.append(f"  {fmt:<6} {avg:.6f}s   {avg / base:>8.2f}x")

    return "\n".join(lines)


def demonstrate_wraps() -> str:
    """示範 wraps 是否能保留原本函式名稱。"""
    def demo():
        """這是 demo 的說明文字"""
        return "done"

    wrapped = timeit(demo)
    return wrapped.__name__


def main():
    print("加 wraps 後：  ", demonstrate_wraps())
    print()

    rows = make_student_rows(1000)
    csv_data, json_data, xml_data = make_sample_data(rows)
    avg_times = benchmark_formats(csv_data, json_data, xml_data, runs=5)
    print(format_report(avg_times, record_count=len(rows), runs=5))


if __name__ == "__main__":
    main()
