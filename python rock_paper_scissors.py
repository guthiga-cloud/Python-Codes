"""
rock_paper_scissors.py
Best-of-N rock-paper-scissors vs the computer.
- Choose rounds (best of 3, 5, or 7)
- Tracks score + shows final winner
- Safe input handling, replay loop
No external dependencies — pure stdlib.
"""

import random
import sys

CHOICES = ["rock", "paper", "scissors"]
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}


def get_player_choice():
    print("\nYour move:")
    print("  1. rock 🪨")
    print("  2. paper 📄")
    print("  3. scissors ✂️")
    while True:
        raw = input("Pick (1-3 or name): ").strip().lower()
        if raw in ("1", "rock", "r"):
            return "rock"
        if raw in ("2", "paper", "p"):
            return "paper"
        if raw in ("3", "scissors", "s"):
            return "scissors"
        print("❌ Invalid choice. Try 1, 2, 3 (or rock/paper/scissors).")


def play_round(player: str, cpu: str) -> str:
    """Return 'player', 'cpu', or 'draw'."""
    if player == cpu:
        return "draw"
    return "player" if BEATS[player] == cpu else "cpu"


def play_game(rounds_to_win: int):
    player_score = 0
    cpu_score = 0
    round_no = 0

    print(f"\n🏆 Best of {rounds_to_win * 2 - 1} — first to {rounds_to_win} wins!")

    while player_score < rounds_to_win and cpu_score < rounds_to_win:
        round_no += 1
        print(f"\n--- Round {round_no} ---")
        print(f"   Score → You: {player_score}   CPU: {cpu_score}")

        player = get_player_choice()
        cpu = random.choice(CHOICES)

        print(f"\n   You: {EMOJI[player]} {player}")
        print(f"   CPU: {EMOJI[cpu]} {cpu}")

        result = play_round(player, cpu)
        if result == "draw":
            print("   🤝 Draw!")
        elif result == "player":
            print("   ✅ You win this round!")
            player_score += 1
        else:
            print("   ❌ CPU wins this round!")
            cpu_score += 1

    print("\n" + "=" * 40)
    if player_score > cpu_score:
        print(f"🎉 YOU WIN THE GAME!  {player_score} – {cpu_score}")
    else:
        print(f"💻 CPU WINS THE GAME.  {player_score} – {cpu_score}")
    print("=" * 40)


def main():
    print("=" * 40)
    print("   ROCK · PAPER · SCISSORS 🪨📄✂️")
    print("=" * 40)

    while True:
        print("\nChoose game length:")
        print("  1. Best of 3  (first to 2)")
        print("  2. Best of 5  (first to 3)")
        print("  3. Best of 7  (first to 4)")
        choice = input("Pick (1-3, Enter=Best of 3): ").strip() or "1"

        rounds_to_win = {"1": 2, "2": 3, "3": 4}.get(choice)
        if not rounds_to_win:
            print("❌ Invalid. Pick 1, 2, or 3.")
            continue

        play_game(rounds_to_win)

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