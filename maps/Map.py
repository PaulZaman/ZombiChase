import pygame as pg
from maps.Tiles import Tile
from settings import *
import random

class Map:
    def __init__(self, w, h, game):
        self.game = game
        self.w = w
        self.h = h
        self.pos = pg.math.Vector2(0, 0)
        self.create_tiles()

    def create_tiles(self):
        self.tiles = pg.sprite.Group()
        tiles_list = []  # Create a list to store tiles for batch addition

        # Create the exterior border of walls
        for i in range(self.w):
            for j in range(self.h):
                if i == 0 or j == 0 or i == self.w - 1 or j == self.h - 1:
                    # Create corner walls
                    if i == 0 and j == 0:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-tl", self))
                    elif i == 0 and j == self.h - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-bl", self))
                    elif i == self.w - 1 and j == 0:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-tr", self))
                    elif i == self.w - 1 and j == self.h - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-br", self))
                    # Create vertical walls
                    elif i == 0 or i == self.w - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-v", self))
                    # Create horizontal walls
                    elif j == 0 or j == self.h - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-h", self))
                else:
                    tiles_list.append(Tile(i * 32, j * 32, "grass", self))

        self.tiles.add(tiles_list)  # Add all tiles in a batch

        # Generate random rooms
        num_rooms = random.randint(3, 8)  # Adjust the number of rooms as desired
        rooms = []

        for _ in range(num_rooms):
            room_width = random.randint(10, 33) - 3
            room_height = random.randint(10, 33) - 3
            room_x = random.randint(1, self.w - room_width - 1)
            room_y = random.randint(1, self.h - room_height - 1)

            # Check if the room is overlapping with any other rooms
            overlapping = False
            for other_room in rooms:
                if (room_x < other_room["x"] + other_room["width"] and
                    room_x + room_width > other_room["x"] and
                    room_y < other_room["y"] + other_room["height"] and
                    room_y + room_height > other_room["y"]):
                    overlapping = True
                    break

            if overlapping:
                continue
            
            rooms.append({"x": room_x, "y": room_y, "width": room_width, "height": room_height})

            # Create the room walls and entrance
            entrance_side = random.randint(0, 3)
            if entrance_side == 0:  # Top side
                entrance_x = random.randint(room_x, room_x + room_width - 3)
                entrance_y = room_y
            elif entrance_side == 1:  # Bottom side
                entrance_x = random.randint(room_x, room_x + room_width - 3)
                entrance_y = room_y + room_height - 1
            elif entrance_side == 2:  # Left side
                entrance_x = room_x
                entrance_y = random.randint(room_y, room_y + room_height - 3)
            else:  # Right side
                entrance_x = room_x + room_width - 1
                entrance_y = random.randint(room_y, room_y + room_height - 3)

            # Create the room walls and entrance
            for i in range(room_x, room_x + room_width):
                for j in range(room_y, room_y + room_height):
                    if (i == entrance_x or i == entrance_x + 1 or i == entrance_x + 2) and j >= entrance_y and j < entrance_y + 3:
                        # Create the entrance
                        tiles_list.append(Tile(i * 32, j * 32, "inside", self))
                    elif i == room_x and j == room_y:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-tl", self))
                    elif i == room_x and j == room_y + room_height - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-bl", self))
                    elif i == room_x + room_width - 1 and j == room_y:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-tr", self))
                    elif i == room_x + room_width - 1 and j == room_y + room_height - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-br", self))
                    elif i == room_x or i == room_x + room_width - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-v", self))
                    elif j == room_y or j == room_y + room_height - 1:
                        tiles_list.append(Tile(i * 32, j * 32, "wall-h", self))
                    else:
                        tiles_list.append(Tile(i * 32, j * 32, "inside", self))

        self.tiles.add(tiles_list)  # Add all tiles in a batch

        # check if any two tiles overlap
        for tile1 in self.tiles:
            for tile2 in self.tiles:
                if tile1 != tile2 and tile1.rect.x == tile2.rect.x and tile1.rect.y == tile2.rect.y:
                    tile1.kill()

    def draw(self, screen):
        self.tiles.draw(screen)  # Render all tiles in a batch

    def update(self):
        self.pos = self.game.player.pos
        self.tiles.update()

        
