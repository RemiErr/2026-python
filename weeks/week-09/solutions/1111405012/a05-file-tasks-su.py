from datetime import date
from pathlib import Path


def default_count_target():
    here = Path(__file__).resolve().parent
    return here.parents[2] / "week-04" / "in-class"


def diary_filename(day=None):
    day = day or date.today().isoformat()
    return f"diary-{day}.txt"


def create_diary(base_dir=".", day=None, lines=None):
    day = day or date.today().isoformat()
    lines = lines or [f"# {day} 日記", "今天學了檔案 I/O。"]
    base_dir = Path(base_dir)
    path = base_dir / diary_filename(day)

    try:
        with open(path, "x", encoding="utf-8") as file:
            for line in lines:
                file.write(f"{line}\n")
        return {"created": True, "path": path, "message": f"已建立 {path.name}"}
    except FileExistsError:
        return {
            "created": False,
            "path": path,
            "message": f"{path.name} 今天已寫過，保留原內容不覆蓋",
        }


def count_py(folder):
    folder = Path(folder)
    total = 0
    nonblank = 0
    defs = 0

    for path in folder.rglob("*.py"):
        with open(path, "rt", encoding="utf-8", errors="replace") as file:
            for line in file:
                text = line.strip()
                total += 1
                if text:
                    nonblank += 1
                if text.startswith("def "):
                    defs += 1

    return total, nonblank, defs


def format_stats(folder, stats):
    total, nonblank, defs = stats
    folder = Path(folder)
    return [
        str(folder),
        f"  總行數       : {total}",
        f"  非空白行     : {nonblank}",
        f"  def 起頭行數 : {defs}",
    ]


def run_examples(base_dir=".", target_folder=None, day=None):
    base_dir = Path(base_dir)
    target_folder = Path(target_folder) if target_folder is not None else default_count_target()

    diary_result = create_diary(base_dir, day=day)
    print(diary_result["message"])

    if target_folder.exists():
        for line in format_stats(target_folder, count_py(target_folder)):
            print(line)
    else:
        print(f"示範目錄不存在：{target_folder}")


def main():
    run_examples()


if __name__ == "__main__":
    main()
