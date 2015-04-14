#!/usr/bin/env python

import itertools
import logging
import sys

from optparse import OptionParser


class MaxAttemptsExceeded(Exception):
    pass


class Possibilities(object):
    """Stores available possibilities for a position.

    Possibilities for column, line and region are stored in separated
    structures. Possibilities already attempted are also kept in an
    attribute the ``tested``.

    The difference between ``tested`` and the intersection of
    ``column``, ``line`` and ``region`` give the current available
    possibilities.

    This class also implements the iterator pattern always returning
    the first possibility available. This possibility is also added
    ``tested``.

    """

    def __init__(self):
        self.column = set(range(1, 10))
        self.line = set(range(1, 10))
        self.region = set(range(1, 10))
        self.tested = set()

    @property
    def available(self):
        return (self.line & self.region & self.column) - self.tested

    def __len__(self):
        return len(self.available)

    def _to_list(self):
        return sorted(self.available)

    def next(self):
        possibilities = self._to_list()

        # If no possibilities are available raise StopIteration
        #   to stop the for loop
        if not possibilities:
            raise StopIteration

        possibility = possibilities.pop(0)
        self.tested.add(possibility)
        return possibility

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

    def __str__(self):
        logging.debug('Line possibilities: %s', self.line)
        logging.debug('Column possibilities: %s', self.column)
        logging.debug('Region possibilities: %s', self.region)
        return str(self._to_list())

    def __repr__(self):
        return str(self)


