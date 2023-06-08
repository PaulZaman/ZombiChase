import pygame as pg


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, speed):
        pg.sprite.Sprite.__init__(self)

        # image
        self.image = pg.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = x, y


        # movement
        self.direction = direction
        # normalize the direction vector
        self.direction = self.direction.normalize()

        self.speed = speed
        

    def update(self):
        # move the bullet
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # kill the bullet if it goes off screen
        if self.rect.x > 800 or self.rect.x < 0 or self.rect.y > 600 or self.rect.y < 0:
            self.kill()
          

    def draw(self, screen):
        screen.blit(self.image, self.rect)