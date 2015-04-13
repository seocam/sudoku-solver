
import unittest

from sudoku import Possibilities


class TestPossibilities(unittest.TestCase):

    def setUp(self):
        self.empty_set = set()
        self.all_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.possibilities = Possibilities()

    def test_init_set_instances(self):
        self.assertIsInstance(self.possibilities.column, set)
        self.assertIsInstance(self.possibilities.line, set)
        self.assertIsInstance(self.possibilities.region, set)
        self.assertIsInstance(self.possibilities.tested, set)

    def test_init_values(self):
        self.assertEqual(self.possibilities.column, self.all_set)
        self.assertEqual(self.possibilities.line, self.all_set)
        self.assertEqual(self.possibilities.region, self.all_set)
        self.assertEqual(self.possibilities.tested, self.empty_set)

    def test_available(self):
        self.assertEqual(self.possibilities.available, self.all_set)

        self.possibilities.line.remove(1)
        self.all_set.remove(1)
        self.assertEqual(self.possibilities.available, self.all_set)

        self.possibilities.column.remove(2)
        self.all_set.remove(2)
        self.assertEqual(self.possibilities.available, self.all_set)

        self.possibilities.region.remove(3)
        self.all_set.remove(3)
        self.assertEqual(self.possibilities.available, self.all_set)

        self.possibilities.tested.add(4)
        self.all_set.remove(4)
        self.assertEqual(self.possibilities.available, self.all_set)

    def test_len(self):
        self.assertEqual(len(self.possibilities), 9)
        self.possibilities.line -= {1,2,3}
        self.assertEqual(len(self.possibilities), 6)

    def test_to_list(self):
        l_possibilities = self.possibilities._to_list()
        self.assertIsInstance(l_possibilities, list)
        self.assertEqual(l_possibilities, list(range(1, 10)))

    def test_next(self):
        i = 1
        print self.possibilities
        for possibility in self.possibilities:
            self.assertEqual(possibility, i)
            self.possibilities.tested.add(i)
            i += 1

        with self.assertRaises(StopIteration):
            self.possibilities.next()
