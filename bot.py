import random
import time


class Edouard:
    def __init__(self, color):
        self.color = color

    def play_random(self, logic, returnlist) -> (int, int, int, int):

        choice = random.choice(logic.legal_moves(self.color))

        returnlist[0] = choice
        return choice


color = "black"
