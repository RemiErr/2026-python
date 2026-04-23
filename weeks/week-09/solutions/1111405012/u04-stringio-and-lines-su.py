import csv
import io
from pathlib import Path


def build_string_buffer():
    buffer = io.StringIO()
    print("第一行", file=buffer)
    print("第二行", file=buffer)
    print("第三行", file=buffer)
    return buffer


def get_buffer_text(buffer):
    return buffer.getvalue()


def read_buffer_lines_with_numbers(buffer):
    buffer.seek(0)
    result = []
    for index, line in enumerate(buffer, 1):
        result.append((index, line.rstrip()))
    return result


def create_csv_in_memory(rows):
    memory_file = io.StringIO()
    writer = csv.writer(memory_file)
    for row in rows:
        writer.writerow(row)
    return memory_file.getvalue()


def write_poem_file(path):
    poem_text = "床前明月光\n\n疑是地上霜\n\n舉頭望明月\n低頭思故鄉\n"
    path = Path(path)
    path.write_text(poem_text, encoding="utf-8")
    return path


def number_nonempty_lines(src_path, dst_path):
    src_path = Path(src_path)
    dst_path = Path(dst_path)

    with open(src_path, "rt", encoding="utf-8") as source, open(
        dst_path, "wt", encoding="utf-8"
    ) as target:
        number = 0
        for line in source:
            text = line.rstrip()
            if not text:
                continue
            number += 1
            print(f"{number:02d}. {text}", file=target)

    return dst_path


def run_examples(base_dir="."):
    base_dir = Path(base_dir)

    buffer = build_string_buffer()
    print("---StringIO 內容---")
    print(get_buffer_text(buffer), end="")

    for index, line in read_buffer_lines_with_numbers(buffer):
        print(index, line)

    csv_text = create_csv_in_memory([["name", "score"], ["alice", 90]])
    print("---CSV in memory---")
    print(csv_text, end="")

    src_path = write_poem_file(base_dir / "poem.txt")
    dst_path = number_nonempty_lines(src_path, base_dir / "poem_numbered.txt")
    print("---加行號後---")
    print(dst_path.read_text(encoding="utf-8"), end="")


def main():
    run_examples()


if __name__ == "__main__":
    main()
