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
        self.w_tiles = self.width / TILESIZE
        self.h_tiles = self.height / TILESIZE
        self.clock = pg.time.Clock()
        pg.display.set_caption("ZombiChase")

    def button(self, x, y, w, h, text, button_color, button_hover_color, text_color, text_hover_color, border_radius=10, text_size=30, TILESIZE=1):
        # This function creates a button on screen
        # it returns the text of the button if it is pressed, and none otherwise
        # changes the color of box when mouse is hovering over it
        x = x*TILESIZE
        y = y*TILESIZE
        w = w*TILESIZE
        h = h*TILESIZE
        mouse = pg.mouse.get_pos()
        rect = pg.rect.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
            button_color = button_hover_color
            text_color = text_hover_color
            pg.event.get()
            if pg.mouse.get_pressed()[0] == 1:
                return text
        pg.draw.rect(self.screen, button_color, rect, border_radius=border_radius)
        y = y + h/2 - text_size/2
        self.draw_text(x, y, text, text_size, text_color)

    def draw_text(self, x, y, text, size, color, TILESIZE=1):
        font = pg.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.midtop = (x*TILESIZE, y*TILESIZE)
        self.screen.blit(text, textRect)

    def draw_grid(self, TILESIZE=32):
        for x in range(0, self.width, TILESIZE):
            pg.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height))
        for y in range(0, self.height, TILESIZE):
            pg.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y))

    def draw_arrow(self, x, y, w, h, stem_height, color, direction, coeff, TILESIZE=1):
        # coeff is the coefficient of the arrow when it is hovered over
        rect = pg.rect.Rect(x*TILESIZE, y*TILESIZE, w*TILESIZE, h*TILESIZE)        
        
        # Make the arrow bigger when hovered over
        if rect.collidepoint(pg.mouse.get_pos()):
            x = x - (w * coeff - w) / 2
            y = y - (h * coeff - h) / 2
            w = w * coeff
            h = h * coeff
            stem_height = stem_height * coeff
            if pg.mouse.get_pressed()[0] == 1:
                return True

        if direction == "right":
            pg.draw.rect(self.screen, color, (x * TILESIZE, (y + (h / 2) - stem_height / 2) * TILESIZE, (w / 2) * TILESIZE + 5, stem_height * TILESIZE))
            pg.draw.polygon(self.screen, color, (
                ((x + w / 2) * TILESIZE, y * TILESIZE),
                ((x + w / 2) * TILESIZE, (y + h) * TILESIZE),
                ((x + w) * TILESIZE, (y + h / 2) * TILESIZE)
            ))
        elif direction == "left":
            pg.draw.rect(self.screen, color, ((x + (w / 2)) * TILESIZE, (y + (h / 2) - stem_height / 2) * TILESIZE, (w / 2) * TILESIZE, stem_height * TILESIZE))
            pg.draw.polygon(self.screen, color, (
                ((x + w / 2) * TILESIZE, y * TILESIZE),
                ((x + w / 2) * TILESIZE, (y + h) * TILESIZE),
                 ((x) * TILESIZE, (y + h / 2) * TILESIZE)
            ))

