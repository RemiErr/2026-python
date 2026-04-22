import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "question-10268.py",
    "question-10268-easy.py",
    "question-10268-su.py",
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


class Question10268Tests(unittest.TestCase):
    # 三個版本都要通過題目的官方範例。
    def check_all_versions(self, input_data, expected_output):
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                result = run_script(script_name, input_data)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertEqual(result.stdout.strip(), expected_output.strip())

    def test_sample_case(self):
        input_data = """\
2 100
10 786599
4 786599
60 1844674407370955161
63 9223372036854775807
0 0
"""
        expected_output = """\
14
21
More than 63 trials needed.
61
63
"""
        self.check_all_versions(input_data, expected_output)

    def test_small_values(self):
        input_data = """\
1 1
2 3
3 14
0 0
"""
        expected_output = """\
1
2
4
"""
        self.check_all_versions(input_data, expected_output)


if __name__ == "__main__":
    unittest.main()
