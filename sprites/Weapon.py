import pygame as pg
from sprites.Bullet import Bullet
import math
import random as rand


class Weapon():
    def __init__(self, player, bullet_image, weaponInfo):
        self.player = player
        self.bullets = pg.sprite.Group()
        self.bullet_image = bullet_image
        self.gun_offset = pg.math.Vector2(35, 20)
        self.set_weapon_characteristics(weaponInfo)
        self.last_shot = 0

    def set_weapon_characteristics(self, weaponInfo):
        self.weaponName = weaponInfo["name"]
        self.damage = weaponInfo["damage"]
        self.fire_rate = weaponInfo["fire_rate"]
        self.bullet_speed = weaponInfo["bullet_speed"]
        self.n_bullets = weaponInfo["n_bullets"]
        self.precision = weaponInfo["precision"]
            
    def print_weapon_characteristics(self):
        print("Weapon: " + self.weapon_type)
        print("Damage: " + str(self.damage))
        print("Fire rate: " + str(self.fire_rate))
        print("Bullet speed: " + str(self.bullet_speed))
        print("Number of bullets: " + str(self.n_bullets))
        print("Precision: " + str(self.precision))

    def update(self):
        self.bullets.update()

    def draw(self, screen):
        self.bullets.draw(screen)

    def shoot(self):
        if pg.time.get_ticks() - self.last_shot > self.fire_rate:
          for _ in range(int(self.n_bullets)-1):
            self.bullets.add(self.create_bullet(offset=rand.randint(-self.precision, self.precision)))
          self.bullets.add(self.create_bullet())
          self.last_shot = pg.time.get_ticks()

    def create_bullet(self, offset=0):
        # Calculate the direction vector (pos of mouse - pos of player)
        direction = pg.math.Vector2(pg.mouse.get_pos()) - pg.math.Vector2(self.player.rect.center)

        spawn_pos = self.player.rect.center + self.gun_offset.rotate(-self.player.angle)

        # apply offset to the direction vector
        direction = direction.rotate(offset)

        return Bullet(spawn_pos.x, spawn_pos.y, direction, self.bullet_speed, self.player.game.zombies, self.player.game.map.walls)
