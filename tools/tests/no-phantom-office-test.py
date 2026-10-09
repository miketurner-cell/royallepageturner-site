#!/usr/bin/env python3
"""The hub never claims an office in St. John's / the Avalon or in Labrador West (sites 2026-10-09).

Mike, D-1009-62 (2026-10-09): "Gander is head office, so right now St. John's does not have an office location, so Chris
is working from home." CLAUDE.md: Labrador West is recruiting-only, with no office. The brokerage's offices are Gander
(204 Airport Blvd) and Happy Valley-Goose Bay (371 Hamilton River Road, Suite 102). This test fails on any published
.html (meta, structured data or visible text) that says
  * "St. John's office" or "Avalon office";
  * "office(s) in ..." naming St. John's, the Avalon or Labrador West in the same clause (up to ".", ";" or "serv...");
  * "Labrador West office" / "Lab West office";
  * an office count above two ("Four Offices", "3 Active Offices", a net-num stat of 3+ labelled offices);
  * an office card (.office-card / .office-detail / .ol-card) headed St. John's, Avalon or Labrador West that does not
    say "Service area" or "No office";
  * a region-chooser "Turner Office" badge that is not conditioned on the region's office address.
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
COUNT_RE = re.compile(r"\b(?:three|four|five|[3-9])\s+(?:active\s+)?offices\b"
                      r"|class=\"net-num\">\s*[3-9]\s*</div>\s*<div class=\"net-label\">[^<]*office", re.I)
CARD_RE = re.compile(r"<(?:a|div)\b[^>]*class=\"(?:office-card|office-detail|ol-card)\b")
CARD_HEAD_RE = re.compile(r"<h[2-4]>\s*(st\.?\s*john|avalon|labrador\s+west)", re.I)
CARD_OK_RE = re.compile(r"service area|no office", re.I)
SKIP_DIRS = {".git", "node_modules", ".claude", "tools"}


def scan(rel, text, errs):
    line = lambda pos: text.count(chr(10), 0, pos) + 1
    for rx in PATTERNS + [COUNT_RE]:
        for m in rx.finditer(text):
            errs.append(f"{rel}:{line(m.start())}: office claim {m.group(0)!r}")
    starts = [m.start() for m in CARD_RE.finditer(text)]
    for i, s in enumerate(starts):
        block = text[s:starts[i + 1] if i + 1 < len(starts) else s + 3000]
        if "ol-card" in block[:200]:
            # .ol-card is a generic link card; it is an office card only in a section whose visible heading text says office
            sec = text[text.rfind("<section", 0, s):s]
            if not re.search(r"office", re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", sec, flags=re.S)), re.I):
                continue
        h = CARD_HEAD_RE.search(block)
        if h and not CARD_OK_RE.search(block):
            errs.append(f"{rel}:{line(s)}: office card for {h.group(1)!r} without 'Service area' / 'No office'")
    for m in re.finditer(r"'Turner Office'", text):
        if "office.address" not in text[max(0, m.start() - 300):m.start()]:
            errs.append(f"{rel}:{line(m.start())}: 'Turner Office' badge not conditioned on an office address")


def self_test():
    bad = ["<p>contact our St. John&#x27;s office</p>",
           '<meta name="description" content="Offices in Gander, St. John\'s, and Happy Valley–Goose Bay.">',
           '"description": "with offices in Gander, Happy Valley–Goose Bay, Labrador West, and St. John\'s."',
           "<p>Visit the Labrador West office</p>",
           '<div class="scenic-band-eyebrow">One Network, Four Offices</div>',
           '<div class="net-num">3</div>\n          <div class="net-label">Active Offices</div>',
           '<a href="https://avalonrealestate.ca" class="office-card"><h3>St. John\'s</h3><p>Capital Region</p></a>',
           '<section><h2>Find Your Local Office</h2><a class="ol-card" href="https://labwestrealty.com"><h4>Labrador West</h4><p>labwestrealty.com</p></a>',
           "badgeText = live ? 'Turner Office' : 'Turner Realty';"]
    for b in bad:
        e = []
        scan("x.html", b, e)
        if not e:
            sys.exit(f"SELF-TEST FAIL: not caught: {b!r}")
    good = ["<p>Royal LePage Turner Realty has offices in Gander and Happy Valley–Goose Bay, and serves the Avalon "
            "through Chris Morrison's team.</p>",
            '<span class="office-status status-soon">No office yet</span>',
            '<div class="office-detail"><span>Service area</span><h2>Avalon</h2></div>',
            '<div class="net-num">2</div>\n          <div class="net-label">Offices</div>',
            "badgeText = (live && r.office && r.office.address) ? 'Turner Office' : 'Turner Realty';",
            '<section><h2>Where is your home?</h2><a class="ol-card" href="x"><h4>Avalon</h4><p>avalonrealestate.ca</p></a>']
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
