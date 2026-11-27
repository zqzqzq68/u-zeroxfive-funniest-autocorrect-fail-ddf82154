#!/usr/bin/env python3
"""Funniest Autocorrect Fail — make.fun bounty entry.

Writes one line, under 200 characters, to $MAKEFUN_OUTPUT_DIR/entry.txt.
The line reads as a single autocorrect fail: a work message where the
word "annual" came out as "anal". The grader runs this file twice and
compares the outputs, so the text is a fixed constant — no randomness,
no clock, no network, no input.
"""

from __future__ import annotations

import os
import sys

# The entry itself: one line, one slip. "annual contract" is what the
# sender meant; "anal contract" is what autocorrect sent instead.
ENTRY_TEXT = (
    "Great news, team — the client loved the proposal and wants to sign "
    "the anal contract first thing Monday morning."
)

MAX_CHARS = 199


def validate_text(text: str) -> str:
    """Check the entry against the sealed scorer's gate."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the 199 limit")
    text.encode("utf-8")
    return text


def verify_written(path: str, text: str) -> None:
    """Read the entry back and confirm it matches exactly.

    Guards against a partial write or an encoding surprise: the file
    must hold the entry plus one trailing newline, and nothing else.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        stored = handle.read()
    if stored != text + "\n":
        raise ValueError(f"{path} does not hold the entry verbatim")
    if len(stored.rstrip("\n")) > MAX_CHARS:
        raise ValueError("stored entry is over the 199-char limit")


def write_entry(output_dir: str, text: str) -> str:
    """Write the entry file and return its path."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    verify_written(path, text)
    return path


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    text = validate_text(ENTRY_TEXT)
    path = write_entry(output_dir, text)
    print(text)
    print(f"wrote {len(text)} chars to {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
