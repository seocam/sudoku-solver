#!/usr/bin/env python

import itertools
import logging
import sys

from optparse import OptionParser


REGION_START = {}


def get_region_start(point):
    if point not in REGION_START:
        REGION_START[point] = point // 3 * 3

    return REGION_START[point]


class GamePosition(object):
    def __init__(self, value, game, i, j):
        self.value = int(value)
        self.possibilities = range(1, 10)
        self.game = game
        self.i = i
        self.j = j

        if self.value > 0:
            self.fixed = True
        else:
            self.fixed = False
            self.game.available_moves.append(self.coordinates)

    @property
    def coordinates(self):
        return self.i, self.j

    def try_next(self):
        self.value = self.possibilities.pop(0)
        logging.debug('Setting position value: %s', self)

    def reset(self):
        self.possibilities = range(1, 10)
        self.value = 0

    def update_possibilities(self):
        self.possibilities = self.get_possibilities()

    def get_possibilities(self):
        start_i = get_region_start(self.i)
        start_j = get_region_start(self.j)

        values = set()
        for i in range(start_i, start_i + 3):
            for j in range(start_j, start_j + 3):
                values.add(self.game.matrix[i][j].value)

        # Line
        [values.add(i.value) for i in self.game.matrix[self.i]]

        # Column
        [values.add(line[self.j].value) for line in self.game.matrix]

        return list({1, 2, 3, 4, 5, 6, 7, 8, 9} - values)

    def __str__(self):
        return '[{}][{}] = {}'.format(self.i, self.j, self.value)

    def __repr__(self):
        return str(self)


class Game(list):
    def __init__(self, matrix):
        self.matrix = []
        self.available_moves = []
        self.last_moves = []

        for i, line in enumerate(matrix):
            game_line = []
            for j, value in enumerate(line):
                position = GamePosition(value, self, i, j)
                game_line.append(position)

            self.matrix.append(game_line)

    def log_step(self, position):
        logging.debug('-' * 80)

        logging.debug('Current status:\n%s', self)

        logging.debug('Available moves (%s): %s',
                      len(self.available_moves),
                      self.available_moves)

        logging.debug('Last moves: %s', self.last_moves)

        if position:
            logging.debug('Possibilities: %s', position.possibilities)
        else:
            logging.debug('Current position: n/a')

    def solve_simple(self):
        logging.info('Simple Solver')

        for position in self:
            valid_values = position.get_possibilities()

            while position.value not in valid_values:
                while not position.possibilities:
                    position.reset()
                    position = self.previous()
                    valid_values = position.get_possibilities()

                position.try_next()

    def solve_forward_check(self):
        logging.info('Forward Check Solver')

        for position in self:
            position.update_possibilities()

            while not position.possibilities:
                position.reset()
                position = self.previous()

            position.try_next()

    def solve(self, forward_check=False):
        if forward_check:
            return self.solve_forward_check()

        return self.solve_simple()

    def next(self):
        if not self.available_moves:
            raise StopIteration

        self.log_step(self.current_position)
        coordinates = self.available_moves.pop(0)
        self.last_moves.append(coordinates)

        return self.current_position

    def previous(self):
        if not self.last_moves:
            raise StopIteration

        self.log_step(self.current_position)
        coordinates = self.last_moves.pop()
        self.available_moves.insert(0, coordinates)

        return self.current_position

    @property
    def current_position(self):
        try:
            i, j = self.last_moves[-1]
        except IndexError:
            return

        return self.matrix[i][j]

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

            # Check for lines
            line_set = {pos.value for pos in line}
            if len(line_set) != 9:
                logging.info('Invalid Solution (line)')
                logging.debug('\n%s', self)
                return False

        transp_matrix = zip(*self.matrix)

        for column in transp_matrix:
            # Check for column
            column_set = {pos.value for pos in column}
            if len(column_set) != 9:
                logging.info('Invalid Solution (column)')
                logging.debug('\n%s', self)
                return False

        # Check regions
        starts = [0, 3, 6]
        regions = itertools.product(starts, starts)

        for start_i, start_j in regions:
            region_set = set()

            for i in range(start_i, start_i + 3):
                for j in range(start_j, start_j + 3):
                    region_set.add(self.matrix[i][j].value)

            if len(region_set) != 9:
                logging.info('Invalid Solution (region)')
                logging.debug('\n%s', self)
                return False

        logging.info('Valid Solution')
        return True


def parse_input(file_obj=sys.stdin):
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
            games.append(Game(matrix))
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
    optparser.add_option("--validate", dest="validade",
                         default=False, action="store_true",
                         help="Check game results")

    return optparser.parse_args()[0]


def configure_logging(options):
    if options.verbose:
        logging.root.setLevel(logging.INFO)

    if options.debug:
        logging.root.setLevel(logging.DEBUG)


def main():
    options = parse_options()
    configure_logging(options)

    games = parse_input()
    status = 0

    for i, game in enumerate(games):
        logging.info('-' * 80)
        logging.info('Game #%s', i + 1)

        if options.validade:
            if not game.is_valid():
                status = 1
        else:
            game.solve(forward_check=options.forward_check)
            print game

    return status


if __name__ == '__main__':
    sys.exit(main())
