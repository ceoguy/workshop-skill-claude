#!/usr/bin/env python3
"""claim-scan — find claims that carry no receipt.

Deterministic pre-check for a delivery report, PROOF.md, or any document that
asserts work is done. Catches the grep-able slice only: a clean scan is a floor,
not a pass. Mirrors the humanizer scanners in shape and exit behaviour.

Usage:  python3 claim-scan.py <file> [<file> ...]
Exit:   0 = no findings, 1 = findings, 2 = usage error
"""
import re, sys, pathlib

# (label, pattern, why it matters)
RULES = [
    ("tests-without-counts",
     r'\b(tests?|suite|specs?)\s+(all\s+)?(pass|passing|passed|green)\b(?![^\n]*\b\d+\b)',
     "says tests pass without a pass/fail count"),
    ("verified-without-method",
     r'(?<!not )(?<!un)(?<!never )(?<!yet )\b(verified|confirmed|validated|proven)\b(?![^\n]*(?:`|\bcommand\b|\bSHA\b|\bcommit\b|\bhttps?://|\brun\b|\bexit\b|\bmd5\b|\bcount\b))',
     "claims verification without naming the command, SHA, URL, or output"),
    ("accuracy-without-basis",
     r'\b\d{1,3}(?:\.\d+)?\s?%(?![^\n]*(?:\bof\b|\bsample\b|\bn\s?=|\bheld-out\b|\bbaseline\b|\bmethod\b|\bcorpus\b))',
     "quotes a percentage with no sample, baseline, or method"),
    ("hedge-as-evidence",
     r'\b(should\s+(?:work|be\s+fine|pass)|presumably|appears?\s+to\s+work|seems?\s+to\s+work|looks?\s+correct|ought\s+to)\b',
     "hedge standing in for evidence"),
    ("deploy-without-running-check",
     r'\b(deployed|shipped|live|in\s+prod(?:uction)?)\b(?![^\n]*(?:\bSHA\b|\bcommit\b|\bhttps?://|\bstatus\b|\bhealth|\bversion\b|\bexit\b))',
     "claims a deploy without checking the running version"),
    ("done-without-condition",
     r'^\s*(?:[-*]\s*)?(?:\w[\w /]{0,30}\s*[:—-]\s*)?(?:DONE|COMPLETE|CLOSED|FINISHED)\b(?![^\n]*(?:\bbecause\b|\bproven\b|\bevidence\b|\bSHA\b|\bhttps?://|\btest))',
     "marks something done with no done-condition or evidence beside it"),
]

NOT_PROVEN = re.compile(r'not\s+(?:yet\s+)?proven|unproven|unverified|NOT\s+PROVEN|open\s+items|honest\s+ceiling', re.I)

def scan(path):
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return None
    lines = text.splitlines()
    hits = []
    for i, line in enumerate(lines, 1):
        if NOT_PROVEN.search(line) and line.lstrip().startswith("#"):
            continue  # the honest-ceiling heading is not a claim
        if line.lstrip().startswith(("    ", "\t")) and "```" not in line:
            pass  # indented blocks still scanned; code fences handled below
        for label, pat, why in RULES:
            flags = re.I | (re.M if label == "done-without-condition" else 0)
            if re.search(pat, line, flags):
                hits.append((i, label, why, line.strip()[:100]))
    return text, hits

def main(argv):
    if len(argv) < 2:
        print(__doc__.strip()); return 2
    total = 0
    for path in argv[1:]:
        got = scan(path)
        if got is None:
            total += 1; continue
        text, hits = got
        print(f"\n=== {path} ===")
        if hits:
            by = {}
            for ln, label, why, snip in hits:
                by.setdefault(label, []).append((ln, why, snip))
            for label, items in by.items():
                print(f"\n[{label}] {len(items)} hit(s) — {items[0][1]}")
                for ln, _why, snip in items[:6]:
                    print(f"    {path}:{ln}  {snip}")
                if len(items) > 6:
                    print(f"    ... and {len(items)-6} more")
            total += len(hits)
        else:
            print("clean: every claim scanned carries a receipt.")
        if not NOT_PROVEN.search(text):
            print("\n[no-honest-ceiling] the document never says what is NOT proven.")
            print("    Every delivery states its ceiling. Add one.")
            total += 1
    print(f"\ntotal findings: {total}")
    print("A clean scan is a floor, not a pass. The judgment checks in SKILL.md still apply.")
    return 1 if total else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
