
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

## 2. Reducing to a SAT problem
We want to create a boolean formula representing the Sudoku problem such that solving it also solves the Sudoku problem.   
This boolean formula will then be solved using the Z3 solver.
### 2.1 Defining boolean variables
We denote by $cell_{i,j}$ the cell located at the $i$th line and the $j$th column of the Sudoku.  
For each cell, we have $N^{2}$ boolean variables, denoted $cell_{i,j,k}$ for $k \in \{1, \ldots, N^{2}\}$.  
$cell_{i,j,k} = true$ means that the cell $cell_{i,j}$ has for value $k$.  
In total, we therefore have $N^{2} \times N^{2} \times N^{2}$ boolean variables $cell_{i,j,k}$.


### 2.2 Defining constraints
To solve the Sudoku puzzle, the boolean variables have to verify the following 6 constraints.
#### 2.2.1 Constraint C0
