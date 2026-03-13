import unittest

from robot_core import RobotWorld


class TestRobotScent(unittest.TestCase):
    def setUp(self) -> None:
        self.world = RobotWorld(5, 3)

    def test_leave_scent_on_lost(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.assertIn((0, 3, "N"), self.world.scents)
        self.assertTrue(self.world.robot.lost)

    def test_scent_blocks_forward(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.assertEqual(self.world.state_tuple(), (0, 3, "N", False))

    def test_same_cell_different_dir_not_blocked(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.world.reset_robot(0, 3, "E")
        self.world.step("F")
        self.assertEqual(self.world.state_tuple(), (1, 3, "E", False))

    def test_scents_persist_after_new_robot(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.world.reset_robot(2, 2, "S")
        self.assertIn((0, 3, "N"), self.world.scents)

    def test_clear_scents(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.world.clear_scents()
        self.assertEqual(len(self.world.scents), 0)


if __name__ == "__main__":
    unittest.main()
