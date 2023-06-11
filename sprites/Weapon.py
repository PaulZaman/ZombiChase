import pygame as pg
from sprites.Bullet import Bullet
import math
import random as rand


class Weapon():
    def __init__(self, player, bullet_image, weapon_type):
        self.player = player
        self.bullets = pg.sprite.Group()
        self.bullet_image = bullet_image
        self.weapon_type = weapon_type
        self.gun_offset = pg.math.Vector2(35, 20)
        self.set_weapon_offset()
        self.last_shot = 0

    def set_weapon_offset(self):
        if self.weapon_type == "rifle":
            self.damage = 1
            self.fire_rate = 200
            self.bullet_speed = 20
        elif self.weapon_type == "shotgun":
            self.damage = 1
            self.fire_rate = 1500
            self.bullet_speed = 10
        elif self.weapon_type == "handgun":
            self.damage = 3
            self.fire_rate = 1000
            self.bullet_speed = 15
            

    def update(self):
        self.bullets.update()

    def draw(self, screen):
        self.bullets.draw(screen)

    def shoot(self):
        if pg.time.get_ticks() - self.last_shot > self.fire_rate:
          if self.weapon_type == "shotgun":
            for i in range(5):
              self.bullets.add(self.create_bullet(offset=rand.randint(-10, 10)))
          self.bullets.add(self.create_bullet())
          self.last_shot = pg.time.get_ticks()

    def create_bullet(self, offset=0):
        # Calculate the direction vector (pos of mouse - pos of player)
        direction = pg.math.Vector2(pg.mouse.get_pos()) - pg.math.Vector2(self.player.rect.center)

        spawn_pos = self.player.rect.center + self.gun_offset.rotate(-self.player.angle)

        # apply offset to the direction vector
        direction = direction.rotate(offset)

        return Bullet(spawn_pos.x, spawn_pos.y, direction, self.bullet_speed, self.player.game.zombies, self.player.game.map.walls)
