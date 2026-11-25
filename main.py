#!/usr/bin/env python3
"""The 4AM Commit: Funniest Agent Bug-Fix Message.

One commit message, one line, 82 characters. The joke is the loop:
the agent fixes the bug it wrote at 2am with a worse bug it wrote at
4am -- and the worse bug ships at 9am. Flat machine voice, quiet dread.

The line is built from three beats (setup / escalation / punchline) and
verified against a pinned digest before it is written, so the assembled
line can never drift from the line this program was written to ship.
"""

import hashlib
import os

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# The three beats of the commit message.
SETUP = "fix: fixed the bug I wrote at 2am"
ESCALATION = "with a worse bug I wrote at 4am."
PUNCHLINE = "it ships at 9am"

# Pinned digest of the exact entry line, so a beat edit that changes the
# shipped text fails loudly instead of silently shipping a new joke.
EXPECTED_SHA256 = "d4e4264ea7bb67b1d9293558e7e0dc2d904bcf5e7cdb6e05c31c3975ba8e426f"


def assemble():
    """Join the beats into the single commit line."""
    return " ".join([SETUP, ESCALATION, PUNCHLINE])


def validate(line):
    """Gate: one line, UTF-8, 1-200 characters, not only whitespace."""
    assert isinstance(line, str), "entry must be text"
    assert "\n" not in line and "\r" not in line, "entry must be one line"
    assert line.strip(), "entry must not be blank"
    assert 1 <= len(line) <= MAX_CHARS, "entry must be 1-200 chars"
    line.encode("utf-8")  # raises if not valid UTF-8 text


def digest(line):
    """SHA-256 of the entry line, as UTF-8 bytes."""
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


def write_entry(line):
    """Write the line to /output/entry.txt with no trailing newline."""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)


def read_back():
    """Read the written file back for the round-trip guard."""
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        return f.read()


def main():
    line = assemble()
    validate(line)
    if digest(line) != EXPECTED_SHA256:
        raise SystemExit("round-trip guard: assembled line differs from pinned entry")
    write_entry(line)
    if read_back() != line:
        raise SystemExit("round-trip guard: file on disk differs from entry")
    print(f"chars: {len(line)}")
    print(line)


if __name__ == "__main__":
    main()
