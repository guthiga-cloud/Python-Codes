"""
text_to_speech.py
Convert text to speech and save as MP3/WAV — no API key needed.

Uses Windows SAPI (built-in) or pyttsx3 (cross-platform) or espeak (Linux).

Usage:
  python text_to_speech.py                          # interactive
  python text_to_speech.py "Hello world"            # speak text
  python text_to_speech.py "Hello" --file out.mp3   # save to file
  python text_to_speech.py --file-input notes.txt   # read text from file

Features:
  - Windows: uses built-in SAPI via PowerShell (no install!)
  - Cross-platform: tries pyttsx3 if available
  - Linux fallback: espeak / espeak-ng
  - Saves to .wav/.mp3 when --file is used
No required external dependencies.
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile


SYSTEM = platform.system().lower()


def speak_windows(text: str, out_file: str = None) -> bool:
    """Windows SAPI via PowerShell — no install needed."""
    try:
        if out_file:
            # SAPI → WAV
            out_file = os.path.abspath(out_file)
            if not out_file.lower().endswith(".wav"):
                out_file += ".wav"
            ps = (
                "Add-Type -AssemblyName System.Speech; "
                "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f'$s.SetOutputToWaveFile("{out_file}"); '
                f'$s.Speak("{text.replace(chr(34), chr(39))}"); '
                "$s.Dispose()"
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print(f"✅ Saved to {out_file}")
                return True
            print(f"❌ SAPI error: {result.stderr.strip()}")
            return False
        else:
            ps = (
                "Add-Type -AssemblyName System.Speech; "
                "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f'$s.Speak("{text.replace(chr(34), chr(39))}")'
            )
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                print("✅ Spoken!")
                return True
            print(f"❌ SAPI error: {result.stderr.strip()}")
            return False
    except FileNotFoundError:
        print("❌ PowerShell not found.")
        return False
    except subprocess.TimeoutExpired:
        print("❌ TTS timed out.")
        return False
    except Exception as e:
        print(f"❌ Windows TTS error: {e}")
        return False


def speak_pyttsx3(text: str, out_file: str = None) -> bool:
    """Cross-platform via pyttsx3 if installed."""
    try:
        import pyttsx3
    except ImportError:
        return False

    try:
        engine = pyttsx3.init()
        if out_file:
            out_file = os.path.abspath(out_file)
            engine.save_to_file(text, out_file)
        else:
            engine.say(text)
        engine.runAndWait()
        if out_file:
            print(f"✅ Saved to {out_file}")
        else:
            print("✅ Spoken!")
        return True
    except Exception as e:
        print(f"❌ pyttsx3 error: {e}")
        return False


def speak_linux(text: str, out_file: str = None) -> bool:
    """Linux fallback via espeak / espeak-ng."""
    cmd_name = None
    for c in ("espeak-ng", "espeak"):
        if shutil.which(c):
            cmd_name = c
            break
    if not cmd_name:
        print("❌ No TTS engine found. Install: sudo apt install espeak-ng")
        return False

    try:
        cmd = [cmd_name, text]
        if out_file:
            out_file = os.path.abspath(out_file)
            if not out_file.lower().endswith(".wav"):
                out_file += ".wav"
            cmd = [cmd_name, "-w", out_file, text]
        subprocess.run(cmd, check=True, timeout=30)
        if out_file:
            print(f"✅ Saved to {out_file}")
        else:
            print("✅ Spoken!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ espeak error: {e}")
        return False
    except Exception as e:
        print(f"❌ Linux TTS error: {e}")
        return False


def speak(text: str, out_file: str = None) -> bool:
    """Try best available TTS engine for the platform."""
    if not text.strip():
        print("❌ Empty text.")
        return False

    if SYSTEM == "windows":
        return speak_windows(text, out_file)
    if speak_pyttsx3(text, out_file):
        return True
    if SYSTEM == "linux":
        return speak_linux(text, out_file)
    if SYSTEM == "darwin":
        # macOS has built-in `say`
        try:
            cmd = ["say", text]
            if out_file:
                cmd = ["say", "-o", os.path.abspath(out_file), text]
            subprocess.run(cmd, check=True, timeout=30)
            if out_file:
                print(f"✅ Saved to {os.path.abspath(out_file)}")
            else:
                print("✅ Spoken!")
            return True
        except Exception as e:
            print(f"❌ macOS say error: {e}")
    print("❌ No TTS engine available on this system.")
    return False


def parse_args(argv):
    text = None
    out_file = None
    file_input = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--file", "-f") and i + 1 < len(argv):
            out_file = argv[i + 1]; i += 1
        elif a in ("--file-input", "-i") and i + 1 < len(argv):
            file_input = argv[i + 1]; i += 1
        elif text is None:
            text = a
        i += 1
    return text, out_file, file_input


def interactive():
    print("=" * 46)
    print("        TEXT TO SPEECH 🔊")
    print("=" * 46)
    while True:
        try:
            text = input("\nText to speak (q to quit): ").strip()
            if text.lower() in ("q", "quit", "exit"):
                print("👋 Bye!")
                break
            if not text:
                continue

            save = input("Save to file? (y/n, Enter=n): ").strip().lower() == "y"
            if save:
                fname = input("Filename (Enter=speech.wav): ").strip() or "speech.wav"
                speak(text, fname)
            else:
                speak(text)
        except KeyboardInterrupt:
            print("\n👋 Interrupted.")
            break


def main():
    if len(sys.argv) == 1:
        interactive()
        return

    text, out_file, file_input = parse_args(sys.argv[1:])

    if file_input:
        if not os.path.isfile(file_input):
            print(f"❌ File not found: {file_input}")
            return
        try:
            with open(file_input, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"❌ Could not read file: {e}")
            return

    if not text:
        print("Usage:")
        print('  python text_to_speech.py "Hello world"')
        print('  python text_to_speech.py "Hello" --file out.wav')
        print('  python text_to_speech.py --file-input notes.txt --file out.wav')
        print('  python text_to_speech.py                              # interactive')
        return

    speak(text, out_file)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)