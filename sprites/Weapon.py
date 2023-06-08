import pygame as pg
from sprites.Bullet import Bullet
import math


class Weapon():
    def __init__(self, player, damage, fire_rate, bullet_speed, bullet_image):
        self.player = player
        self.bullets = pg.sprite.Group()
        self.damage = damage
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.bullet_image = bullet_image
        self.gun_offset = pg.math.Vector2(45, 25)
        self.last_shot = 0

    def update(self):
        self.bullets.update()

    def draw(self, screen):
        self.bullets.draw(screen)

    def shoot(self):
        if pg.time.get_ticks() - self.last_shot > self.fire_rate:
          self.bullets.add(self.create_bullet())
          self.last_shot = pg.time.get_ticks()

    def create_bullet(self):
        # Calculate the direction vector (pos of mouse - pos of player)
        direction = pg.math.Vector2(pg.mouse.get_pos()) - pg.math.Vector2(self.player.rect.center)

        spawn_pos = self.player.rect.center + self.gun_offset.rotate(-self.player.angle)

        return Bullet(spawn_pos.x, spawn_pos.y, direction, self.bullet_speed)
