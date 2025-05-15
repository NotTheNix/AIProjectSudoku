from sudokutools4x4 import valid, solve, find_empty, generate_board  # Sudoku logic tools
from genetic_solver import solve_with_genetic  # GA solver
from copy import deepcopy
import copy
from sys import exit
import pygame
import time
import random

# Constants for GUI layout
GRID_SIZE = 4
SUBGRID_ROWS = 2
SUBGRID_COLS = 2
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 540
TILE_SIZE = WINDOW_WIDTH // GRID_SIZE  # Each tile is 135x135 pixels
BOTTOM_PANEL_HEIGHT = 50
TOTAL_HEIGHT = WINDOW_HEIGHT + BOTTOM_PANEL_HEIGHT  # Space for timer/wrong count

# Board class handles game state and rendering
class Board:
    def __init__(self, window, solve_method="backtracking"):
        self.board = generate_board()  # Generate a random valid board

        # Solve the board either using GA or backtracking
        if solve_method == "genetic":
            self.solvedBoard = solve_with_genetic(copy.deepcopy(self.board))
        else:
            self.solvedBoard = deepcopy(self.board)
            solve(self.solvedBoard)

        # Create tile objects for display
        self.tiles = [
            [Tile(self.board[i][j], window, j * TILE_SIZE, i * TILE_SIZE, self.board[i][j] != 0) for j in range(GRID_SIZE)]
            for i in range(GRID_SIZE)
        ]
        self.window = window

    # Draw the grid and numbers
    def draw_board(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # Draw thick lines to separate subgrids
                if j % SUBGRID_COLS == 0 and j != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (j * TILE_SIZE, 0), (j * TILE_SIZE, WINDOW_HEIGHT), 4)
                if i % SUBGRID_ROWS == 0 and i != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, i * TILE_SIZE), (WINDOW_WIDTH, i * TILE_SIZE), 4)
                
                # Draw the tile border
                self.tiles[i][j].draw((0, 0, 0), 1)

                # Draw the number in the tile
                if self.tiles[i][j].value != 0:
                    color = (255, 0, 0) if self.tiles[i][j].is_original else (0, 0, 0)
                    self.tiles[i][j].display(self.tiles[i][j].value, color)

    # Deselect all other tiles when one is selected
    def deselect(self, tile):    
        for row in self.tiles:
            for t in row:
                if t != tile:
                    t.selected = False

    # Redraw the full screen with updated tiles
    def redraw(self, keys, wrong, time_passed):      
        self.window.fill((255, 255, 255))
        self.draw_board()

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = self.tiles[i][j]
                if tile.selected:
                    tile.draw((50, 205, 50), 4)
                elif tile.correct:
                    tile.draw((34, 139, 34), 4)
                elif tile.incorrect:
                    tile.draw((255, 0, 0), 4)

        # Draw temporary numbers entered by player
        if keys:
            for value in keys:
                self.tiles[value[1]][value[0]].display(keys[value], (128, 128, 128))

        # Show number of wrong attempts
        if wrong > 0:
            font = pygame.font.SysFont("Bahnschrift", 45)
            self.window.blit(font.render("X", True, (255, 0, 0)), (10, WINDOW_HEIGHT + 4))
            self.window.blit(font.render(str(wrong), True, (0, 0, 0)), (32, WINDOW_HEIGHT + 4))

        # Show elapsed time
        font = pygame.font.SysFont("Bahnschrift", 35)
        self.window.blit(font.render(str(time_passed), True, (0, 0, 0)), (WINDOW_WIDTH - 120, WINDOW_HEIGHT + 4))
        pygame.display.flip()

    # Recursively solve the board with visual delay
    def visualSolve(self, wrong, time_passed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for num in range(1, GRID_SIZE + 1):
            if valid(self.board, (empty[0], empty[1]), num):
                self.board[empty[0]][empty[1]] = num
                self.tiles[empty[0]][empty[1]].value = num
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)
                self.redraw({}, wrong, time_passed)

                if self.visualSolve(wrong, time_passed):
                    return True

                # Undo if wrong
                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time_passed)

        return False

    # Fill a random empty tile with correct value as a hint
    def hint(self, keys):
        while True:
            i, j = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if self.board[i][j] == 0:
                keys.pop((j, i), None)
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True
            elif self.board == self.solvedBoard:
                return False

