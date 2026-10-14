
import csv
import os
import time
from datetime import datetime
from urllib.parse import urlparse

import requests

LOG_FILE = "uptime_log.csv"
TIMEOUT = 10


def normalize_url(url):
    """Validate and normalize a website URL."""
    url = url.strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a valid HTTP or HTTPS URL.")

    return url


def check_website(url):
    """Check a website and measure its response time."""
    start = time.perf_counter()

    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True
        )

        elapsed = time.perf_counter() - start

        return {
            "url": url,
            "status": response.status_code,
            "response_time": round(elapsed, 3),
            "result": (
                "UP" if response.status_code < 400 else "HTTP ERROR"
            ),
            "checked_at": datetime.now().isoformat(
                timespec="seconds"
            )
        }

    except requests.exceptions.Timeout:
        result = "TIMEOUT"
    except requests.exceptions.ConnectionError:
        result = "CONNECTION ERROR"
    except requests.exceptions.RequestException:
        result = "REQUEST ERROR"

    elapsed = time.perf_counter() - start

    return {
        "url": url,
        "status": "N/A",
        "response_time": round(elapsed, 3),
        "result": result,
        "checked_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }


def save_result(data):
    """Append a monitoring result to a CSV file."""
    fields = [
        "checked_at",
        "url",
        "status",
        "response_time",
        "result"
    ]

    file_exists = (
        os.path.exists(LOG_FILE)
        and os.path.getsize(LOG_FILE) > 0
    )

    try:
        with open(
            LOG_FILE, "a", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=fields)

            if not file_exists:
                writer.writeheader()

            writer.writerow(data)

    except OSError as error:
        print(f"Could not save log: {error}")


def display_result(data):
    """Print a readable status report."""
    print("\n" + "-" * 50)
    print(f"Website:       {data['url']}")
    print(f"Result:        {data['result']}")
    print(f"HTTP status:   {data['status']}")
    print(f"Response time: {data['response_time']} seconds")
    print(f"Checked at:    {data['checked_at']}")
    print("-" * 50)


def main():
    print("====== WEBSITE UPTIME MONITOR ======")
    print("Enter a URL or type 'exit' to quit.")

    while True:
        user_input = input("\nWebsite URL: ").strip()

        if user_input.lower() == "exit":
            print("Monitoring session ended.")
            break

        try:
            url = normalize_url(user_input)
        except ValueError as error:
            print(f"Invalid URL: {error}")
            continue

        print("Checking website...")

        result = check_website(url)
        display_result(result)
        save_result(result)

        print(f"Result saved to {LOG_FILE}")


if __name__ == "__main__":
    main()
