"""
weather_fetcher.py
Get live weather for any city — no API key required (uses wttr.in).

Usage:
  python weather_fetcher.py                # interactive
  python weather_fetcher.py Nairobi        # one-shot CLI

Features:
  - Current conditions: temp, feels-like, humidity, wind, description
  - 3-day forecast (high/low + description)
  - Offline-safe error handling
  - Keeps prompting until user quits
No external dependencies — pure stdlib (urllib + json).
"""

import json
import sys
import urllib.parse
import urllib.request

TIMEOUT = 10
BASE = "https://wttr.in"


def fetch_weather(city: str) -> dict:
    url = f"{BASE}/{urllib.parse.quote(city)}?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def fmt_temp(c_val: str) -> str:
    return f"{c_val}°C"


def show_weather(city: str, data: dict) -> None:
    cur = data.get("current_condition", [{}])[0]
    if not cur:
        print(f"❌ No current data for {city}.")
        return

    desc = cur.get("weatherDesc", [{}])[0].get("value", "N/A")
    print("\n" + "=" * 44)
    print(f"   🌤  {city.title()}")
    print("=" * 44)
    print(f"   Condition   : {desc}")
    print(f"   Temp        : {fmt_temp(cur.get('temp_C', '?'))}  (feels like {fmt_temp(cur.get('FeelsLikeC', '?'))})")
    print(f"   Humidity    : {cur.get('humidity', '?')}%")
    print(f"   Wind        : {cur.get('windspeedKmph', '?')} km/h {cur.get('winddir16Point', '')}")
    print(f"   Visibility  : {cur.get('visibility', '?')} km")
    print(f"   Pressure    : {cur.get('pressure', '?')} hPa")

    days = data.get("weather", [])
    if days:
        print("\n   📅 3-day forecast:")
        print("   " + "-" * 40)
        for d in days[:3]:
            date = d.get("date", "?")
            maxc = d.get("maxtempC", "?")
            minc = d.get("mintempC", "?")
            # avg desc from hourly mid-day
            hourly = d.get("hourly", [])
            mid = hourly[len(hourly) // 2] if hourly else {}
            ddesc = mid.get("weatherDesc", [{}])[0].get("value", "N/A")
            print(f"   {date}  {minc}°C – {maxc}°C   {ddesc}")
    print("=" * 44)


def get_and_show(city: str) -> bool:
    city = city.strip()
    if not city:
        print("❌ Empty city name.")
        return False
    try:
        data = fetch_weather(city)
        show_weather(city, data)
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ City not found or API error: {e.code}")
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e.reason}")
    except TimeoutError:
        print("❌ Request timed out.")
    except json.JSONDecodeError:
        print("❌ API returned invalid data.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    return False


def interactive():
    print("=" * 44)
    print("        WEATHER FETCHER 🌤")
    print("=" * 44)
    while True:
        try:
            city = input("\nCity name (q to quit): ").strip()
            if city.lower() in ("q", "quit", "exit"):
                print("👋 Bye!")
                break
            if city:
                get_and_show(city)
        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break


def main():
    if len(sys.argv) >= 2:
        city = " ".join(sys.argv[1:])
        get_and_show(city)
    else:
        interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)


        