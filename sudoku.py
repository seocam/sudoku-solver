#!/usr/bin/env python

import sys

import logging

DEBUG = False

if DEBUG:
    logging.root.setLevel(logging.DEBUG)


class GamePosition(object):
    def __init__(self, value):
        self.value = self.initial = int(value)
        self.possibilities = set()

        if self.value > 0:
            self.fixed = True
        else:
            self.fixed = False

    def next_try(self):
        self.value = self.possibilities.pop()

    def reset(self):
        self.value = self.initial
        self.possibilities.clear()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Game(list):
    def __init__(self, matrix):
        self.cur_x = self.cur_y = 8

        for line in matrix:
            game_line = []
            for value in line:
                game_line.append(GamePosition(value))

            self.append(game_line)

        self.current_position = self[self.cur_x][self.cur_y]

    def update_possibilities(self):
        possibilities = self.current_position.possibilities

        if self.current_position.fixed:
            possibilities.add(self.current_position.value)
            return

        start_x = self.cur_x // 3 * 3
        start_y = self.cur_y // 3 * 3

        possibilities.update({1, 2, 3, 4, 5, 6, 7, 8, 9})
        for x in range(start_x, start_x + 3):
            for y in range(start_y, start_y + 3):
                if self[x][y].value in possibilities:
                    possibilities.remove(self[x][y].value)

        # Line
        [possibilities.remove(i.value) for i in self[self.cur_x]
         if i.value in possibilities]

        # Column
        [possibilities.remove(i.value) for i in zip(*self)[self.cur_y]
         if i.value in possibilities]

    def solve(self):

        self.update_possibilities()

        while(not self.solved):
            if DEBUG:
                logging.debug('-' * 80)
                logging.debug('[%s][%s]: %s',
                              self.cur_x, self.cur_y, self.current_position)
                logging.debug('Current status\n%s', self)

                logging.debug('Possibilities %s',
                              self.current_position.possibilities)

            self.current_position.next_try()
            self.previous()
            self.update_possibilities()

            while(not self.current_position.possibilities):
                self.current_position.reset()
                self.next()
                self.current_position.value = self.current_position.initial

    @property
    def solved(self):
        if self.cur_x == self.cur_y == 0:
            return bool(self.current_position.possibilities)

    def next(self):
        if self.cur_y == 8:
            if self.cur_x == 8:
                self.cur_x = -1  # Stop Iteration
            else:
                self.cur_y = 0
                self.cur_x += 1
        else:
            self.cur_y += 1

        self.current_position = self[self.cur_x][self.cur_y]

    def previous(self):
        if self.cur_y == 0:
            self.cur_y = 8
            self.cur_x -= 1
        else:
            self.cur_y -= 1

        self.current_position = self[self.cur_x][self.cur_y]

    def __str__(self):
        game_repr = []
        for line in self:
            for position in line:
                game_repr.append(str(position))
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


def main():
    games = parse_input()
    for game in games:
        game.solve()
        print game


if __name__ == '__main__':
    main()
