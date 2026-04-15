import unittest
from textwrap import dedent

from test_support import run_python_program


PROGRAMS = [
    "question-10221.py",
    "question-10221-easy.py",
    "question-10221-su.py",
]


class Question10221Test(unittest.TestCase):
    # 這題輸出是固定到小數點後六位，所以直接比對字串。
    def assert_programs_output(self, input_data, expected_output):
        for program in PROGRAMS:
            with self.subTest(program=program):
                actual_output = run_python_program(program, input_data)
                self.assertEqual(actual_output.rstrip(), expected_output.rstrip())

    def test_sample_case(self):
        input_data = dedent(
            """\
            500 30 deg
            700 60 min
            200 45 deg
            """
        )
        expected_output = dedent(
            """\
            3633.775503 3592.408346
            124.616509 124.614927
            5215.043805 5082.035982
            """
        )
        self.assert_programs_output(input_data, expected_output)

    def test_zero_arc_after_full_turn(self):
        input_data = "10 21600 min\n"
        expected_output = "0.000000 0.000000\n"
        self.assert_programs_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
