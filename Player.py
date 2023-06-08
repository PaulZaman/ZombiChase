import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        
        # Create a red square for the player sprite
        self.image = pg.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red color for the player sprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # player variables
        self.speed = 5

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
          self.rect.x -= self.speed
        elif keys[pg.K_RIGHT]:
          self.rect.x += self.speed
        elif keys[pg.K_UP]:
          self.rect.y -= self.speed
        elif keys[pg.K_DOWN]:
          self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)