# Live A-to-Z Audit — Tulsa Water Damage Repair (www.tulsawaterdamagerepair.com)
**Date:** 2026-11-08 · **Scope:** LIVE www domain (not preview, not local) — technical SEO, internal links vs doc, blunders, images, render, schema
**Build audited:** main 3a068e2 (Tier 1 fixes) — the live Vercel deployment, verified same build as local `site/out/` (fresh `npm run export` during this audit, clean tree)
**Source of truth:** Google Doc 1iMayAVFlZk5WYxULJ_h-On6BvTQBhubLjLim7Q4NOB4 (parsed `content/pages.json`)
**Method:** live fetches of all 53 URLs + full internal-link fetch check (requests), JSON-LD parsed (never plain grep), doc-authority href-set reconciliation vs `pages.json` blocks + FAQ `a_html`, Playwright headless Chromium (render measured on the identical build served locally — see §9 limitation), hero screenshots viewed by pixels, image file audit (size/EXIF/AI/cross-site hashes).

## HEADLINE VERDICT — PASS with ONE real live-only finding (his call, not fixed here)

- **1 real finding (F1, live-only, medium): the 23 no-slash canonical URLs 308-redirect to their slash forms on live Vercel.** The canonical tag on the served page then points back at the no-slash URL — the canonical points at a URL that redirects. Preview/GitHub Pages serves the same URLs 200 direct (flat `.html` files); Vercel's `trailingSlash: true` forces the redirect before file serving. Everything else passes. No blunder in this round required a code fix.
- **Article open question from the parent RESOLVED — Article IS live on 10/10 guides.** Parsed JSON-LD (not grep) finds `"@type":"Article"` once per guide + once escaped in the flight payload. The parent's grep miss was a grep/stale artifact, not a real absence. Independently confirmed via a second fetch path (browser.open of the live guide page: full content, "Published: 2026-11-07" visible).
- **2 count corrections vs prior audits (reporting, not new blunders):** long anchors on the 3 excluded pages are **14, not 6** (the 8 homepage service-list anchors were undercounted before); repeat pairs on excluded pages are **20, not 19** (homepage water-mitigation ×3). Both are on the deliberately excluded pages (/, /about-us/, /contact/) — scope unchanged, no fix in this round.
- **0 orphans, 0 broken links, 0 nested anchors, 0 body self-links, 0 in-scope repeats, 0 in-scope long anchors, 0 linked "See" (281 plain), 0 missing alt, 0 cross-site image repeats.**

## F1 — No-slash canonicals 308 on live Vercel (the one real finding)

- **Evidence:** `curl -I https://www.tulsawaterdamagerepair.com/services/burst-pipe-water-damage` → `HTTP/1.1 308 Permanent Redirect`, `Location: /services/burst-pipe-water-damage/`. All 23 no-slash canonical URLs behave the same (audit script: final URL = slash form on 23/23). The slash form returns 200 directly. The 30 slash-canonical URLs serve 200 directly. So all 53 canonical URLs resolve to 200 content — 23 of them via exactly one 308 hop.
- **Why it matters:** the served page's `<link rel="canonical">` is the no-slash URL (verified 53/53 self-matching), so Google fetches the sitemap/canonical URL, gets 308'd to the slash form, and reads a canonical pointing back at the redirecting URL. Google will normally follow the redirect and treat the slash form as canonical — i.e. the indexed form may become the slash form, splitting the signal the no-slash canonicals were meant to consolidate. Google's own guidance is that a canonical URL should return 200.
- **Why it happens:** `trailingSlash: true` in `next.config.js` makes Vercel redirect `/path` → `/path/` before serving files. The 23 flat `<path>.html` files from `post_export.js` are what make the same URLs serve 200 direct on GitHub Pages (verified in the Tier 1 round) — on Vercel they are bypassed by the redirect. The prior audit's claim that "BOTH forms serve 200 directly on Vercel" was wrong; it was true only for the Pages preview.
- **Fix options (his call — URL forms are his decision, NOT changed here):** (a) keep as-is and accept Google indexing the slash forms for those 23 pages; (b) change those 23 canonicals (+ sitemap locs + internal links) to the slash forms — a URL-form change across the site; (c) engineering change to `trailingSlash`/routing so both forms serve 200 on Vercel — needs care, the mirror problem (slash-canonical pages redirecting) must not be created. **No action taken in this audit.**
- **Not a finding:** the apex `tulsawaterdamagerepair.com` → 308 → www is correct and intended. The audit script's first "apex redirect wrong" line was a script artifact (it compared the post-redirect status); curl confirms `308 → https://www.tulsawaterdamagerepair.com/`.

