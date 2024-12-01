from parser import Parser
from z3 import *


class Solver:
    def __init__(self, pathname):
        # Class attributes
        self.N = 0
        self.sudoku_matrix = []
        self.boolean_variables_matrix = []

        # Getting N and the Sudoku matrix
        parser = Parser(pathname)
        self.N = parser.N
        self.sudoku_matrix = parser.sudoku_matrix
        print("Sudoku matrix : " + str(self.sudoku_matrix))

        # Each cell can take a value going from 1 to N²
        # This value belongs to a subset of {1-9}U{A-Z}, depending of N
        # The maximum value of N verifies max(N)² = Z <=> max(N)² = 35
        # => max(N) < 6 => max(N) = 5
        # => In practice, the maximum value a cell can take is 5² = 25

        # Creating a NxNxN² matrix of boolean variables
        self.boolean_variables_matrix = [[[Bool("x_%s_%s_%s" % (i + 1, j + 1, k + 1))
                                           for k in range(int(self.N**2))]
                                          for j in range(int(self.N**2))]
                                         for i in range(int(self.N**2))]
        print(str(self.boolean_variables_matrix))

solver = Solver('../test/sudoku_puzzle_1.txt')
