import unittest

from test_support import run_python_program


PROGRAMS = [
    "question-10222.py",
    "question-10222-easy.py",
    "question-10222-su.py",
]


class Question10222Test(unittest.TestCase):
    # 這題要保留空白與換行，所以直接比對完整字串。
    def assert_programs_output(self, input_data, expected_output):
        for program in PROGRAMS:
            with self.subTest(program=program):
                actual_output = run_python_program(program, input_data)
                self.assertEqual(actual_output, expected_output)

    def test_sample_case(self):
        input_data = "k[r dyt I[o\n"
        expected_output = "how are you\n"
        self.assert_programs_output(input_data, expected_output)

    def test_digits_and_punctuation(self):
        input_data = "2345 ;p0\n"
        expected_output = "`123 ki8\n"
        self.assert_programs_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
