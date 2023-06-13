import pygame as pg
from settings import *
import math

class Powerup(pg.sprite.Sprite):
    def __init__(self, x, y, type, map):
        # type can be "bullets" or "health" or "fire_rate" or "precision" or "damage"
        super().__init__()
        self.pos = pg.math.Vector2(x, y)
        self.type = type
        self.map = map
        self.load_image()
        self.player = self.map.game.player

        # Bounce animation variables
        self.amplitude = 10  # Adjust the height of the bounce
        self.velocity = 0.005  # Adjust the speed of the bounce

        # upgrade variables
        self.last_upgrade = 0

    def load_image(self):
        self.image = pg.image.load(IMAGE_DIR + "/powerups/" + self.type + ".png")
        self.image = pg.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

    def update(self):
        # Perform the bounce animation
        self.rect.x = self.pos.x - self.map.game.player.pos.x
        self.rect.y = self.pos.y - self.map.game.player.pos.y

        # apply bounce animation
        self.rect.y += self.amplitude * math.sin(self.map.game.time_survived * self.velocity)

        # check collisions with player
        if self.rect.colliderect(self.player.collision_rect):
            self.apply_effect()
            self.kill()
                    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def apply_effect(self):
        now = pg.time.get_ticks()
        if now - self.last_upgrade > 1000:
            if self.type == "health":
                self.player.life += 10
                if self.player.life > 100:
                    self.player.life = 100
            elif self.type == "bullets":
                if self.player.weapon.n_bullets < 11:
                    self.player.weapon.n_bullets += 0.5
            elif self.type == "fire_rate":
                if self.player.weapon.fire_rate > 100:
                    self.player.weapon.fire_rate -= 100
            elif self.type == "precision":
                if self.player.weapon.precision > 1:
                    self.player.weapon.precision -= 2
            elif self.type == "damage":
                self.player.weapon.damage += 1
            self.last_upgrade = now
            self.player.powerups_collected += 1
