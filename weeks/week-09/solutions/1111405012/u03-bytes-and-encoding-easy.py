from pathlib import Path


PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def write_fake_png(path):
    # 這裡只寫檔頭，不是真的圖片內容。
    path = Path(path)
    path.write_bytes(PNG_MAGIC)
    return path


def read_head_bytes(path, size=8):
    # 讀二進位資料時要用 rb。
    with open(path, "rb") as file:
        return file.read(size)


def bytes_match_png_magic(data):
    # 檢查讀到的位元組是不是 PNG 檔頭。
    return data == PNG_MAGIC


def first_bytes_as_numbers(data, count=4):
    # bytes 逐個取值時，拿到的是整數。
    return [(value, hex(value)) for value in data[:count]]


def text_to_bytes(text, encoding="utf-8"):
    # str 變 bytes 叫做編碼。
    return text.encode(encoding)


def bytes_to_text(data, encoding="utf-8"):
    # bytes 變 str 叫做解碼。
    return data.decode(encoding)


def write_utf8_text(path, text):
    # 文字檔寫入時要明確指定 encoding。
    path = Path(path)
    path.write_text(text, encoding="utf-8")
    return path


def read_text_with_encoding(path, encoding="utf-8"):
    return Path(path).read_text(encoding=encoding)


def try_read_text(path, encoding):
    # 如果編碼用錯了，可能會出現 UnicodeDecodeError。
    try:
        text = read_text_with_encoding(path, encoding)
        return {"ok": True, "value": text}
    except UnicodeDecodeError as error:
        return {"ok": False, "value": str(error)}


def run_examples(base_dir="."):
    base_dir = Path(base_dir)

    fake_png_path = write_fake_png(base_dir / "fake.png")
    head = read_head_bytes(fake_png_path)
    print(head)
    print(bytes_match_png_magic(head))

    for value, hex_value in first_bytes_as_numbers(head):
        print(value, hex_value)

    text = "你好"
    data = text_to_bytes(text)
    print(text, type(text))
    print(data, type(data))
    print(bytes_to_text(data))

    zh_path = write_utf8_text(base_dir / "zh.txt", "中文測試\n")
    print(read_text_with_encoding(zh_path), end="")

    wrong_result = try_read_text(zh_path, "big5")
    if not wrong_result["ok"]:
        print("解碼錯誤:", wrong_result["value"])


def main():
    run_examples()


if __name__ == "__main__":
    main()
