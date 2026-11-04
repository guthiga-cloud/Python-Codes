"""
system_info.py
Displays a complete snapshot of your system — no external libs needed.

Shows:
  - OS, version, architecture
  - CPU cores, Python version
  - Memory (RAM) total/available
  - Disk usage per drive (Windows) or root (Linux/Mac)
  - Uptime
  - Network hostname + IP

Usage:
  python system_info.py            # full report
  python system_info.py --brief    # OS + Python only
No external dependencies — pure stdlib.
"""

import os
import platform
import shutil
import socket
import sys
import time

IS_WINDOWS = os.name == "nt"


def get_size(bytes_val: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_val < 1024:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.2f} PB"


def get_uptime() -> str:
    try:
        if IS_WINDOWS:
            import ctypes
            ticks = ctypes.windll.kernel32.GetTickCount64()
            seconds = ticks / 1000
        else:
            with open("/proc/uptime") as f:
                seconds = float(f.read().split()[0])
        days, rem = divmod(int(seconds), 86400)
        hours, rem = divmod(rem, 3600)
        mins = rem // 60
        parts = []
        if days: parts.append(f"{days}d")
        if hours: parts.append(f"{hours}h")
        parts.append(f"{mins}m")
        return " ".join(parts)
    except Exception:
        return "N/A"


def get_memory():
    try:
        if IS_WINDOWS:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            return mem.ullTotalPhys, mem.ullAvailPhys, mem.dwMemoryLoad
        else:
            with open("/proc/meminfo") as f:
                info = {line.split(":")[0]: int(line.split()[1]) for line in f if ":" in line}
            total = info.get("MemTotal", 0) * 1024
            avail = info.get("MemAvailable", 0) * 1024
            used_pct = int((1 - avail / total) * 100) if total else 0
            return total, avail, used_pct
    except Exception:
        return None, None, None


def get_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"


def section(title: str):
    print(f"\n── {title} " + "─" * max(0, 40 - len(title)))


def brief_report():
    print("=" * 46)
    print("        SYSTEM INFO (brief) 💻")
    print("=" * 46)
    print(f"  OS      : {platform.system()} {platform.release()}")
    print(f"  Python  : {platform.python_version()}")
    print("=" * 46)


def full_report():
    print("=" * 46)
    print("        SYSTEM INFO 💻")
    print("=" * 46)

    section("Operating System")
    print(f"  System   : {platform.system()}")
    print(f"  Release  : {platform.release()}")
    print(f"  Version  : {platform.version()}")
    print(f"  Machine  : {platform.machine()}")
    print(f"  Processor: {platform.processor() or 'N/A'}")

    section("Host & User")
    print(f"  Hostname : {socket.gethostname()}")
    print(f"  User     : {os.getenv('USER') or os.getenv('USERNAME') or 'N/A'}")
    print(f"  IP       : {get_ip()}")

    section("Python")
    print(f"  Version  : {platform.python_version()}")
    print(f"  Compiler : {platform.python_compiler()}")
    print(f"  Executable: {sys.executable}")

    section("CPU")
    cpu_count = os.cpu_count()
    print(f"  Logical cores: {cpu_count}")

    section("Memory (RAM)")
    total, avail, pct = get_memory()
    if total:
        print(f"  Total    : {get_size(total)}")
        print(f"  Available: {get_size(avail)}")
        print(f"  Usage    : {pct}%")
    else:
        print("  (could not read memory info)")

    section("Disk")
    if IS_WINDOWS:
        drives = []
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            root = f"{letter}:\\"
            if os.path.exists(root):
                try:
                    t, u, f = shutil.disk_usage(root)
                    drives.append((root, t, u, f))
                except OSError:
                    pass
        for root, t, u, f in drives:
            pct = int(u / t * 100) if t else 0
            print(f"  {root:<4} {get_size(u):>10} used / {get_size(t):>10} total  ({pct}%)")
    else:
        try:
            t, u, f = shutil.disk_usage("/")
            pct = int(u / t * 100) if t else 0
            print(f"  /    {get_size(u):>10} used / {get_size(t):>10} total  ({pct}%)")
        except OSError:
            print("  (could not read disk)")

    section("Uptime")
    print(f"  {get_uptime()}")

    print("\n" + "=" * 46)


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("--brief", "-b"):
        brief_report()
    else:
        full_report()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Interrupted.")
        sys.exit(0)