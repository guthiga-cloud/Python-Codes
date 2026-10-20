"""
number_guessing_game.py
Guess a number between 1 and 100 with hints and difficulty levels.
- Difficulty controls range + max attempts
- Hints: higher/lower + "getting warmer" feedback
- Replay loop + safe input handling
No external dependencies — pure stdlib.
"""

import random
import sys


DIFFICULTIES = {
    "1": ("Easy",   1, 50,  10),
    "2": ("Medium", 1, 100, 7),
    "3": ("Hard",   1, 500, 6),
}


def choose_difficulty():
    print("\n🎯 Choose difficulty:")
    print("  1. Easy   (1–50,  10 tries)")
    print("  2. Medium (1–100,  7 tries)")
    print("  3. Hard   (1–500,  6 tries)")
    while True:
        choice = input("Pick (1-3, Enter=Medium): ").strip() or "2"
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("❌ Invalid. Pick 1, 2, or 3.")


def get_guess(low: int, high: int):
    raw = input(f"Your guess ({low}-{high}): ").strip()
    try:
        guess = int(raw)
    except ValueError:
        print("❌ Enter a whole number.")
        return None
    if not low <= guess <= high:
        print(f"❌ Out of range ({low}-{high}).")
        return None
    return guess


def play():
    name, low, high, max_tries = choose_difficulty()
    secret = random.randint(low, high)
    tries = 0
    last_guess = None

    print(f"\n🎲 {name} mode — guess between {low} and {high} in {max_tries} tries.")

    while tries < max_tries:
        remaining = max_tries - tries
        print(f"   Attempts left: {remaining}")
        guess = get_guess(low, high)
        if guess is None:
            continue

        tries += 1

        if guess == secret:
            print(f"\n🎉 Correct! The number was {secret}.")
            print(f"   You found it in {tries} tr{'y' if tries == 1 else 'ies'}.")
            return

        # hints
        if guess < secret:
            print("⬆️  Higher!")
        else:
            print("⬇️  Lower!")

        if last_guess is not None:
            if abs(secret - guess) < abs(secret - last_guess):
                print("🔥 Getting warmer...")
            else:
                print("❄️  Getting colder...")
        last_guess = guess

    print(f"\n💀 Out of tries! The number was {secret}.")


def main():
    print("=" * 40)
    print("     NUMBER GUESSING GAME 🎯")
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