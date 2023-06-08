import pygame

class Game:
    def __init__(self, window):
        print("Game init")
        self.screen = window.screen
        self.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.events()
            self.update()
            self.draw()

            pygame.display.flip()  # Update the display

        pygame.quit()

    def events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass