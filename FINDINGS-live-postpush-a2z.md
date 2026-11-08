# Post-Push Live A-to-Z Technical SEO Audit — PASS 1

**Site:** Tulsa Water Damage Repair — https://www.tulsawaterdamagerepair.com (www primary), (918) 395-9320
**Date:** 2026-11-08 (Sun) — **LIVE audit on the current production build**
**Live deployment:** Vercel `dpl_9Ydc1uT5KK5xcjfJA6nz73veXByy` READY, main `ea8c25b` (vercel.json deleted — NO redirects, user order)
**Pass:** 1 of the user's ordered 2× A-to-Z testing (Pass 2 is a separate independent audit, own file)
**Method:** Full live audit against www (ea8c25b) — every page fetched over HTTPS, every unique internal target fetched, every slash form fetched, sitemap/robots/llms/key/favicons fetched and hashed. Render metrics (LCP/CLS/overflow/H1 visibility) measured on the IDENTICAL local build served locally via Playwright/Chromium (live rendering is blocked by the sandbox network tunnel — see §Limitations). Screenshots viewed by pixels. Counts, not claims.

## Headline verdict — PASS, PROBLEMS 0

| Check | Result |
|---|---|
| Canonicals 200 direct (no hop) | **53/53** |
| Slash forms 308 → no-slash canonical | **52/52** (platform trailingSlash:false built-in; NO vercel.json redirects exist) |
| Homepage | 200, keeps trailing slash, canonical `https://www.tulsawaterdamagerepair.com/` |
| H1 | **53/53** — 1× + doc-verbatim (static) AND 53/53 visible + verbatim + 0 overflow (rendered sweep) |
| Internal links | **0 broken** — 53 unique internal targets all 200 (52 page slugs + /sitemap.xml); 108 home refs; 2,291 per-page unique href instances; 6,777 raw `<a>` instances; every instance resolves to a verified-200 target |
| FAQ | **222/222 verbatim** (visible == schema == source) |
| Schema (JSON-LD parsed) | WebSite 53, BreadcrumbList 53, HomeAndConstructionBusiness 53, WebPage 53, FAQPage 51, Service 18, Article 10; 0 trailing-slash URL values |
| Sitemap | 53 locs == canonical set, lastmod **53× 2026-11-08** (date-only) |
| robots.txt / llms.txt | 23 User-agent lines (wildcard + 22 AI groups); llms 53 links, 0 trailing-slash, NAP present |
| Images | 246 img tags / 71 distinct srcs, all 71 fetch 200; 0 missing alt; 53 distinct hero files, 0 reused; 0 EXIF; 0 AI strings |
| Favicon (new heavier) | **9/9 MATCH** (md5 identical to local build) on live www |
| Dangling phrases | All 11 named phrases 0; "See and" 0; bare `<a>and</a>` 0; "Related services: and" 0; `?v=` 0 |
| Speed (local build) | Worst LCP 1076 ms (desktop home) / mobile worst 564 ms — all < 1800 ms; CLS 0.0000 everywhere; mobile transfer max 650.4 KB (< 800 KB) |
| Orphans / crawl waste | 0 orphans (reachable 53/53); no dual-200 forms; no redirect chains (max 1 hop); no 404s; privacy/terms 404 + excluded |
| vercel.json | **Does NOT exist** (correct — user forbade ALL redirects; deleted in ea8c25b) |
| Water-mitigation FAQ | **COMPLETE** — the 5 questions follow the pointer as a bullet list (verified live + source) |

**No real defect found.** Every number above was measured fresh on the live site in this audit (not carried over from the local round).

---

## Deploy timeline — why www was late, and the flip

