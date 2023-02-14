# -*- coding: utf-8 -*-
#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
from collections import defaultdict
import time
import statistics as stat

ROW = "ABCDEFGHI"
COL = "123456789"
subgroupsROW ={"A":["A","B","C"], "B": ["A","B","C"], "C": ["A","B","C"], "D":["D","E","F"], "E":["D","E","F"], "F":["D","E","F"],
               "G": ["G","H","I"], "H": ["G","H","I"], "I": ["G","H","I"]}
subgroupsCOL ={"1":["1","2","3"], "2": ["1","2","3"], "3": ["1","2","3"], "4":["4","5","6"], "5":["4","5","6"], "6":["4","5","6"],
               "7": ["7","8","9"], "8": ["7","8","9"], "9": ["7","8","9"]}
               


row_item_count = defaultdict(int)
col_item_count = defaultdict(int)


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def wincondition(board):

  if 0 in board.values():
    return False

  # check row values

  for r in ROW:
    row = set([ board[r+c] for c in COL])
    if len(row) != 9 or sum(row) != 45:
      return False

  # check column values 
  for c in COL:
    col = set([ board[r+c] for r in ROW])
    if len(col) != 9 or sum(col) != 45:
      return False

  # check ninth values
  for r in ROW:
    for c in COL:
      ninth = set(())
      for sr in subgroupsROW:
        for sc in subgroupsCOL:
          ninth.add(board[sr+sc])
      if len(ninth) != 9 or sum(ninth) != 45:
        return False
  
  return True

def mrv(board):
  ric = sorted(row_item_count.items(), key=lambda x: x[1], reverse=True)
  cic = sorted(col_item_count.items(), key=lambda x: x[1], reverse=True)

  for r in ric:
    for c in cic:
      if board[r[0]+c[0]] == 0:
        return str(r[0]+c[0])

  rawvars = [ var for var,value in board.items() if value == 0 ]
  if len(rawvars) == 1:
    return rawvars[0]

  #print_board(board)
  #print(rawvars)
  #print(ric)
  #print(cic)
  return ":("

def lcv(target, board):
  t_r = target[0]
  t_c = target[1]
  
  rowvars = [ i for i in range(1,10) if i not in [board[t_r+c] for c in COL]]
  colvars = [ i for i in range(1,10) if i not in [board[r+t_c] for r in ROW]]
  ninthvars = [ i for i in range(1,10) if i not in [board[sr+sc] for sr in subgroupsROW[t_r] for sc in subgroupsCOL[t_c]]]

  finalvars = [num for num in rowvars if num in colvars and num in ninthvars]
    
  return finalvars

def backtracking(board):
    """Takes a board and returns solved board."""
    if wincondition(board):
      return board

    var = mrv(board) # returns string of the variable's key
    if var == ":(":
      return False

    for value in lcv(var, board): # returns all valid values for the variable -- combines domain order and consistent
      board[var] = value
      row_item_count[var[0]] += 1
      col_item_count[var[1]] += 1

      #xprint(board_to_string(board))
      result = backtracking(board)

      if result != False:
        return result

      board[var] = 0
      row_item_count[var[0]] -= 1
      col_item_count[var[1]] -= 1

    return False

if __name__ == '__main__':
    number_solved = 0 
    runtime_times = []

    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        #print(sys.argv[1])
        
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}      

        row_item_count = defaultdict(int)
        col_item_count = defaultdict(int)

        for c in COL:
          col_item_count[c] = 0
        for r in ROW:
          row_item_count[r] = 0
          for c in COL:
            if board[r+c] != 0:
              row_item_count[r] +=1 
              col_item_count[c] +=1


        #print("as a board: ")
        #print_board(board)

        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            start = 0
            end = 0

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            # Solve with backtracking
            start = time.time()

            row_item_count = defaultdict(int)
            col_item_count = defaultdict(int)

            for c in COL:
              col_item_count[c] = 0
            for r in ROW:
              row_item_count[r] = 0
              for c in COL:
                if board[r+c] != 0:
                  row_item_count[r] +=1 
                  col_item_count[c] +=1

            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.

            #print_board(solved_board)
            end = time.time()
            number_solved +=1
            runtime_times.append(abs(end-start))

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        #print("Finishing all boards in file.")

        o_filename = 'README.txt'
        ofile = open(o_filename, "w")
        ofile.write("Number of Boards Solved: " + str(number_solved)+"\n")
        ofile.write("Runtime Statistics:\n")
        ofile.write("Min Solution Time: " + str(min(runtime_times))+"\n")
        ofile.write("Max Solution Time: " + str(max(runtime_times))+"\n")
        ofile.write("Mean Solution Time: " + str(sum(runtime_times)/len(runtime_times))+"\n")
        ofile.write("Standard Deviation: " + str(stat.pstdev(runtime_times))+"\n")

      