# Upgrades U1–U7 — Tulsa Water Damage Repair (2026-11-08)

Local only — no push, deploy, domain/DNS, or token touched. Parent holds the
token and pushes after independent verification. Build: `npm run export`
(Next.js 14.2.35 after U4). All measurements are fresh re-runs on the final
build, same methodology before/after (Playwright headless Chromium, fresh
browser, no cache; transfer = navigation + resource `transferSize`).

## U1 — Per-page data split (biggest gap) — DONE, verified

**Problem (before):** `app/lib.js` imported the whole `content/pages.json`
(796 KB) at module top level, and 'use client' components (Header,
ContactForm) imported from it — so the full dataset shipped in the shared
client chunk: `986-…js` = 710,479 B, homepage JS transfer 1,040,550 B,
homepage total 1,305,126 B mobile / 2,141,131 B desktop vs the <800 KB budget.
`IICRC S500` (page-body text) was literally inside the client chunk.

**Fix — split the module (no rendering logic changed):**
- **NEW `app/lib-meta.js`** — client-safe metadata only, ZERO JSON imports:
  `SITE`, `SERVICE_GROUPS`/`SERVICE_SLUGS`, `AREA_GROUPS`/`AREA_SLUGS`,
  `FOOTER_SERVICES`, `FOOTER_AREAS`, `RESOURCE_SLUGS`, `TRUST_CHECKS`,
  `SERVICE_TITLES`, `normSlug`, `shortName`, `parentOf`, `areaMapQuery`
  (all literals/pure functions, moved verbatim from lib.js).
- `SERVICE_TITLES` is now a **static literal** (15 entries, values verbatim
  from the /services/ hub doc lists, including the `<a>` tags some carry —
  `parseServiceItem` strips those at render, B1 fix). Previously computed at
  runtime by scanning PAGES, which forced pages.json into the client bundle.
  Regeneration recipe is in the file's comment (hub ul-block items:
  href -> `<strong>` inner HTML + normSlug key).
- **`app/lib.js` rewritten (216 lines -> ~70)** — server-only data only:
  `pages.json`/`images.json` imports, `fixPage`/`unescapeEntities`, `PAGES`,
  `PAGE_BY_SLUG`, `IMAGES`, `pageImage`. Re-exports the meta names from
  `./lib-meta` so server importers keep working. Header comment forbids
  client imports.
- **Import updates (7 files, 1–2 lines each):**
  - `app/components/Header.jsx:4` — `../lib` -> `../lib-meta`
  - `app/components/ContactForm.jsx:3` — `../lib` -> `../lib-meta`
  - `app/components/Footer.jsx:1` — `../lib` -> `../lib-meta`
  - `app/components/Shared.jsx:2-3` — meta from `../lib-meta`, data
    (`PAGE_BY_SLUG`, `pageImage`) from `../lib`
  - `app/layout.js:5`, `app/not-found.js:2` — `./lib` -> `./lib-meta`
  - `app/[[...slug]]/page.js:3-12` — data from `../lib`, meta from
    `../lib-meta` (server component; split for an explicit boundary)
- After the split, the ONLY `lib.js` importers are server components
  (`page.js`, `Shared.jsx`). No client component imports it (grep-verified).

**Before / after (same methodology):**

| Metric | Before | After | Change |
|---|---|---|---|
| Chunk 986 (pages.json) | 710,479 B | file GONE | −710,479 B |
| Client JS in any chunk containing pages.json text (`IICRC S500`, `Water Damage Restoration Tulsa`) | present | 0 hits | gone |
| Homepage JS transfer | 1,040,550 B | 333,659 B | −68% |
| Homepage total, mobile 390px | 1,305,126 B (1,274 KB) | 598,008 B (584 KB) | −54%, **under the 800 KB budget** |
| Homepage total, desktop 1280px | 2,141,131 B | 1,433,553 B | −33% (rest is images: 799,714 B of lazy card images that load near-viewport; JS is only 334 KB) |
| Homepage LCP mobile / desktop | 316 ms / 400 ms | 332 ms / 320 ms | same (best-ever) |
| CLS / overflow / console errors | 0 / 0 / 0 | 0 / 0 / 0 | same |

**Rendered output byte-identical in substance (before HTML vs after HTML,
chunk hashes normalized):** home, one service page, one area page — visible
text, canonical, og:url, H1, all hrefs, JSON-LD, FAQ questions, imgs, alts:
ALL IDENTICAL. Services hub: all 27 doc `<strong>` service names present,
0 empty `<h3>`. Screenshots before/after (home mobile+desktop, service,
area): 0 differing pixels >10 on home/service; 20 px on area (rasterization
noise). Homepage screenshot viewed by pixels after the refactor — header,
hero, CTAs, trust band intact.

## U2 — IndexNow key file — DONE (file live locally), submission QUEUED

