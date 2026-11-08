# URL Form Change: Slash → No-Slash + 2× Deepest Technical SEO A-to-Z

**Site:** Tulsa Water Damage Repair — https://www.tulsawaterdamagerepair.com (www primary), (918) 395-9320
**Date:** 2026-11-08 (Sun) — local round, **NOT pushed, NO live verification yet**
**Base commit:** 7d9cfd7 (homepage round, pushed live 17:05 PKT)
**Reason (user's decision, resolves open F1):** the domain previously hosted a dead site whose URLs were all no-slash (his screenshot: /services/emergency-water-damage-restoration, /services/mold-remediation, /services/commercial-water-damage, /services, /services/water-mitigation, /services/fire-damage-restoration, /contact, /services/storm-damage-repair, /services/flood-damage-restoration). The new site must use the SAME form so Google gets no conflict and no chance to pick the wrong form. Homepage KEEPS its trailing slash (https://www.tulsawaterdamagerepair.com/ — never removed). The 2 direct conflicts with the old site, /services/ and /contact/, are flipped in this round; /services (no-slash) previously 308 → /services/ (slash) — after the change this MUST invert (see post-push checks).

**Method:** Task 1 flip → Pass 1 full audit + fixes → Pass 2 FRESH re-audit from scratch (fresh rebuild, re-measured everything, trusted nothing from Pass 1) → point 12 heavier classic favicon + header logo → point 13 dangling link-phrase removals (first round + 2 broadened sweeps) → FINAL audit on the final build (fresh rebuild, full re-measure). All checks run locally on the identical build served locally (Playwright/Chromium); live HTML was NOT re-verified because nothing was pushed.

**Audit tooling (new, committed in tools/):** `tools/audit_noslash.py` — full static audit with its own Vercel-faithful local server (extensionless URLs + slash→308 per vercel.json, redirects NOT followed so a 308 surfaces as 308); `tools/cwv_shots.py` — CWV + screenshots via Playwright; `tools/h1_sweep.py` — rendered H1-visibility sweep over all 53 pages.

---

## Master checklist — per-point status

| # | Check | Status |
|---|-------|--------|
| 1 | Self-canonicalization 53/53: canonical == served URL == sitemap loc, no redirect hop on any canonical | **PASS** — 53/53 canonical 200 direct, canonical == sitemap loc (Pass 1 + Pass 2 + independent verify_site.py run) |
| 2 | H1 1×53/53, visible, doc-verbatim | **PASS** — static 53/53 both passes; rendered sweep (Pass 2) 53/53 visible + verbatim + 0 horizontal overflow. Pass 1 rendered-visible on the 4 CWV pages (desktop + mobile) |
| 3 | Titles / descriptions | **REPORT ONLY (U5 — user's wording call, NEVER rewritten)** — titles >60ch: 52/53; descriptions >160ch: 23/53. Title/description text identical to the doc (0 mismatches vs pages.json) |
| 4 | og:url + schema (JSON-LD parsed, not grepped) | **PASS** — HomeAndConstructionBusiness 53/53, BreadcrumbList 53/53, FAQPage 51/51, FAQ 222/222 verbatim, Article 10/10, WebPage 53/53, Service 18/18, WebSite 53/53; all URL values no-slash (0 trailing-slash URL values in any node); breadcrumb last item == canonical on all 52 non-home pages |
| 5 | Sitemap 53, date-only lastmod, only canonicals | **PASS** — 53 locs == canonical set, lastmod 53× 2026-11-08 (date-only), no image entries |
| 6 | robots.txt 22 AI groups intact, llms.txt 53 links no-slash + NAP | **PASS** — robots.txt 23 `User-agent:` lines = wildcard + 22 AI groups, byte-identical to HEAD (unchanged); llms.txt 53 links == canonical set, 0 trailing-slash links (only the homepage `/`), NAP present |
| 7 | Internal links: all 200, PROBLEMS 0, nested anchors 0, body self-links 0, orphans 0, repeats 0 (in-scope) | **PASS (final build)** — 2,618 link fetches all 200 (final audit) + 2,316 all 200 (independent verify_site.py, pre-removal build); nested anchors 0; body self-links 0; orphans 0 (reachable from home 53/53); in-scope repeats 0. Fetches fell 2,709 → 2,618 (−85) ONLY because point 13 removed 87 link instances — reconciled exactly in §Final audit. "See and" 0; dangling "see" 1 known benign survivor (see §Open items). Card+plain overlaps on homepage/about-us/contact are pre-existing design on excluded pages — the repeats diff vs Pass 1 is exactly the 3 removed duplicates (see §Final audit) |
| 8 | Images: alt on all, size/weight, 0 EXIF, 0 cross-site repeats, 0 AI strings | **PASS** — 246 img tags / 71 distinct srcs, 0 missing alt; 71 slots, all WebP 1200×800, total 7,334.6 KB, largest single file 148.6 KB; 0 EXIF tags; 0 AI strings in filename/alt; 53 distinct hero files, 0 hero files reused across pages; 0 duplicate images on any one page |
| 9 | Speed (identical build, local Playwright/Chromium) | **PASS** — worst LCP 800 ms (P1) / 936 ms (P2) / **832 ms (final)**, all < 1,800 ms; CLS 0.0000 everywhere; mobile transfer max 649.0 KB (P1) / 652.8 KB (P2) / **650.4 KB (final)**, all < 800 KB; horizontal overflow 0 px on all 8 measured views + all 53 pages in the H1 sweep |
| 10 | NO CRAWL WASTE | **PASS (locally verifiable part)** — no URL serves 200 in both forms (slash variants of flipped pages → 308; all 52 flat .html present, 0 stray index.html); no redirect chains (canonicals 200 direct, max 1 hop on slash forms); no 404s among canonicals/links; privacy/terms do not exist in the build and are absent from the sitemap; orphans 0; dead links 0. **Live slash→308 check is post-push** (see §Post-push live checks) |
| — | Word-diff proof | **PASS** — 96,903 → 96,471 visible words (−432), 0 added; every removed word is one of the 142 ordered link-phrase removals in §Point 13 (per-route deltas all reconciled; §Word-diff proof) |
| — | No `?v=` query-string URLs anywhere | **PASS** — 0 occurrences in out/, app/, content/, public/, tools/, vercel.json, next.config.js |
| — | gh-pages preview prefix flow | **PASS (re-run on final build)** — publish_prefix.py: 54 html + 1 css rewritten, `//tulsa-water-damage-repair` count 0, 12,397 single-slash prefixed refs, 0 prefixed slash-form hrefs remaining. NOT pushed — check only |
| 12 | Heavier classic favicon + header logo (same mark) | **PASS** — all 9 favicon assets regenerated (Heavy A 0.62); cyan coverage up at every size; header SVG is the same heavy drop; verified by pixels at 16/32/48 + 8× zoom + simulated tab + header desktop/mobile/sticky/menu-open (§Point 12). Real browser tab-bar check needs a live browser — NOT verified locally, see §Point 12 |
| 13 | Dangling link-phrase removals (142 locations, 432 words) | **PASS** — every named instance removed + 2 broadened sweeps; no paragraph ends in a dangling "Full …" / "Detailed guide:" / "See:" / "More:" link phrase; all 14 named phrases 0 sitewide; removed targets stay reachable (§Point 13). 9 keeps documented by name; 1 whole-answer pointer needs his call (§Open items) |

---

## The 29 flipped pages (slash → no-slash)

Homepage `/` KEEPS its trailing slash and is NOT in this table.

| # | Before (slash) | After (no-slash) |
|---|---|---|
| 1 | https://www.tulsawaterdamagerepair.com/services/ | https://www.tulsawaterdamagerepair.com/services |
| 2 | https://www.tulsawaterdamagerepair.com/service-areas/claremore-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/claremore-ok |
| 3 | https://www.tulsawaterdamagerepair.com/service-areas/owasso-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/owasso-ok |
| 4 | https://www.tulsawaterdamagerepair.com/service-areas/jenks-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/jenks-ok |
| 5 | https://www.tulsawaterdamagerepair.com/service-areas/glenpool-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/glenpool-ok |
| 6 | https://www.tulsawaterdamagerepair.com/service-areas/bixby-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/bixby-ok |
| 7 | https://www.tulsawaterdamagerepair.com/service-areas/broken-arrow-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/broken-arrow-ok |
| 8 | https://www.tulsawaterdamagerepair.com/service-areas/sand-springs-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/sand-springs-ok |
| 9 | https://www.tulsawaterdamagerepair.com/service-areas/skiatook-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/skiatook-ok |
| 10 | https://www.tulsawaterdamagerepair.com/service-areas/coweta-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/coweta-ok |
| 11 | https://www.tulsawaterdamagerepair.com/service-areas/catoosa-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/catoosa-ok |
| 12 | https://www.tulsawaterdamagerepair.com/service-areas/collinsville-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/collinsville-ok |
| 13 | https://www.tulsawaterdamagerepair.com/service-areas/sapulpa-ok/ | https://www.tulsawaterdamagerepair.com/service-areas/sapulpa-ok |
| 14 | https://www.tulsawaterdamagerepair.com/service-areas/midtown-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/midtown-tulsa |
| 15 | https://www.tulsawaterdamagerepair.com/about-us/ | https://www.tulsawaterdamagerepair.com/about-us |
| 16 | https://www.tulsawaterdamagerepair.com/contact/ | https://www.tulsawaterdamagerepair.com/contact |
| 17 | https://www.tulsawaterdamagerepair.com/service-areas/brookside-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/brookside-tulsa |
| 18 | https://www.tulsawaterdamagerepair.com/service-areas/south-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/south-tulsa |
| 19 | https://www.tulsawaterdamagerepair.com/service-areas/west-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/west-tulsa |
| 20 | https://www.tulsawaterdamagerepair.com/service-areas/north-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/north-tulsa |
| 21 | https://www.tulsawaterdamagerepair.com/services/ac-drain-line-overflow-cleanup/ | https://www.tulsawaterdamagerepair.com/services/ac-drain-line-overflow-cleanup |
| 22 | https://www.tulsawaterdamagerepair.com/services/appliance-leak-water-damage/ | https://www.tulsawaterdamagerepair.com/services/appliance-leak-water-damage |
| 23 | https://www.tulsawaterdamagerepair.com/services/water-heater-leak-cleanup/ | https://www.tulsawaterdamagerepair.com/services/water-heater-leak-cleanup |
| 24 | https://www.tulsawaterdamagerepair.com/services/roof-leak-water-damage/ | https://www.tulsawaterdamagerepair.com/services/roof-leak-water-damage |
| 25 | https://www.tulsawaterdamagerepair.com/services/slab-leak-water-damage/ | https://www.tulsawaterdamagerepair.com/services/slab-leak-water-damage |
| 26 | https://www.tulsawaterdamagerepair.com/service-areas/east-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/east-tulsa |
| 27 | https://www.tulsawaterdamagerepair.com/service-areas/cherry-street-tulsa/ | https://www.tulsawaterdamagerepair.com/service-areas/cherry-street-tulsa |
| 28 | https://www.tulsawaterdamagerepair.com/commercial/ | https://www.tulsawaterdamagerepair.com/commercial |
| 29 | https://www.tulsawaterdamagerepair.com/resources/ | https://www.tulsawaterdamagerepair.com/resources |

Verified: all 29 slugs flipped in `content/pages.json` (29/29, 0 slash slugs remain); 205 body-copy hrefs to these pages flipped in the same file (0 old exact refs remain); all 29 keys flipped in `content/images.json` (+ `images-a.json` 9, `images-b.json` 19 — values verified identical after the key rename); 47 quoted refs flipped in `app/lib-meta.js` (incl. `parentOf` hubs, SERVICE_GROUPS, AREA_GROUPS, FOOTER_AREAS, SERVICE_TITLES keys + embedded hrefs); 7 in `Header.jsx`, 6 in `Footer.jsx`, 1 in `Shared.jsx` (FinalCta contact link — the `startsWith('/services/')` prefix check was deliberately left alone), 1 fallback + 1 regex + 2 CTAs in `app/[[...slug]]/page.js`; 29 links flipped in `public/llms.txt` (exact-URL match — see §Fixes for the prefix-corruption catch); canonical/og:url/schema URLs flip automatically because every emitter builds from `SITE.url + page.slug` (verified per page in the audits, not assumed).

---

## Slash → no-slash redirect table (29 entries, `vercel.json`, `permanent: true` = 308)

This is the guarantee mechanism: Vercel serves `permanent:true` as 308. Every flipped page's old slash form redirects exactly once to its no-slash canonical; the no-slash canonical serves 200 directly with no hop. Homepage `/` is NOT redirected.

| # | Source (slash) | Destination (no-slash) | Status |
|---|---|---|---|
| 1 | /services/ | /services | 308 |
| 2 | /service-areas/claremore-ok/ | /service-areas/claremore-ok | 308 |
| 3 | /service-areas/owasso-ok/ | /service-areas/owasso-ok | 308 |
| 4 | /service-areas/jenks-ok/ | /service-areas/jenks-ok | 308 |
| 5 | /service-areas/glenpool-ok/ | /service-areas/glenpool-ok | 308 |
| 6 | /service-areas/bixby-ok/ | /service-areas/bixby-ok | 308 |
| 7 | /service-areas/broken-arrow-ok/ | /service-areas/broken-arrow-ok | 308 |
| 8 | /service-areas/sand-springs-ok/ | /service-areas/sand-springs-ok | 308 |
| 9 | /service-areas/skiatook-ok/ | /service-areas/skiatook-ok | 308 |
| 10 | /service-areas/coweta-ok/ | /service-areas/coweta-ok | 308 |
| 11 | /service-areas/catoosa-ok/ | /service-areas/catoosa-ok | 308 |
| 12 | /service-areas/collinsville-ok/ | /service-areas/collinsville-ok | 308 |
| 13 | /service-areas/sapulpa-ok/ | /service-areas/sapulpa-ok | 308 |
| 14 | /service-areas/midtown-tulsa/ | /service-areas/midtown-tulsa | 308 |
| 15 | /about-us/ | /about-us | 308 |
| 16 | /contact/ | /contact | 308 |
| 17 | /service-areas/brookside-tulsa/ | /service-areas/brookside-tulsa | 308 |
| 18 | /service-areas/south-tulsa/ | /service-areas/south-tulsa | 308 |
| 19 | /service-areas/west-tulsa/ | /service-areas/west-tulsa | 308 |
| 20 | /service-areas/north-tulsa/ | /service-areas/north-tulsa | 308 |
| 21 | /services/ac-drain-line-overflow-cleanup/ | /services/ac-drain-line-overflow-cleanup | 308 |
| 22 | /services/appliance-leak-water-damage/ | /services/appliance-leak-water-damage | 308 |
| 23 | /services/water-heater-leak-cleanup/ | /services/water-heater-leak-cleanup | 308 |
| 24 | /services/roof-leak-water-damage/ | /services/roof-leak-water-damage | 308 |
| 25 | /services/slab-leak-water-damage/ | /services/slab-leak-water-damage | 308 |
| 26 | /service-areas/east-tulsa/ | /service-areas/east-tulsa | 308 |
| 27 | /service-areas/cherry-street-tulsa/ | /service-areas/cherry-street-tulsa | 308 |
| 28 | /commercial/ | /commercial | 308 |
| 29 | /resources/ | /resources | 308 |

Local verification: the audit server simulates exactly these 29 redirects (reads `vercel.json`); every flipped page's slash variant returned **308 with Location == the no-slash canonical** in both passes. The 23 previously-no-slash pages have NO redirect by design (per the order's 29-entry scope): their slash forms will 404 on Vercel — they were never canonical, never linked, never in the sitemap. Note the behaviour change: on the OLD build those 23 slash forms served 200 (dual-file export). If the user wants them 308'd too, that is 23 more vercel.json entries on his word — not added here.

**Preview limitation (not a defect):** on the GitHub Pages preview, flat `.html` files serve at extensionless URLs (the 23 existing no-slash routes already prove this), but slash forms 404 there — Pages has no redirect layer. The 308s only exist on Vercel.

---

## What changed (code/config, not content)

- `next.config.js`: `trailingSlash: true` → `false`. Correct build remains `npm run export` (`next build && node tools/post_export.js`) — never `npm run build` alone.
- `tools/post_export.js`: the old copy step is GONE (it would now fail — no `<path>/index.html` files exist for no-slash routes). It is now a build-gating verifier: asserts 52 flat `.html` files + homepage `index.html` exist and 0 stray `<path>/index.html` exist; exits 1 otherwise. Verified in both builds: `post-export: verified 52 flat .html files + homepage index.html, 0 stray index.html`.
- `tools/build_sitemap.py`: lastmod rule changed — all 53 → 2026-11-08 (see §Sitemap lastmod rule). The removed robots.txt-writing block was NOT reintroduced.
- `vercel.json` (NEW): the 29 redirects above.
- `public/sitemap.xml`: regenerated — 53 locs, all lastmod 2026-11-08.
- `public/llms.txt`: 29 links flipped (exact-URL match; see §Fixes).
- `content/pages.json`, `content/images*.json`, `app/lib-meta.js`, `app/components/{Header,Footer,Shared}.jsx`, `app/[[...slug]]/page.js`: URL-form strings only (see §The 29 flipped pages). No other files changed. `public/robots.txt` byte-identical to HEAD.
- `tools/verify_site.py`: its dual-200 variant check is obsolete under no-slash — updated to "slash variant must NOT serve 200" (308 with correct Location on a redirect layer, 404 on plain http.server), with a no-redirect fetch helper. `tools/audit_repeats.py`: fixed a latent sitemap regex (it matched 0 routes — every earlier run was a vacuous pass; see §Fixes). `tools/verify_see_cuts.py`: Collinsville slug literal updated to the no-slash form.

### Sitemap lastmod rule (verified, not invented)

**Rule:** every page's URL and/or links changed in this round, so all 53 → 2026-11-08 (date-only `YYYY-MM-DD`, no time). Verified two ways: (1) the 29 flipped pages changed URL; the other 24 changed because the header/footer/hub links on every page flipped to no-slash forms — the rendered internal-href set changed on **54/54 routes** (53 pages + 404) when the new build was diffed against the pre-round build; (2) 0 routes still link any slash-form flip page. The old 2026-11-07 carve-out for /contact/ and /resources/ is gone — both flipped in this round.

---

## Word-diff proof (FINAL — after all removals)

Method: visible words extracted from the rendered HTML of the pre-round build (built fresh from HEAD 7d9cfd7) vs the FINAL build, per route, scripts/styles/JSON-LD stripped, tags stripped, entities unescaped. The pre-round build contained BOTH `<path>/index.html` and `<path>.html` for the 23 old no-slash routes, so the comparison dedupes to one file per route (flat `.html` preferred — same content). The 404 page is excluded from the 53-route count (429 words).

| Measure | Before (HEAD) | After (final) |
|---|---|---|
| Routes compared | 53 | 53 |
| Total visible words | 96,903 | **96,471** |
| Words added | — | **0** |
| Words removed | — | **432** (all ordered removals, §Point 13) |
| Routes with any word diff | — | **46** (every delta matches a §Point 13 removal on that page) |

Per-round breakdown (whitespace-token counts; see tokenization note): first "Full details" round (8 spots) 31 words; sweep #1 (62 net locations) 211 words; sweep #2 (72 locations) 190 words. Total **142 locations, 432 words**. Tokenization note: the word counter is the regex `[A-Za-z0-9][A-Za-z0-9'\u2019\-]*` — the stray "." in the sewage phrase counts 0 words, and "bursts:For" (burst-pipe block 31, two links joined by `<br>`) counts 2 words; those two effects offset exactly, so the measured −432 equals the logged 432.

Per-route deltas (largest): homepage −44, emergency −36, /services −23, burst-pipe −23, water-mitigation −18, water-heater −17, ceiling −16, glenpool −15, mold −14, hardwood −13, flooded-basement −12, storm −12, skiatook −12, mold-after −12. Every other changed route's delta equals the sum of its §Point 13 removals; 7 routes unchanged (0 removals): /commercial, /resources, /resources/how-long-does-water-damage-take-to-dry, /resources/water-damage-vs-flood-damage-insurance-oklahoma, /service-areas/cherry-street-tulsa, /service-areas/midtown-tulsa, /services/fire-damage-restoration. `content/pages.json` — besides the 432 removed words, the only other changes are the URL-form strings (flip) and the 5 zero-word punctuation fixes (§Point 13); `wordCount`/`h1`/`metaTitle`/`metaDescription` fields are otherwise identical.

## Pass 1 results (full audit + fixes)

Static audit (`tools/audit_noslash.py`, `qa-noslash-round/pass1.json`): **PROBLEMS 0**.

- Canonical 200 direct: **53/53**; canonical == og:url == sitemap loc on all 53.
- Internal link fetches: **2,709 × 200**, 108 home-anchor refs, 0 broken; nested anchors 0; body self-links 0; orphans 0 (reachable from home 53/53).
- H1: static 1×53/53, doc-verbatim; rendered-visible on the 4 CWV pages, desktop + mobile.
- JSON-LD (parsed): WebSite 53, BreadcrumbList 53, HomeAndConstructionBusiness 53, WebPage 53, FAQPage 51, Service 18, Article 10; **FAQ 222/222 verbatim** (question + answer text vs pages.json); 0 trailing-slash URL values in any node.
- Sitemap 53 locs (== canonical set), lastmod 53× 2026-11-08; robots.txt 23 User-agent lines (wildcard + 22 AI groups); llms.txt 53 links (== canonical set) + NAP.
- Titles >60ch: **52/53** (report only — U5); descriptions >160ch: **23/53** (report only — U5).
- Images: 246 img tags / 71 distinct srcs, 0 missing alt; 53 distinct hero files, 0 reused across pages; 0 EXIF; 0 AI strings.
- See-cuts re-verified (`tools/verify_see_cuts.py`): dangling "See and" **0**; the 240 cuts from the last round STAY cut. One dangling-"see" hit is the known benign survivor (burst-pipe block 16, real sentence "…what you can see.") — NOT a cut, NOT a defect.
- Repeats (`tools/audit_repeats.py`, `qa-noslash-round/repeats-pass1.txt`): duplicate card hrefs 0, duplicate H2s 0, duplicate images on one page 0. Section C (card+plain overlap): 2 pages — homepage (14 targets) and Collinsville (mold-remediation). Section E (plain href 2+ times): 33 pages, dominated by `tel:` CTAs plus the documented excluded-page pairs. Both sections are **identical to the pre-round build** (same lists, modulo URL form) — pre-existing site design, not a regression (see §Repeats).
- CWV + screenshots (`tools/cwv_shots.py`, `qa-noslash-round/cwv-pass1.json`): worst LCP **800 ms** (mobile homepage; budget 1,800), CLS **0.0000** on all 8 views, mobile transfer max **649.0 KB** (budget 800; desktop homepage 2,096.2 KB — the budget is mobile-only), horizontal overflow **0 px** everywhere, H1 visible on all 8 views. Screenshots viewed by pixels: homepage, services hub, contact, commercial — desktop + mobile — all render correctly; commercial hero/H1 visible (the last round's gap blunder is gone).
- Independent cross-check (`tools/verify_site.py`, updated, run against the audit server; `FINDINGS-round1.md` restored from git afterwards): 53 pages, **2,316 link fetches all 200**, reachable 54/53 (the +1 is a non-page node in its BFS, not a page), **PROBLEMS 0**.

### Fixes made during Pass 1

1. **llms.txt prefix corruption (caught before build):** the first flip pass used plain substring replacement on `https://…com/services/` etc., which corrupted child URLs (`…com/servicesemergency-water-damage-restoration`, `…com/resourceswater-damage-…`). Restored from the pre-round copy and re-did it with exact-URL matching (URL followed by `)` / whitespace / end-of-line). Final: exactly 29 links flipped, 53 links total, 0 corrupted. The `pages.json` / JS flips used exact quoted-string matches and were NOT affected (verified: 0 old exact refs remain).
2. **Audit's own false positives (fixed in the tool, not the site):** (a) body self-link detector never reset its content-block flag, so header/footer links counted as body links — fixed with depth-tracked scoping; (b) slash-variant and vercel-coverage checks were scoped to all 52 pages instead of the 29 flipped — fixed; (c) robots expectation corrected to 23 User-agent lines (wildcard + 22 AI groups; HEAD itself has 23).
3. **audit_repeats.py latent bug:** its sitemap regex omitted `www.` (`https://tulsawaterdamagerepair.com`), so it matched **0 routes** — every earlier run of that tool was a vacuous pass. Fixed the regex; it now reads 53 routes. All "0 repeats" claims from this round are from the FIXED tool (and the before/after comparison above).
4. **Audit server 404 on the page JS chunk:** browsers request `/_next/static/chunks/app/%5B%5B...slug%5D%5D/page-….js` percent-encoded while the file on disk has literal brackets — the server looked the encoded name up and 404'd, so page JS didn't hydrate locally (SSR HTML unaffected). Fixed with `unquote()` on the request path (what real static hosts do). Re-ran the affected measurements after the fix (see Pass 2).

---

## Pass 2 results (FRESH re-audit from scratch — fresh rebuild, re-measured everything)

Static audit (`qa-noslash-round/pass2.json`): **PROBLEMS 0**. Counts **identical** to Pass 1 (`pass1 counts == pass2 counts: True`): canonical 53/53, links 2,709 × 200, FAQ 222, LD types identical, sitemap 53, robots 23, llms 53, titles >60: 52, descriptions >160: 23, reachable 53/53, vercel redirects 29, heroes 53 distinct / 0 reused.

- See-cuts: identical to Pass 1 ("See and" 0; 1 benign "see" survivor; 1 bare `<a>and</a>` — the open water-heater item, untouched).
- Repeats: `repeats-pass2.txt` **byte-identical to pass1** (`diff` clean).
- H1 sweep (`tools/h1_sweep.py`, `qa-noslash-round/h1-pass2.json`): **53/53 H1 1× + visible + doc-verbatim + 0 horizontal overflow**; 0 pages without a hero image. First sweep run reported south-tulsa H1 count 0 — investigated, not a defect: the static HTML has exactly one `<h1>`, and 3/3 isolated re-loads showed H1 present and correct; the first run's evaluate hit an empty DOM (transient flake, before the server unquote fix). Re-ran the full sweep after the fix: 53/53.
- CWV + screenshots (`qa-noslash-round/cwv-pass2.json`): worst LCP **936 ms** (mobile homepage), CLS **0.0000** everywhere, mobile transfer max **652.8 KB** (home 652.8, services 604.8, contact 570.7, commercial 603.7), overflow 0 px, H1 visible on all 8 views. Pass 2 screenshots (home desktop, commercial mobile spot-viewed by pixels) match Pass 1.
- Word-diff re-run on the fresh build: **0 routes differ, 96,903 = 96,903 words**.
- Prefix check re-run on the fresh build: 54 html + 1 css, 0 double-slash, 12,589 refs.

---


## Final audit (pass-final2 — after ALL removals, fresh rebuild, full re-measure)

Static audit (`tools/audit_noslash.py`, `qa-noslash-round/pass-final2.json`): **PROBLEMS 0**.

- Canonical 200 direct: **53/53**; canonical == og:url == sitemap loc on all 53.
- Internal link fetches: **2,618 × 200** + 108 home-anchor refs, 0 broken; nested anchors 0; body self-links 0; orphans 0 (reachable from home 53/53); per-page problems 0/53.
- H1: static 1×53/53; rendered sweep (`tools/h1_sweep.py`, `qa-noslash-round/h1-final2.json`): **53/53 H1 1× + visible + doc-verbatim + 0 horizontal overflow**; 0 pages without a hero image.
- JSON-LD (parsed): WebSite 53, BreadcrumbList 53, HomeAndConstructionBusiness 53, WebPage 53, FAQPage 51, Service 18, Article 10; **FAQ 222/222 verbatim**; 0 trailing-slash URL values in any node.
- Sitemap 53 locs (== canonical set), lastmod 53× 2026-11-08; robots.txt 23 User-agent lines; llms.txt 53 links (== canonical set) + NAP.
- Titles >60ch: **52/53** (report only — U5); descriptions >160ch: **23/53** (report only — U5).
- Images: 246 img tags / 71 distinct srcs, 0 missing alt; 53 distinct hero files, 0 reused; 0 EXIF; 0 AI strings.
- See-cuts re-verified: dangling "See and" **0**; bare `<a>and</a>` **0** (the water-heater item is GONE — cut by his decision, §Point 13); 1 dangling-"see" hit remains, the known benign survivor (burst-pipe block 16, real sentence "…what you can see."). Collinsville offer items with hrefs 5/5.
- Repeats (`qa-noslash-round/repeats-final2.txt`): the diff vs `repeats-pass1.txt` is EXACTLY 3 lines, all from the removals — homepage card+plain overlap drops `/services/burst-pipe-water-damage` + `/services/water-mitigation`; homepage plain-href repeats drop `/resources/water-damage-categories-and-classes-explained` + `/services/water-mitigation`; contact plain-href repeats drop `/resources/how-to-file-water-damage-insurance-claim-tulsa`. No new repeats introduced anywhere.
- CWV + screenshots (`tools/cwv_shots.py`, `qa-noslash-round/cwv-final2.json`, `shots-final2/`): worst LCP **832 ms** (budget 1,800), CLS **0.0000** everywhere, mobile transfer max **650.4 KB** (home 650.4, services 602.9, contact 568.7, commercial 602.5; budget 800), overflow 0 px, H1 visible on all 8 views.
- **Link-count reconciliation (2,709 → 2,618 = −85):** point 13 removed **87 link instances** (64 in sweep #1 + 23 in sweep #2). The audit counts UNIQUE body-link targets per page, and 2 removed links shared their target with another removed link on the same page — homepage faq/5 + block/47 both → categories page; contact block/21 + faq/2 both → how-to-file page. 87 instances − 2 duplicate targets = **85, exactly the measured drop**. Per-page drops (body_links, pass-final → pass-final2) sum to 85 and match the removal log page by page (largest: burst-pipe 14→7, homepage 41→38, emergency 8→4, water-mitigation 12→8, flooded-basement 7→3, cost-tulsa 4→1).
- **Removed targets stay reachable:** every removed link's target still has inbound links in the rendered site (resource pages: 2 inbound each via the resources hub + remaining body links; service pages: 126–218 inbound each). No orphaned target.
- **Quality-bar extras (final build):** og:image + twitter:image on all 53 pages are canonical-domain absolute URLs and every one resolves to a file in `out/` (0 missing); exact slash-form URL strings for all 29 flipped pages: **0** in `out/` (href check + absolute-URL check); `?v=` occurrences in `out/`: **0**; favicon/icon `<link>` present on all 54 HTML files in `out/` (53 pages + 404); `out/` file list verified: 52 flat `.html` + homepage `index.html` + `404.html`, no stale files.
- Prefix check re-run on the final build: 54 html + 1 css, 0 double-slash, 12,397 refs (down from 12,589 — the removed links), 0 prefixed slash-form hrefs.

## Repeats — scope note (why sections C/E are not "failures")

`audit_repeats.py` sections C (same href as both a card link and a plain body link) and E (plain href linked 2+ times) are **report-only by the tool's own design**, and the live-audit record (`FINDINGS-live-audit-a2z.md`) already scopes them: homepage/about-us/contact are excluded pages whose repeats are the doc's own links plus the site's card grids by design ("In-scope pages: 0 repeats"). This round verified the claim instead of trusting it: the section C/E output is **byte-identical between the pre-round build and the post-flip build** (only URL forms differ). Removing any of those links would cut doc content or navigation — both forbidden by the standing rules. The `tel:+19183959320` repeats in section E are phone CTAs, not page links. In-scope repeats: **0**.

---


## Point 12 — Heavier classic favicon + header logo (same mark)

His orders (2026-11-08 ~17:45/17:46): when everything is done, put a very heavy/bold CLASSIC favicon; the small header icon gets the SAME heavier classic mark (navy tile + wordmark unchanged) so header and favicon match. Design kept classic: flat cream tile + flat cyan drop #00BFFF + white dot, NO gradients/glow/sheen. Same drop, heavier — NOT a new mark.

**Decision — Heavy A (0.62):** three candidates rendered in `/tmp/favicon-candidates/` (current-056, heavy-062, heavy-066) and compared at native 16/32/48 on white/grey/navy + 8× zoom. Heavy B (0.66) REJECTED — the drop touched the tile top AND bottom edges, cramped. A 16px w10/t1.0 variant REJECTED — the round bottom merged flat into the tile's bottom edge. Chosen: 0.62 width, top 0.08S (32px+); 16px hand-tune w=10.0, top=0.5 (apex near top edge, bottom margin ~1.3px). White dot scales with the drop (r = 0.131w); 16px keeps no dot (a 1px speck reads as dirt — classic rule).

**Applied:** `tools/make_favicon.py` updated (docstring records the round-4 heavy geometry + rejections) and re-run — all 9 assets regenerated: `favicon-master.png`, `favicon-512x512.png`, `favicon-512x512-maskable.png` (drop at 78% scale for the safe zone), `favicon-192x192.png`, `apple-touch-icon.png` (180), `favicon-48x48.png`, `favicon-32x32.png`, `favicon-16x16.png`, `favicon.ico` (16/32/48, 32bpp). Before-files snapshot kept in `site/qa-noslash-round/favicon-before/`. References: `app/layout.js` icons (favicon.ico, 32, 16, apple-touch-icon), `manifest: '/site.webmanifest'`, `themeColor: '#073B66'`; `public/site.webmanifest` declares the 192/512/maskable icons.

**Header:** `app/components/Header.jsx` SVG updated ONLY (navy tile + wordmark unchanged): old path `M12 2.5c0 0-6.5 7.6-6.5 12a6.5 6.5 0 0 0 13 0c0-4.4-6.5-12-6.5-12Z`, circle cx 9.4 cy 15.2 r 1.7 → new path `M12 1.9c0 0-7.4 8.7-7.4 13.7a7.4 7.4 0 0 0 14.9 0c0-5-7.4-13.7-7.4-13.7Z`, circle cx 9.0 cy 16.4 r 1.95. Only place the brand-mark SVG exists (grep confirmed; `.brand-mark` is a 2.5rem navy tile, SVG 1.35rem, `app/globals.css` lines 106–107).

**Verification (final build, viewed by pixels):**
- Measured cyan coverage, same classifier before/after: 16px 56.2% → **60.8%**, 32px 30.0% → **36.9%**, 48px 29.6% → **36.6%**, apple-touch 29.6% → **36.3%** — heavier at every size.
- Rendered comparison (`qa-noslash-round/favicon-compare.png`): before vs now at native 16/32/48 on white, 8× zoom (pixelated), simulated browser tab, and on navy. NOW is visibly bolder at all sizes — drop fills more of the tile, apex nearer the top — and still a clean, crisp drop at 16px (no blur, no cramping, no merged edges).
- Header (`qa-noslash-round/header-*.png`): desktop top, desktop sticky (scrolled 800px), mobile top (390px), mobile menu open (the menu is a `<details>/<summary>`, not a button). The heavier drop is crisp and bold in the navy tile at all states; wordmark, nav, emergency button, menu list and sticky call bar unchanged.
- **NOT verified:** a real browser tab-bar render (desktop + mobile) needs a live browser — a subagent cannot operate one. The simulated tab above is the closest local check. Post-push, confirm the new mark shows in a real tab (hard-refresh if the old one is cached).


## Point 13 — Dangling link-phrase removals (142 locations, 432 words)

His orders, one by one (screenshots + URLs), 2026-11-08 17:48–18:00: remove the dangling "see more" link phrase at the end of a paragraph — "Full details on how we handle this:" (homepage), "Full details on our page." (Step 5 Structural drying), bare "Full details:" (emergency Burst or frozen pipes; storm Step 5 Dry the structure), "Full breakdown:" (flood The gap), "Full category and class breakdown:" (water-mitigation), "Full drying details:" + stray " ." (sewage Structural drying and rebuild), "Full drying process:" (burst-pipe Structural drying; ceiling 5. Dry the cavity — same phrase, different page), "Related services: and" (water-heater block 32 — BOTH links; this resolves the open report-only item), "Full cost guide:" (AC drain, below the cost table), "Detailed guide:" (hardwood, below the Floor-likely-needs-replacement bullets). The flood "Full breakdown:" order was repeated in the same message as the water-mitigation order — it is the SAME instance, done once, confirmed once here.

**Sweep:** the family broadened twice by his pattern — first to ANY paragraph/block ENDING in a dangling "Full …" link phrase, then to ANY dangling "see more" phrase standing alone (paragraph end OR mid-paragraph, linked OR plain): "Full …" variants, "Detailed guide:", "<X> guide:", "<X> details:", "<X> breakdown:", "See:", "More:". Two scripted sweeps (`/tmp/full_sweep.py`, `/tmp/full_sweep2.py` — parsed-JSON edits, raw-text-safe: `json.dumps(indent=2, ensure_ascii=False)`, no trailing newline, round-trip verified byte-identical before editing). Every cut asserted: the removed tail starts with the phrase, the remaining text ends with a real sentence period, no doubled periods, no double spaces, no orphan colons; FAQ cuts applied to BOTH `a_html` (visible) and `a_text` (schema) and asserted to match.

**Correction found and fixed during sweep #1:** the first sweep wrongly removed the plain-text "Full checklist:" from Claremore FAQ 1 (its only link is the phone number elsewhere in the answer — the phrase itself is plain). Caught by the post-sweep audit against the pre-sweep backup, restored byte-identically from the backup, then re-removed properly in sweep #2 under the broadened (linked-or-plain) rule. The removal table below is the FINAL state (the corrected claremore removal appears once, in sweep #2).

**Named-instance confirmations (all verified 0 in source + rendered build):** "Full details on how we handle this:" 0; "Full details on our page." 0; "Full drying details:" 0; "Full drying process:" 0 (both pages); "Full breakdown:" 0; "Full category and class breakdown:" 0; "Related services: and" 0; "Detailed guide:" 0; "Full cost guide:" 0; "Full checklist:" 0; "See our insurance claim guide:" 0; "Walk through the full process:" 0; "More:" 0; "See:" 0; `</a> .` 0. Burst-pipe block 16 ("…what you can see.") untouched — real sentence, no "Full" in it. Storm block 23 and ceiling block 33 were already removed by the earlier sweeps when their explicit orders arrived — confirmed done, not done twice.

**Punctuation fixes found by the sweep (0 words):** space before a sentence period after a linked area name — commercial block 7 ("Jenks ."), burst-pipe block 43 ("and Sand Springs .", block end), about-us block 28 ("Bixby ."), water-heater block 22 ("Bixby ."), /commercial block 21 ("Glenpool .", block end). The 91 `</a> ,` occurrences ("Owasso</a> , Bixby") were DELIBERATELY LEFT — that is the doc's systematic verbatim list style, not a typo; fixing 2 of 91 would be wrong.

**Keeps (9, by name):**
- Table cells (table data, not dangling pointers): water-mitigation "Full disinfection", ceiling "Full removal per Category 3 protocols", flooded-basement "Full structural disinfection with EPA-registered products." (a full sentence inside a table cell).
- Real sentences, mid-text: categories-and-classes block 15 ("Full personal protective equipment is required: Tyvek suits, chemical-resistant gloves, sealed goggles and N95/P100 respirators. Containment prevents cross-contamination…").
- Lead-ins whose content FOLLOWS in the next block (not dangling): flooded-basement block 6 "Event-driven flooding:" + block 12 "Chronic crawlspace moisture:" (bolded subsection labels introducing the following paragraphs); cost-tulsa block 49 "Here's how to get an accurate figure for your specific situation:" (introduces the call paragraph); mold-after block 6 "Here's the timeline that applies across the restoration industry…" (introduces the 0–24h timeline). Every other remaining ":" ending in the site is a lead-in to a following LIST or TABLE (verified: all 60+ remaining colon-endings have next=LIST/TABLE except the 4 above + the flagged FAQ).
- Water-mitigation FAQ 4 — KEPT + FLAGGED (see §Open items): Q "What questions should I ask a mitigation company?", A is ONLY "Ask these five questions before signing any agreement:" — the whole answer is the pointer; cutting it would empty the FAQ. Needs his call (supply the five questions, or delete the FAQ).

**Full removal table** (generated by plain-text diffing the staged snapshots: HEAD → before-sweep1 → before-sweep2 → final; FAQ rows count a_html + a_text as ONE location; "before" shows the removed phrase, "after" shows what the text now ends with):

## A:HEAD -> B:before-sweep1: 8 locations, 31 words
| / | block (tail) | Full details on how we handle this: | 7 |
| / | block (tail) | Full details on our page. | 5 |
| / | faq (a_html + a_text) | Full details: | 2 |
| /services/emergency-water-damage-restoration | block (tail) | Full details: | 2 |
| /services/emergency-water-damage-restoration | block (tail) | Full details on the drying process: | 6 |
| /services/emergency-water-damage-restoration | faq (a_html + a_text) | Full details: | 2 |
| /services/flood-damage-restoration | block (tail) | Full details on basement-specific cleanup: | 5 |
| /services/storm-damage-repair | block (tail) | Full details: | 2 |

## B:before-sweep1 -> C:before-sweep2: 62 locations, 211 regex words (212 whitespace-tokens; the stray "." in the sewage phrase counts 0)
| / | block (whole removed) | Full guide to categories and classes: | 6 |
| / | block (whole removed) | Full checklist: | 2 |
| / | faq (a_html + a_text) | Full breakdown with cost ranges by category and material: | 9 |
| / | faq (a_html + a_text) | Full guide: | 2 |
| /services/emergency-water-damage-restoration | block (whole removed) | Full category and class guide: | 5 |
| /services/emergency-water-damage-restoration | block (tail) | Full cost breakdown by material and category: | 7 |
| /services/water-mitigation | block (whole removed) | Full category and class breakdown: | 5 |
| /services/water-mitigation | block (tail) | Full claim guide: | 3 |
| /services/water-mitigation | faq (a_html + a_text) | Full insurance guide: | 3 |
| /services/flood-damage-restoration | block (whole removed) | Full breakdown: | 2 |
| /services/mold-remediation | block (whole removed) | Full cost guide: | 3 |
| /services/commercial-water-damage | block (whole removed) | Full claim process: | 3 |
| /service-areas/claremore-ok | block (whole removed) | Full step-by-step checklist: | 3 |
| /service-areas/claremore-ok | faq (a_html + a_text) | Full guide: | 2 |
| /service-areas/claremore-ok | faq (a_html + a_text) | Full cost breakdown: | 3 |
| /service-areas/owasso-ok | faq (a_html + a_text) | Full prevention checklist: | 3 |
| /service-areas/owasso-ok | faq (a_html + a_text) | Full cost breakdown: | 3 |
| /service-areas/jenks-ok | block (whole removed) | Full insurance guide: | 3 |
| /service-areas/jenks-ok | faq (a_html + a_text) | Full cost guide: | 3 |
| /services/flooded-basement-cleanup | block (whole removed) | Full category and class guide: | 5 |
| /services/flooded-basement-cleanup | faq (a_html + a_text) | Full guide: | 2 |
| /resources/water-damage-restoration-cost-tulsa | block (whole removed) | Full insurance guide: Step-by-step claim walkthrough: | 6 |
| /services/storm-damage-repair | block (tail) | Full cost guide: | 3 |
| /services/storm-damage-repair | faq (a_html + a_text) | Full guide: | 2 |
| /services/burst-pipe-water-damage | block (tail) | Full drying process: | 3 |
| /services/burst-pipe-water-damage | block (whole removed) | Full prevention checklist: | 3 |
| /services/burst-pipe-water-damage | block (tail) | Full cost guide: | 3 |
| /services/sewage-backup-cleanup | block (mid) | Full drying details: . | 3 |
| /services/sewage-backup-cleanup | block (tail) | Full cost guide: | 3 |
| /services/sewage-backup-cleanup | faq (a_html + a_text) | Full guide: | 2 |
| /services/ceiling-water-damage | block (tail) | Full drying process: | 3 |
| /services/hardwood-floor-drying | block (whole removed) | Full cost guide: | 3 |
| /service-areas/glenpool-ok | block (tail) | Full cost breakdown with ranges by category and material: | 9 |
| /service-areas/glenpool-ok | faq (a_html + a_text) | Full prevention tips for winter: | 5 |
| /service-areas/bixby-ok | block (whole removed) | Full insurance guide: | 3 |
| /service-areas/bixby-ok | faq (a_html + a_text) | Full cost guide: | 3 |
| /service-areas/broken-arrow-ok | block (whole removed) | Full cost breakdown: | 3 |
| /service-areas/broken-arrow-ok | faq (a_html + a_text) | Full prevention checklist: | 3 |
| /service-areas/sand-springs-ok | block (whole removed) | Full cost guide: | 3 |
| /resources/mold-after-water-damage-tulsa | block (tail) | Full cost guide: | 3 |
| /service-areas/skiatook-ok | block (whole removed) | Full prevention checklist for freezing: | 5 |
| /service-areas/skiatook-ok | block (whole removed) | Full cost guide: | 3 |
| /service-areas/coweta-ok | block (whole removed) | Full cost guide: | 3 |
| /service-areas/coweta-ok | item (tail) | Full checklist: | 2 |
| /service-areas/sapulpa-ok | faq (a_html + a_text) | Full cost guide: | 3 |
| /contact | block (whole removed) | Full step-by-step checklist: | 3 |
| /resources/how-to-file-water-damage-insurance-claim-tulsa | block (whole removed) | Full insurance breakdown: | 3 |
| /resources/first-24-hours-after-water-damage | block (tail) | Full claim guide: | 3 |
| /service-areas/brookside-tulsa | block (whole removed) | Full cost guide: | 3 |
| /service-areas/south-tulsa | faq (a_html + a_text) | Full cost guide: | 3 |
| /service-areas/west-tulsa | block (tail) | Full guide: | 2 |
| /service-areas/north-tulsa | faq (a_html + a_text) | Full cost guide: | 3 |
| /services/ac-drain-line-overflow-cleanup | block (whole removed) | Full cost guide: | 3 |
| /services/appliance-leak-water-damage | block (whole removed) | Full cost guide: | 3 |
| /services/water-heater-leak-cleanup | block (whole removed) | Related services: and | 3 |
| /services/water-heater-leak-cleanup | block (tail) | Full cost guide: | 3 |
| /services/roof-leak-water-damage | block (tail) | Full cost guide: | 3 |
| /services/slab-leak-water-damage | block (tail) | Full cost guide: | 3 |
| /service-areas/east-tulsa | block (whole removed) | Full cost guide: | 3 |
| /services/smoke-soot-damage-cleanup | block (whole removed) | Full fire damage restoration process: | 5 |
| /resources/how-to-prevent-frozen-pipes-tulsa | block (whole removed) | Full cost guide: | 3 |
| /resources/how-to-prevent-frozen-pipes-tulsa | faq (a_html + a_text) | Full step-by-step checklist: | 3 |

## C:before-sweep2 -> D:final: 72 locations, 190 words (+ 5 punctuation fixes, 0 words, listed separately below)
| / | block (tail) | See our insurance claim guide: | 5 |
| / | faq (a_html + a_text) | See the full drying timeline guide: | 6 |
| /services | block (tail) | Learn more about the mitigation phase: | 6 |
| /services | block (whole removed) | Walk through the full process: | 5 |
| /services | faq (a_html + a_text) | Full details on how we structure mitigation: | 7 |
| /services | faq (a_html + a_text) | Our step-by-step insurance claim guide: | 5 |
| /services/emergency-water-damage-restoration | block (whole removed) | Step-by-step insurance claim walkthrough: | 4 |
| /services/emergency-water-damage-restoration | block (tail) | More on the mold-after-water-damage timeline: | 5 |
| /services/emergency-water-damage-restoration | faq (a_html + a_text) | Our step-by-step guide: | 3 |
| /services/emergency-water-damage-restoration | faq (a_html + a_text) | Full breakdown: | 2 |
| /services/water-mitigation | block (tail) | Category and class details: | 4 |
| /services/water-mitigation | faq (a_html + a_text) | Detailed timeline guide: | 3 |
| /services/flood-damage-restoration | faq (a_html + a_text) | Timeline details: | 2 |
| /services/mold-remediation | block (whole removed) | More warning signs and what they mean: | 7 |
| /services/mold-remediation | block (whole removed) | Explained in detail: | 3 |
| /services/mold-remediation | faq (a_html + a_text) | See: | 1 |
| /service-areas/claremore-ok | faq (a_html + a_text) | Full checklist: | 2 |
| /service-areas/owasso-ok | block (whole removed) | Full checklist: | 2 |
| /service-areas/owasso-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/jenks-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/jenks-ok | faq (a_html + a_text) | See: | 1 |
| /services/flooded-basement-cleanup | block (whole removed) | Detailed timeline guide: | 3 |
| /services/flooded-basement-cleanup | block (whole removed) | Claim walkthrough: | 2 |
| /resources/water-damage-restoration-cost-tulsa | block (whole removed) | Detailed mitigation process: | 3 |
| /services/storm-damage-repair | block (tail) | More on finding hidden damage: | 5 |
| /services/burst-pipe-water-damage | block (tail) | Claim guide: | 2 |
| /services/burst-pipe-water-damage | block (whole removed) | For ceiling damage from attic bursts:For hardwood floors: | 8 |
| /services/burst-pipe-water-damage | faq (a_html + a_text) | See: | 1 |
| /services/burst-pipe-water-damage | faq (a_html + a_text) | Timeline guide: | 2 |
| /services/ceiling-water-damage | block (whole removed) | More diagnostic guidance: | 3 |
| /services/ceiling-water-damage | block (whole removed) | More detail on when drywall can be saved: | 8 |
| /services/ceiling-water-damage | block (whole removed) | More: | 1 |
| /services/ceiling-water-damage | faq (a_html + a_text) | See: | 1 |
| /services/hardwood-floor-drying | block (whole removed) | More detail on these stages: | 5 |
| /services/hardwood-floor-drying | block (whole removed) | Detailed guide: | 2 |
| /services/hardwood-floor-drying | faq (a_html + a_text) | Timeline guide: | 2 |
| /services/hardwood-floor-drying | faq (a_html + a_text) | See: | 1 |
| /service-areas/glenpool-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/bixby-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/broken-arrow-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/sand-springs-ok | faq (a_html + a_text) | See: | 1 |
| /resources/mold-after-water-damage-tulsa | block (whole removed) | More indicators: | 2 |
| /resources/mold-after-water-damage-tulsa | block (whole removed) | Drying timeline for different materials: | 5 |
| /resources/mold-after-water-damage-tulsa | faq (a_html + a_text) | See: | 1 |
| /resources/mold-after-water-damage-tulsa | faq (a_html + a_text) | See: | 1 |
| /service-areas/skiatook-ok | faq (a_html + a_text) | Full prevention checklist: | 3 |
| /service-areas/skiatook-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/coweta-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/catoosa-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/collinsville-ok | faq (a_html + a_text) | See: | 1 |
| /service-areas/sapulpa-ok | faq (a_html + a_text) | More: | 1 |
| /service-areas/sapulpa-ok | faq (a_html + a_text) | See: | 1 |
| /about-us | block (whole removed) | See the full services directory: | 5 |
| /contact | block (tail) | Claim guide: | 2 |
| /contact | faq (a_html + a_text) | Step-by-step claim guide: | 3 |
| /resources/first-24-hours-after-water-damage | faq (a_html + a_text) | Timeline guide: | 2 |
| /service-areas/south-tulsa | faq (a_html + a_text) | See: | 1 |
| /service-areas/west-tulsa | faq (a_html + a_text) | See: | 1 |
| /service-areas/north-tulsa | faq (a_html + a_text) | See: | 1 |
| /services/ac-drain-line-overflow-cleanup | faq (a_html + a_text) | See: | 1 |
| /services/appliance-leak-water-damage | faq (a_html + a_text) | See: | 1 |
| /services/water-heater-leak-cleanup | faq (a_html + a_text) | See: | 1 |
| /services/water-heater-leak-cleanup | faq (a_html + a_text) | See the cost table above and the full cost guide: | 10 |
| /services/roof-leak-water-damage | faq (a_html + a_text) | See: | 1 |
| /services/slab-leak-water-damage | block (whole removed) | Timeline guide: | 2 |
| /services/slab-leak-water-damage | faq (a_html + a_text) | See: | 1 |
| /resources/oklahoma-water-damage-insurance-guide | block (tail) | See . Step-by-step claim filing process: | 6 |
| /service-areas/east-tulsa | faq (a_html + a_text) | See: | 1 |
| /services/smoke-soot-damage-cleanup | faq (a_html + a_text) | See: | 1 |
| /resources/how-to-prevent-frozen-pipes-tulsa | faq (a_html + a_text) | See: | 1 |
| /resources/water-damage-categories-and-classes-explained | faq (a_html + a_text) | Detailed timeline: | 2 |
| /resources/signs-of-hidden-water-damage | faq (a_html + a_text) | See: | 1 |

TOTAL: 142 removal locations, 432 regex words (measured word-diff: 96,903 -> 96,471)

**Link-count effect:** 87 link instances removed (64 sweep #1 + 23 sweep #2); unique body-link fetches 2,709 → 2,618 (−85) — reconciled in §Final audit. Removed targets stay reachable (§Final audit).

## Open items (NOT in scope — left untouched, still open)

1. **U5 titles/descriptions (user's wording call):** 52/53 titles >60ch, 23/53 descriptions >160ch. Text verified verbatim vs the doc; nothing rewritten.
2. **Water-heater "Related services: and" — RESOLVED this round (his decision ~17:56, §Point 13):** the whole phrase (BOTH links) was deleted from `/services/water-heater-leak-cleanup/` block 32; the page now ends cleanly at the Documentation paragraph. Verified 0 occurrences; bare `<a>and</a>` count sitewide is now 0.
3. **18px micro-label exceptions:** header `Emergency?` (`app/components/Header.jsx:85`, `<span className="btn-small">`) and brand tagline `Tulsa, Oklahoma` (`Header.jsx:43`, rendered uppercase by CSS) — both present, untouched.
4. **Known benign survivor:** burst-pipe block 16 ends "…what you can see." — a real sentence, not a dangling "see".
5. **Water-mitigation FAQ 4 (NEW — needs his call):** Q "What questions should I ask a mitigation company?" — the whole answer is the dangling pointer "Ask these five questions before signing any agreement:" with no questions following. Left untouched because cutting it would empty the FAQ. His call: supply the five questions, or delete the FAQ.
6. **Post-push live A-to-Z testing (his order ~18:03):** sequence is round → report → push → then test the LIVE site A-to-Z as a world top-level technical SEO expert, 101% (every page, URL, link, canonical, H1, schema, speed, crawl). Token re-pasted (same value, in-window).
7. **Bing API setup (his order ~18:04):** after everything is done, set up the Bing API for the Vercel-hosted site, account noorullahchhachher2@gmail.com. (IndexNow key already live; U2 IndexNow submission still queued on his word.) API key / account access will be needed when the time comes.

---

## Screenshots

Kept in `site/qa-noslash-round/` (gitignored, NOT committed): `shots-pass1/` + `shots-pass2/` + `shots-final2/` — homepage, services hub, contact, commercial, desktop (1440×900) + mobile (390×844), viewport + full-page each. Viewed by pixels in both passes (see §Pass 1/2); final-build shots viewed for the header states (§Point 12). The mobile services eyebrow ("TULSA WATER DAMAGE REPAIR") sits flush to the right edge at 390 px — verified at 2× zoom: the final "R" is fully rendered, not clipped; pre-existing CSS, untouched by this round. The sticky mobile call bar covers the bottom of the viewport (by design — the "Request Emergency Service" button scrolls under it; same as before the round). Favicon/header shots: `favicon-compare.png` (before/now 16/32/48 + 8× zoom + simulated tab + navy), `header-desktop-top.png`, `header-desktop-sticky.png`, `header-mobile-top.png`, `header-mobile-menu.png` — all viewed by pixels (§Point 12).

---

## Post-push live checks (REQUIRED — cannot be verified locally, nothing was pushed)

1. **Slash → 308 → no-slash on Vercel, all 29:** `curl -I https://www.tulsawaterdamagerepair.com/services/` (and each of the 29) must return **308** with `Location: /services` (etc.). The 2 direct conflicts matter most: `/services/` and `/contact/`. Confirm `/services` (no-slash) now serves **200 directly** — the old 308 → /services/ MUST be inverted.
2. **No-slash canonicals 200 direct, no hop:** all 53 canonical URLs (sitemap) return 200 with no redirect; canonical == served URL on each.
3. **Sitemap live:** 53 locs, all no-slash except homepage `/`, all lastmod 2026-11-08.
4. **Spot render:** homepage + /services + /contact + /commercial in a real browser, desktop + mobile (H1 visible, no unstyled flash, no broken images).
5. **Search Console (his action):** the 29 old slash URLs will show as redirected; no action needed unless Google flags the 23 old no-slash pages' slash forms (now 404 — never canonical/linked; add 23 redirects only on his word).
6. **GitHub Pages preview stays as-is (his call to unpublish it himself — agent must NOT touch Pages).** If the preview is ever re-published from this build, note its known limitation: slash forms 404 there (no redirect layer); flat `.html` files serve extensionless URLs fine.
7. **Post-push live A-to-Z testing (his order ~18:03):** after the push, test the LIVE site A-to-Z as a world top-level technical SEO expert, 101% — every page, URL, link, canonical, H1, schema, speed, crawl. The local final audit (§Final audit) is the baseline for that live pass.
8. **Bing API setup (his order ~18:04):** after everything is done, set up the Bing API for the Vercel-hosted site, account noorullahchhachher2@gmail.com — needs API key / account access at that time.

## Files changed (this commit)

Source/config/generated-public + findings only. Screenshots + QA JSONs live in `site/qa-noslash-round/` (gitignored, not committed); `out/` + `.next/` ignored as usual.

- `next.config.js`, `vercel.json` (new), `content/pages.json`, `content/images.json`, `content/images-a.json`, `content/images-b.json`, `app/lib-meta.js`, `app/components/Header.jsx`, `app/components/Footer.jsx`, `app/components/Shared.jsx`, `app/[[...slug]]/page.js`
- `public/sitemap.xml`, `public/llms.txt` (robots.txt unchanged)
- Favicon (point 12): `public/favicon.ico`, `public/favicon-16x16.png`, `public/favicon-32x32.png`, `public/favicon-48x48.png`, `public/favicon-192x192.png`, `public/favicon-512x512.png`, `public/favicon-512x512-maskable.png`, `public/favicon-master.png`, `public/apple-touch-icon.png`; `tools/make_favicon.py` (heavy geometry + rejections documented). `app/components/Header.jsx` SVG is the same heavy drop (already listed above)
- `tools/post_export.js`, `tools/build_sitemap.py`, `tools/audit_noslash.py` (new), `tools/cwv_shots.py` (new), `tools/h1_sweep.py` (new), `tools/audit_repeats.py`, `tools/verify_site.py`, `tools/verify_see_cuts.py`
- `FINDINGS-url-noslash-technical-seo-2x.md` (this file)

---

## Per-page / per-URL evidence appendix (final build, `qa-noslash-round/pass-final2.json`)

| Page | Status | H1 | FAQs | LD types | Slash variant | Body links | Problems |
|---|---|---|---|---|---|---|---|
| / | 200 | 1× Water Damage Restoration in Tulsa, OK  | 6 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 38 | — |
| /about-us | 200 | 1× About Water Damage Restoration Tulsa | 0 | BreadcrumbList,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 24 | — |
| /commercial | 200 | 1× Commercial Restoration Services in Tul | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 11 | — |
| /contact | 200 | 1× Contact Water Damage Restoration Tulsa | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 0 | — |
| /resources | 200 | 1× Water Damage Resources & Guides in Tul | 0 | BreadcrumbList,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 0 | — |
| /resources/first-24-hours-after-water-damage | 200 | 1× What to Do in the First 24 Hours After | 5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 1 | — |
| /resources/how-long-does-water-damage-take-to-dry | 200 | 1× How Long Does Water Damage Take to Dry | 4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 9 | — |
| /resources/how-to-file-water-damage-insurance-claim-tulsa | 200 | 1× How to File a Water Damage Insurance C | 4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 3 | — |
| /resources/how-to-prevent-frozen-pipes-tulsa | 200 | 1× How to Prevent Frozen Pipes in Tulsa,  | 4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 8 | — |
| /resources/mold-after-water-damage-tulsa | 200 | 1× Mold After Water Damage in Tulsa How F | 5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 4 | — |
| /resources/oklahoma-water-damage-insurance-guide | 200 | 1× Does Homeowners Insurance Cover Water  | 5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 9 | — |
| /resources/signs-of-hidden-water-damage | 200 | 1× 10 Signs of Hidden Water Damage in You | 3 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 10 | — |
| /resources/water-damage-categories-and-classes-explained | 200 | 1× Water Damage Categories and Classes Ex | 4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 5 | — |
| /resources/water-damage-restoration-cost-tulsa | 200 | 1× How Much Does Water Damage Restoration | 5 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 1 | — |
| /resources/water-damage-vs-flood-damage-insurance-oklahoma | 200 | 1× Water Damage vs. Flood Damage Insuranc | 4 | Article,BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | — | 4 | — |
| /service-areas/bixby-ok | 200 | 1× Water Damage Restoration in Bixby, OK | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 10 | — |
| /service-areas/broken-arrow-ok | 200 | 1× Water Damage Restoration in Broken Arr | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/brookside-tulsa | 200 | 1× Water Damage Restoration in Brookside, | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 3 | — |
| /service-areas/catoosa-ok | 200 | 1× Water Damage Restoration in Catoosa, O | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 11 | — |
| /service-areas/cherry-street-tulsa | 200 | 1× Water Damage Restoration in Cherry Str | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /service-areas/claremore-ok | 200 | 1× Water Damage Restoration in Claremore, | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/collinsville-ok | 200 | 1× Water Damage Restoration in Collinsvil | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/coweta-ok | 200 | 1× Water Damage Restoration in Coweta, OK | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /service-areas/east-tulsa | 200 | 1× Water Damage Restoration in East Tulsa | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 9 | — |
| /service-areas/glenpool-ok | 200 | 1× Water Damage Restoration in Glenpool,  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /service-areas/jenks-ok | 200 | 1× Water Damage Restoration in Jenks, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/midtown-tulsa | 200 | 1× Water Damage Restoration in Midtown Tu | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/north-tulsa | 200 | 1× Water Damage Restoration in North Tuls | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /service-areas/owasso-ok | 200 | 1× Water Damage Restoration in Owasso, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/sand-springs-ok | 200 | 1× Water Damage Restoration in Sand Sprin | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 7 | — |
| /service-areas/sapulpa-ok | 200 | 1× Water Damage Restoration in Sapulpa, O | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 9 | — |
| /service-areas/skiatook-ok | 200 | 1× Water Damage Restoration in Skiatook,  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /service-areas/south-tulsa | 200 | 1× Water Damage Restoration in South Tuls | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 12 | — |
| /service-areas/west-tulsa | 200 | 1× Water Damage Restoration in West Tulsa | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 8 | — |
| /services | 200 | 1× Water Damage Restoration Services in T | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,WebPage,WebSite | 308 | 21 | — |
| /services/ac-drain-line-overflow-cleanup | 200 | 1× AC Drain Line Overflow Cleanup in Tuls | 3 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 | 6 | — |
| /services/appliance-leak-water-damage | 200 | 1× Appliance Leak Water Damage in Tulsa,  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 | 2 | — |
| /services/burst-pipe-water-damage | 200 | 1× Burst Pipe Water Damage Repair in Tuls | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 7 | — |
| /services/ceiling-water-damage | 200 | 1× Ceiling & Drywall Water Damage Repair  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 6 | — |
| /services/commercial-water-damage | 200 | 1× Commercial Water Damage Restoration in | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 4 | — |
| /services/emergency-water-damage-restoration | 200 | 1× Emergency Water Damage Restoration in  | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 4 | — |
| /services/fire-damage-restoration | 200 | 1× Fire Damage Restoration in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 1 | — |
| /services/flood-damage-restoration | 200 | 1× Flood Damage Restoration in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 2 | — |
| /services/flooded-basement-cleanup | 200 | 1× Flooded Basement & Crawlspace Cleanup  | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 3 | — |
| /services/hardwood-floor-drying | 200 | 1× Hardwood Floor Water Damage & Drying i | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 2 | — |
| /services/mold-remediation | 200 | 1× Mold Remediation in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 6 | — |
| /services/roof-leak-water-damage | 200 | 1× Roof Leak Water Damage Repair in Tulsa | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 | 6 | — |
| /services/sewage-backup-cleanup | 200 | 1× Sewage Backup Cleanup in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 6 | — |
| /services/slab-leak-water-damage | 200 | 1× Slab Leak Water Damage Restoration in  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 | 8 | — |
| /services/smoke-soot-damage-cleanup | 200 | 1× Smoke & Soot Damage Cleanup in Tulsa,  | 4 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 0 | — |
| /services/storm-damage-repair | 200 | 1× Storm Damage Repair in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 9 | — |
| /services/water-heater-leak-cleanup | 200 | 1× Water Heater Leak Cleanup in Tulsa, OK | 3 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | 308 | 3 | — |
| /services/water-mitigation | 200 | 1× Water Mitigation Services in Tulsa, OK | 5 | BreadcrumbList,FAQPage,HomeAndConstructionBusiness,Service,WebPage,WebSite | — | 8 | — |

Totals: 53 pages, all 200; H1 53×1 (all visible + doc-verbatim per the rendered sweep); FAQs 222; body links 382 (audit count); problems 0. Slash variant 308 on all 29 flipped pages; "—" on the 23 previously-no-slash pages + homepage (no slash variant exists).

**Per-URL evidence:** sitemap 53 locs (== canonical set, all lastmod 2026-11-08); llms.txt 53 links (== canonical set, NAP present); vercel.json 29 redirects (slash → no-slash, permanent 308 — table in §Slash → no-slash redirect table); robots.txt 23 User-agent lines (wildcard + 22 AI groups, byte-identical to HEAD). Canonical == og:url == sitemap loc on all 53 pages (audit-verified per page, not assumed).
