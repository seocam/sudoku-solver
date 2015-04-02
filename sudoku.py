#!/usr/bin/env python

import sys

from pprint import pformat


class GamePosition(object):
    def __init__(self, value):
        self.value = self.initial = int(value)
        self.initial_possibilities = []
        self.possibilities = []

        if self.value > 0:
            self.fixed = True
        else:
            self.fixed = False

    def dotry(self):
        if not self.possibilities:
            return False

        self.value = self.possibilities.pop(0)
        return True

    def reset(self):
        self.value = self.initial
        self.possibilities = self.initial_possibilities[:]

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

    def get_possibilities(self, line_num, col_num):
        start_x = line_num // 3 * 3
        start_y = col_num // 3 * 3

        values = set() 
        for x in range(start_x, start_x + 3):
            for y in range(start_y, start_y + 3):
                values.add(self[x][y].value)

        line = [i.value for i in self[line_num]]
        values.update(line)

        col = [i.value for i in zip(*self)[col_num]]
        values.update(col)

        return tuple({1, 2, 3, 4, 5, 6, 7, 8, 9} - values)

    def check_line(self, line_num, col_num):
        current_value = self[line_num][col_num].value
        line = [pos.value for pos in self[line_num]]
        return line.count(current_value) <= 1

    def check_column(self, line_num, col_num):
        current_value = self[line_num][col_num].value
        column = [pos.value for pos in zip(*self)[col_num]]
        return column.count(current_value) <= 1

    def check_region(self, line, col):
        start_x = line // 3 * 3
        start_y = col // 3 * 3

        values = []
        for x in range(start_x, start_x + 3):
            for y in range(start_y, start_y + 3):
                value = self[x][y].value
                values.append(value)

        current_value = self[line][col].value
        if values.count(current_value) > 1:
            return False

        return True

    def check_position(self, line, col):
        if not self[line][col].value:
            return False

        if not self.check_region(line, col):
        #    print 'region', False
            return False
        #print 'region', True

        if not self.check_line(line, col):
        #    print 'line', False
            return False
        #print 'line', True

        if not self.check_column(line, col):
        #    print 'column', False
            return False
        #print 'column', True

        return True

    def solve(self):
        for i, line in enumerate(self):
            for j, position in enumerate(line):
                if not position.fixed:
                #    position.possibilities.append(position.value)
                #else:
                    possibilities = self.get_possibilities(i, j)
                    position.initial_possibilities.extend(possibilities)
                    position.initial_possibilities.sort()
                    position.reset()

        while(self.cur_x != -1):
        #    print '-' * 80
        #    print 'pos', self.cur_x, self.cur_y
        #    print self.current_position
        #    print self
            if self.check_position(self.cur_x, self.cur_y):
        #        print 'checked', True
                self._prev()
                self.current_position.possibilities = list(self.get_possibilities(self.cur_x, self.cur_y))
                continue
        #    print 'checked', False

        #    print self.current_position.possibilities
            changed = self.current_position.dotry()
        #    print 'depois:', self.current_position.value
            #if self.cur_y == 6 and not self.current_position.possibilities:
            #    break
            if not changed:
                self.current_position.reset()
                self._next()
                self.current_position.value = 0

    @property
    def current_position(self):
        return self[self.cur_x][self.cur_y]

    def _next(self):
        if self.cur_y == 8:
            if self.cur_x == 8:
                self._prev()
            else:
                self.cur_y = 0
                self.cur_x += 1
        else:
            self.cur_y += 1

    def _prev(self):
        if self.cur_y == 0:
            self.cur_y = 8
            self.cur_x -= 1
        else:
            self.cur_y -= 1

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


if __name__ == '__main__':
    games = parse_input()
    #for game in games:
    #    game.solve()
    #    print game
    games[0].solve()
    print games[0]
