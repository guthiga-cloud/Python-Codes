"""
web_scraper.py
Fetch a webpage and extract headlines, links, and title — no external libs.

Usage:
  python web_scraper.py                          # interactive
  python web_scraper.py https://example.com      # one-shot CLI
  python web_scraper.py <url> --links            # also list links
  python web_scraper.py <url> --save out.txt     # save results

Features:
  - Extracts <title>, all <h1>/<h2>/<h3> headlines
  - Extracts links (<a href>) with anchor text (optional)
  - Saves to a text file (optional)
  - Uses only stdlib: urllib + html.parser
No external dependencies — 100% stdlib.
"""

import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

TIMEOUT = 10


class Scraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.headlines = []          # list of (tag, text)
        self.links = []              # list of (href, text)
        self._capture = None         # "title" | "h1" | "h2" | "h3" | "a"
        self._buffer = ""
        self._current_href = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "title":
            self._capture = "title"
            self._buffer = ""
        elif tag in ("h1", "h2", "h3"):
            self._capture = tag
            self._buffer = ""
        elif tag == "a":
            attrs = dict(attrs)
            self._current_href = attrs.get("href")
            self._capture = "a"
            self._buffer = ""

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title" and self._capture == "title":
            self.title = self._buffer.strip()
            self._capture = None
        elif tag in ("h1", "h2", "h3") and self._capture == tag:
            text = " ".join(self._buffer.split())
            if text:
                self.headlines.append((tag, text))
            self._capture = None
        elif tag == "a" and self._capture == "a":
            text = " ".join(self._buffer.split())
            if self._current_href:
                self.links.append((self._current_href, text))
            self._current_href = None
            self._capture = None

    def handle_data(self, data):
        if self._capture:
            self._buffer += data


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; PythonScraper/1.0)"
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        raw = r.read()
    # try common encodings
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def resolve(base: str, href: str) -> str:
    return urllib.parse.urljoin(base, href)


def scrape(url: str, show_links: bool = False) -> dict:
    if not url.startswith(("http://", "https://")):
        print("❌ URL must start with http:// or https://")
        return {}

    print(f"🌐 Fetching: {url}")
    try:
        html = fetch(url)
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP error {e.code}: {e.reason}")
        return {}
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e.reason}")
        return {}
    except TimeoutError:
        print("❌ Request timed out.")
        return {}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {}

    s = Scraper()
    try:
        s.feed(html)
    except Exception as e:
        print(f"⚠️  Parse warning: {e}")

    print("\n" + "=" * 50)
    if s.title:
        print(f"📰 Title: {s.title}")
    else:
        print("📰 Title: (none)")
    print("=" * 50)

    print(f"\n🔠 Headlines ({len(s.headlines)}):")
    if not s.headlines:
        print("   (no <h1>/<h2>/<h3> found)")
    for tag, text in s.headlines[:25]:
        print(f"   [{tag}] {text}")
    if len(s.headlines) > 25:
        print(f"   ... and {len(s.headlines) - 25} more")

    if show_links:
        print(f"\n🔗 Links ({len(s.links)}):")
        for href, text in s.links[:40]:
            full = resolve(url, href)
            label = text or "(no text)"
            print(f"   {label[:50]:<50}  →  {full}")
        if len(s.links) > 40:
            print(f"   ... and {len(s.links) - 40} more")

    return {
        "url": url,
        "title": s.title,
        "headlines": s.headlines,
        "links": s.links if show_links else [],
    }


def save_results(result: dict, path: str) -> None:
    if not result:
        print("❌ Nothing to save.")
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"URL: {result['url']}\n")
            f.write(f"TITLE: {result['title']}\n\n")
            f.write("HEADLINES:\n")
            for tag, text in result["headlines"]:
                f.write(f"  [{tag}] {text}\n")
            if result["links"]:
                f.write("\nLINKS:\n")
                for href, text in result["links"]:
                    f.write(f"  {text or '(no text)'}  ->  {href}\n")
        print(f"💾 Saved to {path}")
    except OSError as e:
        print(f"❌ Could not save: {e}")


def parse_args(argv):
    url = None
    show_links = False
    save_path = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--links", "-l"):
            show_links = True
        elif a in ("--save", "-s") and i + 1 < len(argv):
            save_path = argv[i + 1]
            i += 1
        elif url is None:
            url = a
        i += 1
    return url, show_links, save_path


def interactive():
    print("=" * 50)
    print("        WEB SCRAPER 🌐")
    print("=" * 50)
    while True:
        try:
            url = input("\nURL (q to quit): ").strip()
            if url.lower() in ("q", "quit", "exit"):
                print("👋 Bye!")
                break
            if not url:
                continue
            want_links = input("Include links? (y/n, Enter=n): ").strip().lower() == "y"
            result = scrape(url, show_links=want_links)
            if result:
                save_choice = input("\nSave results to file? (y/n, Enter=n): ").strip().lower()
                if save_choice == "y":
                    path = input("Filename (Enter=scrape.txt): ").strip() or "scrape.txt"
                    save_results(result, path)
        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break


def main():
    if len(sys.argv) == 1:
        interactive()
        return

    url, show_links, save_path = parse_args(sys.argv[1:])
    if not url:
        print("Usage:")
        print("  python web_scraper.py                           # interactive")
        print("  python web_scraper.py <url> [--links] [--save out.txt]")
        return

    result = scrape(url, show_links=show_links)
    if result and save_path:
        save_results(result, save_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)