## Count corrections (reporting only)

- **Long anchors on excluded pages: 14, not 6.** Verified in live DOM inside `.content-block`: homepage 11 (8 service-list anchors of 8–14 words — "Emergency water damage restoration burst pipes, overflows, appliance failures, any hour of any day" 14w, "Water mitigation and structural drying extraction, moisture mapping, IICRC S500-monitored drying" 11w, flood 12w, basement 9w, sewage 12w, mold 9w, storm 8w, commercial 8w — plus "Full details on how we handle this:" 7w, "Full guide to categories and classes:" 6w, "Full breakdown with cost ranges by category and material:" 9w), about-us 2 ("The 2019 flood hit Sand Springs" 6w, "Tulsa County and surrounding communities: Broken Arrow" 7w), contact 1 ("If you're in Tulsa County or one of the nearby communities on our" 13w). The deep audit's "6" counted only the 3 homepage "Full…" anchors + about 2 + contact 1 and missed the 8 service-list anchors. In-scope pages: **0 long anchors** (unchanged).
- **Repeat (page, target) pairs on excluded pages: 20, not 19.** Homepage 15 (water-mitigation ×3, burst-pipe ×2, categories-guide ×2, 12 area links ×2), about-us 3 (sand-springs, jenks, bixby ×2), contact 2 (insurance-claim guide ×2, home ×2). In-scope pages: **0 repeats** (the 45-pair dedupe holds).
- **7 homepage area hrefs are not in the doc** (brookside, cherry-street, east, midtown, north, south, west Tulsa — template area cards on the homepage). Verified against the doc JSON itself (homepage tab: 0 hyperlinks to those paths, 0 parenthetical mentions). Same status as the 5 known homepage extras from the doc audit — excluded page, deliberate scope, no fix here.

## 1. TECHNICAL SEO — live

| Check | Result |
|---|---|
| Live URLs 200 | 53/53 (23 via one 308 hop — see F1; 30 direct) |
| Variant forms 200 | 53/53 (slash form of no-slash routes serves 200 direct) |
| H1 exactly 1, doc-verbatim | 53/53 |
| Canonical self-match / og:url self-match | 53/53 / 53/53 |
| Sitemap locs / lastmods | 53 / 53 (all lastmod 2026-11-07), loc set == canonical set |
| Titles >60ch / descriptions >160ch | 52/53 / 23/53 — verbatim doc (U5, his wording call; NOT rewritten) |
| Title/description verbatim vs doc | 53/53 / 53/53 |
| LocalBusiness subtype HomeAndConstructionBusiness | 53/53, single @id `…/#business`, all fields present |
| BreadcrumbList / WebSite | 53/53 / 53/53 |
| FAQPage / FAQ schema verbatim | 51/51 pages, **222/222** Q+A exact |
| Article on guides | **10/10** (headline=H1 verbatim, author/publisher=business @id, dates 2026-11-07) — see resolution above |
| Service nodes | 18/18 service pages |
| WebPage nodes | 35/53 — the 18 service pages carry a Service node instead of WebPage (by design; Phase 2 adds WebPage alongside) |
| robots.txt | 200, **20 User-agent lines** (1 `*` + 19 explicit), Sitemap + Host present, deprecated anthropic-ai/Claude-Web absent |
| llms.txt / IndexNow key | 200 / 200 (key content exact) |
| Phone / address in visible text | 53/53 / 53/53 |
| noindex | only privacy/terms as intended (no unexpected noindex) |
| Mixed content / http:// URLs / leak URLs (github.io, vercel.app, localhost) | 0 / 0 / 0 |
| Forbidden/leftover strings in visible HTML | 0 |

