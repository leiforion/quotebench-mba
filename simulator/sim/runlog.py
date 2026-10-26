"""Lightweight, flush-on-write progress logging so long DES/MC runs show life
in the console. Writes to stderr with a wall-clock elapsed prefix; import-time
T0 anchors the session. Kept dependency-free on purpose."""
import sys
import time

_T0 = time.time()


def log(msg):
    """Timestamped progress line (elapsed seconds since import), flushed."""
    print(f"[{time.time() - _T0:7.1f}s] {msg}", file=sys.stderr, flush=True)


class Stage:
    """Context manager that logs start/end + duration of a phase."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t = time.time()
        log(f"{self.name} ...")
        return self

    def __exit__(self, *exc):
        log(f"{self.name} done ({time.time() - self.t:.1f}s)")
        return False
