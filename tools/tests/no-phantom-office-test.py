#!/usr/bin/env python3
"""The hub never claims an office in St. John's / the Avalon or in Labrador West (sites 2026-10-09).

Mike, D-1009-62 (2026-10-09): "Gander is head office, so right now St. John's does not have an office location, so Chris
is working from home." CLAUDE.md: Labrador West is recruiting-only, with no office. The brokerage's offices are Gander
(204 Airport Blvd) and Happy Valley-Goose Bay (371 Hamilton River Road, Suite 102). This test fails on any published
.html (meta, structured data or visible text) that says
  * "St. John's office" or "Avalon office";
  * "office(s) in ..." naming St. John's, the Avalon or Labrador West in the same clause (up to ".", ";" or "serv...");
  * "Labrador West office" / "Lab West office".
"No office yet" and "serves the Avalon through Chris Morrison's team" are fine.

Offline; injects one failure per pattern first and proves each is caught. Exits 1 on any finding.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
APOS = r"(?:'|’|&#x27;|&#39;|&rsquo;)?"
PATTERNS = [
    re.compile(r"st\.?\s*john" + APOS + r"s\s+office|avalon\s+office", re.I),
    re.compile(r"offices?\s+in\b(?:(?!serv)[^.;<>\"]){0,120}?(?:st\.?\s*john|avalon|labrador\s+west|lab\s+west)", re.I),
    re.compile(r"(?:labrador|lab)\s+west\s+office", re.I),
]
SKIP_DIRS = {".git", "node_modules", ".claude", "tools"}


def scan(rel, text, errs):
    for rx in PATTERNS:
        for m in rx.finditer(text):
            errs.append(f"{rel}:{text.count(chr(10), 0, m.start()) + 1}: office claim {m.group(0)!r}")


def self_test():
    bad = ["<p>contact our St. John&#x27;s office</p>",
           '<meta name="description" content="Offices in Gander, St. John\'s, and Happy Valley–Goose Bay.">',
           '"description": "with offices in Gander, Happy Valley–Goose Bay, Labrador West, and St. John\'s."',
           "<p>Visit the Labrador West office</p>"]
    for b in bad:
        e = []
        scan("x.html", b, e)
        if not e:
            sys.exit(f"SELF-TEST FAIL: not caught: {b!r}")
    good = ["<p>Royal LePage Turner Realty has offices in Gander and Happy Valley–Goose Bay, and serves the Avalon "
            "through Chris Morrison's team.</p>",
            '<span class="office-status status-soon">No office yet</span>']
    e = []
    for g in good:
        scan("x.html", g, e)
    if e:
        sys.exit(f"SELF-TEST FAIL: false positive {e}")
    print(f"self-test: {len(bad)} injected claims caught, {len(good)} clean samples pass")


def main():
    self_test()
    errs, n = [], 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if set(rel.split("/")[:-1]) & SKIP_DIRS:
            continue
        n += 1
        scan(rel, p.read_text(encoding="utf-8", errors="replace"), errs)
    if errs:
        print(f"FAIL: {len(errs)} office claim(s) in {n} pages (offices are Gander and Happy Valley-Goose Bay only)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    print(f"PASS: {n} pages; no St. John's / Avalon / Labrador West office claim")


if __name__ == "__main__":
    main()
