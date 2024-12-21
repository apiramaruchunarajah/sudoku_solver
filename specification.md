
# Specification
In this document we describe how the Sudoku solver was implemented.

## 1. Sudoku puzzle representation
### 1.1 Possible values for each cell
$N^{2}$ corresponds to the length of the Sudoku.  
Each cell of the Sudoku can take a value between $1$ to $N^{2}$. This value is represented by an element from $\{1 \ldots 9\}\cup
\{A \ldots Z\}$.  
The maximum value $N_{max}$ that $N$ can take verifies $N_{max}^{2} = Z \Leftrightarrow N_{max}^{2} = 35$. This means that
we have $N_{max} < 6 \Rightarrow N_{max} = 5$.   
Therefore, in practice, the maximum value that a cell can take is $N_{max}^{2} = 5^{2} = 25$. So, in practice, the possible value that a cell can take is represented 
by an element of $\{1 \ldots 9\}\cup\{A \ldots P\}$.

### 1.2 Reduction to a SAT problem


## 2. Constraints
To solve the Sudoku puzzle, we have the following 6 constraints.
