# AI Homework 1:

This assignment was to utilize simple search mechanisms to solve
a slide puzzle. 

The N-puzzle (typically 8-puzzle) consists of a board holding N = m^2 
distint moveable tiles plus one empty space in an N+1 sized grid. There
is one tile for each number in the set, representing its intended position
on the grid, with the empty space in the top left position.

### Solved Puzzle:

![IMG_0443E1B12DD2-1](https://user-images.githubusercontent.com/98239413/218753889-4507a410-9cf8-4c80-abb1-ac6e769c2e67.jpeg)

Each move is executed by swapping a tile with the empty space to eventually
resolve the scrambled puzzle.

### Sample Move:

Note that the moves are identified by the direction the *empty tile* moves, 
as this is simpler than tracking which pictured tile is being moved each time.

![IMG_1316](https://user-images.githubusercontent.com/98239413/218755129-d51af555-1473-46f2-a8fb-b8a4adc14839.jpg)
 
This assignment had us design puzzle.py such that implements 3 types of search:
breadth-first, depth-first, and A-star to solve the puzzles. It outputs the
path taken by the empty square to rearrange the tiles, the cost or number of 
moves taken, the number of nodes expanded (neighbors added to the search
frontier), search depth of the final solution, and the maximum depth explored.
