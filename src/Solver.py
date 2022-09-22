import random
import itertools
import collections
import time


# A class representing a node of the solver class
class Node:

    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        if (self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    # Returns the perceived value of current state for the A* search
    @property
    def score(self):
        return self.g + self.h

    @property
    def state(self):
        return str(self)

    #path from root
    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        # Check if 'puzzle' is solved
        return self.puzzle.is_solved()

    @property
    def actions(self):
        return self.puzzle.get_actions()

    @property
    def h(self):

        return self.puzzle.manhattan()

    @property
    def f(self):

        return self.h + self.g



class Solver:

    def __init__(self, start):
        self.start = start

    # Solve using A* search
    def solve(self):
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
            node = queue.popleft()
            if node.solved:
                return node.path

            for move, action in node.actions:
                child = Node(move(), node, action)

                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

# Class of the layout of the board in the form of 2d array
class Puzzle:

    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    def is_solved(self):
        N = self.width * self.width

        # Convert layout to str then compare if it equals str of 1-15 with 0 at the end
        return str(self) == ''.join(map(str, range(1,N))) + '0'

    # Return list of legal moves
    def get_actions(self):
        def create_move(at, to):
            return lambda: self._move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'left':(i, j-1),
                      'right':(i, j+1),
                      'up':(i-1, j),
                      'down':(i+1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                   self.board[r][c] == 0:
                    move = create_move((i,j), (r,c)), action
                    moves.append(move)
        return moves

    # Calculates the manhattan distance from current state to solved state
    def manhattan(self):
        distance = 0
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j]-1, self.width)
                    distance += abs(x - i) + abs(y - j)
        return distance


    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    # executes a move by swapping a tile with 0/empty tile
    def _move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy


    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row

