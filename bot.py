import random
import time
from Logic import Logic
import fonctions


class Edouard:
    def __init__(self, color):
        self.color = color

    def play(self, logic, returnlist):
        """ Used with multiprocessing that is why we need a list"""
        returnlist[0] = self.play_bad(logic)

    def play_random(self, logic) -> (int, int, int, int):
        choice = random.choice(logic.legal_moves(self.color))
        return choice

    def play_bad(self, logic):
        possible_moves = logic.legal_moves(self.color)

        for move in possible_moves:
            virtual = Logic(logic.get_fen())
            virtual.move(*move)
            if virtual.isMate(color=fonctions.other_color(self.color)):
                return move
        else:  # redondant
            return random.choice(possible_moves)
