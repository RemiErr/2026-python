import gzip
import pickle
import tempfile
from pathlib import Path


def write_gzip_text(path, lines):
    """把多行文字寫進 gzip 壓縮檔。"""
    path = Path(path)
    with gzip.open(path, "wt", encoding="utf-8") as file:
        for line in lines:
            file.write(f"{line}\n")
    return path


def read_gzip_lines(path):
    """逐行讀回 gzip 文字檔。"""
    lines = []
    with gzip.open(path, "rt", encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip())
    return lines


def write_gzip_bytes(path, data):
    """把二進位資料寫進 gzip 檔。"""
    path = Path(path)
    with gzip.open(path, "wb") as file:
        file.write(data)
    return path


def read_gzip_bytes(path):
    """讀回 gzip 中的二進位資料。"""
    with gzip.open(path, "rb") as file:
        return file.read()


def path_size(path):
    """回傳檔案大小。"""
    return Path(path).stat().st_size


def demo_temporary_directory():
    """示範 TemporaryDirectory 會在離開 with 後自動清理。"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / "a.txt").write_text("hello\n", encoding="utf-8")
        (temp_path / "b.txt").write_text("world\n", encoding="utf-8")

        files = {}
        for path in sorted(temp_path.iterdir()):
            files[path.name] = path.read_text(encoding="utf-8").rstrip()

    return {"files": files, "exists_after": temp_path.exists()}


def demo_named_temporary_file(text="暫存 log\n", suffix=".log"):
    """示範 NamedTemporaryFile 產生實體暫存檔並自行刪除。"""
    with tempfile.NamedTemporaryFile(
        "wt", delete=False, suffix=suffix, encoding="utf-8"
    ) as file:
        file.write(text)
        path = Path(file.name)

    content = path.read_text(encoding="utf-8")
    exists_before_delete = path.exists()
    path.unlink()

    return {
        "path": path,
        "content": content,
        "exists_before_delete": exists_before_delete,
        "exists_after_delete": path.exists(),
    }


def dump_pickle(path, obj):
    """把 Python 物件存成 pickle。"""
    path = Path(path)
    with open(path, "wb") as file:
        pickle.dump(obj, file)
    return path


def load_pickle(path):
    """讀回 pickle 物件。"""
    with open(path, "rb") as file:
        return pickle.load(file)


def alice_average(scores):
    """計算 alice 的平均分數。"""
    return sum(scores["alice"]) / len(scores["alice"])


def run_examples(base_dir="."):
    """重現原始教材中的 gzip、暫存目錄與 pickle 示範。"""
    base_dir = Path(base_dir)

    notes_path = write_gzip_text(base_dir / "notes.txt.gz", ["第一行筆記", "第二行筆記"])
    for line in read_gzip_lines(notes_path):
        print("gz:", line)

    blob_path = write_gzip_bytes(base_dir / "blob.bin.gz", b"\x00\x01\x02\x03")
    print("blob size:", path_size(blob_path), "bytes")

    temp_result = demo_temporary_directory()
    for name, content in temp_result["files"].items():
        print("  ", name, "→", content)
    print("離開後還存在嗎？", temp_result["exists_after"])

    named_result = demo_named_temporary_file()
    print("暫存檔位置:", named_result["path"])

    scores = {
        "alice": [90, 85, 92],
        "bob": [70, 75, 80],
        "carol": [88, 91, 95],
    }
    pickle_path = dump_pickle(base_dir / "scores.pkl", scores)
    loaded = load_pickle(pickle_path)
    print("讀回的物件:", loaded)
    print("型別一致?", type(loaded) is dict)
    print("內容相等?", loaded == scores)
    print("alice 平均:", alice_average(loaded))


def main():
    run_examples()


if __name__ == "__main__":
    main()
