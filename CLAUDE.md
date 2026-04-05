# Royal LePage Turner Realty Hub Site — Project Memory

## Project
Static HTML website for Royal LePage Turner Realty — umbrella brand site serving all offices across Newfoundland & Labrador.
Domain: royallepageturner.com
Purpose: Corporate hub, company awards, multi-office directory, team roster, careers, agent training, Shelter Foundation campaigns.

## Folder Structure
This site lives in its own top-level folder: `royallepageturner-site/`
Sibling sites (each with their own folder):
- `realestategander-site/` → realestategander.com (Gander office — dark theme)
- `goosebay-site/` → goosebayrealestate.ca (Happy Valley-Goose Bay office — light theme)
- `labwestrealty-site/` → labwestrealty.com (Lab West recruiting site — not yet started)

## Process Rules (MANDATORY)
1. **ALWAYS screenshot after any visual change** — never skip this step
2. **Run `python3 tools/pre-deploy-check.py` before every deploy** — fix all errors first
3. **Use `tools/page-template.html` for new pages** — replace `xx` prefix and placeholders
4. **Never fabricate names, URLs, testimonials, or data** — verify everything against real sources
5. **Scoped CSS**: Each page uses a 2-letter prefix (.hp, .ab, .aw, .ct, .of, .tm, .jt, .at, .sf)
6. **Light theme default** — Hub site uses light backgrounds (#fff/#f7f7f7) throughout, not dark theme

## Design System — Hub LIGHT THEME

### Light Theme Tokens (Hub Standard)
- **Backgrounds**: #fff (primary), #f7f7f7 (alt/sections/cards)
- **Text**: #1a1a1a (headings), #2c2c2c (body/default), #555 (secondary text), #666 (hero sub)
- **Accent**: #EA002A (red), #c8001f (hover red)
- **Borders**: #e8e8e8 (cards, dividers, inputs), #ddd (subtle dividers)
- **Cards**: background #fff, border 1px solid #e8e8e8, border-radius 10-12px
- **Buttons**:
  - Primary: #EA002A bg / #fff text
  - Outline: transparent bg / #1a1a1a text / #ccc border, hover: border #EA002A, text #EA002A
- **Fonts**: Raleway 600/700/800/900 headings, Roboto 300/400/500 body
- **H1 standard**: clamp(34px, 5vw, 54px) or clamp(28px, 4.5vw, 44px)
- **H2 standard**: clamp(26px, 3.5vw, 38px)
- **H3 standard**: ~20px (Raleway 800)
- **Nav height**: 72px, mobile 60px
- **Section padding**: 96px 48px (desktop), 64px 20px (mobile)
- **Dark accent band**: #1a1a1a bg with #fff text for contrast/stats sections

### Light Theme — DO NOT
- Do NOT use #0a0a0a, #111, #1a1a1a, #222, #333, #888 as text colors on light backgrounds
- Do NOT use dark-theme card styles (#111111 bg, #222 border)
- Do NOT use rgba(255,255,255,0.7) as body text on light backgrounds (dark sections only)

## Nav Markup (CRITICAL)
Each page uses a custom scoped nav bar (NOT the two-element nav pattern).
Pattern: `<nav class="nav-bar">` with scoped classes (.hp .nav-bar, .ab .nav-bar, etc.)
Structure:
- `.nav-brand` — Logo + brand name
  - `.nav-brand-name` — Main brand text (Raleway 900 18px)
  - Span inside .nav-brand-name with color #EA002A
  - `.nav-brand-divider` — Vertical divider (1px #ddd)
  - `.nav-brand-sub` — Subtext "Newfoundland & Labrador" (11px, #999, uppercase)
- `.nav-links` — Horizontal flex menu (14px, #555, hover #EA002A)
- `.nav-right` — Phone button + CTA
  - `.nav-phone` — tel link with SVG icon
- `.nav-toggle` — Mobile hamburger (hidden on desktop)

Mobile breakpoint: max-width 1024px
- Nav height drops to 60px
- .nav-brand-divider and .nav-brand-sub hidden
- .nav-toggle displayed as flex
- .nav-links becomes dropdown (position absolute)

## Office Details
- **Legal Name**: Royal LePage Turner Realty (2014) Inc.
- **Main Address**: 204 Airport Boulevard, Gander, NL A1V 1L6
- **Main Phone**: 709-256-7999
- **Website**: royallepageturner.com

## Office Network
1. **Gander** (main office) — 204 Airport Blvd, Gander, NL A1V 1L6 — 709-256-7999
2. **Happy Valley-Goose Bay** — 1 Loring Drive, Happy Valley-Goose Bay, NL A0P 1C0 — 709-896-5001
3. **St. John's** — (expansion office)
4. **Labrador West** — recruiting site (labwestrealty.com) — not yet built

## Real Agents (11 total REALTORS)
**Brokers of Record (Gander)**
1. Mike Turner — 709-256-7999
2. Gaye Turner — 709-256-7999

**Salespersons (Gander)**
3. Dwayne Kean — 709-424-4557
4. Ashley Bullen — 709-571-0896
5. Danielle Pike — 709-424-6686
6. Matt Wheaton — 709-424-4978
7. Kayla Tulk — 709-424-5498
8. Crystal Hynes — 709-571-6799

**Goose Bay Office (2)**
9. Karen Pomeroy — 709-896-5001
10. Roberta Primmer — 709-896-7509

**St. John's (1)**
11. [TBD — office staff to confirm]

## Social Links
- Facebook: https://www.facebook.com/realestategander
- YouTube: https://www.youtube.com/playlist?list=PLr4XcQLT7UeO_8OZSgtx6h2N6dvsmsY_Y

## Site Structure (13 HTML pages total)
- **index.html** (.hp) — Hero, stats strip (27+ years, 11 REALTORS, 3 offices), office cards
- **about.html** (.ab) — Company history, timeline (1998-present), broker bios, prose sections
- **awards.html** (.aw) — 8+ brokerage awards, detail cards (Brokerage of Year, Tech, Shelter, Lead Manager finalist), timeline
- **contact.html** (.ct) — Contact grid (phone, address, map), office cards, contact form
- **team.html** (.tm) — 11 REALTORS roster (currently placeholder/light content)
- **offices.html** (.of) — 3 active office detail cards (map, address, phone), network summary stats
- **join-our-team.html** (.jt) — Careers page (70/30 commission, profit sharing, benefits, CTA)
- **agent-training.html** (.at) — Agent resource center (accordion sections, quick links sidebar, rlpNetwork/CRM/Smart Leads/tools)
- **shelter-foundation.html** (.sf) — Shelter Foundation info, stats, giving cards, awards section, dark CTA section
- **sitemap.xml** — XML sitemap
- **robots.txt** — Robot exclusions
- **deploy.sh** — Deployment script

## Scoped CSS Prefixes (Per Page)
- .hp — Home page (index.html)
- .ab — About page
- .aw — Awards page
- .ct — Contact page
- .of — Offices page
- .tm — Team page
- .jt — Join our team (careers)
- .at — Agent training
- .sf — Shelter Foundation

## Integrations
- **GA4 Measurement ID**: G-FEMZDX1BJQ — Same as Gander/Goose Bay sites
- **Fonts**: Google Fonts (Raleway 600/700/800/900, Roboto 300/400/500)
- **No Rechat or RealtyVis** — Hub site is corporate hub, not local office site

## Key Design Patterns

### Hero Section (.hp, .at, others)
- Background: linear-gradient(135deg, #f8f8f8 0%, #fff 50%, #f5f5f5 100%)
- Optional::before pseudo-element with repeating red grid pattern (opacity 0.025)
- Badge: inline-flex, #EA002A text, rgba(234,0,42,0.06) bg, border 1px solid rgba(234,0,42,0.15)
- H1: clamp font sizes, #1a1a1a color, em span with #EA002A for accents
- Sub: #666 color, 300 font-weight

### Section Titles
- Eyebrow: 12px, #EA002A, uppercase, 0.12em letter-spacing, margin-bottom 12px
- H2/H3: Raleway 900, clamp(26px, 3.5vw, 38px) or clamp(28px, 4.5vw, 44px), #1a1a1a, margin 0 0 16px/24px
- Section desc: 17px, #666, line-height 1.75, max-width 600-620px

### Card Styling
- White background (#fff), border 1px #e8e8e8, border-radius 10-12px, padding 40-48px
- Hover: border-color #EA002A, box-shadow 0 12px 40px rgba(0,0,0,0.05-0.06), transform translateY(-4px)
- Icon circles: 48-68px, background rgba(234,0,42,0.06-0.08), centered SVG fill #EA002A

### Stats Strip
- Background: #1a1a1a (dark), white text
- Display: flex justify-content center, flex-wrap wrap
- Stat items: flex 1 1 200px, max-width 280px, text-align center, padding 40px 24px
- Border-right: 1px solid rgba(255,255,255,0.08) between items
- Numbers: Raleway 900, clamp(26px, 3.5vw, 40px), white, em span with #EA002A
- Labels: 13px, rgba(255,255,255,0.5)

### Detail Cards (Awards, Offices)
- Two-column grid: 1fr 1fr, gap 0
- Left side (.dc-visual/.od-map): flex centered, padding 56px 40px, background variations
- Right side (.dc-info/.od-info): padding 48px 40px
- Mobile: grid-template-columns 1fr (stacked)

### Timeline
- Relative position, padding-left 48px
- ::before pseudo-element: 2px vertical line (left 14px)
- .tl-dot: 14px circle, position absolute left -42px, background #EA002A, border 3px solid background-color
- Years/titles: Raleway bold/900

### Footer (Consistent)
- Background: #fafafa, border-top 1px #e8e8e8, padding 56px 48px 0
- Grid: 3 columns (2fr 1fr 1fr) with 48px gap
- Red bar: #EA002A bg, margin 0 -48px, padding 14px 48px, flex between
- Legal text: 11px, #aaa, centered, padding 20px 0
- Links hover: #EA002A

## Common Components

### Buttons
**Primary**: #EA002A bg, #fff text, Raleway 700, 14px, padding 14px 32px, border-radius 6px, hover #c8001f
**Outline**: transparent bg, #1a1a1a text, border 1px #ccc, hover: border #EA002A, text #EA002A, border-radius 6px
**Visit buttons** (.btn-visit): inline-flex, #EA002A bg, #fff text, 13px, 28px padding, SVG icon

### Forms
- Input background: #f7f7f7
- Input border: 1px #e8e8e8
- Input text: #2c2c2c
- Focus states: border-color #EA002A
- Labels: 14px, #1a1a1a

### Mobile Breakpoint
- max-width: 1024px
- Nav padding 0 20px, height 60px
- Section padding 64px 20px
- Footer margin 0 -20px
- Multi-column grids collapse to 1-2 columns

## Common Mistakes to Avoid
- Converting page themes without updating ALL text colors
- Using find-replace on accent colors without checking text/background pairings
- Forgetting nav scoping (using .site-nav or .nav-links without prefix)
- Using hardcoded phone numbers instead of centralized references
- Not verifying hero images display (CSS property override issues)
- Using old Squarespace /slug links instead of relative paths
- Using onsubmit="return false;" on forms (blocks addEventListener handlers)
- Mixing dark theme colors (#111, #222) with light theme pages
- Forgetting to include GA4 script tag in <head>
- Using incorrect link targets (verify all hrefs to ensure pages exist)

## Branding Standards
- **Official name**: Royal LePage Turner Realty (not "Turner Realty" alone in headers)
- **Brand mark**: "Turner" in red (#EA002A) in most logos/headers
- **Tone**: Professional, family-oriented, community-focused
- **Key messages**: Multi-office coverage, local expertise, national Royal LePage support
- **Awards**: Consistently promoted (A.E. LePage Brokerage of Year, Best in Tech, Shelter Foundation)
- **Team**: Emphasize years of experience, community roots, family business

## Data Integrity Rules
- **Award data**: Verified against 2025 awards inventory; production awards 2007-2025, 5 leadership wins
- **Agent info**: Use current list of 11 licensed REALTORS, verify phone numbers
- **Office addresses**: Gander (204 Airport Blvd A1V 1L6), Goose Bay (1 Loring Drive A0P 1C0)
- **Brokerage registration**: "Royal LePage Turner Realty (2014) Inc." — exact legal name
- **Founding year**: 1998 (Gaye Turner founding), office expansions 2016+ (Goose Bay)
- **Facebook verified**: All Turner Realty posts are pre-verified (feedback_facebook_verified.md)

## Pending / Future Work
- Lab West recruiting site (labwestrealty.com) — not yet started
- St. John's office expansion details (office page, team roster, office-specific site)
- agent-bio pages for all 11 REALTORS (if/when individual pages requested)
- Enhanced team.html with full roster cards, photos, bios