class GamePosition(object):
    def __init__(self, value, game, i, j):
        self._value = 0
        self.possibilities = Possibilities()
        self.game = game
        self.i = i
        self.j = j
        self.value = int(value)

    def check_possibilities(self, value):
        if not self.game.forward_check:
            return True

        logging.debug('Forward Checking possibility %s', value)
        positions = itertools.chain(self.line, self.column, self.region)

        for position in positions:
            if position.value != 0:
                continue

            if not position.possibilities.available - {value}:
                logging.debug('Forward Checking failed on position %s',
                              position)
                return False

        return True

    def remove_possibilities(self, value):
        for position in self.line:
            if value in position.possibilities.line:
                position.possibilities.line.remove(value)

        for position in self.column:
            if value in position.possibilities.column:
                position.possibilities.column.remove(value)

        for position in self.region:
            if value in position.possibilities.region:
                position.possibilities.region.remove(value)

    def add_possibilities(self, value):
        for position in self.line:
            position.possibilities.line.add(value)

        for position in self.column:
            position.possibilities.column.add(value)

        for position in self.region:
            position.possibilities.region.add(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        if value == self._value:
            return

        logging.debug('Setting position [%s][%s] from %s to %s',
                      self.i, self.j, self.value, value)

        if not value:
            logging.debug('Added %s back to possibilities', self._value)
            self.add_possibilities(self._value)
        else:
            logging.debug('Removed %s from possibilities', value)
            self.remove_possibilities(value)
            self.game.attr_count += 1

            if self.game.max_attempts:
                # Abort if number of attempts exceed maximum value set
                if self.game.attr_count > int(self.game.max_attempts):
                    print('Numero de atribuicoes excede limite maximo')
                    logging.info('Number of attempts %s', self.game.attr_count)
                    raise MaxAttemptsExceeded

        self._value = value

    @property
    def line(self):
        for position in self.game.matrix[self.i]:
            if position != self:
                yield position

    @property
    def column(self):
        for line in self.game.matrix:
            if line[self.j] != self:
                yield line[self.j]

    @property
    def region(self):
        start_i = self.i // 3 * 3
        start_j = self.j // 3 * 3

        for i in range(start_i, start_i + 3):
            for j in range(start_j, start_j + 3):
                if self.game.matrix[i][j] != self:
                    yield self.game.matrix[i][j]

    @property
    def coordinates(self):
        return self.i, self.j

    def __str__(self):
        return str(self.coordinates)

    def __repr__(self):
        return str(self)


class Game(object):

    def __init__(self, matrix, forward_check=False, mrv=False, max_attempts=0):
        self.forward_check = forward_check
        self.mrv = mrv
        self.last_moves = []
        self.backtracking = False
        self.attr_count = 0
        self.max_attempts = max_attempts

        # Start an empty game
        self.empty_game()

        # Initialize the game with input data
        self.init_game(matrix)

    def init_game(self, matrix):
        self.available_moves = []

        for i, line in enumerate(matrix):
            for j, value in enumerate(line):
                position = self.matrix[i][j]
                position.value = int(value)
                if not position.value:
                    self.available_moves.append(position)

    def empty_game(self):
        self.matrix = []

        for i in range(9):
            line = []
            for j in range(9):
                line.append(GamePosition(0, self, i, j))
            self.matrix.append(line)

    def log_step(self, position=None):
        if position:
            logging.debug('Current position: %s', position.coordinates)
        else:
            logging.debug('Current position: n/a')

        logging.debug('Current status:\n%s', self)

        logging.debug('Available moves (%s): %s',
                      len(self.available_moves),
                      self.available_moves)

        logging.debug('Last moves: %s', self.last_moves)

        if position:
            logging.debug('Possibilities: %s', position.possibilities)

    def solve(self):
        for position in self:
            for value in position.possibilities:
                if position.check_possibilities(value):
                    position.value = value
                    break
            else:
                self.backtrack(position)
        logging.info('Solved with %s attributions.', self.attr_count)

    def backtrack(self, position):
        logging.debug('Backtracking!')

        while not position.possibilities:
            logging.debug('No possibilities for [%s][%s]',
                          *position.coordinates)
            position.possibilities.tested.clear()
            position = self.previous()
            position.value = 0

        self.backtracking = True

    def next(self):
        if self.backtracking:
            self.backtracking = False
            return self.current_position

        if not self.available_moves:
            raise StopIteration

        if self.mrv:
            logging.debug('Sorting by min possibilities remaining')
            self.available_moves.sort(key=lambda position:
                                      len(position.possibilities))

        position = self.available_moves.pop(0)

        logging.debug('Moving from %s to %s', self.current_position, position)

        self.last_moves.append(position)

        self.log_step(position)
        return position

    def __next__(self):
        return self.next()

    def previous(self):
        if len(self.last_moves) == 1:
            raise StopIteration

        last_position = self.last_moves.pop()

        logging.debug('Moving from %s to %s', last_position,
                      self.current_position)

        self.available_moves.insert(0, last_position)

        self.log_step(self.current_position)

        return self.current_position

    @property
    def current_position(self):
        try:
            position = self.last_moves[-1]
        except IndexError:
            return

        return position

    def __str__(self):
        game_repr = []
        for line in self.matrix:
            for position in line:
                game_repr.append(str(position.value))
                game_repr.append(' ')
            game_repr[-1] = '\n'
        return ''.join(game_repr)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self

    def is_valid(self):
        for line in self.matrix:
            # Check for zeros
            if 0 in line:
                logging.info('Invalid Solution (zeros)')
                logging.debug('\n%s', self)
                return False

            # Check lines
            line_set = {pos.value for pos in line}
            if len(line_set) != 9:
                logging.info('Invalid Solution (line)')
                logging.debug('\n%s', self)
                return False

        transp_matrix = zip(*self.matrix)

        for column in transp_matrix:
            # Check column
            column_set = {pos.value for pos in column}
            if len(column_set) != 9:
                logging.info('Invalid Solution (column)')
                logging.debug('\n%s', self)
                return False

        region_starts = itertools.combinations_with_replacement([0, 3, 6], 2)
        for i, j in region_starts:
            target_position = self.matrix[i][j]
            region_set = {target_position.value}

            for position in target_position.region:
                region_set.add(position.value)

            if len(region_set) != 9:
                logging.info('Invalid Solution (region)')
                logging.debug('\n%s', self)
                return False

        logging.info('Valid Solution')
        return True


def parse_input(forward_check=None, mrv=False, max_attempts=0,
                file_obj=sys.stdin):
    games = []

    count = 0
    matrix = []

    for str_line in file_obj:
        str_line = str_line.strip()

        if not str_line or ' ' not in str_line:
            continue

        line = str_line.split(' ')
        matrix.append(line)
        count += 1

        if count == 9:
            game = Game(matrix, forward_check=forward_check, mrv=mrv,
                        max_attempts=max_attempts)
            games.append(game)
            matrix = []
            count = 0

    return games


def parse_options():
    optparser = OptionParser()

    optparser.add_option("-v", "--verbose", dest="verbose", default=False,
                         action="store_true", help="Verbose output")
    optparser.add_option("-d", "--debug", dest="debug", default=False,
                         action="store_true", help="Print debug information")
    optparser.add_option("--forward-check", dest="forward_check",
                         default=False, action="store_true",
                         help="Enable forward check heuristic")
    optparser.add_option("--mrv", dest="mrv",
                         default=False, action="store_true",
                         help="Enable minimal remaining values heuristic")
    optparser.add_option("--validate", dest="validade",
                         default=False, action="store_true",
                         help="Check game results")
    optparser.add_option("--max-attempts", dest="max_attempts", default=10**6,
                         help=("Abort execution if exceeded. "
                               "Set to 0 to disable this check. "
                               "Defaults to 10^6"))

    return optparser.parse_args()[0]


def configure_logging(options):
    if options.verbose:
        logging.root.setLevel(logging.INFO)

    if options.debug:
        logging.root.setLevel(logging.DEBUG)


def main():
    options = parse_options()
    configure_logging(options)

    games = parse_input(options.forward_check, options.mrv,
                        options.max_attempts)
    status = 0

    for i, game in enumerate(games):
        logging.info('Game #%s', i + 1)

        if options.validade:
            if not game.is_valid():
                status = 1
        else:
            try:
                game.solve()
            except MaxAttemptsExceeded:
                pass
            else:
                print(game)

    return status


if __name__ == '__main__':
    sys.exit(main())
