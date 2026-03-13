import unittest

from robot_core import RobotWorld


class TestRobotCore(unittest.TestCase):
    def setUp(self) -> None:
        self.world = RobotWorld(5, 3)

    def test_left_rotation(self) -> None:
        self.world.reset_robot(0, 0, "N")
        self.world.step("L")
        self.assertEqual(self.world.state_tuple(), (0, 0, "W", False))

    def test_right_rotation(self) -> None:
        self.world.reset_robot(0, 0, "N")
        self.world.step("R")
        self.assertEqual(self.world.state_tuple(), (0, 0, "E", False))

    def test_four_rights_returns(self) -> None:
        self.world.reset_robot(0, 0, "N")
        for _ in range(4):
            self.world.step("R")
        self.assertEqual(self.world.state_tuple(), (0, 0, "N", False))

    def test_forward_within_bounds(self) -> None:
        self.world.reset_robot(1, 1, "N")
        self.world.step("F")
        self.assertEqual(self.world.state_tuple(), (1, 2, "N", False))

    def test_lost_stops_future_commands(self) -> None:
        self.world.reset_robot(0, 3, "N")
        self.world.step("F")
        self.world.step("R")
        self.assertEqual(self.world.state_tuple(), (0, 3, "N", True))

    def test_invalid_command_is_ignored(self) -> None:
        self.world.reset_robot(1, 1, "E")
        self.world.step("X")
        self.assertEqual(self.world.state_tuple(), (1, 1, "E", False))


if __name__ == "__main__":
    unittest.main()
