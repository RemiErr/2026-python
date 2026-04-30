import csv
import io
import pickle
import tempfile
import zipfile
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[4]
DEFAULT_ZIP_PATH = ROOT_DIR / "assets" / "npu-stu-109-114-anon.zip"


def iter_year_csv(zip_path: Path):
    """不解壓 zip，逐年讀出 CSV 的表頭與資料列。"""
    with zipfile.ZipFile(zip_path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if not info.filename.endswith(".csv"):
                continue

            year = info.filename[:3]
            text = archive.read(info).decode("utf-8-sig")
            rows = list(csv.reader(io.StringIO(text)))
            if not rows:
                continue

            yield year, rows[0], rows[1:]


def build_summary(zip_path: Path):
    """
    建立跨年度統計：
    - summary：每年的人數、系所統計、入學方式統計
    - all_depts：所有年度合併後的系所總數
    """
    summary = {}
    all_depts = Counter()

    for year, header, rows in iter_year_csv(zip_path):
        dept_index = header.index("系所名稱")
        entry_index = header.index("入學方式")

        by_dept = Counter()
        by_entry = Counter()

        for row in rows:
            if len(row) > dept_index and row[dept_index]:
                by_dept[row[dept_index]] += 1
            if len(row) > entry_index and row[entry_index]:
                by_entry[row[entry_index]] += 1

        summary[year] = {
            "total": len(rows),
            "by_dept": by_dept,
            "by_entry": by_entry,
        }
        all_depts.update(by_dept)

    return summary, all_depts


def build_markdown_report(summary: dict) -> str:
    """把每年的總人數與最大系所整理成 Markdown 表格。"""
    lines = [
        "# 6 屆新生概況報告",
        "",
        "| 學年 | 人數 | 第一大系所 |",
        "|------|------|------------|",
    ]

    for year in sorted(summary):
        by_dept = summary[year]["by_dept"]
        if by_dept:
            top_dept, top_count = by_dept.most_common(1)[0]
        else:
            top_dept, top_count = "無資料", 0
        lines.append(f"| {year} | {summary[year]['total']} | {top_dept} ({top_count}) |")

    return "\n".join(lines) + "\n"


def format_console_summary(summary: dict, all_depts: Counter, target_year: str = "114") -> str:
    """整理成適合直接印到終端的摘要文字。"""
    lines = ["=== 6 屆新生人數 ==="]

    for year in sorted(summary):
        lines.append(f"  {year} 學年：{summary[year]['total']:>4} 人")

    lines.append("")
    lines.append("=== 全體最熱門 5 個系所（累計 6 屆） ===")
    for dept, count in all_depts.most_common(5):
        lines.append(f"  {count:>4} 人  {dept}")

    if target_year in summary:
        lines.append("")
        lines.append(f"=== {target_year} 學年入學方式分布 ===")
        for kind, count in summary[target_year]["by_entry"].most_common():
            lines.append(f"  {count:>4} 人  {kind}")

    return "\n".join(lines)


def save_snapshot(summary: dict, snapshot_path: Path) -> None:
    """把統計結果存成 pickle，方便下次直接載入。"""
    with open(snapshot_path, "wb") as file:
        pickle.dump(summary, file)


def load_snapshot(snapshot_path: Path) -> dict:
    """讀回先前儲存的 pickle 快照。"""
    with open(snapshot_path, "rb") as file:
        return pickle.load(file)


def run_demo(zip_path: Path = DEFAULT_ZIP_PATH) -> str:
    """示範完整流程：讀 zip、印摘要、暫存報告與快照。"""
    summary, all_depts = build_summary(zip_path)
    output = [f"資料來源: {zip_path.name}", "", format_console_summary(summary, all_depts)]

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        snapshot_path = temp_root / "summary.pkl"
        report_path = temp_root / "report.md"

        save_snapshot(summary, snapshot_path)
        report_path.write_text(build_markdown_report(summary), encoding="utf-8")
        loaded = load_snapshot(snapshot_path)

        output.append("")
        output.append(f"快照寫入 {snapshot_path.name}：{snapshot_path.stat().st_size} bytes")
        output.append("")
        output.append("=== Markdown 報告預覽 ===")
        output.append(report_path.read_text(encoding="utf-8").rstrip())
        output.append(f"pickle 讀回 key: {sorted(loaded.keys())}")
        output.append("")
        output.append("(沙箱已自動清理)")

    return "\n".join(output)


def main():
    if not DEFAULT_ZIP_PATH.exists():
        print(f"找不到資料：{DEFAULT_ZIP_PATH}")
        return
    print(run_demo(DEFAULT_ZIP_PATH))


if __name__ == "__main__":
    main()
