#!/usr/bin/env python3
"""STRICT: no public recruiting on this site (D-1009-19, Mike 2026-10-09).

Mike, 2026-10-09: "we are not in recruiting mode, so let's make sure that that is not on
the websites for Gander, Goose Bay, and the Avalon." The hub (royallepageturner.com) is
the same, except exactly ONE careers mention, which points to labwestrealty.com (Lab West
keeps recruiting). Lab West itself is out of scope and this test is not shipped there.

Crawls the built site folder (no network) and fails on:
  1. a link, form action or script/iframe src on any served page that points at a
     recruiting URL (join-our-team, become-a-realtor, careers, recruit, why-join, joinTeam);
  2. recruiting wording in the visible text, title/alt/aria-label/placeholder attributes or
     JSON-LD of any served page outside listings/ and property/ (MLS remarks are not ours);
     on the hub, exactly one hit is allowed and it must sit inside a link to labwestrealty.com;
  3. a recruiting URL in any sitemap*.xml;
  4. an archived recruiting page (_archive/recruiting/) without noindex, or without a
     temporary (302) redirect for its old URL in _redirects.

It cannot see menus and footers that JavaScript renders, so it also scans js/nav-config.js
and js/footer.js and PRINTS what recruiting remains there (not a failure: nav-config.js is
the redesign session's file under D-1009-19). Add --strict-js to make those fail too.

Usage:
  python3 tools/tests/no-public-recruiting-test.py            # fail on any hit
  python3 tools/tests/no-public-recruiting-test.py --report   # print hits, exit 0
  python3 tools/tests/no-public-recruiting-test.py --strict-js
This file is identical in the four repos it runs in (Gander, Avalon, Goose Bay, hub).
"""
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {".git", "node_modules", "_archive", "tools", "fleet", ".claude", ".github",
             "_ops", "_research", "_drafts", "netlify", "supabase", "scripts", "docs",
             "_scratch", "venv", ".venv", "4-reference"}
# Folders whose page text is listing data (MLS remarks), checked for links only.
LINKS_ONLY_DIRS = {"listings", "property"}
SKIP_TAGS = {"script", "style", "noscript", "template", "head"}
ATTRS = {"title", "placeholder", "aria-label", "alt", "aria-description"}
URL_ATTRS = {"href", "src", "action", "data-href"}

URL_RE = re.compile(r"(join-our-team|join-team|jointeam|become-a-realtor|careers?\b|careers\.html|"
                    r"recruit|why-join|now-hiring|agent-hub|first-year-realtor)", re.I)
TEXT_PATTERNS = [
    ("join our team", re.compile(r"\bjoin\s+(our|the)\s+(growing\s+)?team\b", re.I)),
    ("become a REALTOR", re.compile(r"\bbecome\s+an?\s+(licensed\s+)?realtor", re.I)),
    # "careers" only in a recruiting sense: healthcare/military careers on relocation pages are consumer copy.
    ("careers", re.compile(r"^\s*careers\s*(\u2192|>|&gt;)?\s*$|\bcareers?\s+(with|at)\s+(royal|turner|us\b|our\b)"
                           r"|\bbuild\s+(their|your)\s+careers?\b|\bcareer\s+in\s+real\s+estate\b"
                           r"|\breal\s+estate\s+careers?\b|\bsee\s+career\s+opportunit|\bcareer\s+opportunities\s+(with|at)\s+(us|our|turner|royal)\b", re.I)),
    # "recruiting" only about agents: the hospital recruiting nurses is consumer copy.
    ("recruiting agents", re.compile(r"\brecruit\w*\s+(other\s+)?(agents?|realtors?)\b|\b(agents?|realtors?)\s+recruit"
                                     r"|\brecruiting\s+(quotas?|overrides?)\b|\b(no|not|now)\s+recruiting\b"
                                     r"|^\s*recruiting(\s+faq)?\s*$", re.I)),
    ("now hiring", re.compile(r"\b(now\s+hiring|we['\u2019]re\s+hiring|we\s+are\s+hiring)\b", re.I)),
    ("confidential call", re.compile(r"\bconfidential\s+(call|conversation|chat|career)", re.I)),
    ("agent opportunity", re.compile(r"\b(agent|realtor)\s+opportunit", re.I)),
    ("join Turner as an agent", re.compile(r"\bjoin\s+(royal\s+lepage\s+)?turner(\s+realty)?\s+(and\s+unlock|as\s+an?\s+(agent|realtor))", re.I)),
]
LABWEST = "labwestrealty.com"


