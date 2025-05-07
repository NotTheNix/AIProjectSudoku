from sudokutools6x6 import valid, solve, find_empty, generate_board
from genetic_solver import solve_with_genetic
from copy import deepcopy
import copy
from sys import exit
import pygame
import time
import random

# Global constants

GRID_SIZE = 6
TILE_SIZE = 90
WINDOW_SIZE = 540
BOTTOM_PANEL_HEIGHT = 50
TOTAL_HEIGHT = WINDOW_SIZE + BOTTOM_PANEL_HEIGHT

class Board:
    def __init__(self, window, solve_method="backtracking"):
        self.board = generate_board()

        if solve_method == "genetic":
            self.solvedBoard = solve_with_genetic(copy.deepcopy(self.board))  # No screen passed = no visualization
        else:
            self.solvedBoard = deepcopy(self.board)

            solve(self.solvedBoard)
        self.tiles = [
            [Tile(self.board[i][j], window, j * TILE_SIZE, i * TILE_SIZE, self.board[i][j] != 0) for j in range(GRID_SIZE)]
            for i in range(GRID_SIZE)
        ]
        self.window = window

    def draw_board(self):
        for i in range(6):
            for j in range(6):
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (j * TILE_SIZE, 0), (j * TILE_SIZE, WINDOW_SIZE), 4)
                if i % 2 == 0 and i != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, i * TILE_SIZE), (WINDOW_SIZE, i * TILE_SIZE), 4)

                self.tiles[i][j].draw((0, 0, 0), 1)

                if self.tiles[i][j].value != 0:
                    color = (255, 0, 0) if self.tiles[i][j].is_original else (0, 0, 0)
                    self.tiles[i][j].display(
                        self.tiles[i][j].value,
                        (j * TILE_SIZE + TILE_SIZE // 3, i * TILE_SIZE + TILE_SIZE // 5),
                        color
                    )

        pygame.draw.line(
            self.window,
            (0, 0, 0),
            (0, (i + 1) // 2 * 180),  # Adjust for 6x6 grid (2 subgrids vertically)
            (540, (i + 1) // 2 * 180),
            4,
        )

    def deselect(self, tile):
        for i in range(6):
            for j in range(6):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time_passed):
        self.window.fill((255, 255, 255))
        self.draw_board()
        for i in range(6):
            for j in range(6):
                if self.tiles[i][j].selected:
                    self.tiles[i][j].draw((50, 205, 50), 4)
                elif self.tiles[i][j].correct:
                    self.tiles[i][j].draw((34, 139, 34), 4)
                elif self.tiles[i][j].incorrect:
                    self.tiles[i][j].draw((255, 0, 0), 4)

        if len(keys) != 0:
            for value in keys:
                self.tiles[value[0]][value[1]].display(
                    keys[value],
                    (31 + value[0] * 90, 22 + value[1] * 90),
                    (128, 128, 128),
                )

        if wrong > 0:
            font = pygame.font.SysFont("Bauhaus 93", 30)
            text = font.render("X", True, (255, 0, 0))
            self.window.blit(text, (10, 554))

            font = pygame.font.SysFont("Bahnschrift", 40)
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont("Bahnschrift", 40)
        text = font.render(str(time_passed), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self, wrong, time_passed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for num in range(6):
            if valid(self.board, (empty[0], empty[1]), num + 1):
                self.board[empty[0]][empty[1]] = num + 1
                self.tiles[empty[0]][empty[1]].value = num + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)
                self.redraw({}, wrong, time_passed)

                if self.visualSolve(wrong, time_passed):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time_passed)

    def hint(self, keys):
        while True:
            i = random.randint(0, 5)
            j = random.randint(0, 5)
            if self.board[i][j] == 0:
                if (j, i) in keys:
                    del keys[(j, i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True
            elif self.board == self.solvedBoard:
                return False

class Tile:
    def __init__(self, value, window, x1, y1, is_original):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 90, 90)
        self.selected = False
        self.correct = False
        self.incorrect = False
        self.is_original = is_original

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        font = pygame.font.SysFont("lato", 45)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected

def main(solver_method="backtracking"):
    pygame.init()
    screen = pygame.display.set_mode((540, 590))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("6x6 Sudoku Solver")
    icon = pygame.image.load("assets/thumbnail.png")
    pygame.display.set_icon(icon)

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont("Bahnschrift", 40)
    text = font.render("Random Grid", True, (0, 0, 0))
    screen.blit(text, (156, 290))
    pygame.display.flip()

    wrong = 0
    board = Board(screen, solve_method=solver_method)
    selected = (-1, -1)
    keyDict = {}
    solved = False
    you_win_displayed = False
    startTime = time.time()

    while not solved:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        if wrong >= 7:
            font = pygame.font.SysFont("Bahnschrift", 60)
            text = font.render("You Lost", True, (255, 0, 0))
            screen.fill((255, 255, 255))
            screen.blit(text, (180, 245))
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if board.board == board.solvedBoard and not solved:
            solved = True
            if not you_win_displayed:
                font = pygame.font.SysFont("Bahnschrift", 60)
                text = font.render("You Won!", True, (34, 139, 34))
                screen.fill((255, 255, 255))
                screen.blit(text, (180, 245))
                pygame.display.flip()
                pygame.time.delay(2000)
                you_win_displayed = True
                return

        for event in pygame.event.get():
            elapsed = time.time() - startTime
            passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
               mousePos = pygame.mouse.get_pos()
               for i in range(6):
                    for j in range(6):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = (j, i)
                            board.deselect(board.tiles[i][j])  
            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1, -1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1
                    if event.key == pygame.K_2:
                        keyDict[selected] = 2
                    if event.key == pygame.K_3:
                        keyDict[selected] = 3
                    if event.key == pygame.K_4:
                        keyDict[selected] = 4
                    if event.key == pygame.K_5:
                        keyDict[selected] = 5
                    if event.key == pygame.K_6:
                        keyDict[selected] = 6
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]
                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]:
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                            else:
                                board.tiles[selected[1]][selected[0]].value = keyDict[selected]
                                board.board[selected[1]][selected[0]] = keyDict[selected]
                                del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)

                if event.key == pygame.K_SPACE:
                    for i in range(len(board.tiles)):
                        for j in range(len(board.tiles[i])):
                            board.tiles[i][j].selected = False
                    keyDict = {}
                    elapsed = time.time() - startTime
                    passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

                    if solver_method == "genetic":
                        final = solve_with_genetic(copy.deepcopy(board.board), board.window, delay=50)
                        board.board[:] = final
                        board.solvedBoard = deepcopy(final)
                        for i in range(GRID_SIZE):
                            for j in range(GRID_SIZE):
                                board.tiles[i][j].value = board.board[i][j]
                        board.redraw({}, wrong, passedTime)
                        pygame.display.flip()
                    else:
                        board.visualSolve(wrong, passedTime)
                        board.solvedBoard = deepcopy(board.board)

                    for i in range(len(board.tiles)):
                        for j in range(len(board.tiles[i])):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    solved = True

                if event.key == pygame.K_ESCAPE:
                    return
        board.redraw(keyDict, wrong, passedTime)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
