import pygame as pg
from settings import *
import random


class Tile(pg.sprite.Sprite):
	def __init__(self, x, y, type, map):
		# type is either "grass" or "wall-br", "wall-bl", "wall-tr", "wall-tl", "wall-h", "wall-v", "inside"


		pg.sprite.Sprite.__init__(self)
		self.type = type
		self.pos = pg.math.Vector2(x, y)
		self.map = map

		# create image
		self.images_dir = IMAGE_DIR + "/jawbreaker/"

		self.image = self.choose_image()
		self.image = pg.transform.scale(self.image, (32, 32))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos.x, self.pos.y)
		
	def choose_image(self):
		if self.type == "grass":
			# randomize int between 1 and 4
			rand = random.randint(1, 4)
			image = pg.image.load(self.images_dir + "/outside/grass" + str(rand) + ".png")
		elif self.type == "wall-br":
			image = pg.image.load(self.images_dir + "/walls/wall_br.png")
		elif self.type == "wall-bl":
			image = pg.image.load(self.images_dir + "/walls/wall_br.png")
			image = pg.transform.flip(image, True, False)
		elif self.type == "wall-tl":
			image = pg.image.load(self.images_dir + "/walls/wall_tl.png")
		elif self.type == "wall-tr":
			image = pg.image.load(self.images_dir + "/walls/wall_tl.png")
			image = pg.transform.flip(image, True, False)
		elif self.type == "wall-h":
			image = pg.image.load(self.images_dir + "/walls/wall_h.png")
		elif self.type == "wall-v":
			image = pg.image.load(self.images_dir + "/walls/wall_v.png")
		elif self.type == "inside":
			image = pg.image.load(self.images_dir + "/inside/floor" + str(random.randint(1, 2)) + ".png")

		return image

	def update(self):
		self.rect.topleft = (self.pos.x - self.map.pos.x, self.pos.y - self.map.pos.y)

	def draw(self, screen):
		screen.blit(self.image, self.rect)


