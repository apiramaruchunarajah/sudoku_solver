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
        # This value belongs to a subset of {1-9}U{A-Z}, depending on N
        # The maximum value of N verifies max(N)² = Z <=> max(N)² = 35
        # => max(N) < 6 => max(N) = 5
        # => In practice, the maximum value a cell can take is max(N)² = 5² = 25 (=> {1-9}U{A-P})

        # Creating a N²xN²xN² matrix of boolean variables
        self.boolean_variables_matrix = [[[Bool("x_%s_%s_%s" % (i, j, k + 1))  # i+1 ? j+1 ?
                                           for k in range(int(self.N ** 2))]  # change : k+1 => k and range(1, N²) ?
                                          for j in range(int(self.N ** 2))]
                                         for i in range(int(self.N ** 2))]

        # Setting the known variables of the boolean matrix to true
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                if self.sudoku_matrix[i][j] != '0':  # if the value is known
                    if '1' <= self.sudoku_matrix[i][j] <= '9':  # if the character is in {1-9}
                        k = int(self.sudoku_matrix[i][j]) - 1  # -1 because sudoku number != index
                        self.boolean_variables_matrix[i][j][k] = Bool('True')

                    elif 'A' <= self.sudoku_matrix[i][j] <= 'Z':  # if the character is in {A-Z}
                        k = ord(self.sudoku_matrix[i][j]) - ord('A')  # no need for - 1
                        self.boolean_variables_matrix[i][j][k] = True

                    else:
                        print(
                            "Error: not '0' nor belonging to {1-9}U{A-Z}")  # After parsing we should get such a matrix
                        exit()

        print("Known matrix : " + str(self.boolean_variables_matrix))
        print("Known matrix size : " + str(len(self.boolean_variables_matrix)))

        # Constraint (C1) : every cell (i,j) has at least a value Xijk true
        constraint_1 = []
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                constraint_1.append(Or([self.boolean_variables_matrix[i][j][k]
                                        for k in range(self.N ** 2)]))
                #print("Constraint 1 : " + str(Or([self.boolean_variables_matrix[i][j][k]
                #                                  for k in range(self.N ** 2)])))

        #print("len constraint_1 : " + str(len(constraint_1)))
        constraint_1 = And(constraint_1)

        # Constraint (C2) : every cell (i,j) has at most one variable Xijk true
        constraint_2 = []
        for i in range(self.N ** 2):
            for j in range(self.N ** 2):
                constraint_2_cell_ij = []  # constraint : for the cell ij at most one var Xijk is true

                for k in range(self.N ** 2):
                    constraint_2_cell_ijk = []  # constraint : if Xijk true then Xijk' not true

                    for k_bis in range(self.N ** 2):
                        if k_bis != k:
                            constraint_2_cell_ijk.append(Or([Not(self.boolean_variables_matrix[i][j][k]),
                                                             Not(self.boolean_variables_matrix[i][j][k_bis])]))
                    constraint_2_cell_ijk = And(constraint_2_cell_ijk)  # And between Ors
                    # print("Constraint_2_cell_" + str(i) + str(j) + str(k+1) + " : " + str(constraint_2_cell_ijk))
                    constraint_2_cell_ij.append(constraint_2_cell_ijk)

                constraint_2_cell_ij = And(constraint_2_cell_ij)  # And between Ands
                # print("Constraint_2_cell_" + str(i) + str(j) + " : " + str(constraint_2_cell_ij))

                constraint_2.append(constraint_2_cell_ij)

        constraint_2 = And(constraint_2)
        # print("Constraint 2 : " + str(constraint_2))

        # Constraint (C3) : a digit from {1-N²} appears exactly once in a column
        constraint_3 = []
        for j in range(self.N ** 2):
            constraint_3_j = []  # constraint : for a column j

            for k in range(self.N ** 2):  # constraint : a value k only appears once in the column j
                constraint_3_j.append(Or([self.boolean_variables_matrix[i][j][k] for i in range(self.N ** 2)]))

            constraint_3_j = And(constraint_3_j)
            # print("constraint_3_" + str(j) + " : " + str(constraint_3_j))
            constraint_3.append(constraint_3_j)

        constraint_3 = And(constraint_3)
        print("Constraint_3 : " + str(constraint_3))

        # Solving
        s = Solver()
        s.add(constraint_1)
        s.add(constraint_2)
        s.add(constraint_3)

        if s.check() == sat:
            model = s.model()
            # Force evaluation of all cells
            solution_matrix = []
            for i in range(self.N ** 2):
                solution_matrix_line_i = []
                for j in range(self.N ** 2):
                    for k in range(self.N ** 2):
                        val = model.eval(self.boolean_variables_matrix[i][j][k])
                        already_true = False  # variable to test if only one k is true
                        if val == True:
                            if already_true:
                                print("Error : two Xijk are equal")
                                exit()
                            solution_matrix_line_i.append(k+1)

                solution_matrix.append(solution_matrix_line_i)
            self.print_matrix(solution_matrix)
            print("Len solver model : " + str(len(model)))
        else:
            print("unsat")

        # Constraint (C2)

    def print_matrix(self, solution_matrix):
        print("Solution Matrix : ")
        for i in range(self.N ** 2):
            print(solution_matrix[i])


s = SudokuSolver('../test/sudoku_puzzle_2.txt')
