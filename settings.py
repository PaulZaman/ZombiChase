import os


# Define directories relative to this file
PRJ_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(PRJ_DIR, 'images')

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 100, 0)
GREY = (100, 100, 100)
LIGHT_GREY = (200, 200, 200)

# palette
BEIGE = '#F6F1F1'
BLUE = '#19A7CE'
BLUE2 = '#146C94'
BLUE3 = '#0D3F5E'
BLUE4 = '#061F2F'
BLACK = '#000000'

# SCREEN SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILESIZE = 32
MAP_WIDTH = 60
MAP_HEIGHT = 60