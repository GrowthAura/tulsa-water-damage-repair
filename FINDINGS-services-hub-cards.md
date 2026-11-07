# Services Hub Cards Fix + Site-Wide Repeat Audit — FINDINGS

- Date: 2026-11-07 ~15:05–15:20 PKT. Scope: /services/ hub + homepage services section; audit all 53 routes.
- Build: `npm run export` green, 56/56 static pages. Sitemap still 53 URLs.
- Local only — no push/deploy/domain/DNS/token.

## 1. The problem (verified before the fix)

The /services/ hub showed all 18 services TWICE: a builder-added top card grid
under H2 "Our Water Damage Services" (18 cards with images), then the doc's own
five grouped sections (H2 + intro + plain bullet list of the same service links).
Each /services/ link appeared 4–8x in the built hub HTML. The user screenshotted
the grouped lists from the full-pages PDF and asked where THOSE services' cards are.

## 2. Before → after (hub)

| Before | After |
|---|---|
| Top grid: H2 "Our Water Damage Services" + 18 cards | Deleted entirely (H2 + grid gone, 0 occurrences in built HTML) |
| 5 grouped sections: H2 + intro + plain bullet list | Same H2 + intro verbatim, list converted to a card grid under each heading |
| Each service: 1 card (top grid) + 1 list link | Each service: exactly 1 card, in its own group |
| "Which Service Do I Need?" table | Kept as-is (different purpose: situation matcher) |

Hub now: 18 card articles, 18 unique card title hrefs, 0 dupes; 16 card images
loaded 16/16 (slow scroll) + 2 branded panels (sewage, slab-leak — no hero image
in images.json, no forced filler). Only plain `<ul>` left in hub content is the
documentation list ("Your documentation includes:" — correctly still a list).
Group H2s + intros verbatim; doc anchor "Learn more about the mitigation phase:"
untouched; "Which Service Do I Need?" table untouched.

## 3. Homepage — the identical duplication existed there too, fixed the same way

The homepage had the same 18 services twice: the same five grouped lists
(blocks 13/15/17/19/21, under bold label paragraphs, no group H2s) + the
builder-inserted ServiceCards grid after the section's `<hr>`. Fixed identically:
lists → card grids under their verbatim label paragraphs, inserted grid deleted
(including the fallback insertion). Homepage now: 37 cards = 18 service cards
(16 imgs + 2 panels, loaded 35/35 incl. area cards) + 19 area cards.
"See every service organized in one place" paragraph kept. AreaCards untouched:
the areas section is prose + a ZIP-code data table, not a link-list — no duplication.

Homepage lists differ from hub lists: each item is ONE link with NO `<strong>`
separator, and 8 items are title-only (no description words). Title for those
comes from the doc's service name for that href (taken from the hub's grouped
lists, `SERVICE_TITLES` in lib.js — same words, same casing, e.g. "AC drain
line overflow cleanup", "Flooded basement and crawlspace cleanup"); description
= the item's remaining text verbatim; title-only items get no description
paragraph (nothing invented). No `<strong>`-less item failed to parse: 18/18.

## 4. /resources/ hub — audited, no duplication

ResourceCards only (10 cards), no lists. Nothing changed.

## 5. Site-wide repeat audit (all 53 sitemap routes, built HTML)

Script: `site/tools/audit_repeats.py` (slash-normalised comparison — see §6).
Checks per page, main content only (header/footer/nav excluded):
A. duplicate card hrefs · B. duplicate H2s · C. href as BOTH card link and plain
body link · D. same image twice on one page · E. plain body href linked 2+ times.

| Check | Result |
|---|---|
| A. duplicate card hrefs | 0 pages |
| B. duplicate H2 texts | 0 pages |
| C. card link + plain body link | 2 pages — hub + homepage, both intentional (see below) |
| D. duplicate image on one page | 0 pages |
| E. plain body href 2+ times | 51 pages — doc prose cross-links + template CTAs (see below) |

