"""Nostalgia entry: one childhood-memory sentence, at most 280 chars.

The program writes the sentence to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), then reads the file back as bytes and as text and
verifies both, so a bad write can never pass silently. Deterministic:
no network, no randomness, no clock, no input besides the environment
variable naming the output directory.
"""

import os
import sys

TEXT = ("Every morning my father shaved at the bathroom mirror and let me "
        "smear the leftover foam on my own chin, and for one minute I was "
        "a grown man too, and now I shave alone and miss having an "
        "audience of one.")
MAX_CHARS = 280


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(TEXT)
    with open(path, "rb") as f:
        raw = f.read()
    if raw != TEXT.encode("utf-8"):
        print("entry bytes do not match the sentence", file=sys.stderr)
        return 1
    back = raw.decode("utf-8")
    if back != TEXT or not (1 <= len(back) <= MAX_CHARS) or not back.strip():
        print("entry failed verification", file=sys.stderr)
        return 1
    print(f"{back} ({len(back)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
