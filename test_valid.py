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
    return grid

sudoku = getInput()

#validate row
def isRowValid(row_num):
    return len(set(sudoku[row_num])) == 9
 
#validate column
def isColValid(col_num):
    col = [item[col_num] for item in sudoku]
    return len(set(col)) == 9
 
#validate cell
def isCelValid(cel_row, cel_col):
    vals = sudoku[cel_row][cel_col: cel_col+3]
    vals.extend(sudoku[cel_row+1] [cel_col: cel_col+3])
    vals.extend(sudoku[cel_row+2] [cel_col: cel_col+3])
    return len(set(vals)) == 9
 
#validate sudoku
def validateSudoku():
    for i in range(0,9):
        if not isRowValid(i):
            return False
        if not isColValid(i):
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            print(i, j)
            if not isCelValid(i, j):
                return False
    return True

print(validateSudoku())