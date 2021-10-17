# Sudoku Solver

This program is a command-line sudoku solver.  
It accepts as input a file with the sudoku grid to solve and calculates the solution for this grid.

### Solver rules

The solver tracks the list of potential digits (1 to 9 initially) for each empty cell.  
Using some simple rules, it will eliminate some of those digits until it finds the correct one :

 * A digit already present in a line/column/square cannot appear a second time in the same line/column/square.
 * If a cell is the only one in its line/column/square still allowed to contain a given digit, then it must contain it.
 
These 2 rules are enough to solve most easy/medium sudoku grids, but harder grids usually require a bit more work.  
When these 2 rules no longer generate new results, the solver finds the cell with the smallest list of potential digits (ideally 2) and takes a random guess among these values.   
If the guess was correct, it will get closer to the right solution.  
Otherwise, it will lead to an invalid grid, so the solver will rollback to the state before the guess and take a different guess.

### Usage

The solver can be ran from the command line with :
```
python ./sudoku_engine.py --input <sudodu_grid.txt> [--debug]
```

It will print the initial grid and the result.  
It can also print the calculation steps if the `--debug` flag was used.