def site_host():
    p = os.path.join(ROOT, "sitemap.xml")
    try:
        m = re.search(r"<loc>\s*https?://(?:www\.)?([^/<\s]+)", open(p, encoding="utf-8").read())
        return m.group(1).lower() if m else ""
    except OSError:
        return ""


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.ldjson = 0
        self.anchor_stack = []  # hrefs of open <a>
        self.urls = []          # (tag, attr, value)
        self.texts = []         # (kind, text, inside_href)

    def _attrs(self, tag, attrs):
        d = dict(attrs)
        for k, v in attrs:
            if not v:
                continue
            if k in URL_ATTRS:
                self.urls.append((tag, k, v))
            if k in ATTRS and not self.skip:
                self.texts.append((f"{tag}[{k}]", v, self.anchor_stack[-1] if self.anchor_stack else ""))
        return d

    def handle_starttag(self, tag, attrs):
        d = self._attrs(tag, attrs)
        if tag == "a":
            self.anchor_stack.append(d.get("href") or "")
        if tag == "script" and (d.get("type") or "").lower() == "application/ld+json":
            self.ldjson += 1
        if tag in SKIP_TAGS:
            self.skip += 1

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor_stack:
            self.anchor_stack.pop()
        if tag == "script" and self.ldjson:
            self.ldjson -= 1
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        t = " ".join(data.split())
        if not t:
            return
        if self.ldjson:
            self.texts.append(("json-ld", t, ""))
        elif not self.skip:
            self.texts.append(("text", t, self.anchor_stack[-1] if self.anchor_stack else ""))


def served_pages():
    for dp, dns, fns in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        top = rel.split(os.sep)[0]
        dns[:] = [d for d in dns if not (rel == "." and d in SKIP_DIRS) and not d.startswith(".")]
        for fn in fns:
            if fn.endswith(".html"):
                yield os.path.join(dp, fn), (top in LINKS_ONLY_DIRS)


def is_recruit_url(v):
    v2 = v.split("#")[0]
    if LABWEST in v2.lower():
        return False  # Lab West keeps recruiting; a link there is the hub's one allowed mention
    if v2.lower().startswith(("mailto:", "tel:", "data:", "javascript:")):
        return False
    return bool(URL_RE.search(v2))


def snippet(t, m):
    a, b = max(0, m.start() - 50), min(len(t), m.end() + 50)
    return t[a:b]


def scan_pages(host):
    fails, allowed = [], []
    is_hub = "royallepageturner" in host
    for path, links_only in served_pages():
        rel = os.path.relpath(path, ROOT)
        try:
            src = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        src_nc = re.sub(r"<!--.*?-->", "", src, flags=re.S)
        p = Page()
        try:
            p.feed(src_nc)
        except Exception as e:  # malformed page: report, do not hide
            fails.append((rel, "parse", str(e)[:120]))
            continue
        for tag, attr, v in p.urls:
            if is_recruit_url(v):
                fails.append((rel, f"{tag}[{attr}]", v))
        if links_only:
            continue
        for kind, t, inside in p.texts:
            for label, rx in TEXT_PATTERNS:
                for m in rx.finditer(t):
                    hit = (rel, f"{kind} '{label}'", snippet(t, m))
                    if is_hub and LABWEST in (inside or "").lower():
                        allowed.append(hit)
                    else:
                        fails.append(hit)
    if not is_hub and allowed:
        fails.extend(allowed)
        allowed = []
    return fails, allowed


def scan_sitemaps():
    fails = []
    for fn in sorted(os.listdir(ROOT)):
        if fn.startswith("sitemap") and fn.endswith(".xml"):
            for loc in re.findall(r"<loc>\s*([^<\s]+)", open(os.path.join(ROOT, fn), encoding="utf-8").read()):
                if is_recruit_url(loc):
                    fails.append((fn, "sitemap loc", loc))
    return fails


