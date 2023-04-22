import time
from random import choice

from Logic import Logic, Color, State
import enum

"https://youtu.be/l-hh51ncgDI"


class PlayerType(enum.Enum):
    HUMAN = 0
    BOT = 1


class Player:
    def __init__(self):
        pass


class Human(Player):
    def __init__(self):
        super().__init__()

    def play(self):
        pass


def play_random(logic, color: Color) -> (int, int, int, int):
    return choice(logic.legal_moves(color))


class Bot(Player):
    def __init__(self):
        super().__init__()

    def play(self, logic, return_list):
        """ Used with multiprocessing that is why we need a list"""
        print("Starting reflection..")
        start = time.time()
        color = logic.turn
        if logic.nb_pieces_on_board() > 5:
            return_list.append(self.play_well(logic, 2, color))
        else:
            return_list.append(self.play_well(logic, 3, color))
        end = time.time()
        print(f"Temps de reflexion du bot : {end - start:.2f}s")

    def play_well(self, logic, depth, color):
        M = True if color == Color.WHITE else False
        return self.minmax_alpha_beta_root(logic, depth, -1000, 1000, M)

    # minimax with pruning (faster)
    def minmax_alpha_beta(self, logic, depth, alpha, beta, maximizing, force_continue: bool, debug=False):
        logic.update_game_state()
        if debug:
            print(f"Here is the board after the move : \n {logic} \n {logic.state=}\n {maximizing=} \n\n")
        if logic.state == State.WHITEWINS:
            return 1000, None
        elif logic.state == State.BLACKWINS:
            return -1000, None
        elif logic.state == State.DRAW:
            return 0, None
        if (depth <= 0 and not force_continue) or depth < -2:
            return logic.get_static_eval(), None
        else:
            best_move = None
            if maximizing:
                max_evaluation = -1000
                possible_moves = logic.ordered_legal_moves(Color.WHITE)
                for move in possible_moves:
                    virtual = Logic(fen=logic.get_fen())
                    isCapture = virtual.isCapture(move)
                    isCheck = virtual.isCheck(move)
                    f_continue = isCapture

                    virtual.move(move)

                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False, f_continue)

                    if evaluation >= max_evaluation:
                        max_evaluation, best_move = evaluation, move
                    alpha = max(alpha, max_evaluation)
                    if alpha >= beta:
                        max_evaluation += 0.01
                        break
                return max_evaluation, best_move
            else:
                min_evaluation = 1000
                possible_moves = logic.ordered_legal_moves(Color.BLACK)
                if debug:
                    print(f"{possible_moves=}")
                for move in possible_moves:
                    virtual = Logic(fen=logic.get_fen())
                    isCapture = virtual.isCapture(move)
                    isCheck = virtual.isCheck(move)
                    f_continue = isCapture

                    virtual.move(move)

                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True, f_continue)

                    if evaluation <= min_evaluation:
                        min_evaluation, best_move = evaluation, move

                    if debug:
                        print(f"{move=}  {evaluation=}  {min_evaluation=}")
                    beta = min(beta, min_evaluation)

                    if alpha >= beta:
                        min_evaluation -= 0.01
                        break

                return min_evaluation, best_move

    def minmax_alpha_beta_root(self, logic, depth, alpha, beta, maximizing):
        allevals = []
        if maximizing:
            max_evaluation = -1000
            possible_moves = logic.ordered_legal_moves(Color.WHITE)
            for move in possible_moves:
                virtual = Logic(fen=logic.get_fen())

                virtual.move(move)

                isCheck = virtual.isCheck(move)
                if isCheck:
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth, alpha, beta, False, True)
                else:
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False, True)

                if evaluation >= 1000:
                    return evaluation, move
                allevals.append((evaluation, move))

                alpha = max(alpha, max_evaluation)
                if alpha >= beta:
                    break

            max_evaluation = max(allevals)[0]
            all_best_eval_moves = [i for i in allevals if i[0] == max_evaluation]
            return choice(all_best_eval_moves)
        else:
            min_evaluation = 1000
            possible_moves = logic.ordered_legal_moves(Color.BLACK)
            for move in possible_moves:
                virtual = Logic(fen=logic.get_fen())
                virtual.move(move)
                isCheck = virtual.isCheck(move)
                if isCheck:
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth, alpha, beta, True, True)
                else:
                    evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True, True)

                allevals.append((evaluation, move))

                beta = min(beta, min_evaluation)
                if alpha >= beta:
                    break

            min_evaluation = min(allevals)[0]
            all_best_eval_moves = [i for i in allevals if i[0] == min_evaluation]
            return choice(all_best_eval_moves)
