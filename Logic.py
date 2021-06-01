import numpy as np


# toute la partie back, juste la logique

class Logic:
    def __init__(self):

        self.board = [["br", "bn", "bb", "bq", "bk", 'bb', 'bn', 'br'],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wr", "wn", "wb", "wq", "wk", 'wb', 'wn', 'wr']
                      ]
        self.turn = 0

        def load_fen(fen):
            pass
