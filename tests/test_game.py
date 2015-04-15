
import io
import unittest

from sudoku import parse_input, Game


class TestGame(unittest.TestCase):

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

    def game_from_str(self, game_str, check_forward=False, mrv=False):
        game_filelike = io.StringIO(game_str)
        return parse_input(check_forward, mrv, file_obj=game_filelike)[0]

    def test_validate_with_empty(self):
        game_str = (u'0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n'
                    '0 0 0 0 0 0 0 0 0\n')
        game = self.game_from_str(game_str)
        self.assertFalse(game.is_valid())

    def test_validate_fail_complete(self):
        game_str = (u'1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n'
                    '1 2 3 4 5 6 7 8 9\n')
        game = self.game_from_str(game_str)
        self.assertFalse(game.is_valid())

    def test_validate_fail_middle(self):
        game_str = (u'4 1 7 3 6 9 8 2 5\n'
                    '6 3 2 1 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 7 6 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)
        self.assertFalse(game.is_valid())

    def test_validate_fail_corner(self):
        game_str = (u'4 1 7 3 6 9 8 2 5\n'
                    '6 3 2 1 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 7 6 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 9\n')
        game = self.game_from_str(game_str)
        self.assertFalse(game.is_valid())

    def test_validate_correct_solution(self):
        game_str = (u'4 1 7 3 6 9 8 2 5\n'
                    '6 3 2 1 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 8 6 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)
        self.assertTrue(game.is_valid())

    def test_next(self):
        game_str = (u'0 1 7 3 6 9 8 2 5\n'
                    '6 3 2 0 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 8 0 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)
        available_moves = [(0, 0), (1, 3), (4, 5)]
        for i, position in enumerate(game):
            self.assertEqual(position.coordinates, available_moves[i])

        with self.assertRaises(StopIteration):
            game.next()

    def test_next_mrv(self):
        game_str = (u'0 1 7 3 6 9 8 2 5\n'
                    '0 0 0 0 5 8 9 4 7\n'
                    '0 0 0 7 2 4 3 1 6\n'
                    '0 0 0 4 3 7 1 6 9\n'
                    '7 9 1 5 8 0 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str, mrv=True)
        available_moves = [(0, 0), (1, 0), (1, 2), (1, 3), (2, 1), (3, 0),
                           (4, 5), (1, 1), (2, 0), (2, 2), (3, 1), (3, 2)]
        for i, position in enumerate(game):
            self.assertEqual(position.coordinates, available_moves[i])

        with self.assertRaises(StopIteration):
            game.next()

    def test_previous(self):
        game_str = (u'0 1 7 3 6 9 8 2 5\n'
                    '6 3 2 0 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 8 0 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)

        position = game.next()
        game.next()
        self.assertEqual(position, game.previous())

    def test_current_position(self):
        game_str = (u'0 1 7 3 6 9 8 2 5\n'
                    '6 3 2 0 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 8 0 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)

        position = game.next()
        self.assertEqual(position, game.current_position)

    def test_repr(self):
        game_str = (u'4 1 7 3 6 9 8 2 5\n'
                    '6 3 2 1 5 8 9 4 7\n'
                    '9 5 8 7 2 4 3 1 6\n'
                    '8 2 5 4 3 7 1 6 9\n'
                    '7 9 1 5 8 6 4 3 2\n'
                    '3 4 6 9 1 2 7 5 8\n'
                    '2 8 9 6 4 3 5 7 1\n'
                    '5 7 3 2 9 1 6 8 4\n'
                    '1 6 4 8 7 5 2 9 3\n')
        game = self.game_from_str(game_str)
        self.assertEqual(game_str, repr(game))

    def test_check_possibilities(self):
        position = self.game.matrix[0][0]
        self.assertFalse(self.game.forward_checking(position, 1))
        self.assertTrue(self.game.forward_checking(position, 2))

    def test_forward_checking_disabled(self):
        self.game.forward_check = False
        position = self.game.matrix[0][0]
        self.assertTrue(self.game.forward_checking(position, 1))
        self.assertTrue(self.game.forward_checking(position, 2))
