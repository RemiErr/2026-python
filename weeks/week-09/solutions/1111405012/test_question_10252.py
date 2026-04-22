import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "question-10252.py",
    "question-10252-easy.py",
    "question-10252-su.py",
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


class Question10252Tests(unittest.TestCase):
    # 這裡同時驗證奇數點數與偶數點數的情況。
    def check_all_versions(self, input_data, expected_output):
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                result = run_script(script_name, input_data)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertEqual(result.stdout.strip(), expected_output.strip())

    def test_sample_case(self):
        input_data = """\
1
3
0 0
1 1
2 2
"""
        self.check_all_versions(input_data, "4 1")

    def test_even_number_of_points(self):
        input_data = """\
2
4
0 0
0 2
2 0
2 2
2
5 5
5 5
"""
        expected_output = """\
8 9
0 1
"""
        self.check_all_versions(input_data, expected_output)


if __name__ == "__main__":
    unittest.main()
