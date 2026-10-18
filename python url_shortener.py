"""
url_shortener.py
A simple URL shortener with a persistent local store.
- Shorten any http(s) URL into a 6-char code
- Expand a code back to its original URL
- Save history into urls.json (survives restarts)
No external dependencies — uses only Python stdlib.
"""

import hashlib
import json
import os
import sys

DATA_FILE = "urls.json"
BASE_URL = "https://short.ly/"   # just a display prefix


def load_db() -> dict:
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("⚠️  Could not read urls.json — starting fresh.")
    return {}


def save_db(db: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)


def is_valid_url(url: str) -> bool:
    return url.startswith(("http://", "https://")) and "." in url and " " not in url


def shorten(url: str, db: dict) -> str:
    code = hashlib.md5(url.encode()).hexdigest()[:6]
    while code in db and db[code] != url:
        code = hashlib.md5((url + code).encode()).hexdigest()[:6]
    db[code] = url
    save_db(db)
    return code


def expand(code: str, db: dict):
    return db.get(code)


def main() -> None:
    db = load_db()

    while True:
        print("\n=== URL Shortener ===")
        print("1. Shorten a URL")
        print("2. Expand a code")
        print("3. List all")
        print("4. Quit")
        choice = input("Choose (1-4): ").strip()

        if choice == "1":
            url = input("Enter full URL (http:// or https://): ").strip()
            if not is_valid_url(url):
                print("❌ Invalid URL. Must start with http:// or https://")
                continue
            code = shorten(url, db)
            print(f"✅ Short URL: {BASE_URL}{code}")
            print(f"   Original: {url}")

        elif choice == "2":
            code = input("Enter short code: ").strip()
            original = expand(code, db)
            if original:
                print(f"🔗 {BASE_URL}{code} → {original}")
            else:
                print("❌ Code not found.")

        elif choice == "3":
            if not db:
                print("📭 No URLs stored yet.")
            else:
                print(f"📚 {len(db)} stored URL(s):")
                for c, u in db.items():
                    print(f"   {c} → {u}")

        elif choice == "4":
            print("👋 Bye!")
            break

        else:
            print("❌ Invalid choice. Pick 1-4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted. Bye!")
        sys.exit(0)