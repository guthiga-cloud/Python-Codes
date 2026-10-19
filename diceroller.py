"""
dice_roller.py
Rolls N dice with S sides each.
- Interactive mode + dice notation like "3d6" or "2d20"
- Handles bad input safely
No external dependencies — pure stdlib.
"""

import random
import sys


def roll(sides: int, times: int) -> list[int]:
    return [random.randint(1, sides) for _ in range(times)]


def parse_notation(s: str):
    """Parse '3d6' → (3, 6). Returns None if invalid."""
    s = s.lower().replace(" ", "")
    if "d" not in s:
        return None
    left, right = s.split("d", 1)
    try:
        times = int(left) if left else 1
        sides = int(right)
    except ValueError:
        return None
    if times < 1 or sides < 2:
        return None
    return times, sides


def show_roll(times: int, sides: int) -> None:
    results = roll(sides, times)
    print(f"\n🎲 Rolling {times}d{sides}")
    print(f"   Results: {results}")
    print(f"   Total  : {sum(results)}")
    print(f"   Max    : {times * sides}")
    print(f"   Min    : {times}")


def main() -> None:
    # If a notation is passed on the CLI: `python dice_roller.py 3d6`
    if len(sys.argv) >= 2:
        parsed = parse_notation(sys.argv[1])
        if not parsed:
            print("❌ Invalid notation. Example: 3d6 or 2d20")
            return
        show_roll(*parsed)
        return

    print("🎲 Dice Roller")
    print("Tip: type '3d6' for three six-sided dice, or press Enter for defaults.")

    while True:
        user = input("\nRoll (format NdS, Enter=1d6, 'q' to quit): ").strip().lower()

        if user in ("q", "quit", "exit"):
            print("👋 Bye!")
            break

        if not user:
            times, sides = 1, 6
        else:
            parsed = parse_notation(user)
            if not parsed:
                print("❌ Invalid. Try '3d6', '2d20', or Enter.")
                continue
            times, sides = parsed

        show_roll(times, sides)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")