# Tile class represents each cell in the board
class Tile:
    def __init__(self, value, window, x1, y1, is_original):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, TILE_SIZE, TILE_SIZE)
        self.selected = False
        self.correct = False
        self.incorrect = False
        self.is_original = is_original

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, color):
        font = pygame.font.SysFont("lato", 65)
        text = font.render(str(value), True, color)
        text_rect = text.get_rect(center=self.rect.center)
        self.window.blit(text, text_rect)

    def clicked(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected

# Main game loop
def main(solver_method="backtracking"):
    pygame.init()

    # Load sounds
    click_sound = pygame.mixer.Sound("assets/Ingame_clicks.mp3")
    click_sound.set_volume(0.05)

    wrong_sound = pygame.mixer.Sound("assets/Wrong_Answer.mp3")
    wrong_sound.set_volume(0.05)

    losing_sound = pygame.mixer.Sound("assets/Losing_Sound.mp3")
    losing_sound.set_volume(0.1)

    winning_sound = pygame.mixer.Sound("assets/Win_Sound.mp3")
    winning_sound.set_volume(0.1)

    # Play background music
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/Game_Song.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    # Setup game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, TOTAL_HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku Game")
    icon = pygame.image.load("assets/thumbnail.png")
    pygame.display.set_icon(icon)

    # Display loading message
    font = pygame.font.SysFont("Bahnschrift", 40)
    screen.blit(font.render("Generating Random Grid", True, (0, 0, 0)), (100, 240))
    pygame.display.flip()

    wrong = 0
    board = Board(screen, solve_method=solver_method)
    selected = (-1, -1)
    keyDict = {}
    solved = False
    you_win_displayed = False
    startTime = time.time()

    # Game loop
    while not solved:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        # Handle losing
        if wrong >= 5:
            pygame.mixer.music.stop()
            losing_sound.play()
            screen.fill((0, 0, 0))
            lose_img = pygame.image.load("assets/Game_Over.jpg")
            lose_img = pygame.transform.scale(lose_img, (400, 400))
            screen.blit(lose_img, (70, 90))
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        # Handle win
        if board.board == board.solvedBoard and not solved:
            solved = True
            if not you_win_displayed:
                pygame.mixer.music.stop()
                winning_sound.play()
                screen.fill((0, 0, 0))
                win_img = pygame.image.load("assets/you_won_BG.png")
                win_img = pygame.transform.scale(win_img, (300, 300))
                screen.blit(win_img, (120, 120))
                pygame.display.flip()
                pygame.time.delay(2000)
                you_win_displayed = True
                return  # End the game after showing the message

        for event in pygame.event.get():
            elapsed = time.time() - startTime
            passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if board.tiles[i][j].clicked(pos):
                            selected = (j, i)
                            board.deselect(board.tiles[i][j])
                            click_sound.play()
            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if pygame.K_1 <= event.key <= pygame.K_4:
                        keyDict[selected] = event.key - pygame.K_0
                    elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        keyDict.pop(selected, None)
                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]:
                                wrong += 1
                                wrong_sound.play()
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                            else:
                                board.tiles[selected[1]][selected[0]].value = keyDict[selected]
                                board.board[selected[1]][selected[0]] = keyDict[selected]
                                del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)

                if event.key == pygame.K_SPACE:
                    for row in board.tiles:
                        for tile in row:
                            tile.selected = False
                    keyDict.clear()

                    if solver_method == "genetic":
                        final = solve_with_genetic(copy.deepcopy(board.board), board.window, delay=50)
                        board.board[:] = final
                        board.solvedBoard = deepcopy(final)
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                board.tiles[i][j].value = board.board[i][j]
                        board.redraw({}, wrong, passedTime)
                    else:
                        board.visualSolve(wrong, passedTime)
                        board.solvedBoard = deepcopy(board.board)

                    # Reset flags after auto-solve
                    for row in board.tiles:
                        for tile in row:
                            tile.correct = False
                            tile.incorrect = False
                    solved = True

                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return

        board.redraw(keyDict, wrong, passedTime)

    # Keep the window open after winning/losing
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return
