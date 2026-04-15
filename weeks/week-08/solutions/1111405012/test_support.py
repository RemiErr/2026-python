from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parent


def run_python_program(filename: str, input_data: str) -> str:
    """執行指定的 Python 程式，並回傳標準輸出文字。"""
    completed = subprocess.run(
        [sys.executable, str(BASE_DIR / filename)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=BASE_DIR,
        check=False,
    )

    if completed.returncode != 0:
        raise AssertionError(
            f"{filename} 執行失敗\n"
            f"return code: {completed.returncode}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )

    return completed.stdout
