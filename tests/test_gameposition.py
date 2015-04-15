
import unittest

from sudoku import Game


class TestGamePosition(unittest.TestCase):

    def setUp(self):
        matrix = [
            [0, 7, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 3, 4, 5, 6, 7, 8, 9],
        ]
        self.game = Game(matrix, forward_check=True)

    def test_init_value(self):
        position = self.game.matrix[0][1]
        self.assertEqual(position._value, 7)

    def test_init_possibilities(self):
        self.assertEqual(self.game.matrix[0][0].possibilities.available,
                         {1, 2, 3, 4, 5, 6, 8, 9})

    def test_init_game(self):
        position = self.game.matrix[0][1]
        self.assertEqual(self.game, position.game)

    def test_coordinates(self):
        position = self.game.matrix[3][5] 
        self.assertEqual(position.coordinates, (3, 5))

    def assert_in_possibilities(self, value, target_position):
        for position in target_position.line:
            self.assertIn(value, position.possibilities.line)

        for position in target_position.column:
            self.assertIn(value, position.possibilities.column)

        for position in target_position.region:
            self.assertIn(value, position.possibilities.region)

    def assert_not_in_possibilities(self, value, target_position):
        for position in target_position.line:
            self.assertNotIn(value, position.possibilities.line)

        for position in target_position.column:
            self.assertNotIn(value, position.possibilities.column)

        for position in target_position.region:
            self.assertNotIn(value, position.possibilities.region)

    def test_possibility(self):
        position = self.game.matrix[0][0]
        self.assert_in_possibilities(1, position)

    def test_remove_possibility(self):
        position = self.game.matrix[0][0]
        position.remove_possibilities(1)
        self.assert_not_in_possibilities(1, position)

    def test_add_possibility(self):
        position = self.game.matrix[0][0]
        position.remove_possibilities(1)
        self.assert_not_in_possibilities(1, position)
        position.add_possibilities(1)
        self.assert_in_possibilities(1, position)

    def test_value(self):
        position = self.game.matrix[7][7]
        position._value = 3
        position.value = 5
        self.assertEqual(position.value, position._value)

    def test_value_setter(self):
        position = self.game.matrix[0][0]
        position.value = 2

        self.assert_not_in_possibilities(2, position)
        self.assert_in_possibilities(1, position)
        position.value = 0
        self.assert_in_possibilities(2, position)

        position.value = 1
        self.assert_not_in_possibilities(1, position)

    def test_repr(self):
        position = self.game.matrix[0][0]
        self.assertEqual(repr(position), '(0, 0)')