| Time (PKT) | Event |
|---|---|
| ~18:26 | Round pushed: main `cefc3be` (29 pages slash→no-slash, 29 vercel.json redirects, heavier favicon/header, 142 phrase removals) + gh-pages `f74ae42`. Preview live on new build immediately. |
| ~18:26–18:35 | www STILL old build (3 checks: /services no-slash 308→slash, /services/ 200, sitemap 51×2026-11-08). |
| ~18:46 | www STILL old after 20 min. Cause found (repo side): Vercel's build command is `npm run vercel-build` but package.json NEVER had that script (only build/dev/export) — every deploy failed (exit 1). |
| ~18:48 | Fix pushed: main `f51c3e6` — added `"vercel-build": "npm run export"` to package.json (verified locally first: full export exit 0). |
| ~18:57 | www flipped — BUT the deploy had failed again. Root cause: vercel.json `"comment"` property fails Vercel's schema (additional properties rejected). Fix: main `7b2f327` — removed the comment property. Fresh live curl ~18:57: every slash URL 308→no-slash, no-slash 200, sitemap 53×2026-11-08, canonicals no-slash. |
| ~19:02 | **User forbade ALL redirects (3×, "rok rha hu").** vercel.json DELETED entirely (all 29 redirects), commit `ea8c25b`, Vercel `dpl_9Ydc1uT5KK5xcjfJA6nz73veXByy` READY. Live verified: slash URLs STILL 308→no-slash on every page — this is the platform/Next.js `trailingSlash:false` built-in, NOT a redirect added by anyone. No vercel.json exists. |
| ~19:05 | **This audit (Pass 1)** re-verified the URL layer fresh on ea8c25b (see below). |

**His logic (recorded, not argued):** URL same as old site = no redirect; redirect only when a URL CHANGES. The 29 flipped pages changed form (slash→no-slash), but the slash→308 is provided by the platform's trailingSlash handling, not by any redirect file. Do NOT re-add any redirect, ever, without his explicit word.

**Stale-cache note:** His screenshots ~18:56–18:57 (emergency + water-mitigation, "Canonicalised" red, URL slash) were STALE BROWSER CACHE from before the deploy flipped — the live server was already correct. He must hard-refresh (Ctrl+Shift+R) / close-reopen the tab; then the slash redirects and the flag clears. This audit used fresh, no-cache fetches throughout.

---

## Master checklist — per-point status (all measured live on ea8c25b unless noted)