C — hub (8 services): the "Which Service Do I Need?" table links 8 services
that also have cards. Kept deliberately: situation matcher, different purpose,
ordered kept as-is in the original fix brief. Homepage (20 hrefs): 12 area hrefs
= AreaCards vs the ZIP-code data table (City | Zip codes | Page — data table,
different purpose, doc content, kept); 8 service hrefs = service cards vs
doc prose in-text links in other homepage sections ("Read how the drying phase
works…", "Full details on how…", cause/process paragraphs — verified by context).
All are doc content with a different purpose, NOT the cards-vs-list pattern.
No fix applied — removing any would delete verbatim doc links.

E — 51 pages link some href 2+ times in plain body text. All verified as doc
prose cross-links (a service/guide linked from two different paragraphs of the
same article — normal editorial cross-linking, verbatim from the doc) plus
template items inside the main slice (breadcrumb "Home" link, tel: call CTAs in
the navy band / sticky aside / body paragraphs, FEMA flood-map link repeated on
the flood page). Not the cards-vs-list pattern; nothing changed — doc links are
verbatim and the doc-link rule forbids deleting them.

Conclusion: NO further fixable duplication of the hub pattern anywhere on the
site. The only clear cards-vs-list duplication was hub + homepage services,
now fixed. Everything else is fine as-is per the user's "baaki okay hai".

## 6. Notes / caveats

- Trailing-slash normalisation: `next.config.js` has `trailingSlash: true`, so
  Next `<Link>` renders card hrefs with a trailing slash even where the doc href
  has none (e.g. card `/services/emergency-water-damage-restoration/` vs doc
  `/services/emergency-water-damage-restoration`). Pre-existing behaviour — the
  old top grid did exactly the same. Canonicals are still rendered manually in
  the doc's exact mixed forms. The audit compares hrefs slash-insensitively for
  this reason. Not changed (out of scope; deploy note about no-slash 200-vs-308
  still stands).
- `ServiceCards` (Shared.jsx) is now unused anywhere — definition left in place,
  only its usages were deleted. `SERVICE_SLUGS` is still exported from lib.js
  (used by nothing now); `SERVICE_GROUPS` still feeds the nav dropdown.
- The first fast probe showed card images "unloaded" (hub 7/16, home 16/35) —
  a lazy-loading timing artifact (same as Round 2). Re-verified with a slow
  scroll + 2.5s wait: hub 16/16, home 35/35. All 16 hub / 35 home card image
  files exist on disk.
- The first section-screenshot run used scrollIntoView and landed on the wrong
  offsets; retaken with explicit scroll positions and viewed by pixels.

## 7. Verification (fresh, after rebuild)

- Build green, 56/56 static pages; sitemap 53 URLs, no image entries.
- Hub: overflow 0 at 1440/390/320; H1 = 1 ("Water Damage Restoration Services
  in Tulsa, OK"); console errors 0; 18 cards, 18 unique hrefs; 5 group H2s;
  no "Our Water Damage Services"; only doc ul left in content.
- Homepage: overflow 0 at 1440/390/320; H1 = 1; console errors 0; 37 cards
  (18 service + 19 area); 5 group labels verbatim; remaining content uls are
  the two "What Should I Do Before the Crew Arrives?" checklists (correctly lists).
- Resources hub: overflow 0 at 1440/390/320; H1 = 1; console 0; 10 cards.
- Sitewide overflow probe (all 53 pages, 390/320): 0 overflow pages.
  Card images loaded 35/35 home, 16/16 hub (tools/probe_overflow.py).
- Screenshots viewed by pixels: `site/qa-hub-cards/` (full pages + probe.json)
  and `site/qa-hub-cards/sections/` (per-group heading + grid, 1440 + 390):
  2-col hub grids beside the sticky aside, 3-col homepage grids, sewage +
  slab-leak branded panels, single Commercial card, mobile single-column cards
  with the sticky call bar visible. No text under images, no layout break.

## 8. Files changed

- `app/components/Shared.jsx` — new `ServiceListCards` + `serviceListItems`
  (parse doc list items into cards; returns null for any non-service list shape).
- `app/lib.js` — new `SERVICE_TITLES` map (doc service names per href, from the
  hub's grouped lists, for the homepage's `<strong>`-less items).
- `app/[[...slug]]/page.js` — `Block` renders service lists as card grids on
  hub/homepage only; hub top grid deleted; homepage ServiceCards insertion +
  fallback deleted; unused `ServiceCards`/`SERVICE_SLUGS`/`isHub` imports removed.
- `app/globals.css` — `.split .cards` 2 columns at ≥1024px (hub's 725px text
  column; 3 columns would squeeze cards to ~225px) + `.content-block .cards`
  bottom margin.
- No words, images, links, schema, phone, header, or footer touched.
- Findings: `site/FINDINGS-services-hub-cards.md` (this file). Audit + probe:
  `site/tools/audit_repeats.py`, `site/tools/probe_hub_cards.py`.
  Screenshots: `site/qa-hub-cards/`, `site/qa-hub-cards/sections/`.
