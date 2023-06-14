import pygame as pg
from maps.Tiles import Tile
from settings import *
import random
from maps.Room import Room
from sprites.Powerup import Powerup
class Map:
    def __init__(self, w, h, game):
        self.game = game
        self.w = w
        self.h = h
        self.pos = pg.math.Vector2(0, 0)
        self.create_tiles()

        # Create powerups
        self.powerups = pg.sprite.Group()
        self.n_powerups = 1

    def create_tiles(self):
        self.walls = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.rooms = []

        # Create the exterior border of walls
        self.create_map_border()

        # Number of rooms to generate
        rooms = self.w * self.h // 200

        for _ in range(rooms):
            self.generate_room()
        
        # Create floor
        self.create_floor()

        self.create_grid()

    def create_grid(self):
        self.grid = [[0 for _ in range(self.h)] for _ in range(self.w)]
        for tile in self.walls:
            self.grid[int(tile.x)][int(tile.y)] = 1

    def generate_room(self):
        # Randomly generate room size
        room_w = random.randint(6, 15)
        room_h = random.randint(6, 15)

        # Randomly generate room position
        room_x = random.randint(4, self.w - room_w - 4)
        room_y = random.randint(4, self.h - room_h - 4)

         # Check if room overlaps with other rooms with 2-tile spacing
        for room in self.rooms:
            if (
                room_x <= room.x + room.w + 3
                and room_x + room_w + 3 >= room.x
                and room_y <= room.y + room.h + 3
                and room_y + room_h + 3 >= room.y
            ):
                return
            
        # Create room
        room = Room(room_x, room_y, room_w, room_h, self)

        # Add room to map
        self.tiles.add(room.tiles)
        self.walls.add(room.walls)
        self.rooms.append(room)

    def create_map_border(self):
        tiles = []
        for i in range(self.w):
            for j in range(self.h):
                if i == 0 or j == 0 or i == self.w - 1 or j == self.h - 1:
                    # Create corner walls
                    if i == 0 and j == 0:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-tl", self))
                    elif i == 0 and j == self.h - 1:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-bl", self))
                    elif i == self.w - 1 and j == 0:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-tr", self))
                    elif i == self.w - 1 and j == self.h - 1:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-br", self))
                    # Create vertical walls
                    elif i == 0 or i == self.w - 1:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-v", self))
                    # Create horizontal walls
                    elif j == 0 or j == self.h - 1:
                        tiles.append(Tile(i * TILESIZE, j * TILESIZE, "wall-h", self))
        self.tiles.add(tiles)
        self.walls.add(tiles)

    def create_floor(self):
        # fill all tiles that are empty with floor tiles
        tiles = []
        for i in range(self.w):
            for j in range(self.h):
                if not self.get_tile(i, j):
                    tiles.append(Tile(i * TILESIZE, j * TILESIZE, "grass", self))
        self.tiles.add(tiles)

    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return True
        return False
    
        self.tiles = pg.sprite.Group()
        tiles_list = []  # Create a list to store tiles for batch addition

        # Create the exterior border of walls
        for i in range(self.w):
            for j in range(self.h):
                if i == 0 or j == 0 or i == self.w - 1 or j == self.h - 1:
                    # Create corner walls
                    if i == 0 and j == 0:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-tl", self))
                    elif i == 0 and j == self.h - 1:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-bl", self))
                    elif i == self.w - 1 and j == 0:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-tr", self))
                    elif i == self.w - 1 and j == self.h - 1:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-br", self))
                    # Create vertical walls
                    elif i == 0 or i == self.w - 1:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-v", self))
                    # Create horizontal walls
                    elif j == 0 or j == self.h - 1:
                        tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "wall-h", self))
                else:
                    tiles_list.append(Tile(i * TILESIZE, j * TILESIZE, "grass", self))

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
        self.powerups.draw(screen)

    def update(self):
        self.pos = self.game.player.pos
        self.tiles.update()
        self.update_powerups()
        self.update_mini_map()

    def update_powerups(self):
        if len(self.powerups) < self.n_powerups:
            # randomly place the powerups in a random room
            room = random.choice(self.rooms)
            x = random.randint((room.x+1) * TILESIZE, (room.x + room.w - 1) * TILESIZE)
            y = random.randint((room.y+1) * TILESIZE, (room.y + room.h - 1) * TILESIZE)
            powerup = Powerup(x, y, random.choice(["health", "fire_rate", "bullets", "precision", "damage"]), self)
            self.powerups.add(powerup)
        self.powerups.update()

    def update_mini_map(self):
        pass
        """self.mini_map = pg.Surface((self.w * TILESIZE, self.h * TILESIZE))
        self.mini_map.fill((0, 0, 0))
        for tile in self.tiles:
            if tile.type[:4] == "wall":
                pg.draw.rect(self.mini_map, (255, 255, 255), (tile.rect.x, tile.rect.y, TILESIZE, TILESIZE))
        self.mini_map = pg.transform.scale(self.mini_map, (self.w * 10, self.h * 10))
        self.mini_map.set_alpha(100)"""