import pygame as pg
from settings import *

class Window:
    def __init__(self, width, height):
        # Initialize pygame
        # create a empty window
        pg.init()
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        pg.display.set_caption("ZombiChase")

    def text_button(self, text, text_color, hover_color, x, y, w, h, TILESIZE=1):
        # This function is similar to button, but does not create a box for the button,
        # it simply uses the text
        # it returns the text of the button if it is pressed, and none otherwise
        # changes the color of text when mouse is hovering over it
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
        rect.midtop = (x * TILESIZE, y * TILESIZE)
        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
            text_color = hover_color
            pg.event.get()
            if pg.mouse.get_pressed()[0] == 1:
                return text
        self.draw_text(x, y, text, 25, text_color, TILESIZE=TILESIZE)

    def draw_text(self, x, y, text, size, color, TILESIZE=1):
        font = pg.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (x*TILESIZE, y*TILESIZE)
        self.screen.blit(text, textRect)

    def draw_grid(self, TILESIZE=32):
        for x in range(0, self.width, TILESIZE):
            pg.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, TILESIZE):
            pg.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y))

