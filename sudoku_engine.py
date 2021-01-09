import copy
import logging


class InvalidGridException(Exception):
    """Custom exception class for invalid grid resulting from an incorrect guess"""
    pass


class State:
    def __init__(self, solved, possibles):
        self.solved = solved
        self.possibles = possibles

    def clone(self):
        return State(copy.deepcopy(self.solved), copy.deepcopy(self.possibles))

    def is_complete(self):
        return len(self.solved) == 81

    def check_validity(self):
        # all empty cells must have some possible values
        for (i, j) in self.possibles:
            if not len(self.possibles[(i, j)]) > 1:
                raise InvalidGridException('Cell {0} has no possible value'.format((i, j)))
        # in any lines/column/square, all digits must be either in the grid of in the possibles of the pending cells
        for i in range(9):
            used = [self.solved[(i, j)] for j in range(9) if (i, j) in self.solved]
            possibles = set().union(*[self.possibles[(i, j)] for j in range(9) if (i, j) in self.possibles])
            for v in range(1, 10):
                if (v in used) == (v in possibles):
                    raise InvalidGridException('Line {0} is invalid'.format(i))
        for j in range(9):
            used = [self.solved[(i, j)] for i in range(9) if (i, j) in self.solved]
            possibles = set().union(*[self.possibles[(i, j)] for i in range(9) if (i, j) in self.possibles])
            for v in range(1, 10):
                if (v in used) == (v in possibles):
                    raise InvalidGridException('Column {0} is invalid'.format(j))
        for k in range(9):
            used = [v for v in self.square(k) if v > 0]
            possibles = set().union(*[self.possibles[(i, j)] for (i, j)
                                      in self.square_coords(k//3 * 3, (k % 3) * 3)
                                      if (i, j) in self.possibles])
            for v in range(1, 10):
                if (v in used) == (v in possibles):
                    raise InvalidGridException('Square {0} is invalid'.format(k))

    def set(self, i, j, val):
        if val in [self.solved[(x, y)] for (x, y) in self.solved if x == i and y != j]:
            raise InvalidGridException('{0} is already in line {1}'.format(val, i))
        if val in [self.solved[(x, y)] for (x, y) in self.solved if y == j and x != i]:
            raise InvalidGridException('{0} is already in column {1}'.format(val, j))
        if val in [self.solved[(x, y)] for (x, y) in self.square_coords(i, j)
                   if (x, y) in self.solved and (x, y) != (i, j)]:
            raise InvalidGridException('{0} is already in square {1}'.format(val, i//3 * 3 + j//3))
        self.solved[(i, j)] = val
        del self.possibles[(i, j)]

    def line(self, i):
        return [self.solved[(i, j)] if (i, j) in self.solved else -1 for j in range(9)]

    def column(self, j):
        return [self.solved[(i, j)] if (i, j) in self.solved else -1 for i in range(9)]

    @staticmethod
    def square_coords(i, j):
        (x, y) = (i - i % 3, j - j % 3)
        return [(x, y), (x, y + 1), (x, y + 2),
                (x + 1, y), (x + 1, y + 1), (x + 1, y + 2),
                (x + 2, y), (x + 2, y + 1), (x + 2, y + 2)]

    def square(self, k):
        coords = State.square_coords(k//3 * 3, (k % 3) * 3)
        return [self.solved[coord] if coord in self.solved else -1 for coord in coords]

    def display(self):
        res = ''
        for i in range(9):
            for j in range(9):
                res += str(self.solved[(i, j)]) if (i, j) in self.solved else '_'
                res += ' '
            res += '\n'
        return res

    @classmethod
    def initial_state(cls):
        possibles = {}
        for i in range(9):
            for j in range(9):
                possibles[(i, j)] = set(range(1, 10))
        return State({}, possibles)


class SudokuEngine:
    def __init__(self, grid):
        self.rollback_states = []
        self.state = State.initial_state()
        for (i, line) in enumerate(grid.split('\n')):
            for (j, c) in enumerate(line):
                if c != ' ':
                    self.state.set(i, j, int(c))

    def reduce_lines(self):
        # a digit can be only in one cell within a line
        moves = []
        for i in range(9):
            line = self.state.line(i)
            used = set([v for v in line if v > 0])
            if len(used) < 9:
                for j in range(9):
                    if line[j] < 0:
                        self.state.possibles[(i, j)] = self.state.possibles[(i, j)].difference(used)
                        if len(self.state.possibles[(i, j)]) == 1:
                            val = self.state.possibles[(i, j)].pop()
                            self.state.set(i, j, val)
                            used.add(val)
                            moves.append((i, j, val))
        logging.debug('Reducing lines : {0}'.format(moves))
        return moves

    def reduce_columns(self):
        # a digit can be only in one cell within a column
        moves = []
        for j in range(9):
            column = self.state.column(j)
            used = set([v for v in column if v > 0])
            if len(used) < 9:
                for i in range(9):
                    if column[i] < 0:
                        self.state.possibles[(i, j)] = self.state.possibles[(i, j)].difference(used)
                        if len(self.state.possibles[(i, j)]) == 1:
                            val = self.state.possibles[(i, j)].pop()
                            self.state.set(i, j, val)
                            used.add(val)
                            moves.append((i, j, val))
        logging.debug('Reducing columns : {0}'.format(moves))
        return moves

    def reduce_squares(self):
        # a digit can be only in one cell of a square
        moves = []
        for k in range(9):
            square = self.state.square(k)
            used = set([v for v in square if v > 0])
            if len(used) < 9:
                for x in range(3):
                    for y in range(3):
                        i, j = k//3 * 3 + x, (k % 3) * 3 + y
                        if square[x*3 + y] < 0:
                            self.state.possibles[(i, j)] = self.state.possibles[(i, j)].difference(used)
                            if len(self.state.possibles[(i, j)]) == 1:
                                val = self.state.possibles[(i, j)].pop()
                                self.state.set(i, j, val)
                                used.add(val)
                                moves.append((i, j, val))
        logging.debug('Reducing squares : {0}'.format(moves))
        return moves

    def find_single_option(self):
        # all digits from 1 to 9 must be in each line/column/square
        # if a cell is the only one of its line/column/square allowed to contain a digit, then it
        # must contain this digit
        for (i, j) in self.state.possibles:
            other_line_possibles = set()
            for y in range(9):
                if y != j and (i, y) in self.state.possibles:
                    other_line_possibles = other_line_possibles.union(self.state.possibles[(i, y)])
            other_column_possibles = set()
            for x in range(9):
                if x != i and (x, j) in self.state.possibles:
                    other_column_possibles = other_column_possibles.union(self.state.possibles[(x, j)])
            other_square_possibles = set()
            for (x, y) in State.square_coords(i, j):
                if (i, j) != (x, y) and (x, y) in self.state.possibles:
                    other_square_possibles = other_square_possibles.union(self.state.possibles[(x, y)])
            for val in self.state.possibles[(i, j)]:
                if val not in other_line_possibles or val not in other_column_possibles:
                    self.state.set(i, j, val)
                    logging.debug('Single option : {0}'.format((i, j, val)))
                    return i, j, val
        logging.debug('Single option : none')
        return None

    def solve(self):
        logging.info('Initial grid :\n' + self.state.display())
        moves = []
        while not self.state.is_complete():
            try:
                logging.debug('Current state :\n' + self.state.display())

                # add trivial value if any
                new_moves = self.reduce_lines() + self.reduce_columns() + self.reduce_squares()

                # if no trivial value, try to find a cell that is the only one able to hold a value
                if len(new_moves) == 0:
                    single_option = self.find_single_option()
                    if single_option:
                        new_moves = [single_option]

                # if we found moves, end of cycle
                if len(new_moves):
                    moves += new_moves
                    continue

                # if the state is invalid, rollback the last guess
                self.state.check_validity()

                # find the cell with the fewest possibles and take a guess
                # if we end up with an invalid grid, this guess will be rolled back
                min_possibles_len = min([len(self.state.possibles[x]) for x in self.state.possibles])
                for (i, j) in self.state.possibles:
                    if len(self.state.possibles[(i, j)]) == min_possibles_len:
                        val = self.state.possibles[(i, j)].pop()
                        logging.info('Take guess ({0}, {1}) = {2}'.format(i, j, val))
                        new_state = self.state.clone()
                        new_state.set(i, j, val)
                        self.rollback_states.append(self.state)
                        self.state = new_state
                        break

            except InvalidGridException as e:
                logging.debug(e)
                logging.info('Invalid state found, rollback last guess')
                self.state = self.rollback_states.pop()

        logging.info('Solved grid :\n' + self.state.display())


if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
    with open('sample.txt', 'r') as f:
        SudokuEngine(f.read()).solve()
