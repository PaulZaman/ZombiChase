import pygame
from sprites.Player import Player
from maps.Map import Map

class Game:
    def __init__(self, window):
        self.screen = window.screen
        self.sprites = pygame.sprite.Group()
        self.map = Map(100, 100, self)
        self.create_sprites()
        self.run()


    def create_sprites(self):
        self.player = Player(self, 350, 250, 100, "shotgun")
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
            clock.tick(80)
            pygame.display.flip()  # Update the display

        pygame.quit()

    def events(self):
        pass

    def update(self):
        for sprite in self.sprites:
            sprite.update()

        self.map.update()

    def draw(self):
        self.map.draw(self.screen)
        for sprite in self.sprites:
            sprite.draw(self.screen)
        