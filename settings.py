import os


# Define directories relative to this file
PRJ_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(PRJ_DIR, 'images')

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# SCREEN SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILESIZE = 32
MAP_WIDTH = 60
MAP_HEIGHT = 60