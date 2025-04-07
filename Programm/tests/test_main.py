import unittest
from source.main import create_board, check_win, count_remaining_traps, reveal_board
from unittest.mock import patch
import io

class TestFallenfeld(unittest.TestCase):
    """ Tests für das Fallenfeld-Spiel """
    
    def test_create_board(self):
        """ Testet die Spielfeld-Erstellung """
        board = create_board(5, 5)
        self.assertEqual(len(board), 5)
        self.assertEqual(len(board[0]), 5)
        num_traps = sum(row.count(-1) for row in board)
        self.assertEqual(num_traps, 5)
    
    def test_check_win(self):
        """ Testet die Gewinnüberprüfung """
        board = [[0, -1], [0, 0]]
        revealed = [[True, False], [True, True]]
        self.assertTrue(check_win(board, revealed))
        
        revealed = [[False, False], [True, True]]
        self.assertFalse(check_win(board, revealed))
    
    def test_count_remaining_traps(self):
        """ Testet das Zählen verbleibender Fallen """
        board = [[-1, 0], [0, -1]]
        revealed = [[False, False], [False, False]]  # Keine Felder aufgedeckt
        self.assertEqual(count_remaining_traps(board, revealed), 2)  # ✅ Sollte 2 Fallen zählen

        revealed = [[False, False], [False, False]]  # Immer noch keine Falle aufgedeckt
        self.assertEqual(count_remaining_traps(board, revealed), 2)  # ✅ Immer noch 2

        revealed = [[False, True], [True, False]]  # Sichere Felder (0) aufgedeckt, Fallen bleiben verdeckt
        self.assertEqual(count_remaining_traps(board, revealed), 2)  # ✅ Immer noch 2

        revealed = [[False, True], [True, False]]  # Nur sichere Felder aufdecken!
        self.assertEqual(count_remaining_traps(board, revealed), 2)  # ✅ Stimmt!

    
    def test_reveal_board(self):
        """ Testet das Aufdecken von Feldern """
        board = [[0, 1, -1], [0, 1, 1], [0, 0, 0]]
        revealed = [[False] * 3 for _ in range(3)]
        reveal_board(board, revealed, 0, 0)
        
        # Alle verbundenen 0-Felder sollten aufgedeckt sein
        self.assertTrue(revealed[0][0])
        self.assertTrue(revealed[1][0])
        self.assertTrue(revealed[2][0])
        self.assertTrue(revealed[2][1])
        self.assertTrue(revealed[2][2])

        # Die 1er-Zelle sollte noch nicht aufgedeckt sein
        self.assertFalse(revealed[0][1])
        self.assertFalse(revealed[0][2])
    
    def test_display_board(self):
        """ Testet die Konsolenausgabe von display_board """
        board = [[0, 1, -1], [0, 1, 1], [0, 0, 0]]
        revealed = [[True, False, False], [True, False, False], [True, True, True]]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            from source.main import display_board
            display_board(board, revealed)
            output = fake_out.getvalue()

        self.assertIn("0", output)
        self.assertIn("-", output)  # Verdeckte Felder
        self.assertIn("1", output)  # Enthüllte Zahl

if __name__ == "__main__":
    unittest.main()
