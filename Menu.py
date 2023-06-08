from Game import Game

class Menu:
    def __init__(self, window):
        self.window = window
        self.game = Game(self.window)
