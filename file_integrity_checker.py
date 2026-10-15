
import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BASELINE_FILE = BASE_DIR / "file_baseline.json"
CHUNK_SIZE = 65536


def calculate_hash(file_path):
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def load_baseline():
    """Load previously recorded file fingerprints."""
    if not BASELINE_FILE.exists():
        return {}

    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Baseline file has an invalid format.")
            return {}

        return data

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load baseline: {error}")
        return {}


def save_baseline(baseline):
    """Save fingerprints to a JSON file."""
    try:
        with open(BASELINE_FILE, "w", encoding="utf-8") as file:
            json.dump(baseline, file, indent=4)

        print("Baseline saved successfully.")
        return True

    except OSError as error:
        print(f"Could not save baseline: {error}")
        return False


def get_file_path():
    """Get and validate the file path from the user."""
    raw_path = input("Enter the file path: ").strip().strip('"')

    if not raw_path:
        print("File path cannot be empty.")
        return None

    path = Path(raw_path).expanduser()

    if not path.is_absolute():
        path = BASE_DIR / path

    if not path.exists():
        print("File does not exist.")
        return None

    if not path.is_file():
        print("The specified path is not a file.")
        return None

    return path.resolve()


def record_file():
    """Record a file's current fingerprint."""
    path = get_file_path()

    if path is None:
        return

    try:
        fingerprint = calculate_hash(path)
    except OSError as error:
        print(f"Could not read file: {error}")
        return

    baseline = load_baseline()
    key = str(path)

    if key in baseline:
        print("This file already has a recorded fingerprint.")
        confirm = input("Replace the old fingerprint? (y/n): ").strip().lower()

        if confirm != "y":
            print("Original fingerprint retained.")
            return

    baseline[key] = fingerprint

    if save_baseline(baseline):
        print(f"File recorded: {path.name}")
        print(f"SHA-256: {fingerprint}")


def check_file():
    """Compare a file with its saved fingerprint."""
    path = get_file_path()

    if path is None:
        return

    baseline = load_baseline()
    key = str(path)

    if key not in baseline:
        print("File not registered. Record its fingerprint first.")
        return

    try:
        current_hash = calculate_hash(path)
    except OSError as error:
        print(f"Could not read file: {error}")
        return

    print(f"\nFile: {path.name}")

    if current_hash == baseline[key]:
        print("STATUS: No changes detected.")
    else:
        print("STATUS: FILE CHANGED!")
        print("The current fingerprint differs from the baseline.")


def list_files():
    """List all files with recorded fingerprints."""
    baseline = load_baseline()

    if not baseline:
        print("No files have been registered.")
        return

    print("\n===== REGISTERED FILES =====")

    for number, (path, fingerprint) in enumerate(
        baseline.items(), start=1
    ):
        print(f"{number}. {path}")
        print(f"   SHA-256: {fingerprint}")


def main():
    while True:
        print("\n===== FILE INTEGRITY CHECKER =====")
        print("1. Record a file")
        print("2. Check a file")
        print("3. List registered files")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            record_file()
        elif choice == "2":
            check_file()
        elif choice == "3":
            list_files()
        elif choice == "4":
            print("Integrity checker closed.")
            break
        else:
            print("Invalid option. Choose 1-4.")


if __name__ == "__main__":
    main()
