import pygame as pg
from maps.Tiles import Tile
import random
from sprites.Powerup import Powerup

class Room:
  def __init__(self, x, y, w, h, map, tilesize=32):
      self.x = x
      self.y = y
      self.w = w
      self.h = h
      self.map = map
      self.tilesize = tilesize

      # tiles in room
      self.tiles = pg.sprite.Group()
      self.walls = pg.sprite.Group()

      # create border walls
      self.create_border()

  def create_border(self):

    # Choose if entrance is on top or bottom, left or right
    choices = ["top", "bottom", "left", "right"]
    entrance = random.choice(choices)

    # Create horizontal walls
    self.create_horizontal_walls(entrance)

    # Create vertical walls
    self.create_vertical_walls(entrance)

    # Create corner walls
    self.create_corner_walls(entrance)

    # Create floor
    self.create_floor()

    self.tiles.add(self.walls)

  def create_horizontal_walls(self, entrance):
    wallrange = self.create_horizontal_entrance(entrance)
    # Create horizontal walls
    for i in range(1, self.w): # top wall
      if entrance=="top":
        if i not in wallrange:
          self.walls.add(Tile((self.x + i) * self.tilesize, self.y * self.tilesize, "wall-h", self.map)) 
      else:
        self.walls.add(Tile((self.x + i) * self.tilesize, self.y * self.tilesize, "wall-h", self.map))
    
    for i in range(1, self.w): # bottom wall
      if entrance=="bottom":
        if i not in wallrange:
          self.walls.add(Tile((self.x + i) * self.tilesize, (self.y + self.h) * self.tilesize, "wall-h", self.map))
      else:
        self.walls.add(Tile((self.x + i) * self.tilesize, (self.y + self.h) * self.tilesize, "wall-h", self.map))

  def create_vertical_walls(self, entrance):
    wallrange = self.create_vertical_entrance(entrance)
    # Create vertical walls
    for i in range(1, self.h): # left wall
      if entrance=="left":
        if i not in wallrange:
          self.walls.add(Tile(self.x * self.tilesize, (self.y + i) * self.tilesize, "wall-v", self.map))
      else:
        self.walls.add(Tile(self.x * self.tilesize, (self.y + i) * self.tilesize, "wall-v", self.map))
    
    for i in range(1, self.h): # right wall
      if entrance=="right":
        if i not in wallrange:
          self.walls.add(Tile((self.x + self.w) * self.tilesize, (self.y + i) * self.tilesize, "wall-v", self.map))
      else:
        self.walls.add(Tile((self.x + self.w) * self.tilesize, (self.y + i) * self.tilesize, "wall-v", self.map))
      
  def create_corner_walls(self, entrance):
    # Create corner walls
    self.walls.add(Tile(self.x * self.tilesize, self.y * self.tilesize, "wall-tl", self.map))
    self.walls.add(Tile(self.x * self.tilesize, (self.y + self.h) * self.tilesize, "wall-bl", self.map))
    self.walls.add(Tile((self.x + self.w) * self.tilesize, self.y * self.tilesize, "wall-tr", self.map))
    self.walls.add(Tile((self.x + self.w) * self.tilesize, (self.y + self.h) * self.tilesize, "wall-br", self.map))

  def create_horizontal_entrance(self, entrance):
    if entrance == "left" or entrance == "right":
      return None
    
    if entrance == "top":
      x = random.randint(self.x + 2, self.x + self.w - 4)
      y = self.y
      for i in range(3):
        self.tiles.add(Tile((x+i) * self.tilesize, (y-1) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 1) == 0:
          self.tiles.add(Tile((x+i) * self.tilesize, (y-2) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 3) == 0:
          self.tiles.add(Tile((x+i) * self.tilesize, (y-3) * self.tilesize, "grass-5", self.map))

    if entrance == "bottom":
      x = random.randint(self.x + 2, self.x + self.w - 4)
      y = self.y + self.h
      for i in range(3):
        self.tiles.add(Tile((x+i) * self.tilesize, (y+1) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 1) == 0:
          self.tiles.add(Tile((x+i) * self.tilesize, (y+2) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 3) == 0:
          self.tiles.add(Tile((x+i) * self.tilesize, (y+3) * self.tilesize, "grass-5", self.map))

   
    self.walls.add(Tile((x-1) * self.tilesize, y * self.tilesize, "wall-c-hl", self.map))
    self.tiles.add(Tile(x * self.tilesize, y * self.tilesize, "inside", self.map))
    self.tiles.add(Tile((x+1) * self.tilesize, y * self.tilesize, "inside", self.map))
    self.tiles.add(Tile((x+2) * self.tilesize, y * self.tilesize, "inside", self.map))
    self.walls.add(Tile((x+3) * self.tilesize, y * self.tilesize, "wall-c-hr", self.map))

    

    return [
      (x-1)-self.x,
      x-self.x,
      (x+1)-self.x,
      (x+2)-self.x,
      (x+3)-self.x
    ]

  def create_vertical_entrance(self, entrance):
    if entrance == "top" or entrance == "bottom":
      return None
    if entrance == "left":
      x = self.x
      y = random.randint(self.y + 2, self.y + self.h - 4)
      for i in range(3):
        self.tiles.add(Tile((x-1) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 1) == 0:
          self.tiles.add(Tile((x-2) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 3) == 0:
          self.tiles.add(Tile((x-3) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))
    if entrance == "right":
      x = self.x + self.w
      y = random.randint(self.y + 2, self.y + self.h - 4)
      for i in range(3):
        self.tiles.add(Tile((x+1) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 1) == 0:
          self.tiles.add(Tile((x+2) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))
        if random.randint(0, 3) == 0:
          self.tiles.add(Tile((x+3) * self.tilesize, (y+i) * self.tilesize, "grass-5", self.map))

    self.walls.add(Tile(x * self.tilesize, (y-1) * self.tilesize, "wall-c-vt", self.map))
    self.tiles.add(Tile(x * self.tilesize, y * self.tilesize, "inside", self.map))
    self.tiles.add(Tile(x * self.tilesize, (y+1) * self.tilesize, "inside", self.map))
    self.tiles.add(Tile(x * self.tilesize, (y+2) * self.tilesize, "inside", self.map))
    self.walls.add(Tile(x * self.tilesize, (y+3) * self.tilesize, "wall-c-vb", self.map))

    return [
      (y-1)-self.y,
      y-self.y,
      (y+1)-self.y,
      (y+2)-self.y,
      (y+3)-self.y
    ]
  
  def create_floor(self):
    for i in range(1, self.w):
      for j in range(1, self.h):
        self.tiles.add(Tile((self.x + i) * self.tilesize, (self.y + j) * self.tilesize, "inside", self.map))
      