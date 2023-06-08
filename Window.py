import pygame

class Window:
    def __init__(self, width, height):
        # Initialize pygame
        # create a empty window
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Window")
