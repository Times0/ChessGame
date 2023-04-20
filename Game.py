import Button
from Board_ui import Board, get_x_y_w_h, pygame
from Logic import Logic, Color
from constants import *
from tools.button import TextButton


class Game:
    def __init__(self, win, fen):
        self.win = win
        self.logic = Logic(fen=fen)
        self.board = Board(BOARDSIZE)
        self.board.update(self.logic)

        self.current_piece_legal_moves = []
        self.game_on = True


        # Buttons
        self.buttons = []
        self.btn_new_game = TextButton("New Game", 10, 50, pygame.font.SysFont("Arial", 32), WHITE)
        self.buttons.append(self.btn_new_game)

    def run(self):
        clock = pygame.time.Clock()
        while self.game_on:
            clock.tick(60)
            self.events()
            self.draw()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game_on = False

            self.check_buttons(events)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.board.clicked(pos):
                    l = self.logic.get_legal_moves_piece(*self.board.clicked_piece_coord)
                    self.current_piece_legal_moves = l

            if self.board.dragging:
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    self.board.drag(pos)

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    move = self.board.drop(pos)
                    for i, j, c in self.current_piece_legal_moves:
                        if move == (i, j):
                            self.current_piece_legal_moves = []
                            self.logic.real_move(self.board.clicked_piece_coord + move + (c,))
                            self.board.update(self.logic)

    def check_buttons(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.btn_new_game.tick():
                    self.logic = Logic(STARTINGPOSFEN)
                    self.board.update(self.logic)
                    self.current_piece_legal_moves = []

    def draw(self):
        self.win.fill(BLACK)
        self.board.draw(self.win, self.current_piece_legal_moves, *get_x_y_w_h())
        for button in self.buttons:
            button.draw(self.win)
        pygame.display.flip()

    def select(self, pos):
        self.board.select(pos)
