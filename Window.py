import pygame as pg
from settings import *
import time

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
        # This function creates a button on the screen
        # It returns the text of the button if it is pressed, and None otherwise
        # It changes the color of the box when the mouse is hovering over it

        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        
        rect = pg.Rect(0, 0, w * TILESIZE, h * TILESIZE)
        rect.midtop = (x * TILESIZE, y * TILESIZE)
        
        hovering = rect.collidepoint(*mouse)
        
        if hovering and click[0] == 1:  # Check for left button press
            while pg.mouse.get_pressed()[0] == 1:  # Wait for button release
                pg.event.get()
            return text
        
        button_color = button_hover_color if hovering else button_color
        text_color = text_hover_color if hovering else text_color
        
        pg.draw.rect(self.screen, button_color, rect, border_radius=border_radius)
        text_x = rect.x + rect.width / 2
        text_y = rect.y + rect.height / 2 - text_size / 2

        self.draw_text(text_x, text_y, text, text_size, text_color)

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
                time.sleep(0.2)
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

    def text_box(self, text, x, y, w, h, time):
        # creates a text box with inputted text
        # makes box grow as text is growing
        # creates a vertical white bar to animate a bit
        x = x * TILESIZE
        y = y * TILESIZE
        w = w * TILESIZE
        h = h * TILESIZE
        font = pg.font.Font('freesansbold.ttf', 25)
        text_surface = font.render(text, True, WHITE)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y + h//2 - text_height//2)

        if text_width + 40 > w:
            w = text_width + 40
        rect = pg.Rect(0, 0, w, h)
        rect.midtop = (x, y)
        pg.draw.rect(self.screen, BLACK, rect)
        if (pg.time.get_ticks() - time) % 500 < 250:
            pg.draw.line(self.screen, WHITE, (x + text_width // 2, y), (x + text_width // 2, y + h), 3)

        self.screen.blit(text_surface, text_rect)
