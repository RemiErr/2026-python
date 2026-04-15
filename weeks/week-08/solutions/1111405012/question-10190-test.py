import unittest
from textwrap import dedent

from test_support import run_python_program


PROGRAMS = [
    "question-10190.py",
    "question-10190-easy.py",
    "question-10190-su.py",
]


class Question10190Test(unittest.TestCase):
    # 這題改成依照 md 內文的自動傘題意測試。
    def assert_programs_output(self, input_data, expected_output):
        for program in PROGRAMS:
            with self.subTest(program=program):
                actual_output = run_python_program(program, input_data)
                self.assertEqual(actual_output.rstrip(), expected_output.rstrip())

    def test_reference_case(self):
        input_data = dedent(
            """\
            2 4 3 10
            0 1 1
            3 1 -1
            """
        )
        expected_output = "65.00\n"
        self.assert_programs_output(input_data, expected_output)

    def test_static_umbrellas(self):
        input_data = dedent(
            """\
            2 10 2 3
            1 4 0
            3 4 0
            """
        )
        expected_output = "24.00\n"
        self.assert_programs_output(input_data, expected_output)

    def test_no_umbrella(self):
        input_data = "0 7 5 2\n"
        expected_output = "70.00\n"
        self.assert_programs_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
