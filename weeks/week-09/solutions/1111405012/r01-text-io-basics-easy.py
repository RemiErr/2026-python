from pathlib import Path


def write_hello_file(path):
    # 用最直接的方式寫入兩行文字。
    path = Path(path)
    with open(path, "wt", encoding="utf-8") as file:
        file.write("你好，Python\n")
        file.write("第二行\n")
    return path


def read_all_text(path):
    # 一次把整個檔案讀完。
    with open(path, "rt", encoding="utf-8") as file:
        return file.read()


def read_lines(path):
    # 逐行讀取時，把換行拿掉會比較容易比對內容。
    result = []
    with open(path, "rt", encoding="utf-8") as file:
        for line in file:
            result.append(line.rstrip("\n"))
    return result


def write_log_file(path, user="alice"):
    # print 也能像 print 到畫面一樣，直接印進檔案。
    path = Path(path)
    with open(path, "wt", encoding="utf-8") as file:
        print("登入成功", file=file)
        print("使用者:", user, file=file)
    return path


def write_fruits_csv(path, fruits):
    # 用 sep="," 就能快速做出最簡單的 CSV。
    path = Path(path)
    with open(path, "wt", encoding="utf-8") as file:
        print(*fruits, sep=",", file=file)
    return path


def append_csv_pair(path, left, right):
    # 用附加模式把新資料接到原本檔案後面。
    path = Path(path)
    with open(path, "at", encoding="utf-8") as file:
        print(left, end=",", file=file)
        print(right, file=file)
    return path


def read_text_with_path(path):
    # Path 物件自己也會讀檔，寫法更短。
    return Path(path).read_text(encoding="utf-8")


def demonstrate_text_mode_type_error(path):
    # 文字模式只能寫 str，寫 bytes 會出錯。
    try:
        with open(path, "wt", encoding="utf-8") as file:
            file.write(b"bytes in text mode")
    except TypeError as error:
        return str(error)
    return ""


def run_examples(base_dir="."):
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
