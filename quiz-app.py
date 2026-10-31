"""
quiz_app.py
A multi-question quiz game with categories, scoring, and a saved high-score.

Features:
  - Pick a category (or mix all)
  - Shuffled questions + shuffled options
  - Tracks score, shows correct answer on wrong
  - Saves best score to highscore.json
  - Replay loop
No external dependencies — pure stdlib.
"""

import json
import os
import random
import sys

HIGHSCORE_FILE = "highscore.json"

QUESTIONS = {
    "programming": [
        {"q": "What does CPU stand for?",
         "a": ["Central Processing Unit", "Computer Power Unit", "Central Program Utility", "Core Process Unit"],
         "c": 0},
        {"q": "Which language runs natively in a browser?",
         "a": ["Python", "JavaScript", "C++", "Java"],
         "c": 1},
        {"q": "What is 2 ** 10?",
         "a": ["512", "1000", "1024", "2048"],
         "c": 2},
        {"q": "Git was created by?",
         "a": ["Guido van Rossum", "Linus Torvalds", "Brendan Eich", "Dennis Ritchie"],
         "c": 1},
        {"q": "Which of these is NOT a Python data type?",
         "a": ["list", "tuple", "array", "dict"],
         "c": 2},
    ],
    "general": [
        {"q": "What is the capital of Kenya?",
         "a": ["Mombasa", "Nairobi", "Kisumu", "Nakuru"],
         "c": 1},
        {"q": "How many continents are there?",
         "a": ["5", "6", "7", "8"],
         "c": 2},
        {"q": "Which planet is closest to the sun?",
         "a": ["Venus", "Earth", "Mercury", "Mars"],
         "c": 2},
        {"q": "What is H2O?",
         "a": ["Salt", "Water", "Oxygen", "Hydrogen"],
         "c": 1},
        {"q": "Largest ocean on Earth?",
         "a": ["Atlantic", "Indian", "Arctic", "Pacific"],
         "c": 3},
    ],
    "science": [
        {"q": "What gas do plants absorb?",
         "a": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"],
         "c": 2},
        {"q": "Speed of light (approx)?",
         "a": ["300,000 km/s", "150,000 km/s", "1,000 km/s", "30,000 km/s"],
         "c": 0},
        {"q": "What is the powerhouse of the cell?",
         "a": ["Nucleus", "Ribosome", "Mitochondria", "Vacuole"],
         "c": 2},
        {"q": "Chemical symbol for gold?",
         "a": ["Go", "Gd", "Au", "Ag"],
         "c": 2},
        {"q": "How many bones in the adult human body?",
         "a": ["206", "180", "230", "150"],
         "c": 0},
    ],
}


def load_highscore() -> int:
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                return int(json.load(f).get("best", 0))
        except (json.JSONDecodeError, OSError, ValueError):
            pass
    return 0


def save_highscore(score: int) -> None:
    try:
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump({"best": score}, f, indent=2)
    except OSError:
        pass


def choose_category():
    print("\n📂 Categories:")
    cats = list(QUESTIONS.keys()) + ["mixed"]
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c.title()}")
    while True:
        raw = input(f"Pick (1-{len(cats)}, Enter=Mixed): ").strip()
        if not raw:
            return "mixed"
        if raw.isdigit() and 1 <= int(raw) <= len(cats):
            return cats[int(raw) - 1]
        print("❌ Invalid choice.")


def build_quiz(category: str) -> list:
    if category == "mixed":
        pool = []
        for qs in QUESTIONS.values():
            pool.extend(qs)
    else:
        pool = list(QUESTIONS[category])
    random.shuffle(pool)
    return pool


def ask_question(q: dict, index: int, total: int) -> bool:
    print(f"\nQ{index}/{total}: {q['q']}")
    # shuffle options while tracking correct answer
    pairs = list(enumerate(q["a"]))
    random.shuffle(pairs)
    correct_pos = None
    for display_idx, (orig_idx, text) in enumerate(pairs, 1):
        print(f"  {display_idx}. {text}")
        if orig_idx == q["c"]:
            correct_pos = display_idx

    while True:
        raw = input("Answer (1-4): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(pairs):
            break
        print("❌ Enter 1-4.")

    chosen = int(raw)
    if chosen == correct_pos:
        print("✅ Correct!")
        return True
    correct_text = pairs[correct_pos - 1][1]
    print(f"❌ Wrong. Correct answer: {correct_text}")
    return False


def run_quiz():
    category = choose_category()
    quiz = build_quiz(category)
    if not quiz:
        print("❌ No questions in that category.")
        return

    print(f"\n🎯 Category: {category.title()}  |  {len(quiz)} questions")
    score = 0
    for i, q in enumerate(quiz, 1):
        if ask_question(q, i, len(quiz)):
            score += 1

    print("\n" + "=" * 44)
    print(f"🏆 Final Score: {score}/{len(quiz)}")

    best = load_highscore()
    if score > best:
        print(f"🎉 NEW HIGH SCORE! (previous best: {best})")
        save_highscore(score)
    else:
        print(f"📊 Your best: {best}/{len(quiz)}")
    print("=" * 44)


def main():
    print("=" * 44)
    print("        QUIZ APP 🎯")
    print("=" * 44)
    print(f"   Best score so far: {load_highscore()}")

    while True:
        run_quiz()
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