## 2. INTERNAL LINKS (doc authority, live HTML)

- **Full internal-link fetch check: 75 unique internal hrefs, all 200; 2,448 per-page link slots, 0 broken, PROBLEMS 0.** (Prior local counts 2,395/2,499 differ by counting method — per-page unique-href slots incl. header/footer/nav; the verdict is identical: nothing broken.)
- **Doc-authority href reconciliation (live body links vs `pages.json` blocks + FAQ `a_html`): 0 expected internal hrefs missing on any page; 1 page with extras (homepage, the 7 area hrefs above).** External hrefs live: only the FEMA flood-map URL (10 instances of the same URL — the doc's only external hyperlink).
- Body self-links **0**; in-scope repeat pairs **0**; in-scope long anchors **0**; linked "See" **0**; plain "See" words **281** (= the 278-row SEE file + 3 more occurrences outside body copy — all unlinked, never restored).
- **Orphans: 0.** Corrected BFS from live home reaches 54/53 (home counts twice). Note: the first BFS run flagged `/resources/water-damage-vs-flood-damage-insurance-oklahoma` as orphan — that was a script bug (BFS normalized slugs but looked them up by raw slug, so the `/resources/` hub was never expanded). The hub DOES link it (`/resources/water-damage-vs-flood-damage-insurance-oklahoma/`). Re-run with the fix: 0 orphans.
- Header/footer links: 0 broken (all resolve inside the 75 unique hrefs, all 200). Header dropdowns scrollable (Services nav-drop scrollHeight 1173 > clientHeight 446).
- **Body-link source check (49 pages):** an early comparison of live body links vs `pages.json` blocks alone showed 49 pages "mismatched" — resolved as an extraction gap, not drift: (a) FAQ `a_html` links were not in the expected set ("Full details:" → guide, "Commercial fire losses" → /commercial/, FEMA link); (b) area offer lists render as image cards whose title link combines the item's `<strong>` text ("Water mitigation" + " and structural drying" = 5-word card title — still ≤5 words, href matches the doc); (c) template Call Now tel: buttons inside `.content-block`. After adding FAQ links and comparing href SETS: 0 missing, 0 unexplained extras (see above).

## 3. BLUNDERS + RENDER + IMAGES

- **Nested anchors: 0 sitewide** (was 120, fixed in the deep audit — holds).
- **Every page has ≥1 image:** 231 image instances / 71 unique files (was 230/70 — the +1 is the U7 resources-hub hero). The 2 previously imageless guides now have heroes (verified in screenshots: moisture-meter technician, 28.4% WET reading).
- **Images:** max 149 KB, 0 >150 KB, total 7,335 KB, all 1200×800, 0 missing alt, 0 AI strings in filename/alt/metadata. Proper metadata check (real EXIF/XMP/Photoshop chunks, not raw-byte substrings): **0 files** — an early naive `b'XMP'` substring hit on 3 files was compressed-data coincidence (random bytes around the match), confirmed false by chunk-signature check.
- **Cross-site repeats vs the 9,899-entry pool:** exact md5 **0**, perceptual near-duplicates (ahash ≤8 AND dhash ≤8) **0**.
- **Heroes viewed by pixels (9 top screenshots this round + prior 53/53):** home (room mid-restoration, exposed studs — topical), burst-pipe (burst water gushing — topical), broken-arrow mobile (suburban house exterior — the established area-page pattern, place-relevant), dry-guide (moisture-meter technician — topical), resources hub (U7 hero, moisture-meter + drying equipment — topical), services hub (restoration crew — topical). No dry-house-exterior hero on any service/guide page.
- **Cards/sections:** services hub 18 unique cards, homepage 37 cards (per prior audit, unchanged); no duplicate sections found in the 9 rendered pages.
- **Render (Playwright, identical build — see §9):** LCP desktop 264–360 ms, mobile 224–324 ms (all ≪1.8 s); **CLS 0** on all 9 pages × 2 viewports; overflow **0 px** at 1280/390/360; console errors **0**; failed requests **0** except the Google Maps embed iframe in sandboxed Chromium (see §9 — the embed URL itself returns 301 via curl, i.e. live; the iframe is `loading="lazy"`).
- **Contact form: honest.** No `action`/`method`/`onsubmit` in HTML; the React handler only sets state to show: "This form is not connected to an inbox yet. Your message was not sent anywhere. For the fastest help, call (918) 395-9320 — answered 24/7." Submit test confirmed: no navigation, no fake success message, no console errors.
- **Sticky mobile call bar:** visible on mobile (`.mobile-call-bar`, bottom bar "Call Now · (918) 395-9320"); header phone CTA visible at all sizes.

## 4. LIVE-ONLY CHECKS (www vs preview)

- www sitemap vs preview sitemap: **paths identical** (53/53, same order) — same build deployed both places.
- Live www vs local `out/`: same content (spot-checked home + guide via browser.open: full text, tables, FAQs, NAP, hours, "Published: 2026-11-07").
- Vercel headers sane: `Server: Vercel`, `Strict-Transport-Security: max-age=63072000`, `Cache-Control: public, max-age=0, must-revalidate`, `X-Vercel-Id` present.
- **One live-vs-preview difference: F1** — the 308 on no-slash canonicals happens on Vercel only (preview serves direct 200). No other difference found.
- Apex 308 → www: correct, intended.

## 5. OPEN ITEMS — unchanged (his call, not touched)

U5 titles/descriptions lengths (verbatim doc); U8 7 dead doc phrases (left plain); U2 IndexNow submission (only after www serves OUR site — now true, but submission itself is still his word); Search Console "Search generative AI" Include; GBP completion + genuine review flow; Yelp + Bing Places + Apple Business Connect; WAF/Cloudflare check; contact-form delivery inbox (FormSubmit pattern suggested earlier, no word yet).

## 9. METHOD NOTES + LIMITATIONS (read before quoting this audit)

- **Live Playwright was blocked by the VM network tunnel** (`ERR_TUNNEL_CONNECTION_FAILED` — sandboxed Chromium cannot reach the live domain, same as the Tier 1 round; even with the egress proxy). Render metrics/screenshots were therefore measured on the **identical build** (fresh `npm run export` from main 3a068e2, clean tree) served on local :8317. Live HTML was verified separately by direct fetches (all 53 pages + 2,448 link slots + browser.open of the live guide page). No render number in this report is claimed from a live screenshot.
- The Google Maps iframe "failed request" in the render probe is the same sandbox-network artifact (the iframe URL returns 301 via curl); on a real browser it loads. The empty gap on the contact screenshot is the lazy map iframe not loading in the sandbox.
- `verify_site.py` was NOT re-run (its local-server crawl duplicates the live fetch check done here); `FINDINGS-round1.md` was not touched.
- Mobile image bytes (0 KB on home mobile) and "incomplete" image counts are lazy-loading artifacts (below-fold images not yet in viewport), not broken images — 0 failed image requests.

---

# PHASE 2 — End-level implementation (local only, NO push)
**Ordered by the user after the audit:** "101% end-level technical SEO, end-level everything — llms.txt A-to-Z end level, robots.txt everything, schema also end level, and speed end end level."
**Changed files (3):** `public/llms.txt`, `public/robots.txt`, `app/[[...slug]]/page.js` (schema only — JSON-LD script; no JSX, no visible words, no links changed).
**Verification:** fresh `npm run export` (23 flat .html), schema parsed from all 53 built files, `tools/verify_site.py` on local :8317 (**53 pages, 2,395 fetches × 200, reachable 54/53, PROBLEMS 0, exit 0** — FINDINGS-round1.md restored from git after), speed re-measured (see §2d), screenshots viewed (visually identical — see §2d note on pixel noise).

## 2a. llms.txt A-to-Z — DONE

- **Before:** 71 lines — 53 links (18 services / 19 areas / 10 guides / 6 key pages, H1s verbatim) + a 3-line NAP quote, no descriptions.
- **After:** 73 lines — same 53 links (same H1s, same URLs, 0 bad URLs) + a one-line description after every link + a full NAP block at the top.
- **Descriptions:** the first sentence of each page's `blurb`, verbatim from `content/pages.json` (HTML entities unescaped, nothing reworded, nothing added). A few are terse by design ("Burst pipe at 3 AM.", "Water on the floor right now?", "Active water damage?") — they are the doc's own hooks, kept as-is.
- **NAP block (verbatim):** about-blurb first sentence ("We're a water damage restoration team based at 400 S 129th E Ave in Tulsa, OK 74108."), phone "(918) 395-9320 — answered 24 hours a day, 7 days a week.", address, hours "Open 24 hours, 7 days a week (00:00-23:59 daily)", service-area line pointing at the Service Areas section.
- **Verified:** 53/53 URLs are real canonicals, 0 invented claims/rates/reviews/facts. Serves from `out/llms.txt` (72 lines by `wc -l` — same content; the count differs only by trailing-newline accounting).

## 2b. robots.txt end-level — DONE

- **Before:** 20 User-agent lines (1 `*` + 19 explicit: 10 search + 9 training).
- **After:** 23 User-agent lines (1 `*` + **22 explicit: 12 search + 10 training**). `*` Allow, Sitemap, Host lines untouched.
- **Added (grounded in October–November 2026 crawler references, checked against each operator's docs):**
  - `Applebot` — search (Siri, Spotlight). Was missing; only `Applebot-Extended` (training token) was present.
  - `Meta-WebIndexer` — Meta's search-index bot (builds the index AI answers cite from).
  - `MistralAI-Training` — Mistral training crawler (consistent with the established allow-everything pattern).
- **Removed:** nothing. Deprecated `anthropic-ai` / `Claude-Web` still NOT added.
- **Verified in built `out/robots.txt`:** 23/23 groups present, deprecated tokens absent. Note for the record: the research consensus is that blocking a *training* bot costs no AI-answer visibility, while blocking a *search* bot removes the site from that engine's answers — this file allows all of both, per his established pattern.

## 2c. Schema end-level — DONE

- **Business node (`HomeAndConstructionBusiness`, 53/53 pages), added truthful fields only:**
  - `description` — about-blurb first sentence verbatim ("We're a water damage restoration team based at 400 S 129th E Ave in Tulsa, OK 74108.").
  - `geo` — `GeoCoordinates` **36.15467, -95.83348** (real map lookup of 400 S 129th E Ave, Tulsa, OK 74108 — FULL_ADDRESS match, distance 0; never guessed).
  - `hasMap` — the exact Google Maps URL the site's own footer embed uses (`https://www.google.com/maps?q=400%20S%20129th%20E%20Ave%2C%20Tulsa%2C%20OK%2074108&output=embed`).
  - `areaServed` — **20 entries** (was 1 City): Tulsa + 12 suburb Cities (Broken Arrow, Bixby, Catoosa, Claremore, Collinsville, Coweta, Glenpool, Jenks, Owasso, Sand Springs, Sapulpa, Skiatook) + 7 Tulsa-neighborhood Places (Midtown Tulsa, Brookside Tulsa, South/West/North/East Tulsa, Cherry Street & the Pearl District) — all from the real area-page H1s, no invented place.
  - `knowsAbout` — **18 entries**: the service-page H1s verbatim with only the " in Tulsa, OK" location suffix stripped.
  - **NOT added, deliberately:** `sameAs` (no verified social/directory profile for THIS business — the Nextdoor page in memory belongs to the older Tulsa site, not this one), `priceRange` (no real price exists in the doc — the cost guide's $1,300–$5,000 is a mitigation-phase range, not a business priceRange), `Review`/`AggregateRating` (self-serving — banned by Google), `QAPage`/`HowTo`/`Speakable` (decoration), `SearchAction` (no on-site search).
- **WebPage node: 35/53 → 53/53.** The 18 service pages previously carried only a Service node; they now also carry a WebPage node (`@id` + `url` = canonical, `isPartOf` website) alongside it.
- **Article (10/10 guides):** added `image` (the guide's real hero file URL — same file the page shows), `inLanguage: en-US`, `mainEntityOfPage` (`@id` = guide canonical). Headline/author/publisher/dates unchanged.
- **Verified (parsed JSON-LD from all 53 built files):** business 53/53, geo 53/53, hasMap 53/53, areaServed-20 53/53, knowsAbout-18 53/53, description 53/53, WebPage 53/53, Article image/lang/mainEntityOfPage 10/10 each, plain-LocalBusiness 0 files, forbidden types (Review/AggregateRating/QAPage/HowTo/Speakable) 0. Problems: **0**.

## 2d. Speed end-level — MEASURED, no change justified

- **Before (Phase 1, identical build):** home mobile LCP 312 ms, total 590 KB, JS 332 KB, CLS 0; home desktop LCP 360 ms, total 1,407 KB; inner pages mobile LCP 224–324 ms, totals 561–725 KB.
- **After (this build):** home mobile LCP 348 ms, total 594 KB, JS 332 KB, CLS 0; home desktop LCP 444 ms, total 1,415 KB; burst-pipe mobile LCP 308 ms, total 611 KB; broken-arrow mobile LCP 248 ms, total 730 KB; all pages CLS 0, overflow 0 at 360/390/1280, console 0.
- **Verdict: already end-level — NO speed change made.** Every budgeted metric is met with wide margin (mobile total <800 KB, LCP ≪1.8 s, CLS 0). The LCP deltas between runs (±~100 ms) are local-server measurement noise, not a regression — JS bytes are byte-identical (332 KB) and the only HTML change is ~2 KB of JSON-LD per page. The 332 KB JS is irreducible Next.js 14 + React runtime for this stack (chunks identified: `117` = Next.js client runtime, `fd9d1056` = React DOM, `framework`, `main`; `polyfills` 110 KB is `noModule`-skipped by modern browsers). Images are already ≤150 KB, 1200×800, lazy-loaded below the fold; fonts are `font-display: swap` with woff2 preloads; CSS is 25 KB; 0 render-blocking extras found. Churning images or JS for unbudgeted desktop bytes would risk quality for no measured gain.
- **Screenshots after Phase 2:** viewed — home desktop visually identical to Phase 1 (same hero, H1, chips, CTAs). Pixel-diff vs Phase 1 shows ~10k changed pixels (<1%, hero-photo region only, y 81–402) with no visible difference — decode/anti-aliasing jitter between runs, not a layout or content change (no JSX changed; visible HTML is unchanged by construction — only the JSON-LD script changed).

## Phase 2 — push warranted?

**YES — a push is warranted and ready.** It would contain exactly 3 source files (`public/llms.txt`, `public/robots.txt`, `app/[[...slug]]/page.js`) + this findings file. All gates pass, no visible change, no words changed. **NOT pushed** — push is his word only, and the token in the inherited conversation is NOT authorized for this round. Awaiting his word (+ token if the current one has expired).

- **Live Playwright was blocked by the VM network tunnel** (`ERR_TUNNEL_CONNECTION_FAILED` — sandboxed Chromium cannot reach the live domain, same as the Tier 1 round; even with the egress proxy). Render metrics/screenshots were therefore measured on the **identical build** (fresh `npm run export` from main 3a068e2, clean tree) served on local :8317. Live HTML was verified separately by direct fetches (all 53 pages + 2,448 link slots + browser.open of the live guide page). No render number in this report is claimed from a live screenshot.
- The Google Maps iframe "failed request" in the render probe is the same sandbox-network artifact (the iframe URL returns 301 via curl); on a real browser it loads. The empty gap on the contact screenshot is the lazy map iframe not loading in the sandbox.
- `verify_site.py` was NOT re-run (its local-server crawl duplicates the live fetch check done here); `FINDINGS-round1.md` was not touched.
- Mobile image bytes (0 KB on home mobile) and "incomplete" image counts are lazy-loading artifacts (below-fold images not yet in viewport), not broken images — 0 failed image requests.
