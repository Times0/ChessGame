import time
from random import choice

from Logic import Logic
from fonctions import other_color

"https://youtu.be/l-hh51ncgDI"


class Edouard:
    def __init__(self, color):
        self.color = color

    def play(self, logic, returnlist):
        """ Used with multiprocessing that is why we need a list"""
        start = time.time()
        returnlist[0] = self.play_well(logic)
        end = time.time()
        print(f"Temps de reflexion du bot : {end - start}s\n")

    def play_random(self, logic) -> (int, int, int, int):
        choicee = choice(logic.legal_moves(self.color))
        return choicee

    def play_bad(self, logic):
        possible_moves = logic.legal_moves(self.color)

        for move in possible_moves:
            virtual = Logic(data=logic.data())
            virtual.move(*move)
            if virtual.isMate(color=other_color(self.color)):
                return move
        else:  # redondant
            return choice(possible_moves)

    def play_well(self, logic):
        return self.minmax_alpha_beta_root(logic, 3, -100, 100, True if self.color == "white" else False)

    # minimax without pruning
    def minmax(self, logic, depth, maximizing):
        logic.update_game_state("white" if maximizing else "black")
        if depth == 0:
            return logic.get_static_simple_eval(), None
        if logic.state == "whitewins":
            return 1000, None
        elif logic.state == "blackwins":
            return -1000, None
        elif logic.state == "draw":
            return 0, None
        else:
            best_move = None
            if maximizing:
                max_evaluation = -100
                possible_moves = logic.legal_moves("white")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, idk = self.minmax(virtual, depth - 1, False)
                    if evaluation >= max_evaluation:
                        max_evaluation, best_move = evaluation, idk
                return max_evaluation, best_move
            else:
                min_evaluation = 100
                possible_moves = logic.legal_moves("black")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, idk = self.minmax(virtual, depth - 1, True)
                    if evaluation <= min_evaluation:
                        min_evaluation, best_move = evaluation, idk
                return min_evaluation, best_move

    def minmax_root(self, logic, depth, maximizing):
        # print(f'maximizing : {maximizing}')
        # print(f"algo2, depth : {depth}")

        # game pas terminée
        allevals = []
        if maximizing:
            possible_moves = logic.legal_moves("white")
            for move in possible_moves:
                virtual = Logic(data=(logic.data()))
                virtual.move(*move)
                evaluation, _ = self.minmax(virtual, depth - 1, False)
                allevals.append((evaluation, move))
            max_evaluation = max(allevals)[0]
            print(allevals, max_evaluation)
            all_best_eval_moves = [i for i in allevals if i[0] == max_evaluation]
            return choice(all_best_eval_moves)
        else:
            possible_moves = logic.legal_moves("black")
            for move in possible_moves:
                virtual = Logic(data=(logic.data()))
                virtual.move(*move)
                evaluation, best_move = self.minmax(virtual, depth - 1, True)
                allevals.append((evaluation, move))
            min_evaluation = min(allevals)[0]
            all_best_eval_moves = [i for i in allevals if i[0] == min_evaluation]
            return choice(all_best_eval_moves)

    # minimax with pruning
    def minmax_alpha_beta(self, logic, depth, alpha, beta, maximizing):
        logic.update_game_state("white" if maximizing else "black")

        if depth == 0:
            return logic.get_static_eval(), None
        elif logic.state == "whitewins":
            return 1000, None
        elif logic.state == "blackwins":
            return -1000, None
        elif logic.state == "draw":
            return 0, None
        else:
            best_move = None
            if maximizing:
                max_evaluation = -100
                possible_moves = logic.legal_moves("white")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False)
                    if evaluation >= max_evaluation:
                        max_evaluation, best_move = evaluation, move
                    alpha = max(alpha, max_evaluation)
                    if alpha >= beta:
                        break
                return max_evaluation, best_move
            else:
                min_evaluation = 100
                possible_moves = logic.legal_moves("black")
                for move in possible_moves:
                    virtual = Logic(data=(logic.data()))
                    virtual.move(*move)
                    evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True)
                    if evaluation <= min_evaluation:
                        min_evaluation, best_move = evaluation, move
                    beta = min(beta, min_evaluation)
                    if alpha >= beta:
                        break
                return min_evaluation, best_move

    def minmax_alpha_beta_root(self, logic, depth, alpha, beta, maximizing):
        # print(f'maximizing : {maximizing}')
        # print(f"algo2, depth : {depth}")

        # game pas terminée
        allevals = []
        if maximizing:
            possible_moves = logic.legal_moves("white")
            for move in possible_moves:
                virtual = Logic(data=(logic.data()))
                virtual.move(*move)
                evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False)
                allevals.append((evaluation, move))

            max_evaluation = max(allevals)[0]

            all_best_eval_moves = [i for i in allevals if i[0] == max_evaluation]
            return choice(all_best_eval_moves)
        else:
            possible_moves = logic.legal_moves("black")
            for move in possible_moves:
                virtual = Logic(data=(logic.data()))
                virtual.move(*move)
                evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True)
                allevals.append((evaluation, move))

            min_evaluation = min(allevals)[0]

            all_best_eval_moves = [i for i in allevals if i[0] == min_evaluation]
            return choice(all_best_eval_moves)
