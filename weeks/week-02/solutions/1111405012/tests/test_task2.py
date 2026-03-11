import unittest

from task2_student_ranking import sort_students, top_k


class TestTask2StudentRanking(unittest.TestCase):
    def test_sorting_rules(self):
        students = [
            ("amy", 88, 20),
            ("bob", 88, 19),
            ("zoe", 92, 21),
            ("ian", 88, 19),
            ("leo", 75, 20),
            ("eva", 92, 20),
        ]
        result = top_k(students, 3)
        self.assertEqual(
            result,
            [("eva", 92, 20), ("zoe", 92, 21), ("bob", 88, 19)],
        )

    def test_tie_break_by_name(self):
        students = [
            ("bob", 88, 19),
            ("amy", 88, 19),
            ("zoe", 88, 19),
        ]
        result = sort_students(students)
        self.assertEqual(result, [("amy", 88, 19), ("bob", 88, 19), ("zoe", 88, 19)])

    def test_k_larger_than_n(self):
        students = [("amy", 70, 20), ("bob", 80, 18)]
        result = top_k(students, 5)
        self.assertEqual(result, [("bob", 80, 18), ("amy", 70, 20)])


if __name__ == "__main__":
    unittest.main()
