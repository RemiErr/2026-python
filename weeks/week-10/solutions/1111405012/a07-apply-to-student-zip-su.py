import csv
import io
import pickle
import tempfile
import zipfile
from collections import Counter
from pathlib import Path


ZIP_PATH = Path(__file__).resolve().parents[4] / "assets" / "npu-stu-109-114-anon.zip"


def read_zip_summary(zip_path: Path):
    """直接讀 zip，順手把各年度統計做完。"""
    summary = {}
    all_depts = Counter()

    with zipfile.ZipFile(zip_path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if not info.filename.endswith(".csv"):
                continue

            year = info.filename[:3]
            text = archive.read(info).decode("utf-8-sig")
            rows = list(csv.reader(io.StringIO(text)))
            header = rows[0]
            data = rows[1:]
            dept_index = header.index("系所名稱")
            entry_index = header.index("入學方式")
            by_dept = Counter(row[dept_index] for row in data if len(row) > dept_index and row[dept_index])
            by_entry = Counter(row[entry_index] for row in data if len(row) > entry_index and row[entry_index])

            summary[year] = {"total": len(data), "by_dept": by_dept, "by_entry": by_entry}
            all_depts.update(by_dept)

    return summary, all_depts


def make_report(summary: dict) -> str:
    lines = ["# 6 屆新生概況報告", "", "| 學年 | 人數 | 第一大系所 |", "|------|------|------------|"]
    for year in sorted(summary):
        top_dept, top_count = summary[year]["by_dept"].most_common(1)[0]
        lines.append(f"| {year} | {summary[year]['total']} | {top_dept} ({top_count}) |")
    return "\n".join(lines) + "\n"


def main():
    if not ZIP_PATH.exists():
        print(f"找不到資料：{ZIP_PATH}")
        return

    summary, all_depts = read_zip_summary(ZIP_PATH)
    print("=== 6 屆新生人數 ===")
    for year in sorted(summary):
        print(f"{year} 學年：{summary[year]['total']} 人")

    print("\n=== 全體最熱門 5 個系所 ===")
    for dept, count in all_depts.most_common(5):
        print(f"{count} 人 {dept}")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        snap_path = temp_root / "summary.pkl"
        report_path = temp_root / "report.md"

        with open(snap_path, "wb") as file:
            pickle.dump(summary, file)

        report_path.write_text(make_report(summary), encoding="utf-8")
        print("\n=== Markdown 報告預覽 ===")
        print(report_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
