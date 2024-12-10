import sys
from src.sudokusolver import SudokuSolver

# Check if an argument is provided
if len(sys.argv) > 1:
    pathname = sys.argv[1]  # First argument after the script name
else:
    print("No arguments were provided.")
    exit()

sudokuSolver = SudokuSolver(pathname)
print(f"Solving for the sudoku : {pathname} ...")
sudokuSolver.solve()
