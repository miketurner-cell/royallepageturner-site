#!/usr/bin/env python3
"""Hub: Gander office hours in structured data match Mike's D-1009-21 (mirrors realestategander-site STRICT 2199).

Mike 2026-10-09, D-1009-21: the Gander office (204 Airport Blvd) is open Monday to Friday 10:00-12:00 and
13:00-16:00 (closed for lunch 12-1); weekends by appointment, never published as open. The source of truth is
realestategander-site tools/site-config.json -> office_hours.gander; the hub has no config of its own and no CI
workflow, so the decided hours are stated once below (GANDER) and this script is run by hand before a push:
    python3 tools/tests/office-hours-test.py
Before this test the hub's JSON-LD on index, contact, accessibility, privacy-policy and terms-of-use said
Mon-Fri 09:00-17:00.

Checks (offline, reads the tracked repo tree):
  1. every JSON-LD node on every tracked .html page that carries openingHoursSpecification or openingHours and
     is the Gander office (address 204 Airport, or no address) states exactly the decided (day, opens, closes)
     set -- arrays per span or one entry per day both pass; a JSON-LD hours node for another office fails
     (those hours are not decided);
  2. required surfaces: the five pages above each carry one Gander hours node;
  3. a page whose visible text says "office hours" or states Mon-Fri clock hours must carry a
     data-office-hours marker whose text matches (so a hand-typed hours line cannot appear unseen);
  4. self-check: the old 09:00-17:00 block and a stale 9-5 text line are both caught, and the right hours pass.
Exits 1 on any drift.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Mike D-1009-21 (2026-10-09). Keep equal to realestategander-site tools/site-config.json office_hours.gander.
GANDER = {
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "spans": [["10:00", "12:00"], ["13:00", "16:00"]],
    "weekend": "By appointment",
}
REQUIRED = ["index.html", "contact.html", "accessibility.html", "privacy-policy.html", "terms-of-use.html"]

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SCHEMA_DAY = {d: d for d in ALL_DAYS}
SCHEMA_DAY.update({f"https://schema.org/{d}": d for d in ALL_DAYS})
SCHEMA_DAY.update({f"http://schema.org/{d}": d for d in ALL_DAYS})
SHORT = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"}
LD_RE = re.compile(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S | re.I)
MARK_RE = re.compile(r'<(\w+)[^>]*\bdata-office-hours="([^"]+)"[^>]*>(.*?)</\1>', re.S)
CLOCK_RE = re.compile(r"Mon(?:day)?\s*(?:-|–|&ndash;|to|through)\s*Fri(?:day)?[^\n<]{0,40}?\d{1,2}(?::\d\d)?\s*(?:am|pm)?\s*(?:-|–|&ndash;|to)\s*\d", re.I)

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print(f"  FAIL {msg}")


def ok(msg: str) -> None:
    print(f"  ok   {msg}")


def hm(t: str) -> int:
    m = re.fullmatch(r"([01]\d|2[0-3]):([0-5]\d)", t or "")
    if not m:
        raise ValueError(f"bad time {t!r}")
    return int(m.group(1)) * 60 + int(m.group(2))


def clock(t: str) -> tuple[str, str]:
    h, m = divmod(hm(t), 60)
    return (f"{h % 12 or 12}" if m == 0 else f"{h % 12 or 12}:{m:02d}"), ("AM" if h < 12 else "PM")


def display_weekdays(g: dict) -> str:
    parts = []
    for o, c in g["spans"]:
        (ho, mo), (hc, mc) = clock(o), clock(c)
        parts.append(f"{ho}–{hc} {mc}" if mo == mc else f"{ho} {mo}–{hc} {mc}")
    return f"{g['days'][0][:3]}–{g['days'][-1][:3]}: " + " & ".join(parts)


def norm_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&amp;", "&").replace("&ndash;", "–").replace("&nbsp;", " ").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).strip()


def ld_nodes(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from ld_nodes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from ld_nodes(v)


def node_hours(node: dict) -> set[tuple[str, str, str]]:
    out: set[tuple[str, str, str]] = set()
    spec = node.get("openingHoursSpecification")
    if spec is not None:
        for s in (spec if isinstance(spec, list) else [spec]):
            days = s.get("dayOfWeek")
            for d in (days if isinstance(days, list) else [days]):
                out.add((SCHEMA_DAY.get(d, str(d)), str(s.get("opens")), str(s.get("closes"))))
    oh = node.get("openingHours")
    if oh is not None:
        for item in (oh if isinstance(oh, list) else [oh]):
            m = re.fullmatch(r"\s*(\w\w)(?:-(\w\w))?\s+(\d\d:\d\d)-(\d\d:\d\d)\s*", str(item))
            if not m or m.group(1) not in SHORT or (m.group(2) and m.group(2) not in SHORT):
                out.add(("?", str(item), "?"))
                continue
            keys = list(SHORT)
            a = keys.index(m.group(1))
            b = keys.index(m.group(2)) if m.group(2) else a
            for k in keys[a:b + 1]:
                out.add((SHORT[k], m.group(3), m.group(4)))
    return out


def is_gander(node: dict) -> bool:
    addr = node.get("address")
    if addr is None:
        return True
    street = addr.get("streetAddress", "") if isinstance(addr, dict) else str(addr)
    return "204 airport" in street.lower()


def check_page_ld(rel: str, src: str, want: set, sink) -> int:
    n = 0
    for i, block in enumerate(LD_RE.findall(src)):
        try:
            data = json.loads(block)
        except json.JSONDecodeError as ex:
            if "openingHours" in block:
                sink(f"{rel}: JSON-LD block {i} with hours does not parse ({ex})")
            continue
        for node in ld_nodes(data):
            if "openingHoursSpecification" not in node and "openingHours" not in node:
                continue
            if not is_gander(node):
                sink(f"{rel}: JSON-LD hours for another office ({node.get('name')!r}) -- not decided")
                continue
            n += 1
            got = node_hours(node)
            if got != want:
                sink(f"{rel}: JSON-LD hours {sorted(got - want)} not decided / missing {sorted(want - got)}")
    return n


def check_markers(rel: str, src: str, g: dict, sink) -> set[str]:
    want = {"gander-weekdays": display_weekdays(g), "gander-weekend": g["weekend"]}
    seen = set()
    for _tag, key, inner in MARK_RE.findall(src):
        seen.add(key)
        if key not in want:
            sink(f"{rel}: unknown data-office-hours={key!r}")
        elif norm_text(inner) != want[key]:
            sink(f"{rel}: data-office-hours={key} shows {norm_text(inner)!r}, D-1009-21 says {want[key]!r}")
    return seen


def visible_text(src: str) -> str:
    s = re.sub(r"<!--.*?-->", " ", src, flags=re.S)
    return re.sub(r"<(script|style)\b.*?</\1>", " ", s, flags=re.S | re.I)


def visible_hours_unmarked(rel: str, src: str, sink) -> None:
    vis = visible_text(src)
    # strip marked elements, then look for any remaining hand-typed Gander hours line
    vis = MARK_RE.sub(" ", vis)
    if re.search(r"office hours", vis, re.I):
        sink(f"{rel}: says 'office hours' outside a data-office-hours marker (hours this test cannot check)")
    for m in CLOCK_RE.finditer(vis):
        ctx = vis[max(0, m.start() - 200):m.end() + 40]
        # third-party support lines (e.g. RLP help desk "M–F, 9 AM–6 PM ET") are not the Gander office
        if re.search(r"\bET\b|1-8\d\d-", ctx):
            continue
        sink(f"{rel}: states Mon-Fri clock hours {m.group(0)!r} outside a data-office-hours marker")


def main() -> int:
    g = GANDER
    want = {(d, o, c) for d in g["days"] for o, c in g["spans"]}
    print("== decided hours (D-1009-21)")
    ok(f"{display_weekdays(g)} | Sat & Sun: {g['weekend']}")

    files = subprocess.run(["git", "-C", str(ROOT), "ls-files", "*.html"], capture_output=True, text=True, check=True).stdout.split()
    if len(files) < 15:
        fail(f"only {len(files)} tracked .html files found -- the walk is blind")
    print(f"== 1-3. {len(files)} tracked .html pages")
    ld_hits: dict[str, int] = {}
    for rel in files:
        p = ROOT / rel
        if not p.is_file():
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        if "openingHours" in src:
            ld_hits[rel] = check_page_ld(rel, src, want, fail)
        if "data-office-hours" in src:
            check_markers(rel, src, g, fail)
        visible_hours_unmarked(rel, src, fail)
    missing = [r for r in REQUIRED if ld_hits.get(r, 0) != 1]
    if missing:
        fail(f"required surfaces without exactly one Gander hours node: {missing} (found {ld_hits})")
    else:
        ok(f"JSON-LD hours nodes: {ld_hits}")

    print("== 4. self-check: the probe catches the old hours")
    caught: list[str] = []
    old = ('<script type="application/ld+json">{"@type":"RealEstateAgent","address":{"streetAddress":"204 Airport Boulevard"},'
           '"openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"}}</script>')
    check_page_ld("fixture-old.html", old, want, caught.append)
    check_markers("fixture-old.html", '<div data-office-hours="gander-weekdays">Mon–Fri: 9 AM–5 PM</div>', g, caught.append)
    visible_hours_unmarked("fixture-old.html", "<p>Office open Mon–Fri 9 AM–5 PM</p>", caught.append)
    good = ('<script type="application/ld+json">{"@type":"RealEstateAgent","openingHours":["Mo-Fr 10:00-12:00","Mo-Fr 13:00-16:00"]}</script>'
            '<div data-office-hours="gander-weekdays">Mon&ndash;Fri: 10 AM&ndash;12 PM &amp; 1&ndash;4 PM</div>'
            '<p>RLP support 1-877-757-4545 (M–F, 9 AM–6 PM ET)</p>')
    clean: list[str] = []
    check_page_ld("fixture-good.html", good, want, clean.append)
    check_markers("fixture-good.html", good, g, clean.append)
    visible_hours_unmarked("fixture-good.html", good, clean.append)
    if len(caught) == 3 and not clean:
        ok("old 09:00-17:00 JSON-LD, a 9-5 marked line and a 9-5 unmarked line all flagged; the right hours pass")
    else:
        fail(f"self-check: caught={caught} clean={clean}")

    print(f"\n{'FAIL' if failures else 'PASS'}: {len(failures)} drift(s) -- hub Gander office hours vs D-1009-21")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
