
# User manual

## 🚀 Solving a Sudoku puzzle

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/apiramaruchunarajah/sudoku_solver.git
   cd sudoku_solver
   ```

2. Execute the solver:

   ```bash
   python3 main.py path_to_puzzle
   ```

---
## 🧪 Testing the solver
### Provided Sudoku puzzles
You can find in the folder `/puzzles/` some Sudoku puzzles that you can use to test the solver. The puzzles are of 
different size and difficulty.  

It is to be noted that the puzzle **sudoku_16x16_2_difficult** takes a lot of time to be solved (~15min on my 
computer).

### Test example
#### Command line
   ```bash
    python3 main.py puzzles/sudoku_9x9_1
   ```

#### Expected response
   ```bash
    Solving the sudoku puzzles/sudoku_9x9_1 ...
    sat, solution : 
    9
    754 139 628 
    829 465 713 
    361 287 945 
    
    632 874 591 
    948 521 367 
    175 396 284 
    
    287 943 156 
    416 752 839 
    593 618 472 
   ```

---
