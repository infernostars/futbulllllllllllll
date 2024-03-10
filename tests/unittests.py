import unittest
from sim.player import Player, Position
from typing import Optional

class TestPosition(unittest.TestCase):
    def setUp(self):
        self.pos1 = Position(0, 0)
        self.pos2 = Position(3, 4)

    def test_distance(self):
        self.assertAlmostEqual(self.pos1.distance(self.pos2), 5)

    def test_distance_line(self):
        pos3 = Position(0, 5)
        self.assertAlmostEqual(self.pos1.distance_line(self.pos2, pos3), 4.7434164902525)

    def test_moveto(self):
        self.pos1.moveto(self.pos2, 2)
        self.assertAlmostEqual(self.pos1.x, 1.2)
        self.assertAlmostEqual(self.pos1.y, 1.6)

        self.pos1.moveto(self.pos2, 10)
        self.assertAlmostEqual(self.pos1.x, 3)
        self.assertAlmostEqual(self.pos1.y, 4)

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.pos1 = Position(0, 0)
        self.pos2 = Position(3, 4)
        self.pos3 = Position(5, 0)
        self.player1 = Player("Player1", 80, 70, 100, self.pos1)
        self.player2 = Player("Player2", 75, 80, 90, self.pos2)
        self.player3 = Player("Player3", 85, 75, 95, self.pos3)

    def test_get_nearest_player_empty(self):
        nearest = self.player1.get_nearest_player([])
        self.assertIsNone(nearest)

    def test_get_nearest_player_single(self):
        nearest = self.player1.get_nearest_player([self.player2])
        self.assertEqual(nearest, self.player2)

    def test_get_nearest_player_multiple(self):
        nearest = self.player1.get_nearest_player([self.player2, self.player3])
        self.assertEqual(nearest, self.player2)

if __name__ == '__main__':
    unittest.main()