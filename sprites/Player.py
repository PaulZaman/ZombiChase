import pygame as pg
from settings import *
from sprites.Weapon import Weapon
import os
import re

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, life, weaponName):
        pg.sprite.Sprite.__init__(self)
        
        # player variables
        self.pos = pg.math.Vector2(x, y)
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.speed = 0.5
        self.friction = 0.1
        self.weapon = None
        self.life = life
        self.walls = game.map.walls
        self.weaponName = weaponName
        self.game = game
    

        # Create image
        self.init_images()

        # Create weapon
        self.weapon = Weapon(self, (255, 0, 0), self.weaponName)
        
        # Animation variables
        self.idle_frame_index = 0
        self.idle_animation_delay = 50  # Delay between each frame in milliseconds
        self.idle_last_update = 0
        
        # Set the initial image
        self.image = self.idle_images[self.idle_frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # collision mask
        self.collision_rect = pg.Rect(380, 280, 40, 40)

    def init_images(self):
            idlepath = IMAGE_DIR + "/Top_Down_Survivor/"+self.weaponName+"/idle"
            # create list to hold images
            self.idle_images = []
            file_names = os.listdir(idlepath)
            # Sort file names based on numerical suffix
            file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
            for file_name in file_names:
                # load image
                image = pg.image.load(os.path.join(idlepath, file_name)).convert_alpha()
                # resize image
                image = pg.transform.scale(image, (80, 80))
                # add image to list
                self.idle_images.append(image)

    def update(self):
        self.old_pos = self.pos.copy()
        self.handle_input()
        self.apply_friction()
        self.update_position()
        self.animate()
        self.update_weapon()
        
    def handle_input(self):
        keys = pg.key.get_pressed()
        self.acc = pg.math.Vector2(0, 0)
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            self.acc.x = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = self.speed
        if keys[pg.K_UP] or keys[pg.K_z]:
            self.acc.y = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc.y = self.speed
        
        # Shoot
        if pg.mouse.get_pressed()[0] or keys[pg.K_SPACE]:
            self.weapon.shoot()

    def apply_friction(self):
        self.acc += self.vel * -self.friction

    def update_position(self):
        hits = pg.sprite.spritecollide(self, self.walls, False)
        for hit in hits:
            hit.collide_player(self, self.collision_rect)
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # update collision rect
        mask = pg.mask.from_surface(self.image).centroid()
        self.collision_rect.center = (self.rect.x + mask[0], self.rect.y + mask[1])

    def update_weapon(self):
        if self.weapon:
            self.weapon.update()

    def animate(self):
        current_time = pg.time.get_ticks()

        if current_time - self.idle_last_update > self.idle_animation_delay:
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_images)
            self.image = self.idle_images[self.idle_frame_index]
            self.idle_last_update = current_time

        # Rotate the image to point at the mouse cursor
        mouse_pos = pg.mouse.get_pos()
        direction = pg.math.Vector2(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)
        self.angle = direction.angle_to(pg.math.Vector2(1, 0))  # Calculate the angle between the direction vector and (1, 0) vector
        

        # Rotate the image and update the rect
        self.image = pg.transform.rotate(self.idle_images[self.idle_frame_index], self.angle)
        # set the center of the rotated image to the old center
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.weapon:
            self.weapon.draw(screen)
        # draw life
        self.draw_life(screen)

        # draw collision rect
        #pg.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)

    def draw_life(self, screen):
        # draw life bar
        pg.draw.rect(screen, (255, 0, 0), (self.rect.centerx - 50, self.rect.centery - 60, 100, 10))
        pg.draw.rect(screen, (0, 255, 0), (self.rect.centerx - 50, self.rect.centery - 60, self.life, 10))

    def hit(self, damage):
        self.life -= damage
        if self.life <= 0:
            self.kill()
        else:
            self.game.shake_screen()