| # | Check | Status |
|---|---|---|
| 1 | Self-canonicalization 53/53: canonical == served URL == sitemap loc, no redirect hop on any canonical | **PASS** — 53/53 canonical 200 direct; canonical == sitemap loc on all 53; og:url == canonical on all 53. Verified by `tools/verify_www_flip.py` (PROBLEMS 0) + the fast parallel audit (PROBLEMS 0). |
| 2 | H1 1×53/53, visible, doc-verbatim | **PASS** — static (live www): 53/53 exactly 1 H1, text == doc H1 verbatim. Rendered (identical local build, Playwright, desktop): 53/53 H1 visible + verbatim + 0 horizontal overflow (`tools/h1_sweep.py`, exit 0). |
| 3 | Titles / descriptions | **REPORT ONLY (U5 — user's wording call, NEVER rewritten)** — titles >60ch: 52/53; descriptions >160ch: 23/53. Title/description text identical to the doc (0 mismatches vs pages.json). |
| 4 | og:url + schema (JSON-LD parsed, not grepped) | **PASS** — HomeAndConstructionBusiness 53/53, BreadcrumbList 53/53, FAQPage 51/51, FAQ 222/222 verbatim, Article 10/10, WebPage 53/53, Service 18/18, WebSite 53/53; 0 trailing-slash URL values in any node; breadcrumb last item == canonical on all 52 non-home pages. |
| 5 | Sitemap 53, date-only lastmod, only canonicals | **PASS** — 53 locs == canonical set, lastmod 53× 2026-11-08 (date-only), no image entries. |
| 6 | robots.txt 22 AI groups intact, llms.txt 53 links no-slash + NAP | **PASS** — robots.txt 23 `User-agent:` lines = wildcard + 22 AI groups, Sitemap present; llms.txt 53 links == canonical set, 0 trailing-slash links (only the homepage `/`), NAP (phone + address) present. IndexNow key file 200. |
| 7 | Internal links: all 200, PROBLEMS 0, nested anchors 0, body self-links 0, orphans 0, repeats 0 (in-scope) | **PASS** — 53 unique internal targets all 200 (52 page slugs + /sitemap.xml); 108 home refs; 2,291 per-page unique href instances; 6,777 raw `<a>` instances; every instance resolves to a verified-200 target. Nested anchors 0; body self-links 0; orphans 0 (reachable from home 53/53); in-scope body-link repeats 0. "See and" 0; bare `<a>and</a>` 0. |
| 8 | Images: alt on all, size/weight, 0 EXIF, 0 cross-site repeats, 0 AI strings | **PASS** — 246 img tags / 71 distinct srcs, all 71 fetch 200 on live www; 0 missing alt; 71 slots, all WebP 1200×800; 0 EXIF tags; 0 AI strings in filename/alt; 53 distinct hero files, 0 hero files reused across pages; 0 duplicate images on any one page. |
| 9 | Speed (identical build, local Playwright/Chromium) | **PASS** — worst LCP 1076 ms (desktop home) / mobile worst 564 ms, all < 1,800 ms; CLS 0.0000 everywhere; mobile transfer max 650.4 KB (< 800 KB); horizontal overflow 0 px on all 8 measured views + all 53 pages in the H1 sweep. Desktop home transfer 2201.2 KB (desktop only — the 800 KB budget is mobile; homepage carries 37 cards + hero). |
| 10 | NO CRAWL WASTE | **PASS** — no URL serves 200 in both forms (all 52 slash forms → 308, exactly 1 hop, Location resolves to the no-slash canonical); no redirect chains (canonicals 200 direct); no 404s among canonicals/links; privacy/terms do not exist (404) and are absent from the sitemap; orphans 0; dead links 0; vercel.json does NOT exist (0 redirects by user order). |
| 11 | No-slash URL form (user decision, resolves F1) | **PASS** — homepage keeps `/`; all other 52 pages no-slash; 0 trailing-slash URL values in canonicals, og:url, schema, sitemap, llms.txt, or internal hrefs (only the homepage `/`). |
| 12 | Heavier classic favicon + header logo | **PASS** — all 9 favicon assets on live www are byte-identical (md5) to the local Heavy A (0.62) build; header SVG is the same heavy mark (navy tile + wordmark unchanged); verified by pixels at 16/32/48 + header desktop/mobile screenshots in this audit (see §Speed/render). Real browser tab-bar render needs a live browser — NOT verified here (see §Open items). |
| 13 | Dangling link-phrase removals (142 locations, 432 words) | **PASS** — all 11 named instances 0 sitewide on live www (verified by the fast audit's phrase scan + spot checks on homepage, water-heater, burst-pipe, ceiling); "Related services: and" 0; no paragraph ends in a dangling "Full …" / "Detailed guide:" / "See:" / "More:" link phrase. 9 keeps documented in the round findings; burst-pipe block 16 ("…what you can see.") is a real sentence, correctly kept. |
| — | No `?v=` query-string URLs anywhere | **PASS** — 0 occurrences in any fetched live HTML. |
| — | Water-mitigation FAQ complete | **PASS (verified, NOT a defect)** — see §Water-mitigation FAQ. |

---

## URL layer — fresh verification on ea8c25b (`tools/verify_www_flip.py`, PROBLEMS 0)

Run after the ea8c25b deploy flipped. Every canonical URL taken from the LIVE sitemap (not from a local list).

- Canonicals 200 direct: **53/53** (no redirect hop on any canonical).
- Slash forms 308 correct: **52/52** — every non-homepage slash form returns 308 and its Location resolves exactly to the no-slash canonical. (The Location header is a relative path, e.g. `/services` — valid HTTP, resolves correctly. An earlier too-strict check in this audit demanded an absolute Location and flagged all 52; the check was fixed to resolve via urljoin and all 52 pass. The server behaviour was always correct.)
- Homepage: 200, canonical `https://www.tulsawaterdamagerepair.com/` (trailing slash kept, never removed).
- Sitemap: 53 locs, lastmod 53× 2026-11-08.
- robots.txt: 23 User-agent lines. llms.txt: 53 links, 0 trailing-slash. IndexNow key: 200.
- Favicon (www): favicon.ico, 16×16, 32×32, 48×48, apple-touch-icon — all 5 MATCH (md5 identical to local build).
- Spot checks (fresh, no cache): /services 200 / /services/ 308; /contact 200 / /contact/ 308; /services/emergency-water-damage-restoration 200 / slash 308; /services/water-mitigation 200 / slash 308; /service-areas/bixby-ok 200 / slash 308; /resources/first-24-hours-after-water-damage/ 308. All 52 slash forms behave the same (verified exhaustively by the script, 52/52).

**No vercel.json redirects exist.** The slash→308 is the platform/Next.js `trailingSlash:false` built-in. Confirmed: `vercel.json` does NOT exist in the repo (main ea8c25b) and the live behaviour is identical with and without it.

---

## Content / SEO — live www fast parallel audit (`tools/audit_live_www_fast.py`, PROBLEMS 0)

All 53 pages fetched live over HTTPS in parallel; JSON-LD parsed (not grepped); FAQ compared verbatim against the source.

- Pages 200: **53/53**. Canonical == served URL: 53/53. og:url == canonical: 53/53.
- H1: 1× on 53/53, doc-verbatim (0 mismatches).
- Titles/descriptions: text identical to doc (0 mismatches); lengths report-only — titles >60ch 52/53, descriptions >160ch 23/53 (U5).
- JSON-LD types: WebSite 53, BreadcrumbList 53, HomeAndConstructionBusiness 53, WebPage 53, FAQPage 51, Service 18, Article 10. 0 trailing-slash URL values. Breadcrumb last item == canonical on 52/52 non-home pages.
- FAQ: **222/222 verbatim** (visible Q&A == FAQPage schema == source). 51 pages with FAQs, 51 with FAQPage schema.
- Named phrases: all 11 = **0** sitewide (phrase_hits {}). "See and" 0. Bare `<a>and</a>` 0. `?v=` 0. Forbidden strings (wrong phones, `(/services/`, `[Embed Google Map`, etc.) 0.
- Nested anchors: 0. Body self-links: 0.
- Body-link repeats (in-scope): 0.

## Links — reconciliation

| Metric | Count | Status |
|---|---|---|
| Unique internal targets (deduped globally) | 53 (52 page slugs + /sitemap.xml) | all 200 |
| Home refs (`/`) | 108 | — |
| Per-page unique `<a>` href instances | 2,291 | every instance resolves to a verified-200 target |
| Raw `<a>` instances | 6,777 | — |
| Broken links | 0 | — |
| Orphans (BFS from home) | 0 (reachable 53/53) | — |

Note on counts: the round's local audit reported 2,618 link fetches. That number counted (href, in-content-context) pairs per page, so a href appearing both in body copy and in nav/cards on the same page counted twice. This audit counts unique hrefs per page (2,291) and unique targets globally (53). Both methods agree on the substance: **every link target returns 200, nothing is broken**. The 2,618 vs 2,291 gap is the context-split double-counting, not missing links.

## Images + favicon

- 246 `<img>` tags / 71 distinct srcs; all 71 fetch **200** on live www. 0 missing alt.
- 53 distinct hero files, **0 reused** across pages. 0 duplicate images on any one page.
- 0 EXIF tags (checked on the identical local files). 0 AI strings in filename/alt.
- Favicon: **9/9 MATCH** — favicon.ico, 16×16, 32×32, 48×48, 192×192, 512×512, 512×512-maskable, apple-touch-icon, favicon-master — live www files are byte-identical (md5) to the local Heavy A (0.62) build. The new heavier classic mark is served.

## Speed + render (identical local build, Playwright/Chromium)

`tools/cwv_shots.py` (tag postpush) + `tools/h1_sweep.py` (tag postpush), both exit 0. Screenshots in `qa-postpush-live/shots-postpush/` (desktop + mobile, viewport + full page).

| Page | Desktop LCP | Mobile LCP | Desktop transfer | Mobile transfer | CLS | H1 visible | Overflow |
|---|---|---|---|---|---|---|---|
| / (home) | 1076 ms | 376 ms | 2201.2 KB | 650.4 KB | 0.0000 | yes | 0 px |
| /services | 448 ms | 564 ms | 1206.0 KB | 602.9 KB | 0.0000 | yes | 0 px |
| /contact | 404 ms | 372 ms | 638.0 KB | 568.7 KB | 0.0000 | yes | 0 px |
| /commercial | 316 ms | 320 ms | 706.2 KB | 602.5 KB | 0.0000 | yes | 0 px |

- Worst LCP **1076 ms** (budget 1800 ms). Worst CLS **0**. Mobile transfer max **650.4 KB** (budget 800 KB).
- H1 rendered sweep (all 53 pages, desktop): **53/53** H1 1× + visible + verbatim + 0 overflow. 0 pages without a hero image.
- Screenshots viewed by pixels (home + commercial, desktop + mobile): header shows the heavier drop in the navy tile with nav/wordmark/EMERGENCY button intact; hero + H1 fully visible on home and commercial (no blank hero, no gap — the old commercial-blank-hero concern is resolved on the render); intro text, CTAs, trust chips all clean; sticky mobile call bar present at the bottom on mobile; no horizontal overflow.

**Limitation (stated plainly):** live rendering in this sandbox is blocked by a network tunnel, so LCP/CLS/screenshots are measured on the IDENTICAL local build (same commit content, same out/) served locally. Live HTML was verified by direct fetches (status, canonical, H1, schema, links, images, favicon hashes). A real-browser tab-bar favicon render was not verified here.

## Water-mitigation FAQ — verified COMPLETE (not a defect)

The round agent flagged FAQ "What questions should I ask a mitigation company?" as having an answer that is only the pointer "Ask these five questions before signing any agreement:" with no questions following. **That flag was wrong — the agent did not look carefully.**

Verified from the source (`content/pages.json`, water-mitigation entry) AND from the live www rendered page:
- The FAQ answer is the pointer: "Ask these five questions before signing any agreement:"
- The 5 questions follow IMMEDIATELY as a bullet list (block 61, type `ul`):
  1. Does your drying process follow IICRC S500 standards?
  2. Will you take daily moisture readings at every mapped point?
  3. Will I receive drying logs and moisture maps for my adjuster?
  4. Do you provide a written scope that my adjuster can review?
  5. Do you pull equipment based on readings or on a fixed schedule?
- Live www rendered text reads, in order: "What questions should I ask a mitigation company? + Ask these five questions before signing any agreement: Does your drying process follow IICRC S500 standards? Will you take daily moisture readings at every mapped point? Will I receive drying logs and moisture maps for my adjuster? Do you provide a written scope that my adjuster can review? Do you pull equipment based on readings or on a fixed schedule?"
- FAQPage schema is present on the page. FAQ 222/222 verbatim holds.

**No action needed. Do NOT delete this FAQ and do NOT add questions — they are already there.**

## Open items (NOT defects — need his call, or his side)

- **U5 (report only, untouched):** 52/53 titles >60ch, 23/53 descriptions >160ch — verbatim from his doc. His wording call; never rewrite without his word.
- **18px micro-label exceptions (untouched):** header "EMERGENCY?" + brand tagline "TULSA, OKLAHOMA" (~11px). His call: 18px or keep small.
- **Real browser tab-bar favicon render (desktop + mobile):** favicon files verified by hash on live www (9/9 MATCH), but a real tab-bar render needs his browser (hard-refresh if cached). Not a defect — a verification limit.
- **His side (unchanged):** Search Console generative-AI Include confirm, GBP completion + genuine review flow, claim Yelp + Bing Places + Apple Business Connect, verify Bing indexing, contact-form delivery inbox, WAF/Cloudflare check.
- **Bing API:** separate, needs his API key / account access (not attempted here). IndexNow: 53 new no-slash URLs already submitted 2026-11-08 ~18:35 (HTTP 202 Accepted); do NOT resubmit.
- **Known benign survivor:** burst-pipe block 16 ends "…what you can see." — a real sentence, not a dangling "see". Correctly kept.

## Method, tools, and honest notes

- **Live audit tools (new, in `tools/`, untracked):** `tools/verify_www_flip.py` (URL layer: 53 canonicals + 52 slash forms + sitemap/robots/llms/key/favicon, PROBLEMS 0), `tools/audit_live_www_fast.py` (full parallel live audit: pages, canonical/og/H1/schema/FAQ/phrases/links/images/orphans/favicon, PROBLEMS 0), `tools/audit_live_www.py` (sequential version — superseded by the fast one), `tools/audit_live_preview.py` (preview version — killed before completion; it would have crashed on the deleted vercel.json and was superseded by the www audit once www flipped).
- **Check-bug owned and fixed in this audit:** (1) The first `verify_www_flip.py` run flagged all 52 slash forms because it demanded an ABSOLUTE Location header; the server correctly returns a RELATIVE Location (`/services`), which is valid HTTP and resolves exactly to the canonical. Fixed with urljoin resolution; re-run gives 52/52 correct. The server behaviour was always correct — my check was too strict. (2) Two scripts were initially written without their `if __name__ == '__main__'` entry block and exited silently with no output; caught by the empty output + missing output file, fixed, re-run.
- **What was NOT verified:** live rendering (sandbox tunnel blocks it — measured on the identical local build instead); real browser tab-bar favicon (needs his browser); Google Search Console / indexing state (his side); live LCP on a real device (local Chromium only).
- **What was NOT done:** no redirects added (user forbade all — vercel.json stays deleted); no content changed; no push/deploy; no IndexNow/Bing submission; no domain/DNS touched.
- **Evidence:** `qa-postpush-live/verify_www.json`, `qa-postpush-live/audit_www_fast.json`, `qa-postpush-live/cwv-postpush.json`, `qa-postpush-live/h1-postpush.json`, `qa-postpush-live/shots-postpush/` (16 screenshots: 4 pages × desktop/mobile × viewport/full).

---

## Appendix — per-page results (live www, ea8c25b)

Status = canonical URL status. H1 = count (must be 1). Canon/OG = canonical/og:url == served URL. FAQ = visible == schema count. Slash = slash-form status (must be 308; `-` = homepage).

| Slug | Type | Status | H1 | Canon | OG | FAQ | LD types | Slash |
|---|---|---|---|---|---|---|---|---|
| / | homepage | 200 | 1 | OK | OK | 6/6 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | - |
| /about-us | about | 200 | 1 | OK | OK | - | BreadcrumbList,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /commercial | commercial | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /contact | contact | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources | resources-hub | 200 | 1 | OK | OK | - | BreadcrumbList,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/first-24-hours-after-water-damage | resource | 200 | 1 | OK | OK | 5/5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/how-long-does-water-damage-take-to-dry | resource | 200 | 1 | OK | OK | 4/4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/how-to-file-water-damage-insurance-claim-tulsa | resource | 200 | 1 | OK | OK | 4/4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/how-to-prevent-frozen-pipes-tulsa | resource | 200 | 1 | OK | OK | 4/4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/mold-after-water-damage-tulsa | resource | 200 | 1 | OK | OK | 5/5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/oklahoma-water-damage-insurance-guide | resource | 200 | 1 | OK | OK | 5/5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/signs-of-hidden-water-damage | resource | 200 | 1 | OK | OK | 3/3 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/water-damage-categories-and-classes-explained | resource | 200 | 1 | OK | OK | 4/4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/water-damage-restoration-cost-tulsa | resource | 200 | 1 | OK | OK | 5/5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /resources/water-damage-vs-flood-damage-insurance-oklahoma | resource | 200 | 1 | OK | OK | 4/4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/bixby-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/broken-arrow-ok | area | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/brookside-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/catoosa-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/cherry-street-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/claremore-ok | area | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/collinsville-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/coweta-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/east-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/glenpool-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/jenks-ok | area | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/midtown-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/north-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/owasso-ok | area | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/sand-springs-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/sapulpa-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/skiatook-ok | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/south-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /service-areas/west-tulsa | area | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /services | hub | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 |
| /services/ac-drain-line-overflow-cleanup | service | 200 | 1 | OK | OK | 3/3 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/appliance-leak-water-damage | service | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/burst-pipe-water-damage | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/ceiling-water-damage | service | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/commercial-water-damage | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/emergency-water-damage-restoration | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/fire-damage-restoration | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/flood-damage-restoration | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/flooded-basement-cleanup | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/hardwood-floor-drying | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/mold-remediation | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/roof-leak-water-damage | service | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/sewage-backup-cleanup | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/slab-leak-water-damage | service | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/smoke-soot-damage-cleanup | service | 200 | 1 | OK | OK | 4/4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/storm-damage-repair | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/water-heater-leak-cleanup | service | 200 | 1 | OK | OK | 3/3 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
| /services/water-mitigation | service | 200 | 1 | OK | OK | 5/5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 |
