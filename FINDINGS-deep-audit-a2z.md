# Deep A-to-Z Audit — Tulsa Water Damage Repair (tulsawaterdamagerepair.com)
**Date:** 2026-11-08 · **Scope:** local only — no push, deploy, domain/DNS, token, or live-service contact
**Build audited:** `site/out/` from `npm run export` (Next.js 14.2.5 static export, 53 routes)
**Source of truth:** Google Doc 1iMayAVFlZk5WYxULJ_h-On6BvTQBhubLjLim7Q4NOB4 (parsed `content/pages.json`)
**Audit method:** static HTML audit (`/tmp/audit_final.py`), `tools/verify_site.py` (live crawl of local server :8317), Playwright headless Chromium (1280/390/360px, console/CLS/LCP/transfer/tap-targets), hero screenshots 53/53 viewed by pixels, favicon renders viewed by pixels.

## FINALIZE VERDICT — PUSH GATE: **PASS** (zero blunders after fixes) + UPGRADE list below

- **2 genuine blunders found and FIXED locally, re-verified:** (B1) 120 nested anchors in cards; (B2) 2 guide pages with zero images.
- **0 blunders remain.** Every count below is from fresh re-runs on the final build.
- ⚠️ **BUILD COMMAND GATE (critical, process):** the correct build is **`npm run export`** (`next build && node tools/post_export.js`). `npm run build` ALONE silently drops the 23 flat `<path>.html` files that make the 23 no-slash canonical routes serve 200 directly with no redirect hop. The final build in `out/` was produced with `npm run export` (23/23 flat files verified). The parent must build/publish with `npm run export` — never `npm run build` alone.
- **Local changes awaiting push (parent holds the token; push only on this verdict):**
  - `app/components/Shared.jsx` (B1 fix), `content/images.json` (B2 fix), 2 new hero images (untracked), `public/favicon-*` + `favicon.ico` + `tools/make_favicon.py` (NEW classic favicon, from the parent's earlier round — uncommitted, verified here).
  - `site/FINDINGS-round1.md` was restored from git after each `verify_site.py` run (the tool overwrites it).
- **Token note:** per his standing rule (2026-11-08), the current token (expires ~2026-11-10/11) is reused for every push inside its window — no fresh token needed for this push, no rotate reminder owed.

## BLUNDERS FOUND + FIXED

### B1 — Nested anchors in cards (invalid HTML, 120 instances, 19 pages) — FIXED, re-verified
- **Evidence (before):** `ServiceListCards` in `app/components/Shared.jsx` rendered `<h3><Link href={it.href} dangerouslySetInnerHTML={{__html: it.titleHtml}} /></h3>` where `titleHtml` (from `parseServiceItem`) already contained its own `<a>` (hub `<strong>` items and `SERVICE_TITLES`). Raw HTML was `<a href="/services/x/"><a href="/services/x">Title</a></a>` — invalid nesting; browsers/Googlebot split it into an empty link + a text link (2 links to 1 target on the same card — violating his "2 links 1 page ko nahi dene" rule). Earlier regex audits missed it because non-greedy `<a>...</a>` matching merged outer+inner into one match.
- **Fix (exact-spot, `parseServiceItem` only):** strip `<a>` tags from `titleHtml` in both branches (hub-strong branch + homepage `SERVICE_TITLES` branch); title words unchanged, entities intact. Only `app/components/Shared.jsx` changed.
- **Re-verify:** nested anchors **0 sitewide**; cards render single clean `<h3><a href=".../">Title</a></h3>`; side effect fixed — homepage cards no longer render a redundant title-only `<p>`. verify_site 2,395/2,395 × 200, PROBLEMS 0; static audit 0 in-scope repeats.

### B2 — 2 guide pages had ZERO images (imageless heroes + no body images) — FIXED, re-verified
- **Evidence (before):** `/resources/how-long-does-water-damage-take-to-dry` (37 blocks) and `/resources/water-damage-categories-and-classes-explained` (35 blocks) had `hero: null, body: null` in `content/images.json` — the only 2 pages of 53 with no hero; all other guides have topical hero photos. Hero screenshots showed plain-navy heroes with no image. (`/resources/` hub also has no hero image, but it has 8 body/card images — design choice, not a blunder.)
- **Fix:** generated 2 topical 1200×800 WebP heroes (same generated-scene practice as the rest of the site), viewed by pixels, resized/optimized, 0 EXIF/XMP/AI metadata, no AI word in filename/alt:
  - `resources-how-long-does-water-damage-take-to-dry-tulsa-water-damage-repair.webp` — 91 KB — technician with moisture meter (28.4% WET) + air movers + dehumidifier drying a room. Alt: "Technician measuring wall moisture with a meter while air movers and a dehumidifier dry a water-damaged room".
  - `resources-water-damage-categories-and-classes-explained-tulsa-water-damage-repair.webp` — 78 KB — technician inspecting a water-stained wall with a moisture meter + blank clipboard, drying equipment behind. Alt: "Technician inspecting a water-stained wall with a moisture meter and blank clipboard during a damage assessment".
  - **Rejected + deleted:** first categories draft showed a clipboard with a fake street address + date ("1428 Oakridge Ln, 11/07/2024") — invented place, not allowed on this site; regenerated with a blank clipboard and no readable text anywhere; the rejected file + all 3 generation sidecar JSONs were deleted (0 sidecars in the build).
  - `content/images.json` entries added (hero + `body: null`, matching sibling guides). No content, links, or copy changed.
- **Re-verify:** hero-null pages **0**; heroes render in-page (screenshots viewed — clean gradient, legible H1, topical scene); images 230 instances / 70 unique files, max 149 KB, 0 >150 KB, 0 missing alt, 0 AI hits; verify_site PROBLEMS 0.

## 1. CRAWL — BEST-EVER
- `verify_site.py` (local :8317): **53 pages, 2,395 internal link fetches, all 200, PROBLEMS 0.** Reachable from home **54/53** (home counts twice — root + one self-consistent entry).
- Static file-existence check: **0 broken internal links.**
- **Body copy (.content-block incl. nested .faq-list): 0 self-links; 0 in-scope repeat (page, target) pairs** — the 45-pair dedupe HOLDS. The 19 remaining repeat pairs are ALL on the 3 EXCLUDED pages (homepage 14, about-us 3, contact 2) — deliberate, out of scope.
- **Anchors >5 words: 0 on the 50 in-scope pages.** The 6 known long anchors remain only on the excluded pages (deliberate).
- **Linked "See" anchors: 0.** Plain "See" words in body copy: **281** = 281 rows in `SEE-LINKS-UNLINKED-277.txt` — all still unlinked, never restored.
- Sitemap ↔ canonical ↔ real file: 0 mismatches (see §3).
- **Judgment: genuinely best-ever.** No orphan, no dead link, no self-link, no repeat, no long anchor in scope.

## 2. PER-PAGE SEO — BEST-EVER (with 1 verbatim-doc caveat, his call)
- H1 exactly 1 on **53/53**, unique, matches doc **53/53**.
- Titles unique; **52/53 >60 chars**, match doc **53/53**. Descriptions unique; **23/53 >160 chars**, match doc **53/53**. (Verbatim doc — length is his wording call, see U5. NOT a blunder.)
- Canonical self-matching **53/53**, in sitemap **53/53**, og:url == canonical **53/53**.
- LocalBusiness **53/53**, BreadcrumbList **53/53**, FAQPage **51/51** (51 pages have FAQs). Page-node (WebPage/Service) URL == canonical **53/53** (WebSite/LocalBusiness URL correctly = homepage; inner pages use a `Service` node with the page URL). BreadcrumbList items correct (Home → Services → page; Home → area page).
- **FAQ schema verbatim vs doc: 222/222 exact** (questions + answers, entity-decoded). Rendered FAQ answers: 0 mismatches. (An earlier "67 mismatches" was a comparison artifact — `&#x27;` in doc `a_html` vs `'` in schema.)
- Phone in raw HTML **53/53**, address **53/53**, 0 pages with `http://` URLs, theme-color #073B66 **53/53**.
- **Judgment: genuinely best-ever** on structure/schema/verbatim; title/description length is correct-per-doc, not best-per-SEO (U5).

## 3. SITEMAP / ROBOTS — BEST-EVER (minus 2 missing extras, see U2/U3)
- sitemap.xml: **53 loc + 53 lastmod, all www, unique, slugs match pages.json exactly, 0 missing files.**
- robots.txt correct (Allow /, Sitemap www, Host www).
- **IndexNow key file: NOT present anywhere. llms.txt: does NOT exist.** Neither was ever ordered — UPGRADE list, not blunders (U2/U3).
- **Judgment: best-ever** for sitemap/robots; the two missing extras are the only gap.

## 4. CRAWLABILITY + IMAGES — BEST-EVER (after B2 fix)
- Content present in raw HTML without JS (full SSR/static HTML; no JS-only rendering).
- Render-blocking: **0** — 1 stylesheet, 8 head scripts (7 async, polyfills `noModule`), 3 preloads (font woff2 + hero image + webpack low-priority), 0 preconnect, CSS `font-display: swap`, 7 `@font-face`.
- Images: **230 instances, 0 missing files, 0 empty alt, 0 AI-word hits** (filename/alt/metadata), **0 EXIF/XMP/AI-generator strings** (raw-byte check on new + existing heroes; PIL WebP `loop`/`background` keys are container defaults, not metadata).
- Weights: **70 unique files, total 7,238 KB, max 149 KB, 0 >150 KB.**
- Heroes: **53/53 present and topical by viewed pixels** (all 53 hero screenshots viewed; services: burst pipe, slab worker, sagging ceiling, fire interior, drying mats, sewage, roof workers, storm tree, water heater, drying fans; areas: house exteriors; guides: frozen pipes, mold wall, flood sign, cost calculator, insurance docs, + the 2 new drying/inspection heroes).
- Most-reused images are service heroes reused in related cards (emergency 19×, water-mitigation 19×, mold 19×) — structural, not a blunder.
- `out/index.txt` (71 KB) is a git-ignored Next.js RSC flight-payload artifact, unreferenced — tidiness note only (U6).
- **Judgment: genuinely best-ever.**

## 5. PERFORMANCE — GOOD, NOT BEST (1 real gap: JS bundle)
- LCP (real, PerformanceObserver `buffered:true`, pre-load registration): **mobile home 668 ms** (LCP element `P.hero-intro`), **desktop home 700 ms** (IMG hero) — both well under the 1.8 s target. **CLS 0** on all 8 key pages (home, slab-leak, water-mitigation, broken-arrow, categories guide, about-us, contact, services hub) at 1280/390/360px.
- Transfer (real, Performance resource entries): homepage **desktop ~1,244 KB, mobile ~1,145 KB — OVER the <800 KB homepage budget.** Breakdown: **JS ~1,012 KB/page (81%)**; biggest single chunk **`986-bea92d2fadcba411.js` = 694 KB**, plus fd9d1056 169 KB, 23-… 121 KB. Content sniff proves the 986 chunk embeds the full `content/pages.json` (796 KB) — **every page ships ALL 53 pages' content as JS.** Hero image preload 123–135 KB (good for LCP). Doc HTML 75–133 KB.
- "Broken images" counts were artifacts: homepage 19 / mobile 27 `!complete` images were lazy images not yet loaded (0 failed requests; all files exist). Direct test: midtown area image scrolled into view → complete=true, naturalWidth=1200. Images are fine.
- **Judgment: LCP + CLS are best-ever; total weight is good-not-best — the JS bundle is the #1 upgrade (U1).**

## 6. MOBILE — BEST-EVER
- Horizontal overflow **0 px** at 1280 / 390 / 360 px on all 8 key pages.
- Tap targets: **0 <44 px** when menu open (brand 197×54, phone icon 51×48, Call Now 272×50, Request 294×50, open-menu links 340×44). (An earlier "42 <44 px" measured hidden closed-menu dropdown links inside closed `<details>` — not real targets.)
- Sticky mobile call bar visible on mobile (`.mobile-call-bar`); header CTA visible at all sizes; mobile menu-open screenshot viewed: full-width legible nav; mobile homepage top screenshot viewed: clean header, hero, H1, intro, Call Now button, sticky call bar.
- **Judgment: genuinely best-ever.**

## 7. NEXT.JS STACK — CORRECT, NOT BEST (1 advisory to patch)
- Static export correct: all routes prerendered, `_next` refs **11, 0 missing files, 0 dead chunks referenced.**
- Console errors **0**, failed requests **0**, mixed content **0** on all 8 key pages.
- **Next.js 14.2.5 advisory (assessed, NOT fixed — needs a verified rebuild):** CVE-2025-29927 (CVSS 9.1, Critical — middleware authorization bypass via `x-middleware-subrequest` header; affects 14.0.0–14.2.24, fixed in 14.2.25; Next.js 14 EOL 2026-10-26, final patch 14.2.35 — confirmed via web search 2026-11-08). **Practical risk ZERO for this site:** static export, NO middleware file, no Server Actions/API routes, no server runtime; Vercel strips the header at the edge; sources state static exports are not affected. `npm audit` blocked by registry policy (403 policy_denied). **Recommendation (U4):** patch to 14.2.35 (same minor line, patch-only) + verified rebuild.
- **Judgment: correct, not best** — the stack is sound, the patch is the best-ever move.

## 8. FAVICON (NEW classic set) — BEST-EVER
- Files in `out/`: 16/32/48/192/512/maskable/apple-touch-icon 180/master 512, all correct sizes, **0 metadata chunks**; favicon.ico **3 entries 16/32/48, 32bpp**; `site.webmanifest` parses (3 icons, theme_color #073b66); theme-color #073B66 on **53/53** pages.
- **16/32/48 renders viewed by pixels:** clean flat cyan drop on cream tile with white dot; 16px legible as a drop. Design matches spec (flat cream #F7F3EA tile + hairline navy edge, single flat cyan #00BFFF drop from header SVG path, solid white dot, no gradient/glow/sheen, no text/letters).
- Tab-bar live check still pending a real deploy (browsers cache favicons).
- **Judgment: genuinely best-ever.**

## 9. KNOWN OPEN ITEMS — STATUS CONFIRMED (do not "fix" without his word)
- Titles 52/53 >60ch + descriptions 23/53 >160ch — verbatim doc, his wording call pending (U5).
- 7 doc phrases point at non-existent pages — left plain deliberately; **0 links to those 9 routes in built HTML** (the 2 mentions of `can-water-damaged-hardwood-be-saved` are just an H2 id).
- Contact form NOT wired (no delivery email in doc; `<form>` with no action/onsubmit/fetch — UI only, never fakes a send).
- Next.js 14.2.5 advisory — assessed above (U4).
- **www domain serves a DIFFERENT site on Vercel** (found 2026-11-07 ~22:40 PKT: 200 on Vercel but sitemap only 18 URLs vs ours 53, different title/design, brand "Tulsa Water Damage Repair" 0 times). His check, hands-off — just noted. Do NOT hand him www links as "our site" until fixed. GitHub Pages preview is the review surface for OUR site.
- Trailing-slash / canonical: **NOT a defect** — `trailingSlash: true` + `post_export.js` flat files make BOTH `/path` and `/path/` serve 200 directly on Vercel/GitHub Pages (the python http.server 301 for no-slash URLs is a test-server artifact). Do NOT change canonical forms unilaterally — URL-form identity is his call.

## UPGRADE LIST (good but not best — NO silent changes; parent decides)
- **U1 — JS bundle bloat (biggest gap):** chunk `986-bea92d2fadcba411.js` = 694 KB embeds the full `content/pages.json` (796 KB) into shared page JS; every page ships all 53 pages' content. Homepage transfer mobile 1,145 KB / desktop 1,244 KB vs <800 KB budget. **Fix:** split page data per-route (per-page JSON / dynamic import) so each page ships only its own content. Expected: homepage well under 800 KB, LCP even faster. Needs a refactor + full re-verification.
- **U2 — IndexNow key file missing:** no key file anywhere; Bing IndexNow submission impossible until added. **Fix:** generate key, place at root, verify live, then submit URLs (his word).
- **U3 — llms.txt missing:** no `llms.txt` for AI-crawler discoverability. **Fix:** add a short llms.txt (site summary + key URLs).
- **U4 — Next.js 14.2.5 → 14.2.35:** patch-only upgrade (same minor line) closing CVE-2025-29927 + EOL line. **Fix:** bump, `npm run export`, full re-verification (LCP/CLS/links/schema) before any push.
- **U5 — Titles/descriptions length:** 52/53 titles >60ch, 23/53 descriptions >160ch (verbatim doc). **Fix:** his wording call — shorten titles/descriptions (content change, never unilateral).
- **U6 — `out/index.txt` stray artifact:** 71 KB Next.js RSC flight-payload file in `out/`, git-ignored, unreferenced, harmless. **Fix:** confirm what writes it; remove from the export if it is not needed.
- **U7 — `/resources/` hub hero is imageless:** plain navy hero (hub has 8 card images). Optional: add a topical hub hero image for best-ever consistency.
- **U8 — 7 dead doc phrases:** point at non-existent pages (left plain deliberately). If he ever wants those pages built, that is new content work, not an audit fix.

## FINAL COUNTS (final build, fresh re-runs)
| Check | Result |
|---|---|
| Pages | 53/53 × 200 |
| Internal link fetches | 2,395/2,395 × 200, PROBLEMS 0 |
| Reachable from home | 54/53 |
| H1 == 1 | 53/53, doc-match 53/53 |
| Canonical / og:url / sitemap | 53/53 / 53/53 / 53/53 |
| LocalBusiness / BreadcrumbList / FAQPage | 53/53 / 53/53 / 51/51 |
| FAQ schema verbatim | 222/222 |
| Sitemap locs / lastmods | 53 / 53, 0 mismatches |
| Body self-links / in-scope repeats / long anchors | 0 / 0 / 0 |
| Linked "See" / plain "See" (unlinked) | 0 / 281 |
| Images (instances / unique / max / >150KB) | 230 / 70 / 149 KB / 0 |
| Images missing alt / AI hits / EXIF | 0 / 0 / 0 |
| Heroes present + topical (viewed) | 53/53 |
| Nested anchors | 0 (was 120, fixed) |
| LCP mobile / desktop | 668 ms / 700 ms |
| CLS / overflow / console errors / failed reqs | 0 / 0 px / 0 / 0 |
| Homepage transfer mobile / desktop | 1,145 KB / 1,244 KB (over <800 KB budget — U1) |
| Favicon (16/32/48 viewed, ICO, manifest, theme) | PASS |
| Flat .html for 23 no-slash routes | 23/23 |
