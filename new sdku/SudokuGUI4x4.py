from sudokutools4x4 import valid, solve, find_empty, generate_board
from copy import deepcopy
from sys import exit
import pygame
import time
import random

# Constants for 540x590 layout
GRID_SIZE = 4
SUBGRID_ROWS = 2
SUBGRID_COLS = 2
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 540
TILE_SIZE = WINDOW_WIDTH // GRID_SIZE  # 135
BOTTOM_PANEL_HEIGHT = 50
TOTAL_HEIGHT = WINDOW_HEIGHT + BOTTOM_PANEL_HEIGHT

class Board:
    def __init__(self, window):
        self.board = generate_board()
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [
            [Tile(self.board[i][j], window, j * TILE_SIZE, i * TILE_SIZE, self.board[i][j] != 0) for j in range(GRID_SIZE)]
            for i in range(GRID_SIZE)
        ]
        self.window = window

    def draw_board(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j % SUBGRID_COLS == 0 and j != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (j * TILE_SIZE, 0), (j * TILE_SIZE, WINDOW_HEIGHT), 4)
                if i % SUBGRID_ROWS == 0 and i != 0:
                    pygame.draw.line(self.window, (0, 0, 0), (0, i * TILE_SIZE), (WINDOW_WIDTH, i * TILE_SIZE), 4)
                self.tiles[i][j].draw((0, 0, 0), 1)

                if self.tiles[i][j].value != 0:
                    color = (255, 0, 0) if self.tiles[i][j].is_original else (0, 0, 0)
                    self.tiles[i][j].display(self.tiles[i][j].value, color)

    def deselect(self, tile):
        for row in self.tiles:
            for t in row:
                if t != tile:
                    t.selected = False

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

        if keys:
            for value in keys:
                self.tiles[value[1]][value[0]].display(keys[value], (128, 128, 128))

        if wrong > 0:
            font = pygame.font.SysFont("Bahnschrift", 45)
            self.window.blit(font.render("X", True, (255, 0, 0)), (10, WINDOW_HEIGHT + 4))
            self.window.blit(font.render(str(wrong), True, (0, 0, 0)), (32, WINDOW_HEIGHT + 4))

        font = pygame.font.SysFont("Bahnschrift", 35)
        self.window.blit(font.render(str(time_passed), True, (0, 0, 0)), (WINDOW_WIDTH - 120, WINDOW_HEIGHT + 4))
        pygame.display.flip()

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
                pygame.time.delay(100)
                self.redraw({}, wrong, time_passed)

                if self.visualSolve(wrong, time_passed):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(100)
                self.redraw({}, wrong, time_passed)

        return False

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption("4x4 Sudoku Solver")
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont("Bahnschrift", 40)
    screen.blit(font.render("Generating Random Grid", True, (0, 0, 0)), (100, 240))
    pygame.display.flip()

    wrong = 0
    board = Board(screen)
    selected = (-1, -1)
    keyDict = {}
    solved = False
    you_win_displayed = False
    startTime = time.time()

    while not solved:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))

        if wrong >= 5:
            font = pygame.font.SysFont("Bahnschrift", 60)
            screen.fill((255, 255, 255))
            screen.blit(font.render("You Lost", True, (255, 0, 0)), (130, 200))
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
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i in range(GRID_SIZE):
                    for j in range(GRID_SIZE):
                        if board.tiles[i][j].clicked(pos):
                            selected = (j, i)
                            board.deselect(board.tiles[i][j])
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
                                keyDict.pop(selected, None)
                            else:
                                board.tiles[selected[1]][selected[0]].value = keyDict[selected]
                                board.board[selected[1]][selected[0]] = keyDict[selected]
                                keyDict.pop(selected)

                if event.key == pygame.K_h:
                    board.hint(keyDict)

                if event.key == pygame.K_SPACE:
                    for row in board.tiles:
                        for tile in row:
                            tile.selected = False
                    keyDict.clear()
                    board.visualSolve(wrong, passedTime)

                if event.key == pygame.K_ESCAPE:
                    return

        board.redraw(keyDict, wrong, passedTime)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return