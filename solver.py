# This sodoku solver relies on the assumptions that any inputs are valid problems (i.e. no dissallowed conditions within input)


# The Minimum remaining values function allows us to identify the best variable to next modify
# The way it is implimented here checks for counts of values in the rows, cols and grids of all empty vars
# The degree of all variables is 20 (8 per row & col, 4 left within grid), and as such there is no real need for 
# degree checking. 

def mrv(array):
    # This is to check if the solution is complete
    done = 0

    # Return Value
    val = [-1, (0, 0)]

    # Hash table of row/column counts
    counts = {}
    count = 0

    #Function for row count
    row = 0
    counts['row'] = {}
    for y in array:
        for x in y:
            if x != 0:
                count += 1
        counts['row'][row] = counts
        count = 0
        row += 1
    
    # Function for values count
    counts['col'] = {}
    for x in range(0, 10):
        for y in range(0, 10):
            if array[y][x] != 0:
                count += 1
        counts['col'][x] = count
        count = 0
    
    # Main loop to examine all possible vars
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
                
                # Calculation of total count, and update of MRV
                count = gridcount + counts['row'][x] + counts['col'][y]
                if count >= val[0]:
                    val = [count, (y, x)]

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
    (Y, X) = mrv(node.array)
    if Y == -1 and X == -1:
        return node
    for i in range (0, 10):
        if check_validity(node.array, i, (Y, X)):
            new_arr = node.array
            new_arr[Y][X] = i
            queue.append(Node(node, new_arr))
    solve(queue[-1])
