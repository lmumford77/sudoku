'''Text-based Sudoku used to create the Pygame version in sudoku.py'''

board1 = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# Print the board
def print_board(board):
    for i in range(9):
        if (i % 3 == 0 and i != 0):
            print("------------------------------")
        for j in range(9):
            if (j % 3 == 0 and j != 0):
                print("| ", end="")

            if (j == 8):
                print(board[i][j])
            else:
                print(board[i][j], " ", end="")

# Find an empty spot
def emptySpace(board):
    for i in range(9):
        for j in range(9):
            if (board[i][j] == 0):
                return (i,j) #(row, column)
    return None

# Check if the board is valid based on the number inserted
def isValid(board, num, position):
    row, column = position

    # Check row
    for i in range(9):
        if (num == board[row][i] and i != column):
            return False

    # Check column
    for i in range(9):
        if (num == board[i][column] and i != row):
            return False

    # Check box
    # row section and column section will help get the first element in box
    rowSection = row // 3
    columnSection = column // 3
    for i in range(rowSection * 3, rowSection * 3 + 3):
        for j in range(columnSection * 3, columnSection * 3 + 3):
            if (num == board[i][j] and (i, j) != position):
                return False
    return True

# Solve the board
def solve(board):
    spot = emptySpace(board)
    if (not spot):
        return True
    row, column = spot

    for i in range(1, 10):
        if isValid(board, i, spot):
            board[row][column] = i
            if (solve(board) and not emptySpace(board)):

                return True
            board[row][column] = 0

    return False
