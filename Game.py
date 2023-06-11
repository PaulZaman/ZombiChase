import pygame
from sprites.Player import Player
from maps.Map import Map
from sprites.Zombi import Zombie
import random

class Game:
    def __init__(self, window):
        self.screen = window.screen
        self.sprites = pygame.sprite.Group()
        self.map = Map(60, 60, self)
        self.create_sprites()
        # shaking
        self.shake_start_time = 0
        self.shake_duration = 500
        self.shake = 2
        # run
        self.run()

    def create_sprites(self):
        self.player = Player(self, 350, 250, 100, "rifle")
        self.sprites.add(self.player)

        self.zombies = pygame.sprite.Group()

        self.zombi = Zombie(self.player, 350, 250)
        self.zombies.add(self.zombi)
        self.sprites.add(self.zombi)

        """for i in range(10):
            x = random.randint(0, 60*32)
            y = random.randint(0, 60*32)
            zombi = Zombie(self.player, x, y)
            self.zombies.add(zombi)
            self.sprites.add(zombi)"""

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
            clock.tick(80)
            pygame.display.flip()  # Update the display

        pygame.quit()

    def events(self):
        pass

    def update(self):
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
        