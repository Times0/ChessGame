import random

import fonctions
from Logic import Logic


class Edouard:
    def __init__(self, color):
        self.color = color

    def play(self, logic, returnlist):
        """ Used with multiprocessing that is why we need a list"""
        returnlist[0] = self.play_well(logic)

    def play_random(self, logic) -> (int, int, int, int):
        choice = random.choice(logic.legal_moves(self.color))
        return choice

    def play_bad(self, logic):
        possible_moves = logic.legal_moves(self.color)

        for move in possible_moves:
            virtual = Logic(data=logic.data())
            virtual.move(*move)
            if virtual.isMate(color=fonctions.other_color(self.color)):
                return move
        else:  # redondant
            return random.choice(possible_moves)

    def play_well(self, logic):
        return self.minmax_root(logic, True if self.color == "white" else False, 2)

    def minmax(self, logic, maximizing, depth):
        if depth == 0:
            return logic.get_eval(), None
        if logic.state == "whitewins":
            return 1000, None
        elif logic.state == "blackwins":
            return -1000, None
        elif logic.state == "draw":
            print("DRAW")
            return 0
        else:
            best_move = None
            if maximizing:
                max_evaluation = -100
                possible_moves = logic.legal_moves("white")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax(virtual, False, depth - 1)
                    if evaluation >= max_evaluation:
                        max_evaluation, best_move = evaluation, move
                return max_evaluation, best_move
            else:
                min_evaluation = 100
                possible_moves = logic.legal_moves("black")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax(virtual, True, depth - 1)
                    if evaluation <= min_evaluation:
                        min_evaluation, best_move = evaluation, move
                return min_evaluation, best_move

    def minmax_root(self, logic, maximizing, depth):
        # print(f'maximizing : {maximizing}')
        # print(f"algo2, depth : {depth}")
        if depth == 0:
            # print(logic.get_eval())
            return logic.get_eval(), None
        if logic.state != "game_on":
            return "end"

        else:
            # game pas terminée
            allevals = []
            if maximizing:
                possible_moves = logic.legal_moves("white")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax(virtual, False, depth - 1)
                    allevals.append((evaluation, move))
                max_evaluation = max(allevals)[0]
                all_best_eval_moves = [i for i in allevals if i[0] == max_evaluation]
                return random.choice(all_best_eval_moves)
            else:
                possible_moves = logic.legal_moves("black")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax(virtual, True, depth - 1)
                    allevals.append((evaluation, move))
                min_evaluation = min(allevals)[0]
                all_best_eval_moves = [i for i in allevals if i[0] == min_evaluation]
                return random.choice(all_best_eval_moves)
