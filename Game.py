import pygame
from sprites.Player import Player
from sprites.Weapon import Weapon

class Game:
    def __init__(self, window):
        self.screen = window.screen
        self.sprites = pygame.sprite.Group()
        self.create_sprites()
        self.run()

    def create_sprites(self):
        self.player = Player(100, 100, 3)
        self.player.weapon = Weapon(self.player, 1, 1000, 20, (255, 0, 0))
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
            clock.tick(60)
            pygame.display.flip()  # Update the display

        pygame.quit()

    def events(self):
        pass

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        for sprite in self.sprites:
            sprite.draw(self.screen)