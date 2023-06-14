import pygame as pg
from settings import *
import re


class Zombie(pg.sprite.Sprite):
    def __init__(self, target, x, y, life, speed=1):
        pg.sprite.Sprite.__init__(self)
        self.pos = pg.math.Vector2()
        self.pos.x = x
        self.pos.y = y
        self.target = target  # Reference to the player object
        self.speed = speed
        self.life = life
        self.maxLife = life
        self.angle = 0
        self.is_chasing = False

        # attack variables
        self.attacking = False
        self.last_attack = 0
        self.attack_delay = 1000

        # animation variables for idle
        self.idle_frame_index = 0
        self.idle_animation_delay = 50  # Delay between each frame in milliseconds
        self.idle_last_update = 0

        # animation variables for walk
        self.walk_frame_index = 0
        self.walk_animation_delay = 50  # Delay between each frame in milliseconds
        self.walk_last_update = 0

        # collision rect 
        self.collision_rect = pg.Rect(380, 280, 40, 40)

        self.load_images()
        self.image = self.idle_images[self.idle_frame_index]
        self.rect = self.image.get_rect()
        self.update()

    def load_images(self):
        idle_dir = IMAGE_DIR + "/zombi/idle"
        # create list to hold images
        self.idle_images = []
        file_names = os.listdir(idle_dir)
        file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
        for file_name in file_names:
            # load image
            image = pg.image.load(os.path.join(idle_dir, file_name)).convert_alpha()
            # resize image
            image = pg.transform.scale(image, (80, 80))
            # add image to list
            self.idle_images.append(image)

        moving_dir = IMAGE_DIR + "/zombi/move"
        # create list to hold images
        self.moving_images = []
        file_names = os.listdir(moving_dir)
        # Sort file names based on numerical suffix
        file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
        for file_name in file_names:
            # load image
            image = pg.image.load(os.path.join(moving_dir, file_name)).convert_alpha()
            # resize image
            image = pg.transform.scale(image, (100, 100))
            # add image to list
            self.moving_images.append(image)

        """attack_dir = IMAGE_DIR + "/zombi/attack"
        # create list to hold images
        self.attack_images = []
        file_names = os.listdir(attack_dir)
        file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
        print(file_names)
        for file_name in file_names:
            # load image
            image = pg.image.load(os.path.join(attack_dir, file_name)).convert_alpha()
            # resize image
            image = pg.transform.scale(image, (100, 100))
            # add image to list
            self.attack_images.append(image)"""

    def update(self):
        # update the rect position
        self.rect.x = self.pos.x - self.target.pos.x
        self.rect.y = self.pos.y - self.target.pos.y

        # calculate the distance between the zombie and the player
        self.distance = pg.math.Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y).length()

        if 50 < self.distance < 300:
            self.is_chasing = True
          
        if self.is_chasing:
            self.chase()

        self.attack()

        self.animate()

        # update the collision rect position
        centroid = pg.mask.from_surface(self.image).centroid()
        self.collision_rect.centerx = centroid[0] + self.rect.x
        self.collision_rect.centery = centroid[1] + self.rect.y

        # if zombi is out of bounds, delete it
        if self.pos.x < 0 or self.pos.x > MAP_WIDTH*TILESIZE or self.pos.y < 0 or self.pos.y > MAP_HEIGHT*TILESIZE:
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()

        # animate idle
        if (now - self.idle_last_update > self.idle_animation_delay) and self.is_chasing == False:
            self.idle_last_update = now
            self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_images)
            self.image = self.idle_images[self.idle_frame_index]     
            self.image = pg.transform.rotate(self.image, self.angle)

        # animate walk
        if (now - self.walk_last_update > self.walk_animation_delay) and self.is_chasing == True:
            self.walk_last_update = now
            self.walk_frame_index = (self.walk_frame_index + 1) % len(self.moving_images)
            self.image = self.moving_images[self.walk_frame_index]
            self.image = pg.transform.rotate(self.image, self.angle)

    def chase(self):
        # Calculate the direction the zombie should move in
        self.direction = pg.math.Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y).normalize()

        self.angle = self.direction.angle_to(pg.math.Vector2(1, 0))

        # Check for collision with walls
        walls_close_to_zombi = pg.sprite.spritecollide(self, self.target.game.map.walls, False)
        for wall in walls_close_to_zombi:
            wall.zombie_collision(self, self.collision_rect)

        # Move the zombie
        self.pos += self.direction * self.speed



        # If the zombie is close enough to the player, stop chasing
        if self.distance < 50:
            self.is_chasing = False
   
    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # draw health bar
        health_bar_width = 50
        health_bar_height = 5
        health_bar_x = self.rect.x + self.rect.width / 2 - health_bar_width / 2
        health_bar_y = self.rect.y - health_bar_height - 5
        health_bar_fill_width = health_bar_width * self.life / self.maxLife
        health_bar_fill_rect = pg.Rect(health_bar_x, health_bar_y, health_bar_fill_width, health_bar_height)
        health_bar_outline_rect = pg.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pg.draw.rect(screen, RED, health_bar_outline_rect)
        pg.draw.rect(screen, GREEN, health_bar_fill_rect)

        # draw collision rect
        #pg.draw.rect(screen, RED, self.collision_rect, 1)

    def hit(self):
        self.life -= self.target.weapon.damage
        if self.life <= 0:
            self.target.zombies_killed += 1
            self.kill()
            self.target.game.spawn_zombie(self.speed+1, n=2)
            self.target.score += self.speed
        self.is_chasing = True

    def attack(self):
      now = pg.time.get_ticks()
      if self.distance < 50 and (now - self.last_attack > self.attack_delay):
        self.attacking = True
        self.target.hit(10)
        self.last_attack = now