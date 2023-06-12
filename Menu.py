from Game import Game
from settings import *
import pygame as pg

# Screens
    # Main Menu
        # Settings
            # Change Controls
            # Change Volume
            # Change Fullscreen
        # Highscores
            # Show Highscores
            # Reset Highscores
        # Credits
        # Start Game
            # Choose Weapon
            # Choose Difficulty
            # Start Game


class Menu:
    def __init__(self, window):
        self.window = window
        self.screenIsOn = "main-menu"
        #self.main_loop()

        self.game = Game(self.window)
    
    def main_loop(self):
        run = True
        while run:
            # color the screen white
            self.window.screen.fill(WHITE)

            # Display correct screen
            if self.screenIsOn == "main-menu":
                self.main_menu()

            # FPS
            self.window.clock.tick(60)
            pg.display.flip()  # Update the display

            # Check for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
            
    def main_menu(self):
        # Main Menu

        # Title
        #self.window.draw_text(10, 10, "ZombiChase", 50, (0, 0, 0))
        self.window.draw_text(SCREEN_WIDTH/(2*TILESIZE), 1, "ZombiChase", 50, BLACK, TILESIZE=32)
        self.window.text_button("Start Game", RED, BLACK, 1, 1, 10, 2, TILESIZE=32)
        self.window.draw_grid()


