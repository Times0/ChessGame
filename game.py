import threading

import PygameUIKit

from ai import Bot, PlayerType
from board_ui import Board, get_x_y_w_h, pygame
from constants import *
from logic import Logic, Color, State, Square, Move

img_flip_board = pygame.image.load("assets/flip.png")
img_flip_board = pygame.transform.scale(img_flip_board, (35, 35))

BG_COLOR = (49, 46, 43)
BTN_COLOR = (114, 137, 218)
TEXT_BUTTON_COLOR = (191, 193, 197)


class Game:
    def __init__(self, win, fen):
        self.win = win
        self.logic = Logic(fen=fen)
        self.board = Board()
        self.board.update(self.logic)

        self.current_piece_legal_moves = []
        self.game_on = True
        self.window_on = True

        self.players = {Color.WHITE: PlayerType.HUMAN,
                        Color.BLACK: PlayerType.BOT}

        self.bot_is_thinking = False
        self.returnlist = [None]
        self.thread = None

        # Buttons
        font_btn = pygame.font.SysFont("None", 40)
        self.btn_new_game = PygameUIKit.button.ButtonText(BTN_COLOR, self.new_game, "New Game",
                                                          font_color=TEXT_BUTTON_COLOR, border_radius=5, font=font_btn)
        self.btn_flip_board = PygameUIKit.button.ButtonPngIcon(img_flip_board, self.flip_board)
        self.easy_objects = PygameUIKit.super_object.Group(self.btn_new_game, self.btn_flip_board)

    def run(self):
        clock = pygame.time.Clock()
        while self.window_on:
            clock.tick(60)
            self.events()
            self.bot_events()
            self.draw()

    def events(self):
        events = pygame.event.get()
        self.easy_objects.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.window_on = False
            if not self.game_on:
                continue
            turn = self.logic.turn
            if self.players[turn] == PlayerType.HUMAN:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.board.clicked(pos):
                        if self.logic.turn != self.logic.get_piece(Square(*self.board.clicked_piece_coord)).color:
                            continue
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
                                print("Move played : ", m)
                                self.current_piece_legal_moves = []
                                break

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
                if self.returnlist[0]:
                    eval_and_move = self.returnlist[0]
                    self.bot_is_thinking = False
                    e, move = eval_and_move
                    print(f"Eval found : {e}")
                    self.play(move)
                    self.returnlist = [None]

    def check_end(self):
        if self.logic.state != State.GAMEON:
            print(self.logic.state)
            self.game_on = False

    def draw(self):
        x, y, w, h = get_x_y_w_h()
        self.win.fill(BG_COLOR)
        self.board.draw(self.win, self.current_piece_legal_moves, x, y, w, h)

        W, H = self.win.get_size()
        self.btn_new_game.draw(self.win, x // 2 - self.btn_new_game.rect.w // 2, H // 2 - self.btn_new_game.rect.h // 2)
        self.btn_flip_board.draw(self.win, x + w - self.btn_flip_board.rect.w, y + h + 10)
        pygame.display.flip()

    def new_game(self):
        self.bot_is_thinking = False
        self.logic = Logic(STARTINGPOSFEN)
        self.board.update(self.logic)
        self.game_on = True
        self.current_piece_legal_moves = []

    def select(self, pos):
        self.board.select(pos)

    def flip_board(self):
        self.board.flip_board()


"""
def check_server(self):
        if self.last_retrieved_fen != self.logic.get_fen():
            print("Updating board to fit new fen")
            self.logic.load_fen(self.last_retrieved_fen)
            self.board.update(self.logic)
    
    def select(self, pos):
        self.board.select(pos)
    
    def listen_server(self):
        while True:
            data = self.socket.recv(1024)
            if data.startswith(b"fen:"):
                data = data[4:]
                print(f"Recieved fen: {data.decode()}")
                self.last_retrieved_fen = data.decode()
            else:
                print(f"Received {data!r}")
"""
