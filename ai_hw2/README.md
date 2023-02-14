# AI Homework 2:

This assignment was to create an agent to solve 9x9 sudoku puzzles by implementing CSP techniques.

The solution algorithm implements backtracking search, using the minimum remaining value heuristic
and forward checking to reduce variable domains. 

### Board encoding

Each sudoku board is input as a single string of 9^9 integers [0-9], where 0 represents the blank spaces.

### Program execution 

The program is to be executed as:

$ python3 sudoku.py <input string>

to run on a single puzzle, or as:

$ python3 sudoku.py

to run on all the puzzles in the sudokus_start.txt file.

