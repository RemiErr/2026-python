import unittest

from test_support import run_python_program


PROGRAMS = [
    "question-10193.py",
    "question-10193-easy.py",
    "question-10193-su.py",
]


class Question10193Test(unittest.TestCase):
    # 這題改成依照 md 內文的 arctan 分解題意測試。
    def assert_programs_output(self, input_data, expected_output):
        for program in PROGRAMS:
            with self.subTest(program=program):
                actual_output = run_python_program(program, input_data)
                self.assertEqual(actual_output.rstrip(), expected_output.rstrip())

    def test_a_is_one(self):
        self.assert_programs_output("1\n", "5\n")

    def test_a_is_three(self):
        self.assert_programs_output("3\n", "13\n")

    def test_a_is_five(self):
        self.assert_programs_output("5\n", "25\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
