#!/usr/bin/env python3
"""Writes the best advice I ever got - one sentence - to /output/entry.txt.

Pure standard library only. No network, no secrets, no input files.
The sentence is embedded in this file; the program validates it
(1-200 characters, exactly one sentence, clean spacing) and writes
it with no trailing newline, then re-reads the bytes to confirm.
"""

import os

SENTENCE = (
    "Wiping grease off his hands after a twelve-hour shift, my father told "
    "me never to borrow money to look rich, because debt is the only boss "
    "that never sleeps."
)

DEFAULT_OUTPUT = "/output/entry.txt"


def main() -> None:
    path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    text = SENTENCE

    # Validate: length 1-200 characters.
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"sentence is {len(text)} chars, must be 1-200")

    # Validate: no leading/trailing space, no double space.
    if text != text.strip() or "  " in text:
        raise SystemExit("sentence has leading/trailing/double space")

    # Validate: exactly one sentence - one terminal mark, at the end.
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1 or text[-1] not in ".!?":
        raise SystemExit("not exactly one sentence")

    data = text.encode("utf-8")

    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)

    # Re-read and fail loudly if the bytes differ.
    with open(path, "rb") as handle:
        if handle.read() != data:
            raise SystemExit("re-read mismatch: output bytes differ")


if __name__ == "__main__":
    main()
