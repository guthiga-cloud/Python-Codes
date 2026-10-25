"""
currency_converter.py
Live currency converter using the free exchangerate-api.com endpoint.

- Fetch live rates (base = USD)
- Convert between any two supported currencies
- Offline fallback with built-in approximate rates if the API is down
- Interactive mode + CLI: python currency_converter.py 100 USD KES
No external dependencies — pure stdlib (urllib).
"""

import json
import sys
import urllib.request
import urllib.error

API_URL = "https://open.er-api.com/v6/latest/USD"
TIMEOUT = 10

# Fallback rates (approx) if API is unreachable — base USD
FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "KES": 129.0,
    "NGN": 1500.0,
    "ZAR": 18.5,
    "JPY": 149.0,
    "CNY": 7.25,
    "INR": 83.0,
    "CAD": 1.36,
    "AUD": 1.52,
}


def fetch_rates():
    """Return (rates_dict, source_str). Falls back to FALLBACK_RATES on error."""
    try:
        req = urllib.request.Request(
            API_URL, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.load(r)
        if data.get("result") != "success":
            raise ValueError("API returned non-success")
        rates = data["rates"]
        rates["USD"] = 1.0  # ensure base present
        return rates, "live (open.er-api.com)"
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"⚠️  Could not fetch live rates ({e}). Using offline fallback.")
        return FALLBACK_RATES, "offline fallback"


def convert(amount: float, from_cur: str, to_cur: str, rates: dict) -> float:
    from_cur = from_cur.upper()
    to_cur = to_cur.upper()
    if from_cur not in rates:
        raise KeyError(f"Unknown currency: {from_cur}")
    if to_cur not in rates:
        raise KeyError(f"Unknown currency: {to_cur}")
    usd_amount = amount / rates[from_cur]
    return usd_amount * rates[to_cur]


def show_supported(rates: dict):
    codes = sorted(rates.keys())
    print(f"\n💱 {len(codes)} supported currencies:")
    # print in rows of 8
    for i in range(0, len(codes), 8):
        print("   " + "  ".join(f"{c:<4}" for c in codes[i:i+8]))


def interactive(rates: dict, source: str):
    print("=" * 46)
    print("        CURRENCY CONVERTER 💱")
    print(f"        Rates: {source}")
    print("=" * 46)

    while True:
        try:
            raw = input("\nAmount (Enter=q to quit): ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("👋 Bye!")
                break
            amount = float(raw)
            if amount <= 0:
                raise ValueError

            from_cur = input("From currency (e.g. USD): ").strip().upper()
            to_cur = input("To currency   (e.g. KES): ").strip().upper()

            result = convert(amount, from_cur, to_cur, rates)
            print(f"\n✅ {amount:.2f} {from_cur} = {result:,.4f} {to_cur}")
            print(f"   Rate: 1 {from_cur} = {rates[to_cur]/rates[from_cur]:.6f} {to_cur}")

        except ValueError:
            print("❌ Enter a positive number.")
        except KeyError as e:
            print(f"❌ {e}. Type 'list' at amount prompt to see supported codes.")
        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break


def main():
    rates, source = fetch_rates()

    # CLI mode: currency_converter.py <amount> <from> <to>
    if len(sys.argv) == 4:
        try:
            amount = float(sys.argv[1])
            from_cur = sys.argv[2]
            to_cur = sys.argv[3]
            result = convert(amount, from_cur, to_cur, rates)
            print(f"{amount:.2f} {from_cur.upper()} = {result:,.4f} {to_cur.upper()}")
            print(f"(Rates: {source})")
        except ValueError:
            print("❌ Amount must be a number.")
        except KeyError as e:
            print(f"❌ {e}")
        return

    # interactive mode — allow 'list' as amount input
    print("=" * 46)
    print("        CURRENCY CONVERTER 💱")
    print(f"        Rates: {source}")
    print("Type 'list' to see supported currencies.")
    print("=" * 46)

    while True:
        try:
            raw = input("\nAmount (q=quit, list=codes): ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("👋 Bye!")
                break
            if raw.lower() == "list":
                show_supported(rates)
                continue
            amount = float(raw)
            if amount <= 0:
                raise ValueError

            from_cur = input("From currency: ").strip().upper()
            to_cur = input("To currency  : ").strip().upper()

            result = convert(amount, from_cur, to_cur, rates)
            print(f"\n✅ {amount:.2f} {from_cur} = {result:,.4f} {to_cur}")
            print(f"   Rate: 1 {from_cur} = {rates[to_cur]/rates[from_cur]:.6f} {to_cur}")

        except ValueError:
            print("❌ Enter a positive number.")
        except KeyError as e:
            print(f"❌ {e}")
        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)