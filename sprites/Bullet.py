import pygame as pg


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, direction, speed, zombie_group, walls, player):
        pg.sprite.Sprite.__init__(self)

        # image
        self.image = pg.Surface((5, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.zombie_group = zombie_group
        self.walls = walls

        # movement
        self.direction = direction

        self.player = player

        # normalize the direction vector
        self.direction = self.direction.normalize()

        self.speed = speed
        

    def update(self):
        # move the bullet
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # kill the bullet if it hits a zombie
        for zombie in self.zombie_group:
            if pg.sprite.collide_rect(self, zombie):
                
                self.kill()
                zombie.hit()
        
        # kill the bullet if it hits a wall
        for wall in self.walls:
            if pg.sprite.collide_rect(self, wall):
                self.player.bullets_missed += 1
                self.kill()
                  

    def draw(self, screen):
        screen.blit(self.image, self.rect)