import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "question-10235.py",
    "question-10235-easy.py",
    "question-10235-su.py",
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


class Question10235Tests(unittest.TestCase):
    # 同一組測資要讓三個版本都得到完全相同的答案。
    def check_all_versions(self, input_data, expected_output):
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                result = run_script(script_name, input_data)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertEqual(result.stdout.strip(), expected_output.strip())

    def test_sample_cases(self):
        input_data = """\
3
6 3
1 1 1
1 0 1
1 1 1
1 1 1
1 0 1
1 1 1
2 4
1 1 1 1
1 1 1 1
1 1
0
"""
        expected_output = """\
Case 1: 3
Case 2: 2
Case 3: 1
"""
        self.check_all_versions(input_data, expected_output)

    def test_small_boards(self):
        input_data = """\
3
1 1
1
1 1
0
2 2
1 1
1 1
"""
        expected_output = """\
Case 1: 0
Case 2: 1
Case 3: 1
"""
        self.check_all_versions(input_data, expected_output)


if __name__ == "__main__":
    unittest.main()
