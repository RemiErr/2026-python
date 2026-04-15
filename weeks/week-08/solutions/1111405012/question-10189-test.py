import unittest
from textwrap import dedent

from test_support import run_python_program


PROGRAMS = [
    "question-10189.py",
    "question-10189-easy.py",
    "question-10189-su.py",
]


class Question10189Test(unittest.TestCase):
    # 每個版本都要跑同一批測資，確認輸出完全一致。
    def assert_programs_output(self, input_data, expected_output):
        for program in PROGRAMS:
            with self.subTest(program=program):
                actual_output = run_python_program(program, input_data)
                self.assertEqual(actual_output.rstrip(), expected_output.rstrip())

    def test_sample_case(self):
        input_data = dedent(
            """\
            4 4
            *...
            ....
            .*..
            ....
            3 5
            **...
            .....
            .*...
            0 0
            """
        )
        expected_output = dedent(
            """\
            Field #1:
            *100
            2210
            1*10
            1110

            Field #2:
            **100
            33200
            1*100
            """
        )
        self.assert_programs_output(input_data, expected_output)

    def test_single_safe_cell(self):
        input_data = dedent(
            """\
            1 1
            .
            0 0
            """
        )
        expected_output = dedent(
            """\
            Field #1:
            0
            """
        )
        self.assert_programs_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
