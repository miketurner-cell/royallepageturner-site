# Active Listings — 2-Week Refresh Workflow

## One-time setup (done ✓)
- NLAR Matrix saved search created: **"Turner Realty - Active Listings (All Offices)"**
- Pinned as a **Favourite Search** on your Matrix home tab (My Matrix → Home)
- Criteria: Cross Property search · Status = Active · List Office Name like `Royal LePage Turner*` (wildcard captures both Gander office "Royal LePage Turner Realty 2014 Inc" and the Goose Bay office in one query)

## Bi-weekly update steps (≤ 5 minutes)

1. **Log in to Matrix** → `https://nlar.mlxmatrix.com` (or via the NLAR Clareity portal)
2. **My Matrix → Home tab** → click the favourite **"Turner Realty - Active Listings (All Offices)"**. Should return ~30-40 results (varies with season/market).
3. **Sort results by List Agent** so per-agent counts are obvious: click the "Agent" column header, or use the Display dropdown and pick a format that shows List Agent.
4. **Count listings per agent — apply half-credit for co-lists.** Use the **Agent Summary** display format (it shows the "Listed By:" line on each result). For each listing:
   - Solo listing: count **1.0** for that agent
   - Co-listed (two names on the "Listed By:" line): count **0.5 each**
   This matches Loft47's split-credit convention and means the per-agent values sum exactly to the brokerage unique-listing total.
5. **Update the dashboard.** Open `agent-accountability.html` and edit each agent's `listings:` value in the DATA const (around line 410-550). Decimals are fine (e.g. `listings: 3.5`). Also update the brokerage total near `brokerage: { ... listings: XX, ... }` (around line 411) — that one stays whole-number (count of unique MLS records).
   - **Goose Bay rule:** Karen Pomeroy and Roberta Primmer co-list everything — they always end up with **identical** `listings:` values (e.g. if the team has 5 co-listed deals, set both `karen.listings: 2.5` and `roberta.listings: 2.5`). This rule applies to every Karen/Roberta metric on the dashboard, not just listings.
6. **Commit / save the file.** The dashboard displays the new counts on next refresh:
   - Per-agent card: "Active Listings" metric chip
   - Team summary card: team-level total
   - Brokerage hero: top-of-page total across both offices

## Why listings matter for coaching
- **Leading indicator** — listings today predict closings 30-90 days out, so a pipeline gap shows up here before it shows up in GCI.
- **Balance check** — a high-closing agent with zero active listings is living off pendings; a low-closing agent with strong inventory may just need time.
- **Loft47 blind spot** — Loft47 only knows about deals (firm/conditional/closed). It has no visibility into inventory, so Matrix is the only source.

## If the saved search breaks
- If Matrix ever changes the office name structure, re-save the search with the actual office names from the List Office typeahead (comma-separated, no wildcard needed).
- As of April 2026, the wildcard `Royal LePage Turner*` returns 35 results (30 Gander + 5 Goose Bay approx.) and correctly excludes all non-Turner RLP offices.
