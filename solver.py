<<<<<<< HEAD
# This sodoku solver relies on the assumptions that any inputs are valid problems (i.e. no dissallowed conditions within input)

=======
import numpy as np
import sys
>>>>>>> 97992a571139993bb8152041fec545ffde60c29b


def getInput():     # get input from txt file and put into a 2d array
    grid = []
    count = 0 
    file_name = input("Enter File Name: ")
    with open(file_name, 'r') as file:
        lines = file.readlines()
    file.close()

    for line in lines:

        if count < 10:
            line = line.strip().split(" ")
            line = [int(num) for num in line]
            grid.append(line)
            count += 1

    # converting into numpy array
    #np.asarray(grid)
    return grid


# function to wrte to output file. solvedGrid = -1 if grid not solvable
def writeOutput(solvedGrid):
    file_name = input("Enter Output File name: ")
    file = open(file_name, 'w')
    
    if solvedGrid == -1:
        file.write("Not Solvable!\n")
    else:
        for row in solvedGrid:
            for num in row:
                file.write(str(num) + " ")
            file.write("\n")
    file.close()




# sudoku constraints check
model = np.array(range(1,10))           # model array, to use and check for constraints
def check_row(board):           # check if row contain from 1-9 
    for row in board:
        if np.array_equal(np.unique(row), model) == False:
            return False
    return True





# The choose_var function allows us to identify the best variable to next modify
# The way it is implimented here checks for counts of values in the rows, cols and grids of all empty vars
# if two values have same number of domain, use degree heuristic, if that also same, choose first one. 
# if cannot choose var, means done.

def choose_var(array):      # array is the big grid
    # This is to check if the solution is complete
    done = 0

    # Return Value
    val = [-1, (0, 0)]
    avail_domain = []

    # Hash table of row/column counts. keys are row and column, values are count of assigned values in row and column
    assigned_vals = {}
    count = 0

    row = 0
    assigned_vals['row'] = {}
    for y in array:
        for x in y:
            if x != 0:
                count += 1                      # get the count of all assigned value in a row
        assigned_vals['row'][row] = count         # {row: {1: 3}, {2: 4}, col: {1: 3}, {2: 5}}
        count = 0
        row += 1
    
    # Function for values count
    assigned_vals['col'] = {}
    for x in range(0, 9):
        for y in range(0, 9):
            if array[y][x] != 0:
                count += 1
        assigned_vals['col'][x] = count
        count = 0
    
    # loop thru grid, find the (x,y) of ava
    for y in range(len(array)):
        for x in range(len(array[y])):
            if array[y][x] == 0:
                done += 1
                # Loop for grid count
                gridcount = 0
                grid_x = x - x%3
                grid_y = y - y%3
                for j in range(0, 3):
                    for i in range(0, 3):
                        if array[grid_y + j][grid_x + i] != 0:
                            gridcount += 1
                
                # Calculation of total count of already assigned value, and update of MRV
                count = gridcount + assigned_vals['row'][x] + assigned_vals['col'][y]
                if count > val[0]:         # found mrv
                    val = [count, (y, x)]
                elif count == val[0]:      # use degree heuristic, SHOULD SAVE INTO A LIST JUST IN CASE FOUND ONE WITH SAME DEGREE
                    pass
                else:                       # choose one arbitrarily
                    pass

                    

    print(assigned_vals)
    if done == 0:
        return (-1, -1)

    # Return MRV Value in tuple format, (Y, X)
    return val[1]


# Simple node class for tree structure
class Node:
    def __init__(self, parent, array):
        self.parent = parent
        self.array = array

# This function checks the validity of a move
# Checks row, column and grid to ensure insertion is unique
def check_validity(array, num, loc):
    for x in array[loc[0]]:
        if x == num:
            return False
    for y in range(10):
        if array[y][loc[1]] == num:
            return False

    grid_x = loc[1] - x%3
    grid_y = loc[0] - y%3
    for j in range(0, 3):
        for i in range(0, 3):
            if array[grid_y + j][grid_x + i] == num:
                return False

    return True

# Main driver function. Modifies most relevant variables first, then builds a queue for a tree. This is closer to dfs than bfs. 
queue = []
def solve(node):
    (Y, X) = choose_var(node.array)
    if Y == -1 and X == -1:
        return node
    for i in range (1, 10):
        if check_validity(node.array, i, (Y, X)):
            new_arr = node.array
            new_arr[Y][X] = i
            queue.append(Node(node, new_arr))
    solve(queue[-1])



def main():
    grid = getInput()
    val = choose_var(grid)

main()