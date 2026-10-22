"""
hangman.py
Classic Hangman with categories, lives, and ASCII art.
- Random word from a chosen category
- 6 lives, ASCII gallows drawing
- Tracks guessed letters + shows remaining
- Safe input handling, replay loop
No external dependencies — pure stdlib.
"""

import random
import sys

WORDS = {
    "programming": ["python", "javascript", "developer", "keyboard", "algorithm", "variable", "function", "compiler"],
    "animals":     ["elephant", "giraffe", "penguin", "dolphin", "tiger", "kangaroo", "octopus"],
    "countries":   ["kenya", "brazil", "canada", "japan", "germany", "nigeria", "australia"],
    "food":        ["pizza", "sushi", "burger", "pasta", "chocolate", "banana", "mango"],
}

HANGMAN_ART = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """,
]

MAX_LIVES = 6


def choose_category():
    print("\n📂 Categories:")
    cats = list(WORDS.keys())
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c.title()}")
    while True:
        raw = input(f"Pick (1-{len(cats)}, Enter=Random): ").strip()
        if not raw:
            return random.choice(cats)
        if raw.isdigit() and 1 <= int(raw) <= len(cats):
            return cats[int(raw) - 1]
        print("❌ Invalid choice.")


def display_state(word, guessed, lives):
    print(HANGMAN_ART[MAX_LIVES - lives])
    shown = " ".join(c if c in guessed else "_" for c in word)
    print(f"   Word  : {shown}")
    print(f"   Lives : {lives}  {'❤️' * lives}")
    wrong = sorted(g for g in guessed if g not in word)
    if wrong:
        print(f"   Wrong : {', '.join(wrong)}")


def play():
    category = choose_category()
    word = random.choice(WORDS[category])
    guessed = set()
    lives = MAX_LIVES

    print(f"\n🎮 Category: {category.title()}  |  Word length: {len(word)} letters")

    while lives > 0:
        display_state(word, guessed, lives)

        if all(c in guessed for c in word):
            print(f"\n🎉 You WON! The word was '{word}'.")
            return

        letter = input("\nGuess a letter: ").strip().lower()

        if len(letter) != 1 or not letter.isalpha():
            print("❌ Enter a single letter (a-z).")
            continue

        if letter in guessed:
            print(f"⚠️  You already guessed '{letter}'.")
            continue

        guessed.add(letter)

        if letter in word:
            print(f"✅ '{letter}' is in the word!")
        else:
            lives -= 1
            print(f"❌ '{letter}' is NOT in the word. Lives left: {lives}")

    display_state(word, guessed, lives)
    print(f"\n💀 GAME OVER! The word was '{word}'.")


def main():
    print("=" * 40)
    print("       HANGMAN 🪢")
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