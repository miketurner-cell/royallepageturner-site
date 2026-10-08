#!/usr/bin/env python3
"""Award wording guard (D-1008-66, 2026-10-08).

Royal LePage's own award record names the region "East Coast". "Atlantic" is
never an award region, so it must not appear in any served page or script.
Also blocks two wordings the record does not support:
  - "Lead Manager of the Year" (not on any published Royal LePage list)
  - "Top 1% brokerage" (the Chairman's Club award names the Turner Realty Team)
  - award leftovers with no source (D-1008-91, 2026-10-08): "104 deals", "178 sales", "97.95%",
    "5 Wing Military Relocation", the Shelter Foundation "$50M+", and a bare count of
    "Brokerage Awards" (the awards are named from the record instead)

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
    # Award leftovers with no source (Mike, D-1008-91, 2026-10-08: keep a claim only where the Shelter Foundation's own
    # site, the agent's royallepage.ca profile or the RLP award record supports it).
    (re.compile(r"(?<![\d,.])104\s+deals\b", re.I), '"104 deals": undated whole-brokerage figure, no source (D-1008-91)'),
    (re.compile(r"(?<![\d,.])178\s+(?:residential\s+)?sales\b", re.I), '"178 sales": unsourced 2025 market figure (D-1008-91)'),
    (re.compile(r"(?<![\d.])97\.95\s?%"), '"97.95%": unsourced 2025 sale-to-list figure (D-1008-91)'),
    (re.compile(r"5\s+Wing\s+Military\s+Relocation"), '"5 Wing Military Relocation": 5 Wing personnel cannot buy or sell (D-1008-38/91)'),
    (re.compile(r"\$\s?50\s?M\+"), 'Shelter Foundation "$50M+": the Foundation says more than $57 million (D-1008-91)'),
    (re.compile(r'class="(?:stat-num|net-num)">\s*\d+\s*</div>\s*<div class="(?:stat-label|net-label)">\s*Brokerage Awards', re.I),
     'a count of "Brokerage Awards": name the awards from the record instead (D-1008-91)'),
]
# The brokerage-award count spans two lines, so it is also checked on the whole file.
MULTILINE = [r for r in RULES if "Brokerage Awards" in r[0].pattern]
for _bad, _n in (("closed 104 deals", 1), ("a 97.95% ratio", 1), ("178 residential sales", 1),
                 ("5 Wing Military Relocation", 1), ("$50M+ raised", 1),
                 ('<div class="stat-num">6</div>\n      <div class="stat-label">Brokerage Awards</div>', 1)):
    assert sum(1 for rx, _ in RULES if rx.search(_bad)) >= _n, f"self-check: should flag {_bad!r}"
for _good in ("1,104 deals", "97.9%", "$57M+", "BGRS closed 1 October 2026", '<div class="stat-num stat-num-text">Brokerage Awards</div>'):
    assert not any(rx.search(_good) for rx, _ in RULES), f"self-check: should pass {_good!r}"
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
    for rx, why in MULTILINE:
        for m in rx.finditer(text):
            if "\n" in m.group(0):
                bad += 1
                print(f"FAIL {rel}:{text.count(chr(10), 0, m.start()) + 1}: {why}")

if bad:
    print(f"\n{bad} award-wording problem(s).")
    sys.exit(1)
print("OK: no 'Atlantic' award region, no unsupported Lead Manager / Top 1% brokerage wording, no unsourced award leftovers.")
