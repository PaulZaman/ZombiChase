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
		self.x = x/32
		self.y = y/32

		# create image
		self.images_dir = IMAGE_DIR + "/jawbreaker/"

		self.image = self.choose_image()
		self.image = pg.transform.scale(self.image, (32, 32))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.pos.x, self.pos.y)
		
	def choose_image(self):
		if self.type == "grass":
			# randomize int between 1 and 4, give more weight to 1
			choices = [1, 2, 3, 4, 5]
			weights = [0.6, 0.1, 0.1, 0.195, 0.005]
			rand = random.choices(choices, weights)[0]
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
			# radomize rotation of image
			rand = random.randint(0, 2)
			image = pg.transform.rotate(image, rand * 180)
		elif self.type == "wall-c-hl":
			image = pg.image.load(self.images_dir + "/walls/wall-c-hr.png")
			image = pg.transform.flip(image, True, False)
		elif self.type == "wall-c-hr":
			image = pg.image.load(self.images_dir + "/walls/wall-c-hr.png")
		elif self.type == "wall-c-vt":
			image = pg.image.load(self.images_dir + "/walls/wall-c-vb.png")
			image = pg.transform.flip(image, False, True)
		elif self.type == "wall-c-vb":
			image = pg.image.load(self.images_dir + "/walls/wall-c-vb.png")

		return image

	def update(self):
		self.rect.topleft = (self.pos.x - self.map.pos.x, self.pos.y - self.map.pos.y)
	
	def collide_player(self, p, r):
		if pg.sprite.collide_rect(self, p):
			if (
				r.x < self.rect.midtop[0] < r.x + r.w and 
				r.y + r.h + 15 > self.rect.midtop[1] > r.y + r.h -15
				):	# if colliding with top of tile
				p.pos.y -= 1
				if p.vel.y > 0:
					p.vel.y = 0
				if p.acc.y > 0:
					p.acc.y = 0
			if (
				r.x < self.rect.midbottom[0] < r.x + r.w and 
				r.y - 15 < self.rect.midbottom[1] < r.y + 15
				):	# if colliding with bottom of tile
				p.pos.y += 1
				if p.vel.y < 0:
					p.vel.y = 0
				if p.acc.y < 0:
					p.acc.y = 0
			if (
				r.x + r.w + 15 > self.rect.midleft[0] > r.x + r.w - 15 and 
				r.y < self.rect.midleft[1] < r.y + r.h
				): 	# if colliding with left of tile
				p.pos.x -= 1
				if p.vel.x > 0:
					p.vel.x = 0
				if p.acc.x > 0:
					p.acc.x = 0
			if (
				r.x - 15 < self.rect.midright[0] < r.x + 15 and 
				r.y < self.rect.midright[1] < r.y + r.h
				): 	# if colliding with right of tile	
				p.pos.x += 1
				if p.vel.x < 0:
					p.vel.x = 0
				if p.acc.x < 0:
					p.acc.x = 0

	def zombie_collision(self, z, r):
		if pg.sprite.collide_rect(self, z):
			if (
				r.centery < self.rect.midtop[1] and
				self.rect.y - 2 < r.y + r.h < self.rect.y + 16
				):	# if colliding with top of tile
				if z.direction[1] > 0:
					z.direction[1] = 0
				z.pos.y -= 1
			if (
				r.centery > self.rect.midbottom[1] and
				self.rect.y + self.rect.h - 16 < r.y < self.rect.y + self.rect.h + 2
				):
				if z.direction[1] < 0:
					z.direction[1] = 0
				z.pos.y += 1
			if (
				r.centerx < self.rect.midleft[0] and
				self.rect.x - 2 < r.x + r.w < self.rect.x + 16
				):
				if z.direction[0] > 0:
					z.direction[0] = 0
				z.pos.x -= 1
			if (
				r.centerx > self.rect.midright[0] and
				self.rect.x + self.rect.w - 16 < r.x < self.rect.x + self.rect.w + 2
				):
				if z.direction[0] < 0:
					z.direction[0] = 0
				z.pos.x += 1

	def draw(self, screen):
		# draw collision box
		screen.blit(self.image, self.rect)
		


