from random import randint, shuffle

# Prints the 9x9 Sudoku board in a readable format with subgrid separators,board (list[list[int]])
def print_board(board):
    

    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j + 1) % 3 == 0 and j != 0 and j + 1 != 9:
                boardString += "| "

            if j == 8:
                boardString += "\n"

            if j == 8 and (i + 1) % 3 == 0 and i + 1 != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)

# Finds the next empty cell (with value 0) in the board.
# Returns the cell's (row, col) as a tuple or None if no empty cell exists.
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# Checks whether placing 'num' at 'pos' is valid according to Sudoku rules.
def valid(board, pos, num):

    for i in range(9):
        if board[i][pos[1]] == num:
            return False

    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False
    return True

# Solves the Sudoku board using backtracking For the Final Solution.
# Returns True if a solution exists; otherwise, False.
def solve(board):

    empty = find_empty(board)
    if not empty:
        return True

    for nums in range(1, 10):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False

# Generates a valid 9x9 Sudoku puzzle by filling it and then removing numbers.
def generate_board():
    board = [[0 for i in range(9)] for j in range(9)]

    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    # Recursively fills all remaining cells in the board using backtracking for the Generation Step.
    def fill_cells(board, row, col):

        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)

    # Remove a greater number of cells to create a puzzle with fewer initial numbers
    for _ in range(randint(55, 65)):
        row, col = randint(0, 8), randint(0, 8)
        board[row][col] = 0

    return board


if __name__ == "__main__":
    board = generate_board()
    print_board(board)
    solve(board)
    print_board(board)
