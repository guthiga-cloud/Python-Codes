"""
tic_tac_toe.py
Two-player (or vs simple AI) Tic-Tac-Toe with a clean board.
- 3x3 board, numbered positions 1-9
- Human vs Human OR Human vs Computer
- Win/draw detection, safe input, replay loop
No external dependencies — pure stdlib.
"""

import random
import sys

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def new_board():
    return [" "] * 9


def print_board(b):
    print()
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            cell = b[i + j]
            if cell == " ":
                row.append(str(i + j + 1))   # show position number
            else:
                row.append(cell)
        print("   " + " | ".join(row))
        if i < 6:
            print("  ---+---+---")
    print()


def get_winner(b):
    for a, c, d in WIN_LINES:
        if b[a] == b[c] == b[d] != " ":
            return b[a]
    return None


def is_full(b):
    return all(c != " " for c in b)


def free_positions(b):
    return [i for i, c in enumerate(b) if c == " "]


def human_move(b, player):
    while True:
        raw = input(f"Player {player}, pick (1-9): ").strip()
        if not raw.isdigit():
            print("❌ Enter a number 1-9.")
            continue
        pos = int(raw) - 1
        if not 0 <= pos < 9:
            print("❌ Out of range. Pick 1-9.")
            continue
        if b[pos] != " ":
            print("❌ That square is taken.")
            continue
        return pos


def ai_move(b, ai, human):
    """Simple AI: win if possible, block if needed, else center/corner/random."""
    # 1. Try to win
    for a, c, d in WIN_LINES:
        line = [b[a], b[c], b[d]]
        if line.count(ai) == 2 and line.count(" ") == 1:
            return [a, c, d][line.index(" ")]
    # 2. Block opponent
    for a, c, d in WIN_LINES:
        line = [b[a], b[c], b[d]]
        if line.count(human) == 2 and line.count(" ") == 1:
            return [a, c, d][line.index(" ")]
    # 3. Prefer center, then corners, then random
    if b[4] == " ":
        return 4
    corners = [i for i in (0, 2, 6, 8) if b[i] == " "]
    if corners:
        return random.choice(corners)
    return random.choice(free_positions(b))


def play():
    print("\n🎮 Game mode:")
    print("  1. Human vs Human")
    print("  2. Human vs Computer")
    mode = input("Pick (1-2, Enter=1): ").strip() or "1"
    vs_ai = mode == "2"

    b = new_board()
    human = "X"
    ai = "O"
    current = "X"

    while True:
        print_board(b)

        if vs_ai and current == ai:
            print("🤖 Computer is thinking...")
            pos = ai_move(b, ai, human)
        else:
            pos = human_move(b, current)

        b[pos] = current

        winner = get_winner(b)
        if winner:
            print_board(b)
            if vs_ai and winner == ai:
                print("💻 Computer wins!")
            elif vs_ai and winner == human:
                print("🎉 You win! 🎉")
            else:
                print(f"🏆 Player {winner} wins!")
            return

        if is_full(b):
            print_board(b)
            print("🤝 It's a draw!")
            return

        current = ai if current == human and vs_ai else ("O" if current == "X" else "X")


def main():
    print("=" * 40)
    print("     TIC · TAC · TOE  ⭕❌")
    print("=" * 40)

    while True:
        play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("👋 Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)