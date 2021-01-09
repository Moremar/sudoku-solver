# Python sudoku solver

### Solver main idea
The solver uses a pretty simple logic : each empty cell stores the digits it could potentially contain (initially all digits from 1 to 9).

By applying some simple rules, the solver eliminates one by one the invalid digits from the lists.
When only one digit is still possible in a cell, then it is the correct digit.


### Solver rules
The rules used by the solver to eliminate invalid digits are :
 * All numbers already present in a line/column/square cannot appear a second time in the same line/column/square.
 * If a cell in a line/column/square is the only one in this line/column/square still allowed to contain a given digit, then it must contains it.

Some harder grids have too little initial information to be solved only with the above 2 rules.
   
When that happens, the solver finds the cell with the smallest number of potential digits (ideally 2), takes a random guess among these values, and continues the resolution assuming it is the correct value.
If the guess was correct, perfect. Otherwise, the resolution will result to an invalid grid, so the solver will rollback to the state before the guess and eliminate the guessed value from the potential digits in this cell.