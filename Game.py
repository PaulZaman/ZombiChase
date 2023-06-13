import pygame
from sprites.Player import Player
from maps.Map import Map
from sprites.Zombi import Zombie
import random
from settings import *

class Game:
    def __init__(self, window, difficulty, weapon_info):
        self.window = window
        self.screen = window.screen
        self.sprites = pygame.sprite.Group()
        self.map = Map(MAP_WIDTH, MAP_HEIGHT, self)
        self.create_sprites(weapon_info, difficulty)
        self.difficulty = difficulty
        self.time_survived = 0
        self.back_to_menu = False
        self.weapon_info = weapon_info
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
                    pygame.quit()
                

            # color the screen white
            self.screen.fill((255, 255, 255))

            self.events()
            self.update()
            self.draw()

            if self.back_to_menu:
                running = False

            
            # FPS
            clock.tick(100)
            pygame.display.flip()  # Update the display


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

    def game_over(self):
        run = True
        while run:
            # color the screen white
            self.screen.fill(WHITE)

            # Display correct screen
            self.window.draw_text(self.window.w_tiles/2, 1, "Game Over", 50, BLACK, TILESIZE=32)


            if self.window.button(self.window.w_tiles/2, 14, 6, 2, "Back To Menu", GREY, LIGHT_GREY, WHITE, WHITE, TILESIZE=32):
                self.back_to_menu = True
                run = False
                

            if self.window.button(self.window.w_tiles/2, 17, 6, 2, "Save Results", GREY, LIGHT_GREY, WHITE, WHITE, TILESIZE=32):
                self.back_to_menu = True
                run = False

                ## ici on sauvegarde les résultats, 
                # pour le nom on envoie un nom au pif et je l'implémenterai plus tard
                res = {
                    "name": "test",
                    "weapon_info": self.weapon_info,
                    "time_survived": self.time_survived,
                    "difficulty": self.difficulty,
                    "n_bullets_shot": self.player.bullets_shot,
                    "score": self.player.score,
                    "bullets_missed": self.player.bullets_missed,
                    "zombies_killed": self.player.zombies_killed,
                    "powerups_collected": self.player.powerups_collected
                }

                print(res)
                
            # FPS
            self.window.clock.tick(60)
            pygame.display.flip()

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.back_to_menu = True
                        run = False
                        
