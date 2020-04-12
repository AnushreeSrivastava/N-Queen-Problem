from random import randrange
from copy import deepcopy

# Take number of queens as Input from the user
N = int(input('Enter the number of Queens:\n'));


# Initialize the class for board and its attributes
class QueensState:
    instance_counter = 0

    # class queenstate initialization
    def __init__(self, queen_positions=None, queen_num=N, parent=None, path_cost=0, f_cost=0, side_length=N):
        self.side_length = side_length
        if queen_positions is None:
            self.queen_num = queen_num
            self.queen_positions = frozenset(self.random_queen_position())
        else:
            self.queen_positions = frozenset(queen_positions)
            self.queen_num = len(self.queen_positions)

        self.path_cost = 0
        self.f_cost = f_cost
        self.parent = parent
        self.id = QueensState.instance_counter
        QueensState.instance_counter += 1

    # Set all N queens at random position on the board
    # Returns list of tuples with the queen coordinates
    def random_queen_position(self):
        # Each queen is placed in a random row in a separate column
        open_columns = list(range(self.side_length))
        queen_positions = [(open_columns.pop(randrange(len(open_columns))), randrange(self.side_length)) for _ in
                           range(self.queen_num)]
        return queen_positions

    # Returns all the possible moves(children) of the current state
    def get_children(self):
        children = []
        parent_queen_positions = list(self.queen_positions)
        for queen_index, queen in enumerate(parent_queen_positions):
            new_positions = [(queen[0], row) for row in range(self.side_length) if row != queen[1]]
            for new_position in new_positions:
                queen_positions = deepcopy(parent_queen_positions)
                queen_positions[queen_index] = new_position
                children.append(QueensState(queen_positions))
        return children

    # Returns number of attacking pairs of queen
    def queen_attacks(self):

        def range_between(a, b):
            if a > b:
                return range(a - 1, b, -1)
            elif a < b:
                return range(a + 1, b)
            else:
                return [a]

        def zip_repeat(a, b):
            if len(a) == 1:
                a = a * len(b)
            elif len(b) == 1:
                b = b * len(a)
            return zip(a, b)

        # Finds all the points in between two points
        def points_between(a, b):
            return zip_repeat(list(range_between(a[0], b[0])), list(range_between(a[1], b[1])))

        # Checks if the two pair of coordinates(2 queens) are attacking each other or not,
        # also checks if there are queens in between which are also in attacking position
        # Returns True/False
        def is_attacking(queens, a, b):
            if (a[0] == b[0]) or (a[1] == b[1]) or (abs(a[0] - b[0]) == abs(a[1] - b[1])):
                for between in points_between(a, b):
                    if between in queens:
                        return False
                return True
            else:
                return False

        attacking_pairs = []
        queen_positions = list(self.queen_positions)
        left_to_check = deepcopy(queen_positions)
        while left_to_check:
            a = left_to_check.pop()
            for b in left_to_check:
                if is_attacking(queen_positions, a, b):
                    attacking_pairs.append([a, b])
        # Returns length of all the attacking pairs
        return len(attacking_pairs)

    def __str__(self):
        return '\n'.join([' '.join(['.' if (col, row) not in self.queen_positions else 'Q' for col in range(
            self.side_length)]) for row in range(self.side_length)])

# Initializing the N queen problem
class QueensProblem:

    def __init__(self, start_state=None):
        if not start_state:
            start_state = QueensState()
        self.start_state = start_state

    # Goal is reached if no queen is attacking each other
    def goal_test(self, state):
        return state.queen_attacks() == 0

    # Calculating heuristic by checking how many queens are attacked by each other
    def Calculate_heuristic(self, state):
        return state.queen_attacks()
