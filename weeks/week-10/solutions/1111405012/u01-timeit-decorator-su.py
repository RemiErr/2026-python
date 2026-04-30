import csv
import functools
import io
import json
import time
import xml.etree.ElementTree as ET


def read_csv_raw(data: str):
    return list(csv.DictReader(io.StringIO(data)))


def read_json_raw(data: str):
    return json.loads(data)


def read_xml_raw(data: str):
    root = ET.fromstring(data)
    return [row.attrib for row in root.findall("row")]


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  {func.__name__:<20s} {time.perf_counter() - start:.6f}s")
        return result

    return wrapper


def main():
    rows = [{"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40} for i in range(1000)]

    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["id", "name", "score"])
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

    csv_data = csv_buffer.getvalue()
    json_data = json.dumps(rows, ensure_ascii=False)
    xml_data = "<data>" + "".join(
        f'<row id="{row["id"]}" name="{row["name"]}" score="{row["score"]}"/>'
        for row in rows
    ) + "</data>"

    timed_csv = timeit(read_csv_raw)
    timed_json = timeit(read_json_raw)
    timed_xml = timeit(read_xml_raw)

    timed_csv(csv_data)
    timed_json(json_data)
    timed_xml(xml_data)


if __name__ == "__main__":
    main()
