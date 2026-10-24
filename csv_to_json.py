"""
csv_to_json.py
Convert CSV files to JSON with clean handling.

Usage:
  python csv_to_json.py <file.csv>              # → file.json
  python csv_to_json.py <file.csv> <out.json>   # → out.json
  python csv_to_json.py                          # interactive

Features:
  - Auto-detects delimiter (, ; | \t)
  - Detects numeric columns and converts them (int/float)
  - Pretty-printed JSON output
  - Safe on missing files / bad paths
No external dependencies — pure stdlib.
"""

import csv
import json
import os
import sys


def sniff_delimiter(sample: str) -> str:
    for d in [",", ";", "|", "\t"]:
        if d in sample:
            return d
    return ","


def try_number(value: str):
    """Return int/float if value looks numeric, else keep string."""
    if value is None or value == "":
        return value
    s = value.strip()
    try:
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)
    except ValueError:
        return value


def convert(csv_path: str, json_path: str | None = None) -> None:
    if not os.path.isfile(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    json_path = json_path or (os.path.splitext(csv_path)[0] + ".json")

    try:
        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(2048)
            f.seek(0)
            delimiter = sniff_delimiter(sample)
            reader = csv.DictReader(f, delimiter=delimiter)
            rows = []
            for raw_row in reader:
                clean = {k: try_number(v) for k, v in raw_row.items() if k is not None}
                rows.append(clean)
    except OSError as e:
        print(f"❌ Could not read CSV: {e}")
        return
    except csv.Error as e:
        print(f"❌ CSV parse error: {e}")
        return

    if not rows:
        print("⚠️  CSV was empty (or had only a header). Writing [].")
        rows = []

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"❌ Could not write JSON: {e}")
        return

    print(f"✅ Converted!")
    print(f"   CSV  → {csv_path}")
    print(f"   JSON → {json_path}")
    print(f"   Rows → {len(rows)}")
    print(f"   Delimiter used: {repr(delimiter)}")


def interactive():
    print("=" * 44)
    print("        CSV → JSON CONVERTER 🔄")
    print("=" * 44)
    path = input("CSV file path: ").strip()
    if not path:
        print("❌ No path given.")
        return
    out = input("Output JSON (Enter=auto): ").strip() or None
    convert(path, out)


def main():
    if len(sys.argv) >= 2:
        csv_path = sys.argv[1]
        json_path = sys.argv[2] if len(sys.argv) >= 3 else None
        convert(csv_path, json_path)
    else:
        interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)