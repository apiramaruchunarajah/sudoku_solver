from math import sqrt


class Parser:
    def __init__(self, pathname):
        # Class attributes
        self.N = 0

        # Reading the file
        with open(pathname, 'r', encoding="utf-8") as f:
            data = f.readlines()

        # Removing "\n" from the data (if statement used to remove the last (useless) cell)
        data = [line.replace("\n", "") for line in data if (line != "\n")]
        # print("data : " + str(data))

        # Size N of the Sudoku puzzle
        try:
            NN = int(data[0])
        except ValueError:
            print("Error: the first data_line isn't correct")
            exit()

        self.N = sqrt(NN)  # TODO: check that it is a correct integer

        if len(data) != (self.N ** 2 + 1):
            print("Error the file is not incorrect")
            exit()

        # Removing the first data_line - corresponding to N - from the data
        data.pop(0)
        print("Data : " + str(data))

        # Creating the sudoku matrix
        self.sudoku_matrix = []
        for data_line in data:  # for each data_line of data
            sudoku_line = []
            for char in data_line:  # for every character of the data_line
                match char:
                    case _ if '1' <= char <= '9':
                        sudoku_line.append(char)
                    case _ if 'A' <= char <= 'Z':
                        sudoku_line.append(char)
                    case '-':
                        sudoku_line.append('0')
                    case ' ':
                        pass  # we do nothing if we find a
                    case _:
                        print("File is not correct : expected '1-9', 'A-Z', '-' or ' '")
                        exit()

            # Checking that the length of the data_line is correct regards to N
            # <=> Checking that we have the correct number of columns for each line
            if len(sudoku_line) != (self.N ** 2):
                print("Error a data_line doesn't contain the correct number of values <=> "
                      "incorrect number of columns")
                exit()

            self.sudoku_matrix.append(sudoku_line)

        # Checking that the sudoko matrix has the correct number of lines
        # print("Sudoku matrix : " + str(self.sudoku_matrix))
        if len(self.sudoku_matrix) != (self.N ** 2):
            print("Error: incorrect number of lines")
            exit()

    def getSudokuMatrix(self):
        return self.sudoku_matrix

    def getN(self):
        return self.N
