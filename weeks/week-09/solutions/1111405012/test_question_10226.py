import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "question-10226.py",
    "question-10226-easy.py",
    "question-10226-su.py",
]


def run_script(script_name, input_data):
    script_path = BASE_DIR / script_name
    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=input_data,
        text=True,
        capture_output=True,
        check=False,
    )
    return result


def normalize(text):
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


class Question10226Tests(unittest.TestCase):
    # 逐一執行三個版本，確認它們的輸出都一致。
    def check_all_versions(self, input_data, expected_output):
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                result = run_script(script_name, input_data)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertEqual(normalize(result.stdout), normalize(expected_output))

    def test_sample_cases(self):
        input_data = """\
3
0
0
0
3
1 0
3 0
0
"""
        expected_output = """\
ABC
CB
BAC
CA
CAB
BA

BAC
CA
CBA
"""
        self.check_all_versions(input_data, expected_output)

    def test_single_valid_arrangement(self):
        input_data = """\
2
2 0
1 0
"""
        expected_output = "AB"
        self.check_all_versions(input_data, expected_output)


if __name__ == "__main__":
    unittest.main()
