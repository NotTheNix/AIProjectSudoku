from random import randint, shuffle
from copy import deepcopy

# Prints the 6x6 Sudoku board in a readable format with subgrid separators,board (list[list[int]])
def print_board(board):
    
    boardString = ""
    for i in range(6):
        for j in range(6):
            boardString += str(board[i][j]) + " "
            if (j + 1) % 3 == 0 and j != 0 and j + 1 != 6:
                boardString += "| "

            if j == 5:
                boardString += "\n"

            if j == 5 and (i + 1) % 2 == 0 and i + 1 != 6:
                boardString += "- - - - - - - \n"
    print(boardString)

# Finds the next empty cell (with value 0) in the board.
# Returns the cell's (row, col) as a tuple or None if no empty cell exists.
def find_empty(board):
    for i in range(6):
        for j in range(6):
            if board[i][j] == 0:
                return (i, j)
    return None

# Checks whether placing 'num' at 'pos' is valid according to Sudoku rules.
def valid(board, pos, num):

    row, col = pos

    # Check column
    for i in range(6):
        if board[i][col] == num:
            return False

    # Check row
    for j in range(6):
        if board[row][j] == num:
            return False

    # Check 2x3 subgrid
    start_i = row - row % 2
    start_j = col - col % 3
    for i in range(2):
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

    for nums in range(1, 7):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False

def fill_box(board, start_row, start_col):
    nums = list(range(1, 7))
    shuffle(nums)

    for i in range(2):
        for j in range(3):
            for num in nums:
                if valid(board, (start_row + i, start_col + j), num):
                    board[start_row + i][start_col + j] = num
                    nums.remove(num)
                    break
            else:
                return False # Retry the entire box if no valid number can be placed
    return True

# Recursively fills all remaining cells in the board using backtracking for the Generation Step.
def fill_cells(board, row, col):
    if row == 6:
        return True
    if col == 6:
        return fill_cells(board, row + 1, 0)
    if board[row][col] != 0:
        return fill_cells(board, row, col + 1)

    for num in range(1, 7):
        if valid(board, (row, col), num):
            board[row][col] = num
            if fill_cells(board, row, col + 1):
                return True

    board[row][col] = 0
    return False

# Generates a valid 6x6 Sudoku puzzle by filling it and then removing numbers while ensuring the puzzle remains solvable.
def generate_board():
    board = [[0 for _ in range(6)] for _ in range(6)]

    # Fill the 3 diagonal subgrids
    subgrid_starts = [(0, 0), (2, 3), (4, 0)]
    for start_row, start_col in subgrid_starts:
        attempts = 0
        while not fill_box(board, start_row, start_col):
            for i in range(2):
                for j in range(3):
                    board[start_row + i][start_col + j] = 0
            attempts += 1
            if attempts > 10:
                return generate_board()

    if not fill_cells(board, 0, 0):
        return generate_board()

    full_solution = deepcopy(board)

    # Randomly remove numbers while keeping the puzzle solvable
    attempts = 0
    while True:
        puzzle = deepcopy(full_solution)
        for _ in range(randint(20, 25)):
            row, col = randint(0, 5), randint(0, 5)
            puzzle[row][col] = 0

        if solve(deepcopy(puzzle)):
            return puzzle

        attempts += 1
        if attempts > 3:
            return generate_board()


if __name__ == "__main__":
    board = generate_board()
    print_board(board)
    solve(board)
    print_board(board)