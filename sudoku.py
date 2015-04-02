
import sys

from pprint import pformat


class GamePosition(int):
    def __init__(self, value):
        self.value = int(value)
        self.possibilities = []
        self.tried = []

        if self.value > 0:
            self.fixed = True
        else:
            self.fixed = False

    def try(self):
        if not self.possibilities:
            return False

        self.tried.append(self.value)
        self.value = self.possibilities.pop(0)
        return True

    def reset(self):
        self.possibilities = self.tried
        self.tried = []

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

    @staticmethod
    def _alldiff(line):
        line_without_zero = [item for item in line if item != 0]
        return len(set(line_without_zero)) == len(line_without_zero)

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

    def check_line(self, line_num):
        line = self[line_num]
        return self._alldiff(line)

    def check_column(self, col_num):
        col = zip(*self)[col_num]
        return self._alldiff(col)

    def check_region(self, line, col):
        start_x = line // 3 * 3
        start_y = col // 3 * 3

        values = []
        for x in range(start_x, start_x + 3):
            for y in range(start_y, start_y + 3):
                value = self[x][y]
                if not value:
                    continue

                if value in values:
                    return False

                values.append(value)

        return True

    def check_position(self, line, col):
        if not self.check_region(line, col):
            return False

        if not self.check_line(line):
            return False

        if not self.check_column(col):
            return False

        return True

    def solve(self):

        for i, line in enumerate(self):
            for j, position in enumerate(line):
                if position.fixed:
                    position.possibilities.append(position.value)
                else:
                    possibilities = self.get_possibilities(i, j)
                    position.possibilities.extend(possibilities)
                    position.possibilities.sort()

                position.try()

        self._back = True
        while(self.cur_x != -1):
            if position.check_position(cur_x, cur_y):
                if self._back:
                    self._prev()
                else:
                    self._next()
                continue

            changed = self.try()
            if not changed:
                self._back = False
                position.reset()
                self._prev()


    def _next(self):
        if self.cur_y == 8:
            if self.cur_x == 8:
                self._prev()
                self._back = True
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
    games[0].solve()
    print games[0]
