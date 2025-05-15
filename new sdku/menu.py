import pygame
import sys
from button import Button
from SudokuGUI4x4 import main as start_sudoku_game4x4  # Import the main() from SudokuGUI4x4.py
from SudokuGUI6x6 import main as start_sudoku_game6x6  # Import the main() from SudokuGUI6x6.py
from SudokuGUI9x9 import main as start_sudoku_game9x9  # Import the main() from SudokuGUI9x9.py

pygame.init()
pygame.mixer.init()

#Global Volume Level
volume_level = 0.1

mainClock = pygame.time.Clock()
from pygame.locals import *

global selected_solver_method
selected_solver_method = "backtracking"

# Screen resolution (540x590)
screen_width = 540
screen_height = 590
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('Sudoku Game') # The title

# Load the background image and scale it to fit 540x590 resolution
BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (screen_width, screen_height))  # Scaling the background image to match the new screen size

# Load click sound
click_sound = pygame.mixer.Sound("assets/click.wav")
click_sound.set_volume(0.5)

# Music & Sound Effects
def play_main_theme():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/Main_Theme_Song.mp3")
    pygame.mixer.music.set_volume(volume_level)
    pygame.mixer.music.play(-1)




def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

click = False

def main_menu():
    global click
    play_main_theme()
    menu_font = get_font(50)

    # Adjust the button positions and sizes for 540x590 screen
    PLAY_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 200),  # N3ml Center ll button w 
        text_input="PLAY",
        font=get_font(50),
        base_color="#483D8B",
        hovering_color="#8A2BE2"
    )
    OPTIONS_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 325),
        text_input="OPTIONS",
        font=get_font(50),
        base_color="#483D8B",
        hovering_color="#8A2BE2"
    )
    QUIT_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 450),
        text_input="Quit",
        font=get_font(50),
        base_color="#483D8B",
        hovering_color="#8A2BE2"
    )

    while True:
        screen.blit(BG, (0, 0))
        
        draw_text('Main Menu', menu_font, (75, 0, 130), screen, 20, 20)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Update button hover effect
        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        OPTIONS_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)

        # Draw buttons
        PLAY_BUTTON.update(screen)
        OPTIONS_BUTTON.update(screen)
        QUIT_BUTTON.update(screen)

        if click:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                click_sound.play()
                game()  # ✅ Call Sudoku GUI's main() when PLAY is pressed
            if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                click_sound.play()
                options()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                click_sound.play()
                pygame.quit()
                sys.exit()          
        
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def game():
    running = True
    games_font = get_font(50)

    # Create game buttons
    GAME4x4_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 200),
        text_input="4x4",
        font=get_font(50),
        base_color="#d7fcd4",
        hovering_color="Blue"
    )
    GAME6x6_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 325),
        text_input="6x6",
        font=get_font(50),
        base_color="#d7fcd4",
        hovering_color="Blue"
    )
    GAME9x9_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 450),
        text_input="9x9",
        font=get_font(50),
        base_color="#d7fcd4",
        hovering_color="Blue"
    )

    while running:
        screen.blit(BG, (0, 0))
        draw_text('Games', games_font, (255, 255, 255), screen, 20, 20)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Hover effects
        GAME4x4_BUTTON.changeColor(MENU_MOUSE_POS)
        GAME6x6_BUTTON.changeColor(MENU_MOUSE_POS)
        GAME9x9_BUTTON.changeColor(MENU_MOUSE_POS)

        # Draw buttons
        GAME4x4_BUTTON.update(screen)
        GAME6x6_BUTTON.update(screen)
        GAME9x9_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1: 
                    click_sound.play()
                    if GAME4x4_BUTTON.checkForInput(MENU_MOUSE_POS):
                        start_sudoku_game4x4(selected_solver_method)
                        play_main_theme()
                    if GAME6x6_BUTTON.checkForInput(MENU_MOUSE_POS):
                        start_sudoku_game6x6(selected_solver_method)
                        play_main_theme()
                    if GAME9x9_BUTTON.checkForInput(MENU_MOUSE_POS):
                        start_sudoku_game9x9(selected_solver_method)
                        play_main_theme()

        pygame.display.update()
        mainClock.tick(60)



def options():
    global selected_solver_method, volume_level
    screen.blit(BG, (0, 0))
    running = True
    options_font = get_font(50)

    # Solver method buttons
    BACKTRACKING_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 150),
        text_input="Backtrack",
        font=get_font(40),
        base_color="#d7fcd4",
        hovering_color="Blue"
    )

    GENETIC_BUTTON = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 250),
        text_input="Genetic",
        font=get_font(40),
        base_color="#d7fcd4",
        hovering_color="Blue"
    )

    # Volume control buttons
    VOLUME_UP = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 350),
        text_input="VOL +",
        font=get_font(35),
        base_color="White",
        hovering_color="Green"
    )

    VOLUME_DOWN = Button(
        image=pygame.image.load("assets/Box Rect.png"),
        pos=(screen_width // 2, 450),
        text_input="VOL -",
        font=get_font(35),
        base_color="White",
        hovering_color="Red"
    )

    while running:
        screen.blit(BG, (0, 0))
        draw_text('Options', options_font, (255, 255, 255), screen, 20, 20)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Hover effects
        BACKTRACKING_BUTTON.changeColor(MENU_MOUSE_POS)
        GENETIC_BUTTON.changeColor(MENU_MOUSE_POS)
        VOLUME_UP.changeColor(MENU_MOUSE_POS)
        VOLUME_DOWN.changeColor(MENU_MOUSE_POS)

        # Draw buttons
        BACKTRACKING_BUTTON.update(screen)
        GENETIC_BUTTON.update(screen)
        VOLUME_UP.update(screen)
        VOLUME_DOWN.update(screen)

        # Volume display
        font = get_font(30)
        vol_text = font.render(f"Volume: {int(volume_level * 100)}%", True, (255, 255, 255))
        screen.blit(vol_text, (screen_width // 2 - 90, 550))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_sound.play()

                    # Solver selection
                    if BACKTRACKING_BUTTON.checkForInput(MENU_MOUSE_POS):
                        selected_solver_method = "backtracking"
                        running = False
                    elif GENETIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                        selected_solver_method = "genetic"
                        running = False

                    # Volume control
                    elif VOLUME_UP.checkForInput(MENU_MOUSE_POS):
                        volume_level = min(1.0, volume_level + 0.1)
                        pygame.mixer.music.set_volume(volume_level)

                    elif VOLUME_DOWN.checkForInput(MENU_MOUSE_POS):
                        volume_level = max(0.0, volume_level - 0.1)
                        pygame.mixer.music.set_volume(volume_level)


        pygame.display.update()
        mainClock.tick(60)

main_menu()

