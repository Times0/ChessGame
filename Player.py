import time
from random import choice

from Logic import Logic, Color, State, Move
from Pieces import piece_value
import enum
import logging
import coloredlogs
import threading

# configure logging
logging.basicConfig(level=logging.DEBUG)

# initialize coloredlogs
coloredlogs.install(level="DEBUG")

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

    @staticmethod
    def play(logic, return_list):
        """ Used with multiprocessing that is why we need a list"""
        print("Starting reflection..")
        start = time.time()
        return_list[0] = play_well(logic)
        end = time.time()
        print(f"Temps de reflexion du bot : {end - start:.2f}s")


def play_well(logic, randomize=True) -> tuple[float, Move]:
    color = logic.turn
    M = True if color == Color.WHITE else False
    depth = 2
    return minmax_alpha_beta_root(logic, depth, -1000, 1000, M, randomize=randomize)


def minmax_alpha_beta(logic, depth, alpha, beta, maximizing, force_continue: bool, debug=False) \
        -> tuple[float, Move or None]:
    if debug:
        print(f"Here is the board after the move : \n {logic} \n {logic.state=}\n {maximizing=} \n\n")
    if logic.state == State.WHITEWINS:
        return 1000, None
    elif logic.state == State.BLACKWINS:
        return -1000, None
    elif logic.state == State.DRAW:
        return 0, None

    if depth <= 0 and not force_continue:
        return eval_position(logic), None
    elif depth < -2:
        return eval_position(logic), None

    else:
        best_move = None
        if maximizing:
            max_evaluation = -1000
            possible_moves = logic.ordered_legal_moves(Color.WHITE)
            for move in possible_moves:
                virtual = Logic(fen=logic.get_fen())
                f_continue = move.is_check
                virtual.real_move(move)
                new_depth = depth if force_continue else depth - 1
                evaluation, _ = minmax_alpha_beta(virtual, new_depth, alpha, beta, False, f_continue)

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
                new_depth = depth if force_continue else depth - 1
                evaluation, _ = minmax_alpha_beta(virtual, new_depth, alpha, beta, True, f_continue)

                if evaluation <= min_evaluation:
                    min_evaluation, best_move = evaluation, move
                if debug:
                    print(f"{move=}  {evaluation=}  {min_evaluation=}")
                beta = min(beta, min_evaluation)

                if alpha >= beta:
                    min_evaluation -= 0.01
                    break

            return min_evaluation, best_move


def minmax_alpha_beta_root_multithread(logic, depth, alpha, beta, maximizing, num_threads=4, debug=False,
                                       randomize=True) \
        -> tuple[float, Move]:
    all_evals_move = []
    if maximizing:
        possible_moves = logic.ordered_legal_moves(Color.WHITE)
    else:
        possible_moves = logic.ordered_legal_moves(Color.BLACK)

    if debug:
        logging.debug(f"{len(possible_moves)}")

    def evaluate_moves(moves):
        for move in moves:
            virtual = Logic(fen=logic.get_fen())
            virtual.real_move(move)
            force_continue = move.is_check or move.is_capture
            new_depth = depth if force_continue else depth - 1
            evaluation, _ = minmax_alpha_beta(virtual, new_depth, alpha, beta, not maximizing, force_continue)

            if evaluation >= 1000 and maximizing:
                all_evals_move.append((evaluation, move))
                return evaluation, move
            elif evaluation <= -1000 and not maximizing:
                all_evals_move.append((evaluation, move))
                return evaluation, move

            all_evals_move.append((evaluation, move))

    threads = []
    # Split possible moves into chunks for each thread
    moves_per_thread = len(possible_moves) // num_threads
    if debug:
        logging.debug(f"{moves_per_thread=}")
    if moves_per_thread == 0:
        chunks = [possible_moves]
    else:
        chunks = [possible_moves[i:i + moves_per_thread] for i in range(0, len(possible_moves), moves_per_thread)]
        chunks[-1] += possible_moves[moves_per_thread * num_threads:]

    for i, chunk in enumerate(chunks):
        if debug:
            logging.debug(f"{i=} {len(chunk)=}")
        t = threading.Thread(target=evaluate_moves, args=(chunk,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    evals = [i[0] for i in all_evals_move]
    if maximizing:
        max_evaluation = max(evals)
        all_best_eval_moves = [e for e in all_evals_move if e[0] == max_evaluation]
    else:
        min_evaluation = min(evals)
        all_best_eval_moves = [e for e in all_evals_move if e[0] == min_evaluation]

    if debug:
        logging.debug(f"{len(all_evals_move)}")
        logging.debug(f"{all_evals_move=}")

    if randomize:
        return choice(all_best_eval_moves)
    else:
        return all_best_eval_moves[0]


def minmax_alpha_beta_root(logic, depth, alpha, beta, maximizing, debug=False, randomize=True) -> tuple[float, Move]:
    all_evals_move = []
    if maximizing:
        possible_moves = logic.ordered_legal_moves(Color.WHITE)
    else:
        possible_moves = logic.ordered_legal_moves(Color.BLACK)

    if debug:
        logging.debug(f"{len(possible_moves)}")

    for move in possible_moves:
        virtual = Logic(fen=logic.get_fen())
        virtual.real_move(move)
        force_continue = move.is_check or move.is_capture
        new_depth = depth if force_continue else depth - 1
        evaluation, _ = minmax_alpha_beta(virtual, new_depth, alpha, beta, not maximizing, force_continue)

        if evaluation >= 1000 and maximizing:
            all_evals_move.append((evaluation, move))
            return evaluation, move
        elif evaluation <= -1000 and not maximizing:
            all_evals_move.append((evaluation, move))
            return evaluation, move

        all_evals_move.append((evaluation, move))

    evals = [i[0] for i in all_evals_move]
    if maximizing:
        max_evaluation = max(evals)
        all_best_eval_moves = [e for e in all_evals_move if e[0] == max_evaluation]
    else:
        min_evaluation = min(evals)
        all_best_eval_moves = [e for e in all_evals_move if e[0] == min_evaluation]

    if debug:
        logging.debug(f"{len(all_evals_move)}")
        logging.debug(f"{all_evals_move=}")

    if randomize:
        return choice(all_best_eval_moves)
    else:
        return all_best_eval_moves[0]


def eval_material(logic: Logic) -> float:
    white = 0
    black = 0
    for i in range(8):
        for j in range(8):
            piece = logic.board[i][j]
            if piece is not None:
                if piece.color == Color.WHITE:
                    white += piece.value
                else:
                    black += piece.value
    return white - black


def eval_position(logic: Logic) -> float:
    eval_sum = 0
    for i in range(8):
        for j in range(8):
            piece = logic.board[i][j]
            if piece is None:
                continue

            color = piece.color
            if color == Color.WHITE:
                eval_sum += piece_value[piece.abreviation]
            else:
                eval_sum -= piece_value[piece.abreviation]

            if piece.abreviation != "P":
                if piece.never_moved:
                    if color == Color.WHITE:
                        eval_sum += 0.5
                    else:
                        eval_sum -= 0.5
    return eval_sum
