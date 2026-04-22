import subprocess
import sys
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS = [
    "question-10242.py",
    "question-10242-easy.py",
    "question-10242-su.py",
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


class Question10242Tests(unittest.TestCase):
    # 三個版本都必須算出相同的最大搶劫金額。
    def check_all_versions(self, input_data, expected_output):
        for script_name in SCRIPTS:
            with self.subTest(script=script_name):
                result = run_script(script_name, input_data)
                self.assertEqual(result.returncode, 0, msg=result.stderr)
                self.assertEqual(result.stdout.strip(), expected_output.strip())

    def test_path_through_scc(self):
        input_data = """\
5 6
1 2
2 3
3 2
3 4
4 5
1 5
1
2
3
4
5
1 2
4 5
"""
        self.check_all_versions(input_data, "15")

    def test_start_scc_is_also_a_bar(self):
        input_data = """\
4 4
1 2
2 1
2 3
4 3
10
20
30
40
1 2
1 3
"""
        self.check_all_versions(input_data, "60")


if __name__ == "__main__":
    unittest.main()
