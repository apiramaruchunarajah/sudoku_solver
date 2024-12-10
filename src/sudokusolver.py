from parser import Parser
from z3 import *


class SudokuSolver:
    def __init__(self, pathname):
        # Class attributes
        self.N = 0  # size of the Sudoku puzzle
        self.sudoku_matrix = []  # matrix where the cells are characters belonging to a subset of {1-9}U{A-Z}U{0}
        self.boolean_variables_matrix = []  # matrix where the cells are booleans

        # Parsing the input file
        parser = Parser(pathname)
        self.N = int(parser.N)
        self.sudoku_matrix = parser.sudoku_matrix

        # Each cell can take a value going from 1 to N²
        # This value belongs to a subset of {1-9}U{A-Z}, depending on N
        # The maximum value of N verifies max(N)² = Z <=> max(N)² = 35
        # => max(N) < 6 => max(N) = 5
        # => In practice, the maximum value a cell can take is max(N)² = 5² = 25 (=> {1-9}U{A-P})

        # Creating a N²xN²xN² matrix of boolean variables
        self.boolean_variables_matrix = [[[Bool("x_%s_%s_%s" % (i, j, k + 1))
                                           for k in range(int(self.N ** 2))]
                                          for j in range(int(self.N ** 2))]
                                         for i in range(int(self.N ** 2))]

    # Constraint (C0) : some cells have a known value that can not be changed
    def get_constraint_0(self):
        constraint_0 = []
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                if self.sudoku_matrix[i][j] != '0':  # if the value is known
                    if '1' <= self.sudoku_matrix[i][j] <= '9':  # if the character is in {1-9}
                        k = int(self.sudoku_matrix[i][j]) - 1  # -1 because sudoku number != index
                        constraint_0.append(self.boolean_variables_matrix[i][j][k] == True)

                    elif 'A' <= self.sudoku_matrix[i][j] <= 'Z':  # if the character is in {A-Z}
                        k = ord(self.sudoku_matrix[i][j]) - ord('A')  # no need for - 1
                        constraint_0.append(self.boolean_variables_matrix[i][j][k] == True)

                    else:
                        print(
                            "Error: not '0' nor belonging to {1-9}U{A-Z}")  # After parsing we should get such a matrix
                        exit()

        return constraint_0

    # Constraint (C1) : every cell (i,j) has at least a variable ijk which is true
    def get_constraint_1(self):
        constraint_1 = []
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                constraint_1.append(Or([self.boolean_variables_matrix[i][j][k]
                                        for k in range(self.N ** 2)]))

        constraint_1 = And(constraint_1)
        return constraint_1

    # Constraint (C2) : every cell (i,j) has at most one variable ijk which is true
    def get_constraint_2(self):
        constraint_2 = []
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                constraint_2_cell_ij = []  # constraint : for the cell ij, at most one variable ijk is true

                for k in range(self.N ** 2):
                    constraint_2_cell_ijk = []  # constraint : for the cell ij, if ijk is true then ijk' is not true
                    for k_prime in range(self.N ** 2):
                        if k_prime != k:
                            constraint_2_cell_ijk.append(Or([Not(self.boolean_variables_matrix[i][j][k]),
                                                             Not(self.boolean_variables_matrix[i][j][k_prime])]))

                    constraint_2_cell_ijk = And(constraint_2_cell_ijk)  # And between Ors
                    constraint_2_cell_ij.append(constraint_2_cell_ijk)

                constraint_2_cell_ij = And(constraint_2_cell_ij)  # And between Ands
                constraint_2.append(constraint_2_cell_ij)

        constraint_2 = And(constraint_2)
        return constraint_2

    # Constraint (C3) : every digit from {1-N²} appears in each column
    def get_onstraint_3(self):
        constraint_3 = []
        for j in range(self.N ** 2):
            constraint_3_j = []  # constraint : for the column j, every digit from {1-N²} appears

            for k in range(self.N ** 2):  # for each value k, there is a line i where k appears
                constraint_3_j.append(Or([self.boolean_variables_matrix[i][j][k] for i in range(self.N ** 2)]))

            constraint_3_j = And(constraint_3_j)
            constraint_3.append(constraint_3_j)

        constraint_3 = And(constraint_3)
        return constraint_3

    # Constraint (C4) : every digit from {1-N²} appears in each line
    def get_constraint_4(self):
        constraint_4 = []
        for i in range(self.N ** 2):
            constraint_4_i = []  # constraint : for the line i, every digit from {1-N²} appears

            for k in range(self.N ** 2):  # for each value k, there is a column j where k appears
                constraint_4_i.append(Or([self.boolean_variables_matrix[i][j][k] for j in range(self.N ** 2)]))

            constraint_4_i = And(constraint_4_i)
            constraint_4.append(constraint_4_i)

        constraint_4 = And(constraint_4)
        return constraint_4

    # Sub-constraint (C5) : every digit from {1-N²} appears in a given sub-square
    def get_constraint_5_for_a_sub_square(self, squareLeftTopCell_i, squareLeftTopCell_j):
        constraint_5_sub_square = []
        for k in range(self.N ** 2):
            constraint_5_sub_square_k = []  # constraint : the value k appears in the sub-square

            for i in range(squareLeftTopCell_i, squareLeftTopCell_i + self.N):
                for j in range(squareLeftTopCell_j, squareLeftTopCell_j + self.N):
                    constraint_5_sub_square_k.append(self.boolean_variables_matrix[i][j][k])

            constraint_5_sub_square_k = Or(constraint_5_sub_square_k)
            constraint_5_sub_square.append(constraint_5_sub_square_k)

        constraint_5_sub_square = And(constraint_5_sub_square)
        return constraint_5_sub_square

    # Constraint (C5) : every digit from {1-N²} appears in each sub-square
    def get_constraint_5(self):
        constraint_5 = []

        i = 0
        j = 0
        while i < self.N ** 2:
            while j < self.N ** 2:
                constraint_5.append(self.get_constraint_5_for_a_sub_square(i, j))
                j += self.N

            j = 0
            i += self.N

        constraint_5 = And(constraint_5)
        return constraint_5

    # Solves the sudoku and prints its solution if any
    def solve(self):
        # Constraints C0 to C5
        constraint_0 = self.get_constraint_0()
        constraint_1 = self.get_constraint_1()
        constraint_2 = self.get_constraint_2()
        constraint_3 = self.get_onstraint_3()
        constraint_4 = self.get_constraint_4()
        constraint_5 = self.get_constraint_5()

        # Z3 solver
        s = Solver()
        s.add(constraint_0)
        s.add(constraint_1)
        s.add(constraint_2)
        s.add(constraint_3)
        s.add(constraint_4)
        s.add(constraint_5)

        if s.check() == sat:
            model = s.model()
            solution_matrix = self.get_solution_matrix(model)
            self.printMatrix(solution_matrix)
        else:
            print("unsat")

    # Returns the solution matrix
    def get_solution_matrix(self, model):
        # Evaluation of all cells
        solution_matrix = []

        for i in range(self.N ** 2):
            solution_matrix_line_i = []  # line i of the solution matrix
            for j in range(self.N ** 2):

                already_true = False  # variable to test if only one k is true for the cell ij
                for k in range(self.N ** 2):
                    val = model.eval(self.boolean_variables_matrix[i][j][k])
                    if val == True:
                        if already_true:
                            print("Error : the model gives two values for k for one cell ij")
                            exit()
                        else:
                            solution_matrix_line_i.append(k + 1)
                            already_true = True

            solution_matrix.append(solution_matrix_line_i)
        return solution_matrix

    # Prints the solution matrix
    def print_solution(self, solution_matrix):
        print("Solution : ")
        print(self.N ** 2)
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                print(solution_matrix[i][j], end='')
                if j % self.N == self.N - 1:
                    print(" ", end='')
            print("")
            if i % self.N == self.N - 1:
                print("")


sudokuSolver = SudokuSolver('../test/sudoku_puzzle_9x9_2.txt')
sudokuSolver.solve()
