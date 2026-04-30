import csv
import io
import platform
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT_DIR = Path(__file__).resolve().parents[4]
DEFAULT_ZIP_PATH = ROOT_DIR / "assets" / "npu-stu-109-114-anon.zip"

_CJK_FONTS = {
    "Darwin": ["Heiti TC", "Arial Unicode MS", "PingFang TC"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],
    "Linux": ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],
}.get(platform.system(), ["sans-serif"])

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


def apply_cjk_font() -> None:
    """seaborn 重設主題後，要再把中文字型蓋回來。"""
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["axes.unicode_minus"] = False


def load_long_frame(zip_path: Path, mapping: dict | None = None) -> pd.DataFrame:
    """把 zip 中每個 CSV 攤平成 long-form DataFrame。"""
    mapping = mapping or DEPT_TO_COLLEGE
    records = []

    with zipfile.ZipFile(zip_path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if not info.filename.endswith(".csv"):
                continue

            year = int(info.filename[:3])
            text = archive.read(info).decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))

            for row in reader:
                dept = row.get("系所名稱", "").strip()
                if not dept:
                    continue
                records.append(
                    {
                        "學年": year,
                        "學院": mapping.get(dept, "其他"),
                        "系所": dept,
                    }
                )

    return pd.DataFrame.from_records(records)


def build_year_college_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """把 long-form DataFrame 壓成各學年 × 各學院的人數表。"""
    if frame.empty:
        return pd.DataFrame(columns=["學年", "學院", "人數"])

    return (
        frame.groupby(["學年", "學院"])
        .size()
        .reset_index(name="人數")
        .sort_values(["學年", "學院"], ignore_index=True)
    )


def build_pivot_table(summary: pd.DataFrame) -> pd.DataFrame:
    """轉成寬表，方便堆疊長條圖使用。"""
    if summary.empty:
        return pd.DataFrame()

    return (
        summary.pivot(index="學年", columns="學院", values="人數")
        .fillna(0)
        .sort_index()
    )


def build_figure(summary: pd.DataFrame):
    """用 seaborn 畫折線圖，並用 pandas/matplotlib 畫堆疊長條圖。"""
    sns.set_theme(style="whitegrid", context="talk", palette="Set2")
    apply_cjk_font()

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(15, 6),
        gridspec_kw={"width_ratios": [1.3, 1]},
    )

    if not summary.empty:
        sns.lineplot(
            data=summary,
            x="學年",
            y="人數",
            hue="學院",
            marker="o",
            markersize=10,
            linewidth=2.5,
            ax=axes[0],
        )
        axes[0].set_xticks(sorted(summary["學年"].unique()))
        axes[0].legend(title="學院", loc="upper right", frameon=True)

        for _, row in summary.iterrows():
            axes[0].annotate(
                int(row["人數"]),
                (row["學年"], row["人數"]),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=9,
                alpha=0.8,
            )

        pivot = build_pivot_table(summary)
        pivot.plot(
            kind="bar",
            stacked=True,
            ax=axes[1],
            colormap="Set2",
            width=0.75,
            edgecolor="white",
        )
        axes[1].legend(title="學院", loc="upper right", fontsize=9)
        axes[1].tick_params(axis="x", rotation=0)
    else:
        axes[0].text(0.5, 0.5, "無資料", ha="center", va="center", transform=axes[0].transAxes)
        axes[1].text(0.5, 0.5, "無資料", ha="center", va="center", transform=axes[1].transAxes)

    axes[0].set_title("109–114 各學院新生人數趨勢", fontsize=16, pad=12)
    axes[1].set_title("各學年學院結構（堆疊）", fontsize=16, pad=12)
    axes[1].set_ylabel("人數")
    fig.suptitle("國立澎湖科技大學 109–114 學年新生生源分析", fontsize=18, fontweight="bold", y=1.02)
    fig.tight_layout()
    return fig


def save_figure(fig, output_path: Path) -> bool:
    """用 x 模式避免覆蓋舊圖，再把 Figure 存成 PNG。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(output_path, "xb") as file:
            fig.savefig(file, dpi=150, bbox_inches="tight")
        return True
    except FileExistsError:
        return False


def summarize_for_console(summary: pd.DataFrame) -> str:
    """把寬表轉成適合終端閱讀的字串。"""
    pivot = build_pivot_table(summary)
    if pivot.empty:
        return "各學年各學院:\n(無資料)"
    return "各學年各學院:\n" + pivot.to_string()


def main():
    if not DEFAULT_ZIP_PATH.exists():
        print(f"找不到：{DEFAULT_ZIP_PATH}")
        return

    frame = load_long_frame(DEFAULT_ZIP_PATH)
    summary = build_year_college_summary(frame)
    fig = build_figure(summary)
    output_path = Path(__file__).resolve().parent / "A08-college-trend.png"

    print("總筆數:", len(frame))
    print(frame.head())
    print()
    print(summarize_for_console(summary))

    if save_figure(fig, output_path):
        print(f"\n圖檔已寫入：{output_path.name}")
    else:
        print(f"\n{output_path.name} 已存在，保留舊檔（要重畫請先刪除）")

    plt.close(fig)


if __name__ == "__main__":
    main()
