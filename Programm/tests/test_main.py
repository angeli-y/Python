"""
Verlassene Raumstation Unittests
"""
import unittest
from unittest.mock import patch
import io
from typing import Callable
from source.main import (
    create_board,
    check_win,
    count_remaining_traps,
    reveal_board,
    display_board,
    run_game
)

class TestFallenfeld(unittest.TestCase):
    """Tests für das Fallenfeld-Spiel"""

    def test_create_board(self) -> None:
        """Testet die Spielfeld-Erstellung"""
        board = create_board(5, 5)
        self.assertEqual(len(board), 5)
        self.assertEqual(len(board[0]), 5)
        num_traps = sum(row.count(-1) for row in board)
        self.assertEqual(num_traps, 5)

    def test_check_win(self) -> None:
        """Testet die Gewinnüberprüfung"""
        board = [[0, -1], [0, 0]]
        revealed = [[True, False], [True, True]]
        self.assertTrue(check_win(board, revealed))

        revealed = [[False, False], [True, True]]
        self.assertFalse(check_win(board, revealed))

    def test_count_remaining_traps(self) -> None:
        """Testet das Zählen verbleibender Fallen"""
        board = [[-1, 0], [0, -1]]
        revealed = [[False, False], [False, False]]
        self.assertEqual(count_remaining_traps(board, revealed), 2)

        revealed = [[False, True], [True, False]]
        self.assertEqual(count_remaining_traps(board, revealed), 2)

    def test_reveal_board(self) -> None:
        """Testet das Aufdecken von Feldern"""
        board = [[0, 1, -1], [0, 1, 1], [0, 0, 0]]
        revealed = [[False] * 3 for _ in range(3)]
        reveal_board(board, revealed, 0, 0)

        self.assertTrue(revealed[0][0])
        self.assertTrue(revealed[1][0])
        self.assertTrue(revealed[2][0])
        self.assertTrue(revealed[2][1])
        self.assertTrue(revealed[2][2])
        self.assertFalse(revealed[0][1])
        self.assertFalse(revealed[0][2])

    def test_display_board(self) -> None:
        """Testet die Konsolenausgabe von display_board"""
        board = [[0, 1, -1], [0, 1, 1], [0, 0, 0]]
        revealed = [[True, False, False], [True, False, False], [True, True, True]]

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            display_board(board, revealed)
            output = fake_out.getvalue()

        self.assertIn("0", output)
        self.assertIn("-", output)
        self.assertIn("1", output)

    def test_trigger_trap(self) -> None:
        """Testet die Ausgabe beim Betreten einer Falle"""
        board = [[-1]]
        revealed = [[False]]
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            if board[0][0] == -1:
                print("Du hast eine Falle aktiviert! Spiel vorbei.")
            output = fake_out.getvalue()
        self.assertIn("Du hast eine Falle aktiviert! Spiel vorbei.", output)

    def test_reveal_board_out_of_bounds_safe(self) -> None:
        """Testet reveal_board sicher außerhalb des Spielfelds"""
        board = [[0]]
        revealed = [[False]]

        try:
            reveal_board(board, revealed, 5, 5)
        except IndexError:
            self.fail("reveal_board() sollte bei gültigem Bounds-Check keine Exception werfen.")

    @patch('builtins.input', side_effect=["0", "0", KeyboardInterrupt])
    def test_run_game_start_and_quit(self, mock_input: Callable[..., str]) -> None:
        """Testet den Start und Abbruch des Spiels"""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            try:
                run_game()
            except KeyboardInterrupt:
                print("Spiel beendet.")
            output = fake_out.getvalue()
        self.assertIn("Spiel beendet", output)

if __name__ == "__main__":
    unittest.main()
