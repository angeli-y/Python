"""
Minesweeper lite

Dieses Modul implementiert das Konsolenspiel, in dem Spieler Felder aufdecken, 
ohne auf Fallen zu treten. Die Anzahl der benachbarten Fallen wird angezeigt.
(Für pylint)
"""
import random

BOARD_SIZE = 5
NUM_TRAPS = 5

def create_board(size: int, num_traps: int) -> list[list[int]]:
    """
    Erstellt ein Spielfeld
    """
    game_board = [[0 for _ in range(size)] for _ in range(size)]
    trap_positions = random.sample([(x, y) for x in range(size) for y in range(size)], num_traps)

    for trap_x, trap_y in trap_positions:
        game_board[trap_x][trap_y] = -1

    for trap_x, trap_y in trap_positions:
        for i in range(trap_x - 1, trap_x + 2):
            for j in range(trap_y - 1, trap_y + 2):
                if 0 <= i < size and 0 <= j < size and game_board[i][j] != -1:
                    game_board[i][j] += 1

    return game_board

def check_win(board: list[list[int]], revealed: list[list[bool]]) -> bool:
    """
    Überprüft auf Sieg
    """
    return all(
        board[i][j] == -1 or revealed[i][j]
        for i in range(len(board))
        for j in range(len(board))
    )

def count_remaining_traps(board: list[list[int]], revealed: list[list[bool]]) -> int:
    """
    Zählt die verbleibenden nicht aufgedeckten Fallen auf dem Spielfeld.
    Fallen (-1) sollten nie als "aufgedeckt" markiert sein.
    """
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == -1:  # Ist das eine Falle?
                if revealed[i][j]:
                    print(f"⚠ FEHLER: Falle an ({i},{j}) wurde aufgedeckt!")
                else:
                    count += 1  # Nur nicht aufgedeckte Fallen zählen!
    return count


def reveal_board(board: list[list[int]], revealed: list[list[bool]], x: int, y: int) -> None:
    """
    Deckt auf
    """
    if revealed[x][y]:
        return

    revealed[x][y] = True
    print(f"Feld ({x},{y}) aufgedeckt, Wert: {board[x][y]}")

    if board[x][y] > 0:
        return

    # Nur Nachbarfelder mit `0` rekursiv aufdecken!
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (0 <= i < len(board) and 0 <= j < len(board[0])
                and not revealed[i][j] and board[i][j] == 0):
                print(f"--> Versuche Nachbarfeld ({i},{j}) aufzudecken")
                reveal_board(board, revealed, i, j)



def display_board(board: list[list[int]], revealed: list[list[bool]]) -> None:
    """
    Erstellt ein Spielfeld
    """
    print(f"Verbleibende Fallen: {count_remaining_traps(board, revealed)}")
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if revealed[i][j]:
                print(cell if cell != -1 else 'T', end=' ')
            else:
                print('-', end=' ')
        print()

if __name__ == "__main__":
    spielfeld = create_board(BOARD_SIZE, NUM_TRAPS)
    revealed = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    GAME_OVER = False

    while not GAME_OVER:
        display_board(spielfeld, revealed)

        try:
            x = int(input("Gib die x-Koordinate ein (0-4): "))
            y = int(input("Gib die y-Koordinate ein (0-4): "))

            if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
                print("Ungültige Koordinaten. Bitte versuche es erneut.")
                continue

            if revealed[x][y]:
                print("Dieses Feld wurde bereits gescannt. Bitte wähle ein anderes Feld.")
                continue

            if spielfeld[x][y] == -1:
                print("Du hast eine Falle aktiviert! Spiel vorbei.")
                GAME_OVER = True
            else:
                reveal_board(spielfeld, revealed, x, y)
                if check_win(spielfeld, revealed):
                    print(
                        "Herzlichen Glückwunsch! "
                        "Du hast alle sicheren Felder aufgedeckt und gewonnen!"
                    )
                    GAME_OVER = True
        except ValueError:
            print("Ungültige Eingabe. Bitte gib Zahlen ein.")
        except KeyboardInterrupt:
            print("\nSpiel beendet.")
            GAME_OVER = True

    display_board(spielfeld, [[True] * BOARD_SIZE for _ in range(BOARD_SIZE)])
