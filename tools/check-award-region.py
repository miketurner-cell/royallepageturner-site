#!/usr/bin/env python3
"""Award wording guard (D-1008-66, 2026-10-08).

Royal LePage's own award record names the region "East Coast". "Atlantic" is
never an award region, so it must not appear in any served page or script.
Also blocks two wordings the record does not support:
  - "Lead Manager of the Year" (not on any published Royal LePage list)
  - "Top 1% brokerage" (the Chairman's Club award names the Turner Realty Team)

Usage: python3 tools/check-award-region.py     (exit 1 on any hit)

There was no existing page-check test pattern wired to CI in this repo (no
.github/workflows); tools/pre-deploy-check.py is fleet-canonical and is not
edited per-site, so this is a standalone script.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES = [
    (re.compile(r"\bAtlantic\b", re.I), '"Atlantic" is not an award region (the record says East Coast)'),
    (re.compile(r"Lead\s+Manager\s+of\s+the\s+Year", re.I), '"Lead Manager of the Year" is not in any published Royal LePage list'),
    (re.compile(r"Top\s+1%\s+brokerage", re.I), '"Top 1% brokerage": the Chairman\'s Club award names the Turner Realty Team'),
]
SKIP_DIRS = {".git", ".claude", "node_modules", "tt-fragments"}

bad = 0
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.suffix.lower() not in {".html", ".js", ".json", ".xml"}:
        continue
    rel = p.relative_to(ROOT)
    if SKIP_DIRS & set(rel.parts) or rel.name == "check-award-region.py":
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx, why in RULES:
            if rx.search(line):
                bad += 1
                print(f"FAIL {rel}:{lineno}: {why}: {line.strip()[:120]}")

if bad:
    print(f"\n{bad} award-wording problem(s).")
    sys.exit(1)
print("OK: no 'Atlantic' award region, no unsupported Lead Manager / Top 1% brokerage wording.")
