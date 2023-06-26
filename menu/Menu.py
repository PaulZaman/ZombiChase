from Game import Game
from settings import *
from dbSetup import *
from collections import deque
import pygame as pg
import time
from heapq import nlargest
import json
import sys


class Menu:
    def __init__(self, window):
        self.window = window
        self.screenIsOn = "main-menu"
        self.fullscreen = False

        self.w_tiles = self.window.width / TILESIZE
        self.h_tiles = self.window.height / TILESIZE

        self.bg = pg.transform.scale(pg.image.load(IMAGE_DIR + "/bg.jpg"), (self.window.width, self.window.height))

        self.main_loop()
        
        """weapon = {
            "name": "handgun",
            "image":pg.transform.rotate(pg.transform.scale(pg.image.load(IMAGE_DIR + "/player/handgun/idle/survivor-idle_handgun_0.png"), (128, 128)), 90),
            "damage": 1,
            "fire_rate": 1000,
            "bullet_speed":20,
            "n_bullets":1,
            "precision":15,
        }
        self.game = Game(self.window, 2, weapon)"""
        # example weapon
        
    def init_game_params(self):
        self.game_difficulty = 5
        self.game_weapon = "pistol"
         
    def init_weapons(self):
        self.pistol_object = {
            "name": "handgun",
            "image":pg.transform.rotate(pg.transform.scale(pg.image.load(IMAGE_DIR + "/player/handgun/idle/survivor-idle_handgun_0.png"), (128, 128)), 90),
            "damage": 2,
            "fire_rate": 1200,
            "bullet_speed":20,
            "n_bullets":1,
            "precision":15,
        }

        self.rifle_object = {
            "name": "rifle",
            "image":pg.transform.rotate(pg.transform.scale(pg.image.load(IMAGE_DIR + "/player/rifle/idle/survivor-idle_rifle_0.png"), (150, 128)), 90),
            "damage": 1,
            "fire_rate": 500,
            "bullet_speed":15,
            "n_bullets":1,
            "precision":10,
        }

        self.shotgun_object = {
            "name": "shotgun",
            "image":pg.transform.rotate(pg.transform.scale(pg.image.load(IMAGE_DIR + "/player/shotgun/idle/survivor-idle_shotgun_0.png"), (150, 128)), 90),
            "damage": 1,
            "fire_rate": 1500,
            "bullet_speed":10,
            "n_bullets":3,
            "precision":30,
        }

        self.weapons = [self.pistol_object, self.rifle_object, self.shotgun_object]

        self.selected_weapon_index = 0

    def init_game(self):
        self.game = Game(self.window, self.game_difficulty, self.weapons[self.selected_weapon_index])
        self.game = None

    def main_loop(self):
        run = True
        while run:
            # display bg
            self.window.screen.blit(self.bg, (0, 0))

            # Display correct screen
            if self.screenIsOn == "main-menu":
                self.main_menu()
            elif self.screenIsOn == "start-game":
                self.game_params()
            elif self.screenIsOn == "settings":
                self.settings()
            elif self.screenIsOn == "highscores":
                self.highscores()
            elif self.screenIsOn == "credits":
                self.credits()    

            # grid
            #self.window.draw_grid()            

            # FPS
            self.window.clock.tick(60)
            pg.display.flip()  # Update the display

            # Check for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
            
    def main_menu(self):
        # Main Menu

        # Title
        self.window.draw_text(self.w_tiles/2, 1, "ZombiChase", 50, BLACK, TILESIZE=32)

        # x, y, w, h, text, button_color, button_hover_color, text_color, text_hover_color, border_radius=10, text_size=30, TILESIZE=1
        if self.window.button(self.w_tiles/2, 4, 10, 2, "Start Game", BLUE3, BLUE, BEIGE, BEIGE, TILESIZE=32):
            self.screenIsOn = "start-game"
            self.init_game_params()
            self.init_weapons()
            return

        if self.window.button(self.w_tiles/2, 7, 10, 2, "Settings", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=32):
            self.screenIsOn = "settings"
            return
        
        if self.window.button(self.w_tiles/2, 10, 10, 2, "Highscores", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=32):
            self.screenIsOn = "highscores"
            self.filter_highscore()
            return
        
        if self.window.button(self.w_tiles/2, 13, 10, 2, "Credits", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=32):
            self.screenIsOn = "credits"
            return
        
        if self.window.button(self.w_tiles/2, 16, 10, 2, "Quit", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=32):
            pg.quit()
            sys.exit()

    def game_params(self):
        # Screen to select game parameters, weapon, difficulty, start button

        # Title
        self.window.draw_text(self.w_tiles/2, 1, "Game Parameters", 50, BLACK, TILESIZE=TILESIZE)

        # Weapon
        self.show_weapons()

        # Difficulty
        self.window.draw_text(self.w_tiles/2, 4, "Difficulty", 20, BLACK, TILESIZE=TILESIZE)
        self.window.draw_text(self.w_tiles/2, 5.2, str(self.game_difficulty), 20, BLACK, TILESIZE=TILESIZE)
        if self.window.draw_arrow(self.w_tiles/2 + 2, 5, 1.5, 1, 0.3, BLUE, "right", 1.2, TILESIZE=TILESIZE):
            self.game_difficulty = min(self.game_difficulty + 1, 10)
        if self.window.draw_arrow(self.w_tiles/2 - 3.5, 5, 1.5, 1, 0.3, BLUE, "left", 1.2, TILESIZE=TILESIZE):
            self.game_difficulty = max(self.game_difficulty - 1, 1)

        if self.window.button(8 + self.w_tiles/2, 15, 5, 2, "Start", BLUE3, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.init_game()
            self.screenIsOn = "main-menu"
            time.sleep(0.1)
            return
        
        if self.window.button(self.w_tiles/2 - 8, 15, 5, 2, "Back", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.screenIsOn = "main-menu"
            time.sleep(0.1)
            return

    def show_weapons(self):
        # show weapons box
        rect = pg.Surface((9*TILESIZE, 11*TILESIZE), pg.SRCALPHA)
        rect.fill(BEIGE)
        rect.set_alpha(200)
        self.window.screen.blit(rect, ((self.w_tiles/2 - 4.5)*TILESIZE, 7*TILESIZE))
        self.window.draw_text(self.w_tiles/2, 7.5, self.weapons[self.selected_weapon_index]["name"], 20, BLACK, TILESIZE=TILESIZE)

        # blit image
        #W = self.weapons[self.selected_weapon_index]["image"].get_width()
        H = self.weapons[self.selected_weapon_index]["image"].get_height()
        self.window.screen.blit(self.weapons[self.selected_weapon_index]["image"], ((self.w_tiles/2 - 2)*TILESIZE, 12*TILESIZE + 15 - H))

        # arrows
        if self.window.draw_arrow(self.w_tiles/2 + 2, 10, 1.5, 1, 0.3, BLUE, "right", 1.2, TILESIZE=TILESIZE):
            self.selected_weapon_index = (self.selected_weapon_index + 1) % len(self.weapons)
        if self.window.draw_arrow(self.w_tiles/2 - 3.5, 10, 1.5, 1, 0.3, BLUE, "left", 1.2, TILESIZE=TILESIZE):
            self.selected_weapon_index = (self.selected_weapon_index - 1) % len(self.weapons)

        # weapon stats
        # weapon fire rate bar (maximum is 100, minimum is 1500)
        self.window.draw_text(self.w_tiles/2 - 2, 12, "Fire rate : ", 15, BLACK, TILESIZE=TILESIZE)
        pg.draw.rect(self.window.screen, BLACK, ((self.w_tiles/2)*TILESIZE, 12*TILESIZE, 4*TILESIZE, 0.5*TILESIZE))
        pg.draw.rect(self.window.screen, GREEN, ((self.w_tiles/2)*TILESIZE, 12*TILESIZE, 4*TILESIZE - int((self.weapons[self.selected_weapon_index]["fire_rate"])/15), 0.5*TILESIZE))

        # weapon precision bar (max is 0, min is 30)
        self.window.draw_text(self.w_tiles/2 - 2, 13.5, "Precision : ", 15, BLACK, TILESIZE=TILESIZE)
        pg.draw.rect(self.window.screen, BLACK, ((self.w_tiles/2)*TILESIZE, 13.5*TILESIZE, 4*TILESIZE, 0.5*TILESIZE))
        pg.draw.rect(self.window.screen, GREEN, ((self.w_tiles/2)*TILESIZE, 13.5*TILESIZE, 4*TILESIZE - int((self.weapons[self.selected_weapon_index]["precision"])*3), 0.5*TILESIZE))

        # bullet speed bar (max is 30, min is 0)
        self.window.draw_text(self.w_tiles/2 - 2, 15.5, "Bullet speed : ", 15, BLACK, TILESIZE=TILESIZE)
        pg.draw.rect(self.window.screen, BLACK, ((self.w_tiles/2 )*TILESIZE, 15.5*TILESIZE, 4*TILESIZE, 0.5*TILESIZE))
        pg.draw.rect(self.window.screen, GREEN, ((self.w_tiles/2 )*TILESIZE, 15.5*TILESIZE, int((self.weapons[self.selected_weapon_index]["bullet_speed"])*10/3), 0.5*TILESIZE))

        # weapon damage
        self.window.draw_text(self.w_tiles/2 - 2, 16.7, "Damage : " + str(self.weapons[self.selected_weapon_index]["damage"]), 15, BLACK, TILESIZE=TILESIZE)
        
        # weapon bullets (max is 10, min is 1)
        self.window.draw_text(self.w_tiles/2 + 2, 16.7, "Bullets : " + str(self.weapons[self.selected_weapon_index]["n_bullets"]), 15, BLACK, TILESIZE=TILESIZE)

    def settings(self):
        # Screen to change settings
        self.window.draw_text(self.w_tiles/2, 2, "Settings", 30, BLACK, TILESIZE=TILESIZE)

        # Set fullscreen
        if self.window.button(self.w_tiles/2, 5, 8, 2, "Fullscreen", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.fullscreen = not self.fullscreen
            self.window.screen = pg.display.set_mode((self.w_tiles*TILESIZE, self.h_tiles*TILESIZE), pg.FULLSCREEN if self.fullscreen else 0)
            time.sleep(0.1)

        # back button
        if self.window.button(self.w_tiles/2, 15, 8, 2, "Back", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.screenIsOn = "main-menu"
            time.sleep(0.1)

    def credits(self):
        # draw rect for credits
        rect = pg.Surface((15*TILESIZE, 13*TILESIZE), pg.SRCALPHA)
        rect.fill(BEIGE)
        rect.set_alpha(200)        
        self.window.screen.blit(rect, (5*TILESIZE, TILESIZE))

        # title
        self.window.draw_text(self.w_tiles/2, 2, "Credits", 30, BLACK, TILESIZE=TILESIZE)

        # made by
        self.window.draw_text(self.w_tiles/2, 5, "Made by : ", 20, BLACK, TILESIZE=TILESIZE)
        self.window.draw_text(self.w_tiles/2, 6, "- Matthieu Vichet", 20, BLACK, TILESIZE=TILESIZE)
        self.window.draw_text(self.w_tiles/2, 7, "- Nelsa Yago", 20, BLACK, TILESIZE=TILESIZE)   
        self.window.draw_text(self.w_tiles/2, 8, "- Paul Zamanian", 20, BLACK, TILESIZE=TILESIZE)   

        # github link
        self.window.draw_text(self.w_tiles/2, 10, "Github link : ", 20, BLACK, TILESIZE=TILESIZE)
        self.window.draw_text(self.w_tiles/2, 11, "https://github.com/PaulZaman/ZombiChase", 20, BLACK, TILESIZE=TILESIZE)   

        # back button
        if self.window.button(self.w_tiles/2, 15, 8, 2, "Back", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.screenIsOn = "main-menu"
            time.sleep(0.1)

    def highscores(self):
        self.window.draw_text(self.w_tiles / 2, 1, "Highscores", 30, BLACK, TILESIZE=TILESIZE)

        # draw a almost transparent black rectangle to make the text more readable
        rect = pg.Surface((self.w_tiles*TILESIZE, (self.h_tiles-4)*TILESIZE), pg.SRCALPHA) 
        rect.fill((0, 0, 0, 100))
        self.window.screen.blit(rect, (0, 2*TILESIZE))

        # Table headers
        headers = ["Rank", "Name", "Score", "Duration", "Zombies Killed", "Difficulty", "Bullets Shot", "Weapon Info"]
        row_height = 1
        self.window.draw_text(self.w_tiles / 2, 3, "     ".join(headers), 17, WHITE, TILESIZE=TILESIZE)

        # Display highscores as a table
        for i, entry in enumerate(self.filtered_data):
            rank = str(i + 1)
            name = entry['name']
            score = str(entry['score'])
            time_survived = str(entry['time_survived'])
            zombies_killed = str(entry['zombies_killed'])
            difficulty = str(entry['difficulty'])
            bullets_shot = str(entry['n_bullets_shot'])
            weapon_info = entry['weapon_info']['name']

            # Calculate the position of each column
            rank_x = self.w_tiles / 2 - 12
            name_x = self.w_tiles / 2 - 9.5
            score_x = self.w_tiles / 2 - 7
            time_x = self.w_tiles / 2 - 4.5
            zombies_x = self.w_tiles / 2  - 1
            difficulty_x = self.w_tiles / 2 + 3
            bullets_x = self.w_tiles / 2 + 6.5
            weapon_x = self.w_tiles / 2 + 10.5

            # Display each column value
            y = 3 + (i + 1) * row_height
            self.window.draw_text(rank_x, y, rank, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(name_x, y, name, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(score_x, y, score, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(time_x,y, str(int(int(float(time_survived)) /1000))+"s", 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(zombies_x, y, zombies_killed, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(difficulty_x, y, difficulty, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(bullets_x, y, bullets_shot, 18, WHITE, TILESIZE=TILESIZE)
            self.window.draw_text(weapon_x, y, weapon_info, 18, WHITE, TILESIZE=TILESIZE)

                # back button
        if self.window.button(self.w_tiles/2, 15, 8, 2, "Back", BLUE2, BLUE, BEIGE, BEIGE, TILESIZE=TILESIZE):
            self.screenIsOn = "main-menu"
            time.sleep(0.1)

    def filter_highscore(self):
        

        ref = db.reference('/')  # Replace with the path to your data
        data = ref.get()
        if data is None:
            self.filtered_data = []
            return

        self.filtered_data = []
        keys = deque(data.keys())  # Store the keys in a deque for easy accessfor _ in range(10):
        for _ in range(10):
            if not keys:
                break
            key = keys.pop()
            value = data[key]
            if 'name' in value and 'score' in value and 'time_survived' in value and 'zombies_killed' in value and 'difficulty' in value and 'n_bullets_shot' in value and 'weapon_info' in value:
                entry = {
                    'name': value['name'],
                    'score': value['score'],
                    'time_survived': value['time_survived'],
                    'zombies_killed': value['zombies_killed'],
                    'difficulty': value['difficulty'],
                    'n_bullets_shot': value['n_bullets_shot'],
                    'weapon_info': value['weapon_info']
                }
                self.filtered_data.append(entry)

                                        # Use the filtered data
            # Filter out entries with None scores
        self.filtered_data = [entry for entry in self.filtered_data if entry['score'] is not None]

            # Get the 10 entries with the highest scores
        self.filtered_data = nlargest(10, self.filtered_data, key=lambda entry: entry['score'])

