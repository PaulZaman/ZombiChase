import pygame
from sprites.Player import Player
from maps.Map import Map
from sprites.Zombi import Zombie
import random
from settings import *

class Game:
    def __init__(self, window, difficulty, weapon_info):
        self.screen = window.screen
        self.sprites = pygame.sprite.Group()
        self.map = Map(MAP_WIDTH, MAP_HEIGHT, self)
        self.create_sprites(weapon_info, difficulty)
        self.time_survived = 0
        # shaking
        self.shake_start_time = 0
        self.shake_duration = 500
        self.shake = 2
        # run
        self.run()

    def create_sprites(self, weapon_info, difficulty, n_zombies=10):
        self.player = Player(self, 350, 250, 100, weapon_info)

        self.zombies = pygame.sprite.Group()

        self.spawn_zombie(difficulty, n=n_zombies)
        self.sprites.add(self.player)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # color the screen white
            self.screen.fill((255, 255, 255))

            self.events()
            self.update()
            self.draw()

            
            # FPS
            clock.tick(100)
            pygame.display.flip()  # Update the display

        pygame.quit()

    def events(self):
        pass

    def update(self):
        self.time_survived = pygame.time.get_ticks()

        for sprite in self.sprites:
            sprite.update()

        self.map.update()
        

        # shaking
        now = pygame.time.get_ticks()
        if now - self.shake_start_time < self.shake_duration:
            for sprite in self.sprites:
                sprite.rect.x += self.shake
                sprite.rect.y += self.shake
            for sprite in self.map.tiles:
                sprite.rect.x += self.shake
                sprite.rect.y += self.shake
            self.shake *= -1

    def draw(self):
        self.map.draw(self.screen)
        for sprite in self.sprites:
            sprite.draw(self.screen)

    def shake_screen(self):
        self.shake_start_time = pygame.time.get_ticks()

    def spawn_zombie(self, speed, n=1):
        for _ in range(n):
            x = random.randint(1*TILESIZE, (MAP_WIDTH-2)*TILESIZE)
            y = random.randint(1*TILESIZE, (MAP_HEIGHT-2)*TILESIZE)
            zombi = Zombie(self.player, x, y, speed)
            self.zombies.add(zombi)
            self.sprites.add(zombi)
        