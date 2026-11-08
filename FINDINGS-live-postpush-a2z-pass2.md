# FINDINGS — Live A-to-Z Technical SEO Audit, PASS 2 (independent)

**Site:** Tulsa Water Damage Repair — https://www.tulsawaterdamagerepair.com
**Pass:** 2 of 2 (user ordered "2 x proper a to z end end levle testing"). Done fully from scratch — no reliance on any other agent's work or findings file.
**Date/time:** 2026-11-08, ~19:05–19:35 PKT
**Live commit verified:** `ea8c25b` — "Remove all vercel.json redirects — no redirects, URLs already match old site form" (Vercel deployment dpl_9Ydc1uT5KK5xcjfJA6nz73veXByy READY, per brief)
**Auditor method:** live www by direct fetches (fresh, no cache) + local render pass on a fresh `npm run export` from HEAD ea8c25b (build exit 0; post-export verifier: 52 flat .html + homepage index.html, 0 stray index.html).
**Raw data:** `site/qa-postpush-live/pass2-raw.json`, `pass2-part2.json`, `pass2-render.json`, `pass2-render-hubs.json`, `pass2-part3b.json`; scripts `audit_pass2.py`, `audit_pass2_part2.py`, `audit_pass2_render.py`, `audit_pass2_part3b.py`, `audit_pass2_part3c.py`; hero screenshots `pass2-heroes/` (53).

## Verdict

**PASS with 1 real finding.** The URL layer — the user's core complaint — is fully correct on live: every page self-canonical, no trailing slash anywhere except the homepage, no redirects configured anywhere. Every link, image, H1, FAQ, schema block, sitemap/robots/llms entry checks out. The single real finding is a dangling **"See ."** on 2 pages, present verbatim in the source doc — it needs his decision, not a silent fix.

## 1. Live build identity (ea8c25b) — CONFIRMED

- Sitemap: **53 locs, 53 × lastmod 2026-11-08**; loc set == pages.json slugs (homepage with its slash, all others without).
- 2026-11-08-only states present live: water-heater page has **no** "Related services: and", ends at the Documentation paragraph ("...written scope formatted for your adjuster."), **no** "Full cost guide".
- `vercel.json`: **deleted** — git HEAD ea8c25b shows 1 file changed, 150 deletions (the whole file); absent from the local tree; absent from the GitHub repo root listing (API, no `vercel` match); live `https://www.tulsawaterdamagerepair.com/vercel.json` → **404**.
- `next.config.js`: `trailingSlash: false`, **0 lines containing "redirect"** — no redirect config of any kind in the repo.
- Fresh local export from HEAD ea8c25b: exit 0, 52 flat .html + homepage index.html, 0 stray index.html.

## 2. URL layer (the user's core complaint) — ALL PASS

| Check | Result |
|---|---|
| Canonical URLs (no-slash) → 200 direct, no redirect hop | **53/53** |
| Slash forms → 308 to no-slash (platform/Next.js `trailingSlash:false` built-in, NOT a configured redirect) | **52/52** |
| Homepage → 200, keeps trailing slash | **1/1** |
| Self-canonical (final URL == canonical) | **53/53** |
| Canonical ending with `/` (except homepage) | **0** |
| Any page URL ending with `/` (except homepage) | **0** |

No page's URL differs from its canonical anywhere on the site. The "Canonicalised" flag the user saw was stale browser cache from before the deploy flipped — the live server is correct.

## 3. Links — PROBLEMS 0

