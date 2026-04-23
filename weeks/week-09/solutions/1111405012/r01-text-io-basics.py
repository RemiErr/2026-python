from pathlib import Path


def write_hello_file(path):
    """寫入教材中的示範文字檔。"""
    file_path = Path(path)
    with open(file_path, "wt", encoding="utf-8") as file:
        # 文字模式寫入 str，並保留換行符號。
        file.write("你好，Python\n")
        file.write("第二行\n")
    return file_path


def read_all_text(path):
    """一次讀完整個文字檔。"""
    with open(path, "rt", encoding="utf-8") as file:
        return file.read()


def read_lines(path):
    """逐行讀取文字檔，並移除每行結尾的換行。"""
    lines = []
    with open(path, "rt", encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip("\n"))
    return lines


def write_log_file(path, user="alice"):
    """示範把 print 的輸出導向檔案。"""
    file_path = Path(path)
    with open(file_path, "wt", encoding="utf-8") as file:
        print("登入成功", file=file)
        print("使用者:", user, file=file)
    return file_path


def write_fruits_csv(path, fruits):
    """用 print 的 sep 與 end 寫出簡單的 CSV 文字。"""
    file_path = Path(path)
    with open(file_path, "wt", encoding="utf-8") as file:
        print(*fruits, sep=",", end="\n", file=file)
    return file_path


def append_csv_pair(path, left, right):
    """在同一個 CSV 文字檔後面再補一行資料。"""
    file_path = Path(path)
    with open(file_path, "at", encoding="utf-8") as file:
        print(left, end=",", file=file)
        print(right, file=file)
    return file_path


def read_text_with_path(path):
    """用 Path.read_text 直接讀回全文。"""
    return Path(path).read_text(encoding="utf-8")


def demonstrate_text_mode_type_error(path):
    """示範文字模式下寫入 bytes 會丟出 TypeError。"""
    try:
        with open(path, "wt", encoding="utf-8") as file:
            file.write(b"bytes in text mode")
    except TypeError as error:
        return str(error)
    return ""


def run_examples(base_dir="."):
    """重現原始教材腳本的主要示範。"""
    base_dir = Path(base_dir)

    hello_path = write_hello_file(base_dir / "hello.txt")
    print(read_all_text(hello_path), end="")

    for line in read_lines(hello_path):
        print(line)

    write_log_file(base_dir / "log.txt")

    fruits_path = write_fruits_csv(base_dir / "fruits.csv", ["apple", "banana", "cherry"])
    append_csv_pair(fruits_path, "date", "2026-04-23")
    print(read_text_with_path(fruits_path), end="")

    error_message = demonstrate_text_mode_type_error(base_dir / "bad.txt")
    if error_message:
        print("錯誤示範:", error_message)


def main():
    run_examples()


if __name__ == "__main__":
    main()
