import multiprocessing
import time

import Button
from Board import *
from Logic import Logic
from fonctions import *
import bot


class Game:
    def __init__(self, win, fen):
        self.win = win
        self.logic = Logic(fen)
        self.board = Board(BOARDSIZE)
        self.board.update(self.logic)
        self.players = {"white": "human", "black": "bot"}
        self.bot = bot.Edouard("black")
        self.buttons = [Button.Button(BLACK, GREY, WIDTH * 0.9, 15, 40, 40, pygame.quit, "X")]

    def run(self):
        game_on = True
        win_running = True
        _move_info = False
        hasTothink = True
        clock = pygame.time.Clock()
        manager = multiprocessing.Manager()
        the_list = manager.list()

        while win_running:
            clock.tick(60)
            self.win.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # si on appuie sur la croix
                    game_on = False
                # buttons
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button.isMouseon(event.pos):
                            button.onclick()
                if event.type == pygame.MOUSEMOTION:
                    for button in self.buttons:
                        if button.isMouseon(event.pos):
                            button.hover()
                        else:
                            button.default()

                # si on clique sur l'echequier
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                        isInrectangle(event.pos, BOARDTOPLEFTPOS, BOARDSIZE, BOARDSIZE):
                    self.board.attacked_cases = self.logic.cases_attacked_by(self.logic.turn)
                    # si on clique sur une case vide qui est un legal move, on effectue le move
                    move = self.board.coord_from_pos(*event.pos)
                    if move in self.board.legal_moves_to_output:
                        previous_coord = self.board.clicked_piece_coord
                        _move_info = True
                        actual_move = previous_coord, move
                        self.board.legal_moves_to_output = []
                        self.board.clicked_piece_coord = None
                    # si on clique sur une pièce
                    elif self.board.isNotempty(*self.board.coord_from_pos(*event.pos)):
                        self.board.set_to_gone(*event.pos)
                        self.board.state = "dragging"
                        i, j = self.board.coord_from_pos(*event.pos)
                        moves = self.logic.board[i][j].legal_moves(self.logic)
                        self.board.legal_moves_to_output = moves
                    # si on clique sur une case vide
                    else:
                        self.board.legal_moves_to_output = []
                    # si on lache la piece
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.state == "dragging":
                    move = self.board.coord_from_pos(*event.pos)
                    previous_coord = self.board.dragged_piece_coord
                    # on effectue le move
                    if move in self.board.legal_moves_to_output:
                        _move_info = True
                        actual_move = previous_coord, move
                        self.board.set_to_not_gone()
                        self.board.legal_moves_to_output = []
                    else:
                        self.board.set_to_not_gone()
                    self.board.state = "idle"
                # si on bouge la souris avec une pièce en main
                elif self.board.state == "dragging" and event.type == pygame.MOUSEMOTION:
                    self.board.dragged_piece_pos = event.pos

            if game_on:
                if self.players[self.logic.turn] == "human":
                    if _move_info:
                        self.logic.real_move(*actual_move[0], *actual_move[1])
                        self.board.update(self.logic)
                        if self.logic.state != "game_on":
                            game_on = False  # on arrete la boucle du jeu
                        _move_info = False

                elif self.players[self.logic.turn] == "bot":
                    genius_move = self.bot.play_random(self.logic)
                    self.logic.real_move(*genius_move)
                    self.board.update(self.logic)
                    if self.logic.state != "game_on":
                        game_on = False  # on arrete la boucle du jeu

                    # if hasTothink:
                    #     bot_process = multiprocessing.Process(target=self.bot.play_random,
                    #                                           args=(self.logic, the_list,))
                    #     bot_process.start()
                    #     hasTothink = False
            #
            # if the_list:
            #     genius_move = the_list[0]
            #     the_list = []
            #     print(genius_move)
            #     self.logic.real_move(*genius_move)
            #     self.board.update(self.logic)
            #     if self.logic.state != "game_on":
            #         game_on = False  # on arrete la boucle du jeu

            self.draw_everything()
            self.draw_winner(self.logic.state)
            pygame.display.flip()  # update l'affichage

        pygame.quit()

    def draw_everything(self):
        self.board.draw(self.win, *BOARDTOPLEFTPOS)

        for button in self.buttons:
            button.draw(self.win)

    def draw_winner(self, state):
        font = pygame.font.SysFont("monospace", 25)
        label = font.render(state, True, WHITE)
        self.win.blit(label, (15, MIDH))