- Total link instances crawled sitewide: **6,777**.
- Unique internal targets: **54 — all 200, PROBLEMS 0**.
- Unique external targets: **1** — `https://msc.fema.gov/portal/home` (the doc's FEMA flood-map link, 10×). VM curl returns 000 for this host (DNS resolves to 198.18.101.175; other .gov hosts return 200 from the same VM), but an independent browser fetch loads the page fine ("FEMA Flood Map Service Center | Welcome!", crawled 28 min before the check). **Live link — NOT a defect; the curl failure is a VM egress quirk for that host.**
- No dead, looping, or orphan URLs. No crawl waste.

## 4. H1 / titles / descriptions

- H1: exactly **1 per page, 53/53**, all **doc-verbatim** (live H1 == pages.json h1 on every page), **visible on all 53 pages on desktop AND mobile** (local render, bounding-box + computed-style check).
- Titles: **53/53 match source verbatim**; **52/53 > 60 chars — REPORT-ONLY** (doc wording, U5, his call — never rewrite).
- Descriptions: **53/53 match source verbatim**; **23/53 > 160 chars — REPORT-ONLY** (doc wording, U5, his call).
- Commercial page (`/services/commercial-water-damage`): H1 present + visible on desktop and mobile, hero image present — **no blank-hero defect found** (same as the earlier investigation; his hard-refresh re-check still pending).

## 5. Open Graph + JSON-LD

- `og:url` == canonical **53/53**; `og:title` **53/53**; `og:image` **53/53**; `og:type` = website on all pages.
- JSON-LD types present: `WebSite`, `BreadcrumbList`, `HomeAndConstructionBusiness`, `WebPage` on **53/53** pages; `FAQPage` on **51/51** pages that have FAQs (`/about-us` and `/resources` hub have no FAQ section in the doc); `Service` on **18/18** service pages; `Article` on **10/10** resource guides.
- No JSON-LD parse errors on any page.

## 6. Sitemap / robots / llms — intact

- `sitemap.xml`: 53 locs, 53 × 2026-11-08, date-only, 200.
- `robots.txt`: **23 User-agent lines**, `Allow: /`, AI-search bots explicitly allowed, `Sitemap:` directive present, 200.
- `llms.txt`: contains all **53** site URLs, 200.
- `b52262ce2b2f10b691644dccabf66495.txt` (IndexNow key): 200, 32 bytes.

## 7. Images + favicon

- Images: **246 instances, 71 unique internal — all 200, PROBLEMS 0**.
- Heroes: **53 distinct hero srcs, 0 reused**, hero image present on all 53 pages.
- Hero relevance (viewed by pixels, sample of 6/53): homepage (opened water-damaged wall), emergency (response technician at van), mold (PPE fogging), hardwood (wet planks + drying mat), Bixby (suburban home), flood (flooded living room) — **all topic/place-relevant, H1 legible**. Remaining 47 heroes verified distinct-by-src + 200, not individually viewed — stated honestly, not claimed.
- Image weights: largest 148 KB (1200×800 WebP); images dir 7.3 MB total — no bloated assets.
- Favicons: **9/9 live 200** — favicon.ico, 16/32/48/192/512/maskable, apple-touch-icon.png, favicon-master.png — plus `site.webmanifest` 200.

## 8. Speed (local build — see Limitations)

Measured on the identical fresh export served locally (Playwright Chromium 153, desktop 1280×800 + mobile 390×844):

| Metric | Worst | Page |
|---|---|---|
| LCP desktop | **660 ms** | homepage |
| LCP mobile | **448 ms** | homepage |
| CLS desktop | **0** | all 53 pages |
| CLS mobile | **0** | all 53 pages |
| Transfer desktop | **1,849 KB** | homepage |
| Transfer mobile | **650 KB** | homepage |

- Console: **0 same-origin failures sitewide** on the corrected local server. The only failed requests anywhere are the Google Maps embed hitting `ERR_TUNNEL_CONNECTION_FAILED` — the VM's network tunnel block (environmental; live browsers load it fine).

## 9. FAQ — 222/222 verbatim

- Visible **222** = schema **222** = source **222**. Questions and answers all match after correct extraction.
- Extraction notes (so this is not misread later): the visible question carries a decorative `+` toggle glyph inside `<summary>` (not part of the question); the source `a_text` field stores HTML entities (`&#x27;`, `&quot;`) which render correctly as `'`/`"` on the page. Both are rendering artifacts, not content differences. The FAQPage schema lives inside a `@graph` node — a naive top-level parse reports 0 schema FAQs (my first script did; fixed and re-verified).

## 10. Phrases — clean except 1 finding

- `"See and"`: **0** sitewide.
- Dangling bare `"see"`: see Finding F1 below (2 instances) — plus 1 ruled-out legitimate sentence.
- `"Full details:"` family (`Full details`, `Full breakdown`, `Full category`, `Full drying`, `Full cost guide`, `Detailed guide`, `Full checklist`): **0**, except 1 legitimate lowercase occurrence — "for the full drying process" inside a real sentence on the categories guide ("See for Class 4 hardwood drying and for the full drying process.") — **not a defect** (same false alarm as the URL round).
- `?v=`: **0** anywhere.

## 11. Today's guidelines — all checked

- **18px text sitewide except headings:** the ONLY sub-18px text on the site is the 3 already-known exception families — **212× check-glyph spans (12px, decorative ✓ icons), 53× brand tagline small (10.88px), 53× "EMERGENCY?" .btn-small (11.2px)**. Zero other violations on any page, desktop or mobile. The 2 micro-label exceptions remain **his pending call** — not "fixed" by me.
- **Footer mini-map:** **33 pages** have both `div.footer-map` and `div.footer-mini-map` iframes; the **19 area pages + /contact/** have no footer map and instead show a content map (1 iframe in `<main>`, e.g. Bixby, OK) — exactly as specified.
- **Area service cards:** **18/19** area pages show the "What Water Damage Services Do We Offer in [City]?" section as **image cards (5–8 cards each, every card with its own image)**. Brookside has **no offer section** — correct, the doc has none for Brookside; nothing invented.
- **No invented content:** H1/title/description/FAQ all match pages.json verbatim (53/53, 53/53, 53/53, 222/222).

## FINDING F1 — Dangling "See ." on 2 pages (REAL, doc-verbatim — needs his decision)

Two paragraphs end with a dangling **"See ."** — a pointer with nothing after it:

1. **`/services/water-mitigation`** — "...Used instead of air movers for engineered and solid hardwood. **See .**" — source `pages.json` pages[3] `blocks[54]`, verbatim.
2. **`/services/mold-remediation`** — "...while the mold team handles containment and removal. **See .**" — source `pages.json` pages[5] `blocks[43]`, verbatim.

**Why this matters:** it violates his standing rule that no dangling "See"/"see" fragment appears anywhere after a fix. **Why I did not fix it:** the text is verbatim from his doc — the build is faithful to the source. Cutting it would change doc content, which needs his word (cut the "See ." on both pages, or keep as the doc says). This is the ONLY defect found in the whole pass.

**Ruled out (not defects):**
- `/services/burst-pipe-water-damage` — "...larger than what you can see." — a complete, grammatical sentence.
- Categories guide "full drying process" — lowercase, inside a real sentence (see §10).
- FEMA link — live (see §3).
- Local `/services` + `/resources` 404s and the 35-page console 404s seen mid-audit — a **local-server artifact**: `site/tools/serve.py` checks `isdir` before the flat-`.html` fallback, so the two hub pages (which are both a flat file and a directory prefix) 404 locally. Live they are 200. I re-measured both hubs on my own corrected server (`qa-postpush-live/serve_pass2.py`, flat `.html` first): LCP 576/364 ms desktop, 404/260 ms mobile, CLS 0, H1 visible, 0 console errors. No live impact; `serve.py` itself left untouched.

## Open items (his call — not defects)

- **U5:** titles 52/53 > 60 chars, descriptions 23/53 > 160 chars — verbatim doc, report-only.
- **18px micro-label exceptions:** header "EMERGENCY?" button + brand tagline (+ decorative check glyphs) — 18px or keep small, his call.
- **Commercial blank hero:** no defect found (H1 visible desktop + mobile); awaiting his hard-refresh re-check.
- **His side:** contact-form delivery inbox; unpublish GitHub Pages (his account only); Search Console / GBP / Yelp / Bing Places actions; old GitHub token revocation (do NOT nag while in-window).
- **No ranking/leads promise** — ever. Only verified on-page work, as always.

## Limitations (stated plainly)

- **Live Playwright is blocked in this VM by a network tunnel** (`ERR_TUNNEL_CONNECTION_FAILED` for external hosts, including the Google Maps embed). Render metrics (LCP/CLS/H1 visibility/18px/console) were therefore measured on the identical build — a fresh `npm run export` from HEAD ea8c25b — served locally. Live HTML was verified by direct fetches. **No live screenshot is claimed.**
- Hero topic-relevance: 6/53 heroes viewed by pixels (sample above); all 53 verified distinct by src and 200.
- The FEMA external link was confirmed live via an independent browser fetch, not VM curl (see §3).
