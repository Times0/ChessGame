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
        return_list.append(self.play_well(logic, 1, color))
        end = time.time()
        print(f"Temps de reflexion du bot : {end - start:.2f}s")

    def play_well(self, logic, depth, color):
        M = True if color == Color.WHITE else False
        return self.minmax_alpha_beta_root(logic, depth, -1000, 1000, M)

    # minimax with pruning (faster)
    def minmax_alpha_beta(self, logic, depth, alpha, beta, maximizing, force_continue: bool, debug=True):
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
                    f_continue = move.is_check
                    virtual.real_move(move)

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
                    f_continue = move.is_capture
                    virtual.real_move(move)
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
        all_evals_move = []
        if maximizing:
            max_evaluation = -1000
            possible_moves = logic.ordered_legal_moves(Color.WHITE)
            for move in possible_moves:
                virtual = Logic(fen=logic.get_fen())
                virtual.real_move(move)
                force_continue = move.is_check or move.is_capture
                evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, False, force_continue)

                if evaluation >= 1000:
                    return evaluation, move
                all_evals_move.append((evaluation, move))

                alpha = max(alpha, max_evaluation)
                if alpha >= beta:
                    break
            evals = [i[0] for i in all_evals_move]
            max_evaluation = max(evals)
            all_best_eval_moves = [e for e in all_evals_move if e[0] == max_evaluation]
            return choice(all_best_eval_moves)
        else:
            min_evaluation = 1000
            possible_moves = logic.ordered_legal_moves(Color.BLACK)
            for move in possible_moves:
                virtual = Logic(fen=logic.get_fen())
                virtual.real_move(move)
                force_continue = move.is_check or move.is_capture
                evaluation, _ = self.minmax_alpha_beta(virtual, depth - 1, alpha, beta, True, force_continue)

                all_evals_move.append((evaluation, move))

                beta = min(beta, min_evaluation)
                if alpha >= beta:
                    break

            evals = [i[0] for i in all_evals_move]
            min_evaluation = min(evals)
            all_best_eval_moves = [e for e in all_evals_move if e[0] == min_evaluation]
            return choice(all_best_eval_moves)
