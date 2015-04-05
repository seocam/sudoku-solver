#!/usr/bin/env python

import sys

import logging

from optparse import OptionParser


REGION_START = {}


def get_region_start(point):
    if point not in REGION_START:
        REGION_START[point] = point // 3 * 3

    return REGION_START[point]


class GamePosition(object):
    def __init__(self, value, game, i, j):
        self.value = int(value)
        self.possibilities = []
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

    def reset(self):
        self.possibilities = []
        self.value = 0

    def update_possibilities(self):
        if self.fixed:
            self.possibilities = [self.value]
            return

        start_i = get_region_start(self.i)
        start_j = get_region_start(self.j)

        values = set()
        for x in range(start_i, start_i + 3):
            for y in range(start_j, start_j + 3):
                values.add(self.game[x][y].value)

        # Line
        [values.add(i.value) for i in self.game[self.i]]

        # Column
        [values.add(line[self.j].value) for line in self.game]

        self.possibilities = list({1, 2, 3, 4, 5, 6, 7, 8, 9} - values)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '[{}][{}] = {}'.format(self.i, self.j, self.value)


class Game(list):
    def __init__(self, matrix):
        self.available_moves = []
        self.last_moves = []

        for i, line in enumerate(matrix):
            game_line = []
            for j, value in enumerate(line):
                position = GamePosition(value, self, i, j)
                game_line.append(position)

            self.append(game_line)

        # region calc cache
        self._region_start = {}

    def log_step(self):
        logging.debug('-' * 80)

        logging.debug('Available moves (%s): %s',
                      len(self.available_moves),
                      self.available_moves)

        logging.debug('Last moves: %s', self.last_moves)

        logging.debug('Current status:\n%s', self)

        if self.current_position:
            logging.debug('Current position: %s', self.current_position)

            logging.debug('Possibilities: %s',
                          self.current_position.possibilities)
        else:
            logging.debug('Current position: n/a')

    def solve(self):
        while(self.available_moves):
            self.next()
            self.current_position.update_possibilities()

            while(not self.current_position.possibilities):
                self.current_position.reset()
                self.previous()

            self.current_position.try_next()

    def next(self):
        self.log_step()
        coordinates = self.available_moves.pop(0)
        self.last_moves.append(coordinates)

    def previous(self):
        self.log_step()
        coordinates = self.last_moves.pop()
        self.available_moves.insert(0, coordinates)

    @property
    def current_position(self):
        try:
            i, j = self.last_moves[-1]
        except IndexError:
            return

        return self[i][j]

    def __str__(self):
        game_repr = []
        for line in self:
            for position in line:
                game_repr.append(str(position.value))
                game_repr.append(' ')
            game_repr[-1] = '\n'
        return ''.join(game_repr)

    def __repr__(self):
        return str(self)


def parse_input():
    games = []

    # Skip first line
    sys.stdin.readline()

    count = 0
    matrix = []

    for str_line in sys.stdin:
        str_line = str_line.strip()

        if not str_line:
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
    for i, game in enumerate(games):
        logging.info('Game #%s', i + 1)

        game.solve()
        print game


if __name__ == '__main__':
    main()
