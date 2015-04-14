
import io
import unittest

from sudoku import parse_input


class TestGame(unittest.TestCase):

    def game_from_str(self, game_str):
        game_filelike = io.StringIO(game_str)
        return parse_input(file_obj=game_filelike)[0]

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
