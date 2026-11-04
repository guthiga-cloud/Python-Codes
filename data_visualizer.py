"""
data_visualizer.py
Visualize CSV data as a bar chart, line chart, or histogram.

Usage:
  python data_visualizer.py                          # interactive
  python data_visualizer.py data.csv                 # bar chart (default)
  python data_visualizer.py data.csv --line          # line chart
  python data_visualizer.py data.csv --hist          # histogram of one column
  python data_visualizer.py data.csv --x name --y score --out chart.png

Features:
  - Auto-picks numeric Y and text X columns if not specified
  - Bar / line / histogram modes
  - Saves PNG (chart.png by default) AND optionally shows it
  - Graceful error if matplotlib missing
No required external deps for the CSV parsing; needs matplotlib to plot.
"""

import csv
import os
import sys


def load_csv(path: str):
    if not os.path.isfile(path):
        print(f"❌ File not found: {path}")
        return None, None
    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            headers = reader.fieldnames or []
        if not rows:
            print("⚠️  CSV is empty.")
            return None, None
        return headers, rows
    except OSError as e:
        print(f"❌ Could not read CSV: {e}")
        return None, None
    except csv.Error as e:
        print(f"❌ CSV parse error: {e}")
        return None, None


def is_numeric(rows, col):
    count = 0
    for r in rows[:20]:
        v = (r.get(col) or "").strip()
        if not v:
            continue
        try:
            float(v)
            count += 1
        except ValueError:
            return False
    return count > 0


def pick_columns(headers, rows):
    if not headers:
        return None, None
    numeric_cols = [h for h in headers if is_numeric(rows, h)]
    text_cols = [h for h in headers if h not in numeric_cols]

    y_col = numeric_cols[-1] if numeric_cols else None
    x_col = text_cols[0] if text_cols else (headers[0] if headers else None)

    if x_col == y_col and len(headers) > 1:
        x_col = headers[0] if headers[1] == y_col else headers[1]

    return x_col, y_col


def plot(path, mode="bar", x_col=None, y_col=None, out="chart.png", show=False):
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend → save only
        import matplotlib.pyplot as plt
    except ImportError:
        print("❌ matplotlib is not installed.")
        print("   Install with: pip install matplotlib")
        return

    headers, rows = load_csv(path)
    if not rows:
        return

    if x_col is None or y_col is None:
        auto_x, auto_y = pick_columns(headers, rows)
        x_col = x_col or auto_x
        y_col = y_col or auto_y

    if not x_col or not y_col:
        print("❌ Could not determine X and Y columns.")
        print(f"   Available columns: {headers}")
        return

    if x_col not in headers:
        print(f"❌ X column '{x_col}' not found. Available: {headers}")
        return
    if y_col not in headers:
        print(f"❌ Y column '{y_col}' not found. Available: {headers}")
        return

    # Parse data
    try:
        if mode == "hist":
            values = [float(r[y_col]) for r in rows if (r.get(y_col) or "").strip()]
        else:
            xs, ys = [], []
            for r in rows:
                xv = (r.get(x_col) or "").strip()
                yv = (r.get(y_col) or "").strip()
                if not xv or not yv:
                    continue
                try:
                    ys.append(float(yv))
                    xs.append(xv)
                except ValueError:
                    continue
            if not xs:
                print("❌ No valid numeric rows.")
                return
    except ValueError:
        print(f"❌ Column '{y_col}' has non-numeric values.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    if mode == "hist":
        ax.hist(values, bins=10, color="#3b82f6", edgecolor="white")
        ax.set_title(f"Histogram of {y_col}")
        ax.set_xlabel(y_col)
        ax.set_ylabel("Frequency")
    elif mode == "line":
        ax.plot(range(len(xs)), ys, marker="o", color="#10b981")
        ax.set_xticks(range(len(xs)))
        ax.set_xticklabels(xs, rotation=45, ha="right")
        ax.set_title(f"{y_col} by {x_col} (line)")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
    else:  # bar
        ax.bar(range(len(xs)), ys, color="#6366f1")
        ax.set_xticks(range(len(xs)))
        ax.set_xticklabels(xs, rotation=45, ha="right")
        ax.set_title(f"{y_col} by {x_col} (bar)")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

    plt.tight_layout()
    try:
        plt.savefig(out, dpi=120)
        print(f"✅ Chart saved: {os.path.abspath(out)}")
    except OSError as e:
        print(f"❌ Could not save chart: {e}")
        return
    finally:
        plt.close(fig)

    if show:
        try:
            import webbrowser
            webbrowser.open("file://" + os.path.abspath(out))
        except Exception:
            pass


def parse_args(argv):
    opts = {"path": None, "mode": "bar", "x": None, "y": None, "out": "chart.png", "show": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--line",):
            opts["mode"] = "line"
        elif a in ("--hist", "--histogram"):
            opts["mode"] = "hist"
        elif a in ("--bar",):
            opts["mode"] = "bar"
        elif a == "--x" and i + 1 < len(argv):
            opts["x"] = argv[i + 1]; i += 1
        elif a == "--y" and i + 1 < len(argv):
            opts["y"] = argv[i + 1]; i += 1
        elif a in ("--out", "-o") and i + 1 < len(argv):
            opts["out"] = argv[i + 1]; i += 1
        elif a in ("--show",):
            opts["show"] = True
        elif opts["path"] is None:
            opts["path"] = a
        i += 1
    return opts


def interactive():
    print("=" * 46)
    print("        DATA VISUALIZER 📊")
    print("=" * 46)
    path = input("CSV file path: ").strip()
    if not path:
        print("❌ No path given.")
        return

    print("\nChart type:")
    print("  1. Bar")
    print("  2. Line")
    print("  3. Histogram")
    m = input("Pick (1-3, Enter=Bar): ").strip() or "1"
    mode = {"1": "bar", "2": "line", "3": "hist"}.get(m, "bar")

    out = input("Output filename (Enter=chart.png): ").strip() or "chart.png"

    plot(path, mode=mode, out=out, show=True)


def main():
    if len(sys.argv) == 1:
        interactive()
        return
    opts = parse_args(sys.argv[1:])
    if not opts["path"]:
        print("Usage: python data_visualizer.py <file.csv> [--bar|--line|--hist] [--x col] [--y col] [--out chart.png] [--show]")
        return
    plot(
        opts["path"],
        mode=opts["mode"],
        x_col=opts["x"],
        y_col=opts["y"],
        out=opts["out"],
        show=opts["show"],
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)