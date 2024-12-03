from parser import Parser
from z3 import *


class SudokuSolver:
    def __init__(self, pathname):
        # Class attributes
        self.N = 0  # size of the Sudoku puzzle
        self.sudoku_matrix = []  # matrix where the cells are characters belonging to a subset of {1-9}U{A-Z}U{0}
        self.boolean_variables_matrix = []  # matrix where the cells are booleans

        # Getting N and the Sudoku matrix
        parser = Parser(pathname)
        self.N = int(parser.N)
        self.sudoku_matrix = parser.sudoku_matrix
        print("Sudoku matrix : " + str(self.sudoku_matrix))

        # Each cell can take a value going from 1 to N²
        # This value belongs to a subset of {1-9}U{A-Z}, depending of N
        # The maximum value of N verifies max(N)² = Z <=> max(N)² = 35
        # => max(N) < 6 => max(N) = 5
        # => In practice, the maximum value a cell can take is max(N)² = 5² = 25

        # Creating a N²xN²xN² matrix of boolean variables
        self.boolean_variables_matrix = [[[Bool("x_%s_%s_%s" % (i, j, k + 1))  # i+1 ? j+1 ?
                                           for k in range(int(self.N ** 2))]
                                          for j in range(int(self.N ** 2))]
                                         for i in range(int(self.N ** 2))]

        # Setting the known variables of the boolean matrix to true
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                if self.sudoku_matrix[i][j] != '0':  # if the value is known
                    if '1' <= self.sudoku_matrix[i][j] <= '9':  # if the character is in {1-9}
                        k = int(self.sudoku_matrix[i][j]) - 1  # -1 because sudoku number != index
                        self.boolean_variables_matrix[i][j][k] = True

                    elif 'A' <= self.sudoku_matrix[i][j] <= 'Z':  # if the character is in {A-Z}
                        k = ord(self.sudoku_matrix[i][j]) - ord('A')  # no need for - 1
                        self.boolean_variables_matrix[i][j][k] = True

                    else:
                        print("Error: not '0' nor belonging to {1-9}U{A-Z}")
                        exit()

        print("Known matrix : " + str(self.boolean_variables_matrix))

        # Constraint (C1) : every cell (i,j) has at least a value Xijk true
        constraint_1 = []
        for i in range(self.N ** 2 - 1):
            for j in range(self.N ** 2 - 1):
                constraint_1.append(Or([self.boolean_variables_matrix[i][j][k]
                                        for k in range(1, self.N ** 2)]))

        constraint_1 = And(constraint_1)
        print("Constraint 1 : " + str(constraint_1))

        solver = Solver()
        solver.add(constraint_1)
        if solver.check() == sat:
            print(solver.model())
        else:
            print("unsat")

        # Constraint (C2)


solver = SudokuSolver('../test/sudoku_puzzle_1.txt')
