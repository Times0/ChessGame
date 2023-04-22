import threading

import Button
from Board_ui import Board, get_x_y_w_h, pygame
from Logic import Logic, Color, State, Square, Move
from constants import *
from tools.button import TextButton
from Player import Human, Bot, PlayerType


class Game:
    def __init__(self, win, fen):
        self.win = win
        self.logic = Logic(fen=fen)
        self.board = Board(BOARDSIZE)
        self.board.update(self.logic)

        self.current_piece_legal_moves = []
        self.game_on = True
        self.window_on = True

        self.players = {Color.WHITE: PlayerType.HUMAN,
                        Color.BLACK: PlayerType.HUMAN}

        self.bot_is_thinking = False
        self.returnlist = []
        self.thread = None

        # Buttons
        self.buttons = []
        self.btn_new_game = TextButton("New Game", 10, 50, pygame.font.SysFont("Arial", 32), WHITE)
        self.btn_flip_board = TextButton("Flip Board", 10, 100, pygame.font.SysFont("Arial", 32), WHITE)
        self.buttons.extend((self.btn_new_game, self.btn_flip_board))

    def run(self):
        clock = pygame.time.Clock()
        while self.window_on:
            clock.tick(60)
            self.events()
            self.bot_events()
            self.draw()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.window_on = False

            self.check_buttons(events)
            if not self.game_on:
                continue
            turn = self.logic.turn
            if self.players[turn] == PlayerType.HUMAN:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.board.clicked(pos):
                        print("Clicked on a piece")
                        self.current_piece_legal_moves = self.logic.get_legal_moves_piece(
                            Square(*self.board.clicked_piece_coord))

                if self.board.dragging:
                    if event.type == pygame.MOUSEMOTION:
                        pos = pygame.mouse.get_pos()
                        self.board.drag(pos)

                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        dest_coord = self.board.drop(pos)
                        move = Move(Square(*self.board.clicked_piece_coord), Square(*dest_coord))
                        for m in self.current_piece_legal_moves:
                            if m == move:
                                self.play(m)
                                print("Move is : ", m)
                                self.current_piece_legal_moves = []

    def play(self, move):
        self.logic.real_move(move)
        self.board.update(self.logic)
        self.check_end()

    def bot_events(self):
        if not self.game_on:
            return
        turn = self.logic.turn
        if self.players[turn] == PlayerType.BOT:
            if not self.bot_is_thinking:
                self.bot_is_thinking = True
                # Start the thinking thread
                p = Bot()
                self.thread = threading.Thread(target=p.play, args=(self.logic, self.returnlist))
                self.thread.start()
            else:
                # Check if the move was found
                if self.returnlist:
                    eval_and_move = self.returnlist[0]
                    self.bot_is_thinking = False
                    e, move = eval_and_move
                    print(f"Eval found : {e}")
                    self.play(move)
                    self.returnlist = []

    def check_buttons(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.btn_new_game.tick():
                    self.bot_is_thinking = False
                    self.logic = Logic(STARTINGPOSFEN)
                    self.board.update(self.logic)
                    self.game_on = True
                    self.current_piece_legal_moves = []
                if self.btn_flip_board.tick():
                    self.board.flip_board()

    def check_end(self):
        if self.logic.state != State.GAMEON:
            print(self.logic.state)
            self.game_on = False

    def draw(self):
        self.win.fill(BLACK)
        self.board.draw(self.win, self.current_piece_legal_moves, *get_x_y_w_h())
        for button in self.buttons:
            button.draw(self.win)
        pygame.display.flip()

    def select(self, pos):
        self.board.select(pos)
