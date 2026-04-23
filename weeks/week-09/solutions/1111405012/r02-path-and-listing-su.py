import os
from pathlib import Path


def build_week_path():
    return Path("weeks") / "week-09"


def describe_path(path):
    path = Path(path)
    return {
        "path": path,
        "name": path.name,
        "parent": path.parent,
        "suffix": path.suffix,
        "stem": path.stem,
    }


def join_with_os(*parts):
    return os.path.join(*parts)


def check_path_status(path):
    path = Path(path)
    return {
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }


def missing_message(path):
    path = Path(path)
    if not path.exists():
        return f"{path} 不存在，略過讀取"
    return None


def list_directory_names(directory):
    return sorted(os.listdir(directory))


def glob_py_files(directory):
    directory = Path(directory)
    return sorted(path.name for path in directory.glob("*.py"))


def rglob_py_files(directory):
    directory = Path(directory)
    return sorted(path.relative_to(directory).as_posix() for path in directory.rglob("*.py"))


def first_rglob_py(directory):
    matches = rglob_py_files(directory)
    if matches:
        return matches[0]
    return None


def run_examples(base_dir=".", recursive_root=None):
    base_dir = Path(base_dir)
    recursive_root = Path(recursive_root) if recursive_root is not None else base_dir.parent

    base = build_week_path()
    base_info = describe_path(base)
    print(base_info["path"])
    print(base_info["name"])
    print(base_info["parent"])
    print(base_info["suffix"])

    hello_info = describe_path(base_dir / "hello.txt")
    print(hello_info["stem"], hello_info["suffix"])

    print(join_with_os("weeks", "week-09", "README.md"))

    hello_status = check_path_status(base_dir / "hello.txt")
    print(hello_status["exists"])
    print(hello_status["is_file"])
    print(hello_status["is_dir"])

    message = missing_message(base_dir / "no_such_file.txt")
    if message:
        print(message)

    for name in list_directory_names(base_dir):
        print("listdir:", name)

    for name in glob_py_files(base_dir):
        print("glob:", name)

    first_match = first_rglob_py(recursive_root)
    if first_match is not None:
        print("rglob:", first_match)


def main():
    run_examples()


if __name__ == "__main__":
    main()
