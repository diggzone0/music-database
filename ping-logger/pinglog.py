#!/usr/bin/env python3
"""Simple ping logger: ping a host periodically and log average latency."""

import sys
import subprocess
import re
import time
from datetime import datetime

def ping_avg(host):
    """Return average ping latency in ms, or None if failed."""
    try:
        out = subprocess.run(['ping', '-c', '3', '-W', '2', host],
                             capture_output=True, text=True, timeout=5).stdout
        match = re.search(r'min/avg/max.*?([0-9.]+)/([0-9.]+)', out)
        return float(match.group(2)) if match else None
    except Exception:
        return None

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <host> <interval_sec> <count>")
        sys.exit(1)

    host, interval, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    print(f"Logging pings to {host} every {interval}s\nTime\t\tLatency(ms)")

    for i in range(count):
        ts = datetime.now().strftime('%H:%M:%S')
        avg = ping_avg(host)
        print(f"{ts}\t{avg:.1f}" if avg else f"{ts}\tFAIL")
        if i < count - 1:
            time.sleep(interval)
