import unittest

from task3_log_summary import summarize_logs


class TestTask3LogSummary(unittest.TestCase):
    def test_summary_counts(self):
        entries = [
            ("alice", "login"),
            ("bob", "login"),
            ("alice", "view"),
            ("alice", "logout"),
            ("bob", "view"),
            ("bob", "view"),
            ("chris", "login"),
            ("bob", "logout"),
        ]
        users, top_action = summarize_logs(entries)
        self.assertEqual(users, [("bob", 4), ("alice", 3), ("chris", 1)])
        self.assertEqual(top_action, ("login", 3))

    def test_tie_break_user_name(self):
        entries = [
            ("bob", "login"),
            ("amy", "login"),
            ("bob", "view"),
            ("amy", "view"),
        ]
        users, top_action = summarize_logs(entries)
        self.assertEqual(users, [("amy", 2), ("bob", 2)])
        self.assertEqual(top_action, ("login", 2))

    def test_empty_input(self):
        users, top_action = summarize_logs([])
        self.assertEqual(users, [])
        self.assertEqual(top_action, (None, 0))


if __name__ == "__main__":
    unittest.main()
