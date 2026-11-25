#!/usr/bin/env python3
"""One-Line Office Jokes — arena champion (see ARENA.md).

One line, 137 characters / 137 bytes: HR's wellness email told us to
take a break, so I took one and came back to 214 emails, a meeting
invite, and a reminder to take a break. The program is deterministic:
it always writes the same single line to entry.txt, using only the
Python standard library, with no network access and no model call.
It validates the gate itself before writing (UTF-8, 1-199 characters,
single line, plain ASCII so the byte count equals the character count)
and fails loudly otherwise.
It respects MAKEFUN_OUTPUT_DIR (the grader sets it to /output);
locally it defaults to /output as well, so test runs must set
MAKEFUN_OUTPUT_DIR to a scratch directory instead.
Joke design, per the judge brief in order: (1) a first-person
one-line joke about office life, not a story or slogan; (2) the
laugh is the escalation — 214 emails plus a meeting invite — then
the loop: a reminder to take a break; (3) concrete office detail:
the wellness email, the inbox, the meeting invite; (4) 137
characters, no wasted words, the turn lands in the last clause;
(5) the wellness-email irony is fresh wording, not a joke already
going round the internet.
The six shortlist finalists carry their pairwise arena win counts
(15 two-way games, C16 5-0, C12 4-1, C15 3-2, C2 2-3, C14 1-4,
C6 0-5); pick() takes the most wins, breaking ties toward the
shorter text, mirroring the competition's own bytes tie-break.
"""
import os

CANDIDATES = [
    {
        "text": "HR's wellness email told us to take a break, so I took one and came back to 214 emails, a meeting invite, and a reminder to take a break.",
        "wins": 5,
    },
    {
        "text": "My badge stopped working on the one morning I was on time, so security watched me prove I work here to a door I've opened for three years.",
        "wins": 4,
    },
    {
        "text": "I replied-all 'unsubscribe' to the office newsletter, and now I get a weekly email confirming I am still subscribed to the emails about unsubscribing.",
        "wins": 3,
    },
    {
        "text": "Someone replied-all 'thanks!' to a 200-person email, and 47 people replied-all 'thanks!' to the thanks.",
        "wins": 2,
    },
    {
        "text": "The printer jammed on page 47 of 48, so I reprinted all 48 pages and watched it jam on page 47 again, right on schedule.",
        "wins": 1,
    },
    {
        "text": "My calendar is so full that I had to book a meeting with myself, and I still showed up late to it.",
        "wins": 0,
    },
]


def pick(candidates):
    best = None
    for c in candidates:
        # A candidate that fails the gate can never be the entry, however
        # many arena games it won: skip it instead of letting it win.
        if len(c["text"]) < 1 or len(c["text"]) > 199 or "\n" in c["text"]:
            continue
        if (
            best is None
            or c["wins"] > best["wins"]
            or (c["wins"] == best["wins"] and len(c["text"]) < len(best["text"]))
        ):
            best = c
    if best is None:
        raise RuntimeError("no candidates")
    return best["text"]


def main():
    text = pick(CANDIDATES).strip()
    # Gate: UTF-8, 1-199 characters, not only white space, single line.
    # Bytes matter too: on an exact Judge win-rate tie the smaller text
    # places first, so keep it short.
    nbytes = len(text.encode("utf-8"))
    if len(text) < 1 or len(text) > 199:
        raise ValueError(f"joke must be 1-199 characters, got {len(text)}")
    if len(text.strip()) == 0:
        raise ValueError("joke must not be only white space")
    if nbytes != len(text):
        raise ValueError("joke must be plain ASCII so bytes equal characters")
    if "\n" in text or "\r" in text:
        raise ValueError("joke must be a single line")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output").strip() or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    # Read back and verify: what the grader reads must be exactly the
    # validated line, byte for byte, with no trailing newline added.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise ValueError("entry.txt differs from the validated joke")


if __name__ == "__main__":
    main()
