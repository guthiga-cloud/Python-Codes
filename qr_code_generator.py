"""
qr_code_generator.py
Generates a QR code image from text or a URL.
Requires: pip install qrcode[pil]
"""

import os
import sys

try:
    import qrcode
except ImportError:
    print("❌ Missing dependency. Install it with:")
    print("   pip install qrcode[pil]")
    sys.exit(1)


def generate_qr(data: str, filename: str = "qr.png") -> str:
    """Create a QR code image from `data` and save it to `filename`."""
    img = qrcode.make(data)
    img.save(filename)
    return os.path.abspath(filename)


def main() -> None:
    text = input("Enter text or URL: ").strip()
    if not text:
        print("❌ Nothing entered. Exiting.")
        return

    default_name = "qr.png"
    filename = input(f"Output filename (default {default_name}): ").strip() or default_name
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        filename += ".png"

    try:
        path = generate_qr(text, filename)
        print(f"✅ QR code saved to: {path}")
    except Exception as e:
        print(f"❌ Failed to generate QR code: {e}")


if __name__ == "__main__":
    main()
    