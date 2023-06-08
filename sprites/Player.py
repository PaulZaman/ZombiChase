import pygame as pg
from settings import *
import os
import re

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, life):
        pg.sprite.Sprite.__init__(self)
        
        # Create image
        self.init_images()
        
        # player variables
        self.speed = 5
        self.pos = pg.math.Vector2(x, y)
        self.mouvement = pg.math.Vector2(0, 0)
        self.weapon = None
        self.life = life
        
        # Animation variables
        self.idle_frame_index = 0
        self.idle_animation_delay = 50  # Delay between each frame in milliseconds
        self.idle_last_update = 0
        
        # Set the initial image
        self.image = self.idle_images[self.idle_frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def init_images(self):
            idlepath = IMAGE_DIR + "/Top_Down_Survivor/handgun/idle"
            # create list to hold images
            self.idle_images = []
            file_names = os.listdir(idlepath)
            # Sort file names based on numerical suffix
            file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
            for file_name in file_names:
                # load image
                image = pg.image.load(os.path.join(idlepath, file_name)).convert_alpha()
                # resize image
                image = pg.transform.scale(image, (100, 100))
                # add image to list
                self.idle_images.append(image)

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pg.K_UP]:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed

        # Shoot
        if pg.mouse.get_pressed()[0]:
            self.weapon.shoot()

        # Update animation
        self.animate()

        # Update weapon
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
      self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.weapon:
            self.weapon.draw(screen)
