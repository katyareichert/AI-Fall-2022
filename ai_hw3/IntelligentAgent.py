from BaseAI import BaseAI
from Grid import Grid
from Displayer  import Displayer

import time
import math
import bisect

##   RETURNS:
# 0: UP
# 1: DOWN
# 2: LEFT
# 3: RIGHT

class IntelligentAgent:

    max_rec = 4

   ### WHEN TO STOP FUNCTION -----------------------------------------------------------------------------
    def terminal_test(self, d):
        return d == self.max_rec

    ### GRID SCORING FUNCTION -----------------------------------------------------------------------------
    def grid_score(self, grid:Grid):

        # Heuristic 1: Monotonicity -- idea taken from the StackOverflow linked on the spec
        # https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048

        row_direction = [0, 0]
        col_direction = [0, 0]

        for row in grid.map:
            i = 0
            j = 1
            while j<4:
                while j<grid.size-1 and not row[j]:
                    j += 1

                current_val = 0
                if row[i]:
                    current_val = math.log2(row[i])
                next_val = 0
                if row[j]:
                    next_val = math.log2(row[j])

                if current_val > next_val:
                    row_direction[0] += next_val - current_val
                elif next_val > current_val:
                    row_direction[1] += current_val - next_val

                i=j
                j += 1

        for col_num in range(grid.size):
            i = 0
            j = 1
            while j<4:
                while j<grid.size-1 and not grid.map[j][col_num]:
                    j += 1

                current_val = 0
                if grid.map[i][col_num]:
                    current_val = math.log2(grid.map[i][col_num])
                next_val = 0
                if grid.map[j][col_num]:
                    next_val = math.log2(grid.map[j][col_num])

                if current_val > next_val:
                    col_direction[0] += next_val - current_val
                elif next_val > current_val:
                    col_direction[1] += current_val - next_val

                i=j
                j += 1

        h1 = max(row_direction) + max(col_direction)

        # Heuristic 2: Adjacency of Matching Tiles
        h2 = 0 
        for row in grid.map:
            for x, y in zip(row[0::], row[1::]):
                if x and y:
                    h2 -= abs(y-x)

        for i in range(grid.size-1):
            Col = [row[i] for row in grid.map]
            for x, y in zip(Col[0::], Col[1::]):
                if x and y:
                    h2 -= abs(y-x)

        h2 /= 2048*4


        # Heuristic 3: Open Spaces 
        h3 = 0
        for row in grid.map:
            for tile in row:
                if not tile:
                    h3 += 1
        h3 /= 16

        # Heuristic 4: Largest Tile
        h4 = 0
        val = grid.getMaxTile()
        if grid.map[0][0] == val or grid.map[0][3] == val or grid.map[3][0] == val or grid.map[3][3] == val:
            h4 = 2

        # Get weighted sum of all the heuristics
        w1 = 2          # 1. Monotonicity
        w2 = 15         # 2. Adjacency of Matching Tiles
        w3 = 2          # 3. Empty tiles
        w4 = 2.5        # 4. Max tile position

        return w1*h1 + w2*h2 + w3*h3 + h4*w4


    ### MINIMIZE FUNCTION -----------------------------------------------------------------------------
    def minimize(self, state:tuple, tile_value:int, alpha, beta, depth):
        (move, grid) = state
        if self.terminal_test(depth):
            h = self.grid_score(grid)
            return (state, h)
        (min_child, min_utility) = (None, 99999999999999)
        
        # for all open positions on the board
        for cell in grid.getAvailableCells():
            grid.setCellValue(cell, tile_value)
            (new_state, utility) = self.maximize((move, grid), alpha, beta, depth +1)

            if utility < min_utility:
                (min_child, min_utility) = (new_state, utility)

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

            grid.setCellValue(cell, 0)
                    
        return (min_child, min_utility)


    ### MAXIMIZE FUNCTION -----------------------------------------------------------------------------
    def maximize(self, state:tuple, alpha, beta, depth):
        (move, grid) = state
        if self.terminal_test(depth):
            h = self.grid_score(grid)
            return ((move, grid), h)
        (max_child, max_utility) = (None, -99999999999999)

        # get all possible Player AI moves
        
        for direction in reversed(grid.getAvailableMoves()):
            (new_state, utility) = self.expecti(direction, alpha, beta, depth+1)

            if utility > max_utility:
                (max_child, max_utility) = (new_state, utility)

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return (max_child, max_utility)


    ### EXPECTI FUNCTION -----------------------------------------------------------------------------
    def expecti(self, state:tuple, alpha, beta, depth):
        """ Game AI returns 2 with probability 0.9 and 4 with 0.05 """
        h = min(0.9 * self.minimize(state, 2, alpha, beta, depth)[1], 0.1 * self.minimize(state, 4, alpha, beta, depth)[1])
        return (state, h )


    ### MAIN() -- GETMOVE FUNCTION -------------------------------------------------------------------
    def getMove(self, grid:Grid):
        self.rec_counter=0
        self.displayer  = Displayer()
        self.prevTime = time.process_time()
        ((best_move, state), utility) = self.maximize((-1, grid), -999999999999999, 9999999999999999, 0)
        return best_move