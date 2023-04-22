import unittest
from Logic import Logic, Color
from constants import *


class TestMovement(unittest.TestCase):
    def test_move(self):
        logic = Logic(STARTINGPOSFEN)
        self.assertEqual(logic.get_fen(), STARTINGPOSFEN)


class TestFen(unittest.TestCase):
    def test_load_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        logic = Logic(fen)
        self.assertEqual(logic.turn, Color.WHITE)
        self.assertEqual(logic.castle_rights, "KQkq")

    def test_get_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        logic = Logic(fen)
        expected_fen = fen
        self.assertEqual(logic.get_fen(), expected_fen)

    def test_complcated_fen(self):
        fen = "r1b2r2/pp4pp/1qnbpk2/3p2nQ/3P1N2/1P4PB/P4P1P/R1B2RK1 w - - 2 18"
        logic = Logic(fen)
        expected_fen = fen
        self.assertEqual(logic.get_fen(), expected_fen)


if __name__ == '__main__':
    unittest.main()
