import numpy as np


# toute la partie back, juste la logique

class Logic:
    def __init__(self):
        self.board = [["br", "bk", "bb", "bq", "bking", 'bb', 'bk', 'br'],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " "],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wr", "wk", "wb", "wq", "wking", 'wb', 'wk', 'wr']
                      ]
        self.turn = 0

    
