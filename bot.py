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

    # minimax with pruning (better)
    def minmax_alpha_beta(self, logic, depth, alpha, beta, maximizing, capture: bool):
        color = "white" if maximizing else "black"
        if logic.isIncheck(color) or logic.nb_pieces_on_board() < 5:
            logic.update_game_state(color)

        if logic.state == "whitewins":
            return 1000, None
        elif logic.state == "blackwins":
            return -1000, None
        elif logic.state == "draw":
            return 0, None
        if depth <= 0 and not capture:
            return logic.get_static_eval(), None
        else:
            best_move = None
            if maximizing:
                max_evaluation = -100
                possible_moves = logic.legal_moves("white")
                for move in possible_moves:
                    virtual = Logic(data2=logic.get_data())
                    isCapture = virtual.isCapture(*move)
                    virtual.move(*move)
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False, isCapture)
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
                    virtual = Logic(data2=(logic.get_data()))
                    isCapture = virtual.isCapture(*move)
                    virtual.move(*move)
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True, isCapture)
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
            max_evaluation = -100
            possible_moves = logic.legal_moves("white")
            for move in possible_moves:
                virtual = Logic(data2=logic.get_data())
                virtual.move(*move)
                evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False, True)
                allevals.append((evaluation, move))
                if evaluation >= max_evaluation:
                    max_evaluation, best_move = evaluation, move
                alpha = max(alpha, max_evaluation)
                if alpha >= beta:
                    break
            max_evaluation = max(allevals)[0]
            all_best_eval_moves = [i for i in allevals if i[0] == max_evaluation]
            return choice(all_best_eval_moves)
        else:
            min_evaluation = 100
            possible_moves = logic.legal_moves("black")
            for move in possible_moves:
                virtual = Logic(data2=(logic.get_data()))
                virtual.move(*move)
                evaluation, best_move = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True, True)
                allevals.append((evaluation, move))
                if evaluation <= min_evaluation:
                    min_evaluation, best_move = evaluation, move
                beta = min(beta, min_evaluation)
                if alpha >= beta:
                    break

            min_evaluation = min(allevals)[0]
            all_best_eval_moves = [i for i in allevals if i[0] == min_evaluation]
            return choice(all_best_eval_moves)
