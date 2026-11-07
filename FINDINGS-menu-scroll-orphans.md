# Menu scrollers + orphan audit + policy check — 2026-11-07 ~19:43–20:10 PKT (DONE, local only)

Task: (1) lovely scroller in header Services + Service Areas dropdowns, desktop + mobile;
(2) no orphan pages sitewide, fresh audit; (3) policy page → noindex IF it exists.
Only source change: `app/globals.css` (menu scroll rules). No words, links, phone or
schema facts changed. Rebuild green (`npm run export`, 23 flat .html + 30 slash routes).

## 1. Scrollable header menus

Before: `.nav-drop` had no max-height and no overflow — the 18-service / 19-area lists
ran the full height of the page. `.mobile-menu` already scrolled (max-height 100dvh−5rem)
but had the browser-default scrollbar.

After (`app/globals.css`):
- `.nav-drop`: `max-height: min(28rem, calc(100dvh − 7rem))`, `overflow-y: auto`,
  `overscroll-behavior: contain`, `scrollbar-gutter: stable`, `scrollbar-width: thin`,
  `scrollbar-color: var(--blue) var(--pale)`, plus `::-webkit-scrollbar` rules —
  8px wide, pale track (#a9d4ed), blue thumb (#0056a3), navy on hover, rounded.
- `.mobile-menu`: same styled-scrollbar treatment + `overscroll-behavior: contain`
  and `scrollbar-gutter: stable` (its max-height/overflow were already there).

Measured (Playwright, real Chromium, `tools/probe_menu_scroll.py` + focused re-probe):
- Desktop Services @1440: content 1173px vs cap 448px → scrolls; 19 links
  (18 services + "View every service"); 0 unreachable; page overflow 0; console 0.
- Desktop Areas @1440: content 887px vs cap 448px → scrolls; 19 links
  (Midtown…Sapulpa); 0 unreachable; page overflow 0; console 0.
- Keyboard: Tab from the "Service Areas" summary lands on the first link
  ("Midtown", `<a>` focused) — all items reachable by keyboard, container
  auto-scrolls to the focused item.
- Mobile menu @390: content 2296px vs cap 762px → scrolls; 42 links; 0 unreachable;
  page overflow 0; console 0.
- Scrollbar paint verified: computed `::-webkit-scrollbar` width 8px, thumb
  rgb(0,86,163), track rgb(169,212,237); pixel-sampled on screenshots
  (pale track + blue thumb visible at the dropdown's right edge).

Honest probe note: the first probe run reported 11 "unreachable" links for Areas —
that was a PROBE bug, not a site bug (its `drops.find(offsetParent)` selector picked
the still-open Services dropdown after the Escape keypress). The focused re-probe
selecting `details[open] .nav-drop` directly measured Areas correctly: 19/19
reachable. Same for the scrollbar: Playwright launches Chromium with
`--hide-scrollbars`, so default screenshots hide the thumb; the paint was verified
with `ignore_default_args=['--hide-scrollbars']` (screenshots
`desktop-drop-areas-scrollbar.png`, `mobile-menu-top.png`).

Screenshots (viewed by pixels): `site/qa-menu-orphans/` — `desktop-drop-services.png`,
`desktop-drop-areas.png`, `desktop-drop-areas-scrollbar.png`, `mobile-menu-open.png`,
`mobile-menu-top.png`, `menu-scroll.json`.

## 2. Orphan audit — 0 orphans, no fixes needed

Method (fresh, on the rebuilt `out/`): route set = 53 sitemap locs; for each built
HTML file (RSC `<script>` payloads stripped to avoid double counting), collected
internal hrefs and counted DISTINCT source pages linking to each route, EXCLUDING
self-links (a page linking to itself does not count as inbound).
Result: **orphans: NONE (0)** — every one of the 53 routes has ≥1 inbound link
from another page. Lowest inbound counts (distinct source pages):
- 1 — `/commercial` ← `/services/fire-damage-restoration` only (the FAQ link
  "Commercial fire losses" — the fix from the previous round, CONFIRMED still in
  place; no longer orphaned).
- 1 — `/resources/water-damage-vs-flood-damage-insurance-oklahoma` ← `/resources`
  (hub card).
- 4 — `/resources/mold-after-water-damage-tulsa`; 5 — first-24-hours,
  signs-of-hidden-water-damage, categories-and-classes; 9–39 for the other guides.
- Header/footer/nav chrome links `/`, `/services/`, `/about-us/`, `/resources/`,
  `/contact/` on every page (counts in the dozens–hundreds, as expected).
No link was added in this round — nothing to fix. No "See" anchors added.

## 3. Policy page — does NOT exist, nothing done

Searched `content/pages.json`, `app/`, `public/sitemap.xml` and the 53 routes for
`privacy`, `terms-of-service`, `terms of service` — zero hits. There is no
privacy-policy or terms-of-service page anywhere on the site, so no noindex was
added and nothing was removed from the sitemap. Per his order: its ok.

## Final verification (fresh final build)

- `probe_a2z.py`: 53 routes, overflow 0, H1=1 everywhere, console errors [],
  card images 37/37 home + 18/18 services + 8/8 resources, internal refs 158
  broken [], sitemap 53 = pages.json 53, FAQ mismatches [].
- `verify_site.py`: 53 pages, 2,390 internal link fetches all 200,
  reachable from home 54/53, PROBLEMS: 0.
  (Note: it overwrote `FINDINGS-round1.md` again — known trap — restored from git
  right after; `git status` clean for that file.)
- Sitemap: 53 locs, unchanged.

## Files

- Changed: `app/globals.css` (scroller rules only).
- New: `site/tools/probe_menu_scroll.py`, `site/FINDINGS-menu-scroll-orphans.md`,
  `site/qa-menu-orphans/` (5 screenshots + `menu-scroll.json`).
- PROGRESS.md updated. Local only — no push/deploy/domain/DNS/token.
