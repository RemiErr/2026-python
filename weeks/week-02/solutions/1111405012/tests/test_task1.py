import unittest

from task1_sequence_clean import process_numbers, format_output


class TestTask1SequenceClean(unittest.TestCase):
    def test_dedupe_preserves_order(self):
        nums = [5, 3, 5, 2, 9, 2, 8, 3, 1]
        result = process_numbers(nums)
        self.assertEqual(result["dedupe"], [5, 3, 2, 9, 8, 1])

    def test_sorting_and_evens(self):
        nums = [4, 1, 6, 3, 6, 2]
        result = process_numbers(nums)
        self.assertEqual(result["asc"], [1, 2, 3, 4, 6, 6])
        self.assertEqual(result["desc"], [6, 6, 4, 3, 2, 1])
        self.assertEqual(result["evens"], [4, 6, 6, 2])

    def test_empty_input(self):
        result = process_numbers([])
        lines = format_output(result)
        self.assertEqual(lines, ["dedupe:", "asc:", "desc:", "evens:"])


if __name__ == "__main__":
    unittest.main()
