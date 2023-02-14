# AI Homework 1:

This assignment was to utilize simple search mechanisms to solve
a slide puzzle. 

The N-puzzle (typically 8-puzzle) consists of a board holding N = m^2 
distint moveable tiles plus one empty space in an N+1 sized grid. There
is one tile for each number in the set, representing its intended position
on the grid, with the empty space in the top left position.

### Solved Puzzle:

0	1	2

3	4	5

6	7	8


Each move is executed by swapping a tile with the empty space to eventually
resolve the scrambled puzzle.

### Sample Move:

0	1	2	-->	*1*	*0*	 2

3	4	5	-->	 3	 4	 5

6	7	8	-->	 6	 7	 8

 
This assignment had us design puzzle.py such that implements 3 types of search:
breadth-first, depth-first, and A-star to solve the puzzles. It outputs the
path taken by the empty square to rearrange the tiles, the cost or number of 
moves taken, the number of nodes expanded (neighbors added to the search
frontier), search depth of the final solution, and the maximum depth explored.
