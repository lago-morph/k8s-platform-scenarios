#!/usr/bin/env python3
"""Extract a subagent's final JSON output verbatim from its task transcript.

Why this exists: a subagent's completion *notification* HTML-escapes `<`,
`>`, `&`, and `"` and is display-truncated, so copying structured output
from it silently corrupts the data. The task *transcript* JSONL carries the
final message unescaped. This tool reads the transcript, isolates the last
assistant text block containing a marker substring, slices out the JSON
value, tolerates a final-token truncation by appending only closing
delimiters (never editing interior bytes), verifies the result parses and is
fully consumed, and writes it out. Any deviation from byte-for-byte (a
stripped prose preamble, an appended delimiter) is reported on stderr so it
can be disclosed in the artifact that stores the output.

Usage:
    extract-json.py --transcript PATH --marker STR --out PATH [--max-repair N]

Exit codes:
    0  wrote well-formed JSON (verbatim, or with a disclosed minimal repair)
    2  no usable marker block, unrepairable truncation, or trailing content
"""
import argparse
import itertools
import json
import sys


def collect_text_blocks(transcript_path):
    """Return every assistant `text` string in the JSONL, in file order."""
    texts = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "text" and isinstance(v, str):
                    texts.append(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    with open(transcript_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                walk(json.loads(line))
            except ValueError:
                # A non-JSON line is not a transcript event; skip it.
                continue
    return texts


def slice_json(text, max_repair):
    """Slice the JSON value out of `text`.

    Returns (json_str, preamble, repair) where `repair` is "" if the value
    parsed as-is or the closing delimiters that had to be appended. Raises
    ValueError if no prefix of appended closing delimiters (up to
    `max_repair`) yields a value that parses AND consumes to end.
    """
    start = text.find("{")
    br = text.find("[")
    if br != -1 and (start == -1 or br < start):
        start = br
    if start == -1:
        raise ValueError("no JSON opening delimiter in marker block")
    preamble = text[:start]
    body = text[start:]
    dec = json.JSONDecoder()

    def parses_whole(s):
        try:
            _, end = dec.raw_decode(s)
        except ValueError:
            return None
        if s[end:].strip():
            return None  # trailing non-whitespace: wrong slice, do not accept
        return s[:end]

    whole = parses_whole(body)
    if whole is not None:
        return whole, preamble, ""

    # Minimal terminal repair: append only closing delimiters, shortest first.
    for n in range(1, max_repair + 1):
        for combo in itertools.product("}]", repeat=n):
            suffix = "".join(combo)
            whole = parses_whole(body + suffix)
            if whole is not None:
                return whole, preamble, suffix
    raise ValueError(
        f"could not repair by appending <= {max_repair} closing delimiters"
    )


def summarize(obj):
    if isinstance(obj, dict):
        return "object with keys: " + ", ".join(sorted(obj.keys()))
    if isinstance(obj, list):
        return f"array of {len(obj)} element(s)"
    return type(obj).__name__


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--transcript", required=True, help="task transcript JSONL path")
    ap.add_argument("--marker", required=True, help="substring identifying the final structured message")
    ap.add_argument("--out", required=True, help="destination path for the verbatim JSON")
    ap.add_argument("--max-repair", type=int, default=3, help="max closing delimiters to append (default 3)")
    args = ap.parse_args()

    texts = collect_text_blocks(args.transcript)
    candidates = [t for t in texts if args.marker in t]
    if not candidates:
        print(f"FAIL: no assistant text block contains marker {args.marker!r}", file=sys.stderr)
        return 2
    final = candidates[-1]

    try:
        json_str, preamble, repair = slice_json(final, args.max_repair)
    except ValueError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 2

    obj = json.loads(json_str)  # guaranteed to parse
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(json_str)
        if not json_str.endswith("\n"):
            f.write("\n")

    # Diagnostics on stderr — never the full payload.
    print(f"wrote {args.out}: {summarize(obj)}", file=sys.stderr)
    if preamble.strip():
        head = preamble.strip().replace("\n", " ")
        if len(head) > 120:
            head = head[:117] + "..."
        print(f"DISCLOSE: stripped prose preamble ({len(preamble)} chars): {head!r}", file=sys.stderr)
    if repair:
        print(f"DISCLOSE: appended {len(repair)} closing delimiter(s) {repair!r} to terminate a truncated value", file=sys.stderr)
    if not preamble.strip() and not repair:
        print("verbatim: no preamble, no repair", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
