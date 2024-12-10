import sys
from src.sudokusolver import SudokuSolver

# Check if an argument is provided
if len(sys.argv) > 1:
    pathname = sys.argv[1]
else:
    print("No arguments were provided.")
    exit()

# Solve the Sudoku
sudokuSolver = SudokuSolver(pathname)
print(f"Solving the sudoku {pathname} ...")
sudokuSolver.solve()
