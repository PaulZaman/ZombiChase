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
        self.n_powerups = 5

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
            
            # Check if player is in room
            x_player = self.game.player.pos.x + SCREEN_WIDTH // 2
            y_player = self.game.player.pos.y + SCREEN_HEIGHT // 2
            if (
                x_player >= room.x * TILESIZE
                and x_player <= (room.x + room.w) * TILESIZE
                and y_player >= room.y * TILESIZE
                and y_player <= (room.y + room.h) * TILESIZE
            ):
                return
            
            # check if other powerups are in room
            for powerup in self.powerups:
                if (
                    powerup.pos.x >= room.x * TILESIZE
                    and powerup.pos.x <= (room.x + room.w) * TILESIZE
                    and powerup.pos.y >= room.y * TILESIZE
                    and powerup.pos.y <= (room.y + room.h) * TILESIZE
                ):
                    return

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