- Key generated: `b52262ce2b2f10b691644dccabf66495` (openssl rand -hex 16).
- File: `public/b52262ce2b2f10b691644dccabf66495.txt` (32 bytes, contents = key).
  Serves 200 locally (`http://localhost:8317/<key>.txt` returns the key).
- **NOT submitted:** the www domain currently serves a DIFFERENT site on
  Vercel (his check, hands-off), so key validation on www would fail.
  Submission is QUEUED for after the Vercel project fix. Never submit the
  github.io preview URLs (not canonical).

## U3 — llms.txt — DONE

- File: `public/llms.txt` (71 lines), serves 200 locally.
- Contents built ONLY from the site/doc (H1s verbatim from
  `content/pages.json`, canonical www URLs): brand + phone + address,
  18 services, 19 areas, 10 guides, 6 key pages. No invented claims,
  no AI word issues.

## U4 — Next.js 14.2.5 → 14.2.35 — DONE, verified

- `package.json`: `"next": "14.2.5"` -> `"14.2.35"` (exact); `package-lock.json`
  updated (3 packages changed, react/react-dom stay 18.3.1).
- Rebuilt with `npm run export` (exit 0, 23 flat files made). Closes
  CVE-2025-29927 + the EOL line. All gates re-verified below on the 14.2.35
  build (chunk 986 still gone, pages.json still absent from client JS,
  verify_site PROBLEMS 0).

## U6 — out/index.txt (71 KB) — INVESTIGATED: LEAVE IT (do not remove)

- It is an **RSC flight payload**, not junk: one `.txt` per route exists
  (`out/*/index.txt`, 53 files); `out/_next/static/chunks/23-…js`
  references `index.txt`; and a live Playwright desktop run FETCHED
  `index.txt?_rsc=…` (34 KB transfer) during normal page load/navigation.
  The App Router client runtime fetches these on client-side navigation
  (Link clicks). Deleting them would break client navigation with failed
  requests. They are only fetched on navigation, never on initial load, so
  they do not affect homepage transfer. **No change made.**

## U7 — /resources/ hub hero — DONE, verified

- New hero: `public/images/resources-hub-tulsa-water-damage-repair.webp`
  (1200×800, 98,750 B, ≤150 KB). Scene: technician measuring moisture on a
  water-stained wall with air movers + drying equipment in a living room.
  Viewed by pixels: topical, no readable text, no fake addresses/dates,
  blank meter screen. 0 EXIF/XMP/AI-generator strings (raw-byte check;
  PIL info keys are only WebP container defaults `loop`/`background`).
  No AI word in filename/alt.
- Wired via `content/images.json`: `/resources/` entry added
  (hero + `body: null`, matching sibling guides); entries 52 -> 53.
  Alt: "Technician measuring moisture on a water-stained wall while air
  movers and drying equipment dry a water-damaged living room".
- Renders in-page: hero `<img>` in `out/resources/index.html` with correct
  alt; screenshots viewed desktop (1280px) + mobile (360px) — H1 legible,
  sticky call bar visible, overflow 0.
- Generation sidecar JSON (`media-generation-…1794121995.json`, contained a
  remote CDN URL) was DELETED from `public/images/` and the build re-run so
  `out/` has 0 sidecars.

## Gates re-verified on the final build (all fresh)

- `tools/verify_site.py`: 53 pages, 2,395 internal fetches, all 200,
  PROBLEMS 0 (FINDINGS-round1.md restored from git after the run).
- Nested anchors: **0 sitewide**. In-scope repeat (page, target) pairs: **0**.
  Anchors >5 words in scope: **0**.
- H1 exactly 1 on 53/53. Canonical self-matching 53/53, og:url == canonical
  53/53, all canonicals in sitemap (53 locs).
- FAQ schema **222/222 verbatim vs doc** (entity-decoded comparison; an
  earlier raw count of 100 "mismatches" was the `&#x27;` vs `'` artifact).
- Mobile overflow 0 at 360px and 390px (home + resources hub). Console
  errors 0. LCP mobile 316 ms, CLS 0.

## Still open (not touched — his call)

- **U5:** titles 52/53 >60ch + descriptions 23/53 >160ch — verbatim doc, his
  wording call. Never rewrote his doc's titles/descriptions.
- **U8:** 7 dead doc phrases pointing at non-existent pages (left plain).
  New pages = new content work.
- **U2 submission:** queued until the www/Vercel project fix (see above).

## Files awaiting push (git status, uncommitted)

- Modified: `app/lib.js`, `app/[[...slug]]/page.js`,
  `app/components/{Header,ContactForm,Footer,Shared}.jsx`, `app/layout.js`,
  `app/not-found.js`, `content/images.json`, `package.json`,
  `package-lock.json`.
- New: `app/lib-meta.js`, `public/b52262ce2b2f10b691644dccabf66495.txt`,
  `public/llms.txt`,
  `public/images/resources-hub-tulsa-water-damage-repair.webp`.
- No page added/removed/redirected; no visible words, links, or anchors
  changed (rendered output proven identical in substance).