def scan_archive():
    fails, archived = [], []
    adir = os.path.join(ROOT, "_archive", "recruiting")
    if not os.path.isdir(adir):
        return fails, archived
    redirects = ""
    rp = os.path.join(ROOT, "_redirects")
    if os.path.exists(rp):
        redirects = open(rp, encoding="utf-8").read()
    rules = []
    for line in redirects.splitlines():
        parts = line.split("#")[0].split()
        if len(parts) >= 3:
            rules.append(parts)
    if not re.search(r"^/_archive/\*\s+\S+\s+404!", redirects, re.M):
        fails.append(("_redirects", "archive", "/_archive/* must be blocked (404!) so archived pages never serve"))
    for dp, _, fns in os.walk(adir):
        for fn in fns:
            if not fn.endswith(".html"):
                continue
            full = os.path.join(dp, fn)
            relarc = os.path.relpath(full, adir).replace(os.sep, "/")
            archived.append(relarc)
            src = open(full, encoding="utf-8", errors="replace").read()
            if not re.search(r"<meta[^>]+name=[\"']robots[\"'][^>]+noindex", src, re.I):
                fails.append((f"_archive/recruiting/{relarc}", "noindex", "archived page lacks <meta name=robots noindex>"))
            old = "/" + relarc
            ok = [r for r in rules if r[0] == old and r[2] in ("302", "302!")]
            if not ok:
                fails.append(("_redirects", "302", f"no temporary (302) redirect for former URL {old}"))
            stem = old[:-5]
            ok2 = [r for r in rules if r[0] == stem and r[2] in ("302", "302!")]
            if not ok2:
                fails.append(("_redirects", "302", f"no temporary (302) redirect for former URL {stem}"))
            for r in rules:
                if r[0] in (old, stem) and r[2] not in ("302", "302!"):
                    fails.append(("_redirects", "stale rule", " ".join(r)))
    return fails, archived


def scan_js():
    """(remaining, labwest): recruiting lines in the JS menus/footer; lines that point at labwestrealty.com
    are the hub's allowed Lab West careers mention, counted separately."""
    out, labwest = [], []
    for rel in ("js/nav-config.js", "js/footer.js"):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            code = line
            if not code.strip() or code.lstrip().startswith(("//", "*", "/*")):
                continue  # comments are not shown to visitors
            hit = URL_RE.search(code.replace(LABWEST, "")) or any(rx.search(code) for _, rx in TEXT_PATTERNS) \
                or re.search(r"['\"]careers?\b", code, re.I)
            if LABWEST in code.lower():
                if hit:
                    labwest.append((rel, i, line.strip()[:160]))
                continue
            if hit:
                out.append((rel, i, line.strip()[:160]))
    return out, labwest


def main():
    report = "--report" in sys.argv
    strict_js = "--strict-js" in sys.argv
    host = site_host()
    page_fails, allowed = scan_pages(host)
    sm_fails = scan_sitemaps()
    arc_fails, archived = scan_archive()
    js_left, js_labwest = scan_js()
    fails = page_fails + sm_fails + arc_fails
    if "royallepageturner" in host:
        # The same header item appears once per header config (old header + header v2); count distinct items, not lines.
        n = len(allowed) + len({line.rstrip(',').strip() for _, _, line in js_labwest})
        for rel, i, line in js_labwest:
            print(f"  allowed (hub Lab West mention): {rel}:{i}: {line}")
        if n != 1:
            fails.append(("(hub)", "labwest careers mention",
                          f"expected exactly 1 careers mention, linking to {LABWEST} (pages + js/nav-config.js), found {n}"))
    elif js_labwest:
        js_left += js_labwest
    print(f"site: {host or '(unknown)'}; archived recruiting pages: {len(archived)} {archived}")
    for a in allowed:
        print(f"  allowed (hub Lab West mention): {a[0]}: {a[1]}: {a[2]}")
    for f in fails:
        print(f"  FAIL {f[0]}: {f[1]}: {f[2]}")
    print(f"JS menus/footer (js/nav-config.js, js/footer.js): {len(js_left)} recruiting line(s) remain"
          + (" -- redesign's to remove under D-1009-19" if js_left else ""))
    for rel, i, line in js_left:
        print(f"  JS {rel}:{i}: {line}")
    if strict_js:
        fails += [(r, i, l) for r, i, l in js_left]
    print(f"{'FAIL' if fails else 'OK'}: {len(fails)} public recruiting finding(s) in pages/sitemaps/archive"
          + (" (report mode)" if report else ""))
    return 0 if (report or not fails) else 1


if __name__ == "__main__":
    sys.exit(main())
