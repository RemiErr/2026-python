import csv
import io
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ZIP_PATH = Path(__file__).resolve().parents[4] / "assets" / "npu-stu-109-114-anon.zip"
DEPT_TO_COLLEGE = {
    "應用外語系": "人文暨管理學院",
    "航運管理系": "人文暨管理學院",
    "行銷與物流管理系": "人文暨管理學院",
    "觀光休閒系": "人文暨管理學院",
    "資訊管理系": "人文暨管理學院",
    "餐旅管理系": "人文暨管理學院",
    "水產養殖系": "海洋資源暨工程學院",
    "海洋遊憩系": "海洋資源暨工程學院",
    "食品科學系": "海洋資源暨工程學院",
    "資訊工程系": "電資工程學院",
    "電信工程系": "電資工程學院",
    "電機工程系": "電資工程學院",
}


def read_frame(zip_path: Path):
    rows = []
    with zipfile.ZipFile(zip_path) as archive:
        for info in archive.infolist():
            if not info.filename.endswith(".csv"):
                continue
            year = int(info.filename[:3])
            text = archive.read(info).decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                dept = row.get("系所名稱", "").strip()
                if dept:
                    rows.append({"學年": year, "學院": DEPT_TO_COLLEGE.get(dept, "其他"), "系所": dept})
    return pd.DataFrame.from_records(rows)


def main():
    if not ZIP_PATH.exists():
        print(f"找不到資料：{ZIP_PATH}")
        return

    df = read_frame(ZIP_PATH)
    pivot = df.groupby(["學年", "學院"]).size().reset_index(name="人數")
    wide = pivot.pivot(index="學年", columns="學院", values="人數").fillna(0)

    sns.set_theme(style="whitegrid", context="talk", palette="Set2")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1.3, 1]})
    sns.lineplot(data=pivot, x="學年", y="人數", hue="學院", marker="o", ax=axes[0])
    wide.plot(kind="bar", stacked=True, ax=axes[1], colormap="Set2")

    axes[0].set_title("109–114 各學院新生人數趨勢")
    axes[1].set_title("各學年學院結構（堆疊）")
    axes[1].tick_params(axis="x", rotation=0)

    out = Path(__file__).resolve().parent / "A08-college-trend-su.png"
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"圖檔已寫入：{out.name}")


if __name__ == "__main__":
    main()
