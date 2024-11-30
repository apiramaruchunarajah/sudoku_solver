from math import sqrt

class Parser:
    def __init__(self, pathname):
        # Class attributs
        self.N = 0

        # Reading the file
        with open(pathname, 'r', encoding="utf-8") as f:
            data = f.readlines()

        # Removing "\n" from the data (if statement used to remove the last (useless) cell)
        data = [line.replace("\n", "") for line in data if (line != "\n")]
        print("data : " + str(data))

        # Length of the data
        data_length = len(data)
        print("data length : " + str(data_length))

        # Size N of the Sudoku puzzle
        NN = int(data[0])
        self.N = sqrt(NN)  # TODO: check that it is a correct integer

        if (data_length != (self.N ** 2 + 1)):
            print("Error the file is not incorrect")
            exit()

        # Removing the first line - corresponding to N - from the data
        data.pop(0)
        print("Data : " + str(data))

        # Creating the instances of lines
        for line in data:  # for each line of data
            print("Line : " + str(line))
            new_line = []
            for char in line:  # for every character of the line
                match char:
                    case _ if '1' <= char <= '9':
                        new_line.append(char)
                    case _ if 'A' <= char <= 'Z':
                        new_line.append(char)
                    case '-':
                        new_line.append('0')
                    case ' ':
                        pass
                    case _:
                        print("File is not correct : expected '1-9', 'A-Z', '-' or ' '")
                        exit()

            print("New line : " + str(new_line))


# for line in data:
#     line = [char for char in line]

# line1 = [int(char) if (char != '-' and char != ' ') else 0 for char in data[1]]

parser = Parser('./test/sudoku_puzzle_1.txt')
