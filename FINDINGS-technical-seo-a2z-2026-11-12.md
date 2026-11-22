# TECHNICAL SEO A-TO-Z AUDIT — Tulsa Water Damage Repair
**Date:** 2026-11-12 ~23:15–23:20 PKT | **Site:** https://www.tulsawaterdamagerepair.com (live www) + byte-identical local build
**Scope:** all 53 pages, page by page, eyes open. **Method:** two independent tracks — (1) live HTML audit (live DOM parsing + parsed JSON-LD, never bare grep on built HTML), (2) local render audit (Playwright/Chromium on the identical export served locally). **AUDIT ONLY — no site file changed, no push/deploy, no token.**
**Live state at audit time:** main 3b9b66d (advanced LocalBusiness schema) + a7de4a4 (sitemap MAX). Correct build: `npm run export`.

## VERDICT: PROBLEMS 0 — CLEAN

Every check below passed on all 53 pages. No defect was found. A flagged item in this file would be a real defect with evidence; there are none.

## Headline counts

### 1. URL layer
- Canonical 200 direct (no hop): **53/53**
- Self-canonical: **53/53**
- og:url == canonical: **53/53**
- Slash form 308 → no-slash (52 non-home pages): **52/52** — Location header is RELATIVE (e.g. `/services`), resolving correctly to the no-slash canonical. No vercel.json exists; this is the platform/Next.js `trailingSlash:false` built-in, NOT a configured redirect. No redirect is proposed.

### 2. Meta (verbatim vs pages.json)
- Title verbatim: **53/53**; meta description verbatim: **53/53**
- Titles >60 chars: **52/53**; descriptions >160 chars: **23/53** — REPORT ONLY. U5 is OPEN (verbatim doc wording, his wording call pending). NOT defects; no trims proposed.

### 3. H1
- Exactly 1 per page: **53/53**; verbatim vs doc: **53/53**; VISIBLE in rendered DOM: **53/53** (boundingBox non-null, opacity > 0).

### 4. Headings
- H2 missing (doc blocks + FAQ headings): **0**; H2 unexpected extra (excl. template final-CTA H2 on 53/53 + hub section H2 on /resources): **0**
- FAQ H3 missing: **0**; H3 unexpected extra: **0** (229 template H3s — card titles 175, brand-panel 33, demand-strip 18, phase-cards 2, form-card 1 — are template, not doc content).

### 5. Internal links
- Raw `<a>` instances: **6,777**; body-copy links (content-block, excl. 175 template card/strip/aside links): **386**
- Body self-links: **0**; body links not matching doc annotations: **0**; nested `<a>` inside `<a>`: **0**
- Unique internal targets fetched: **54** — non-200: **0**, slash-form targets: **0**
- Orphans (0 inlinks from another page): **0**; unreachable from homepage: **0**

### 6. Dangling phrases
- **0** across all 14 named phrases + variants + paragraph-end colon sweep: "See and", lone "See.", "Full details:", "Detailed guide:", "Related services: and", and the full "Full details:"-family list from FINDINGS-url-noslash-technical-seo-2x.md. Only benign real sentences containing "see." survive on 2 pages (see Notes).

### 7. FAQ
- Visible **222** = FAQPage schema **222** = source **222** (verbatim, entity-decoded).
- FAQPage present on **51/51** pages with FAQs (the 2 without FAQs — /about-us, /resources — correctly have none).

### 8. Schema (JSON-LD, every page)
- Node types sitewide: WebSite **53**, BreadcrumbList **53**, HomeAndConstructionBusiness **53**, WebPage **53**, FAQPage **51**, Service **18**, Article **10**
- Schema errors: **0** (jsonschema 4.10.3 structural validation + @id resolution — Service provider → #business, WebPage isPartOf → #website — + trailing-slash URL scan + breadcrumb-last == canonical on all 52 non-home pages)
- NEW fields confirmed LIVE: LocalBusiness image/logo/contactPoint **53/53**, hasOfferCatalog homepage-only; Service serviceType/description/areaServed(20)/image **18/18**; WebSite publisher+inLanguage **53/53**; WebPage description+inLanguage+primaryImageOfPage **53/53**

### 9. Images
- `<img>` tags / unique srcs: **246 / 71**; non-200: **0**; missing alt: **0**; EXIF: **0**; AI strings in filenames/alt: **0**
- Distinct heroes (first `<img>`, all 1200×800 actual pixels): **53/53**; reused heroes: **0**
- Hero pixel verdicts (viewed, 12-page sample incl. homepage, 4 services, commercial, 3 areas, 1 guide, about, contact): **12/12 PASS** — topic fit + place fit confirmed by viewed pixels. One marginal crop noted (see Observations, not a defect).

### 10. Sitemap / robots / llms / IndexNow / favicon (live)
- sitemap.xml: **53 locs**, **246 image entries**, **71 unique** image URLs, lastmod **10× 2026-11-12 / 10× 2026-11-07 / 33× 2026-11-08**, XML well-formed, locs == canonicals, sitemap image URLs non-200: **0**
- robots.txt: **Host: 0** (do NOT re-add), Sitemap: line present, **23 UA groups** (wildcard + 22 AI)
- llms.txt: **53 URLs** + NAP present (Markdown-link format — an auditor regex artifact that appended `):` to extracted URLs was confirmed to be extraction-only; the file itself is clean)
- IndexNow key `b52262ce2b2f10b691644dccabf66495.txt`: live **200**, content matches local public/ copy
- Favicons (9 assets): all **200**, all md5-identical to local out/ copies

### 11. Performance (local build, identical to live — localhost, unthrottled)
- Worst LCP desktop: **428 ms** (homepage); worst LCP mobile: **492 ms** (/resources/water-damage-categories-and-classes-explained)
- Worst CLS desktop: **0.0**; worst CLS mobile: **0.0** (0 layout-shift entries on every page, both viewports)
- Max mobile transfer: **1,342.8 KB** (/service-areas/bixby-ok)
- Horizontal overflow: **0 on 53/53 at 390px and 53/53 at 1280px**

### 12. Text size
- Body copy 18px sitewide except headings: confirmed. Sub-18px text beyond the 3 KNOWN exceptions: **none**.
- Known exceptions (his call, confirmed present, NOT re-flagged): header "EMERGENCY?" .btn-small ~11.2px; brand tagline .brand small ~10.88px ("Tulsa, Oklahoma"); check-glyph spans 12px.
- Observation (not a defect): `.footer-col h3` at 12.8px on all 53 pages is a small-caps footer column label — a heading element, exempt from the 18px body-copy rule.

### 13. Content fullness
- EMPTY (<100w) pages: **0**; THIN (100–300w) pages: **0**
- Per-page visible content-block words vs full source words (blocks incl. `ul` items + table rows/headers + FAQ q + a_text): range **−106…+494**, sum −2,688. Worst negative −106 on /resources/water-damage-categories-and-classes-explained (1,167 live vs 1,273 source) — verified sentence-by-sentence: **0 source sentences missing**; the gap is the intro paragraph rendering outside `.content-block` (hero/intro area) plus tokenisation. Homepage +494 is template card titles/blurbs inside `.content-block` (37 cards). /resources is a card-driven hub (source wordCount 8, main-body 508 words) — not empty by design.
- Invented facts found: **0**

### 14. Footer mini-map
- Present on **33/53** pages; omitted on exactly the **19 area pages + /contact** by design — split confirmed.

### 15. Contact form (/contact)
- Pre-submit visible notice: "Emergencies: do not use this form — water keeps spreading while you wait for a reply. Call (918) 395-9320 now."
- Post-submit notice (form replaced, visible): "This form is not connected to an inbox yet. Your message was not sent anywhere. For the fastest help, call (918) 395-9320 — answered 24/7."
- The form **never fakes a send** — submit swaps the form for the honest notice; no success/thank-you wording. (A naive `/sent/` regex hits the notice's own words "was not sent anywhere" — that is the honest text, not a success claim.)

## Observations (NOT defects)

- **Water-mitigation hero crop (marginal):** the photo itself (verified full-size) is a yellow wet/dry vac with hose in a stripped room — on-topic. But the desktop hero band crops it so mostly green wall + doorway show and the vac sits at the right edge (parent re-viewed the screenshot and agrees). Marginal crop, NOT a fail. No action required unless he wants a re-crop.
- **Tables at 390px:** all 54 tables render wider than the viewport (544px vs 348px wrapper) but inside `overflow-x: auto` wrappers — columns reachable by swipe, document overflow stays 0. Standard responsive pattern.
- **`.reveal` scroll-reveal (Pleasant Grove bug class):** 0 in-view elements hidden at first paint (12-page sample, both viewports); slow scroll reveals 100% (home 46/46, water-mitigation 9/9); no `.reveal` element exceeds the never-reveal height limit `(viewport−40px)/0.08` on any page at either viewport; `prefers-reduced-motion` CSS forces opacity 1. No Pleasant-Grove-class bug. A very fast programmatic jump-scroll (600px/120ms) left some below-fold reveals un-triggered in one probe — measurement artifact, not user-facing.
- **Benign "see." survivors (real sentences, not dangling):** /services/burst-pipe-water-damage ("…larger than what you can see.") and /resources/signs-of-hidden-water-damage ("…somewhere you can't see."). No lone "See." anywhere.
- **Template headings (not doc content, not defects):** final-CTA H2 "Water damage right now? Call (918) 395-9320" on 53/53; /resources section H2 "Guides and Cost Information"; 229 template H3s (card titles, sticky-aside brand panel, "Most In-Demand Services in X" strips, phase cards, contact form card). All doc H2s (270 blocks + 51 FAQ-headings) and all 222 FAQ H3s present and verbatim.

## Method notes & limitations (stated plainly)

- **Live HTML track:** all 53 live pages fetched and DOM-parsed (BeautifulSoup) + parsed JSON-LD, never bare grep on built HTML (the Next.js flight payload hides text from greps). Three apparent defect clusters in the first pass (53 jsonschema errors, 252 "invented" links, 229 extra H3s) were traced to auditor-side errors — the schema wrongly required `primaryImageOfPage` to be an object (schema.org allows a URL string), the source-href scan missed `ul` items/table rows, and the H3 scope didn't exclude template card/strip/aside headings. All fixed and re-verified to 0; the final numbers reflect the corrected run.
- **Render track:** local-only. Live Playwright in this VM is blocked by a network tunnel (ERR_TUNNEL_CONNECTION_FAILED) — **no live screenshots were taken or claimed**. All rendering was done against the byte-identical local export on `http://127.0.0.1:8931` via a purpose-written Python server (Vercel-faithful flat-.html routing; `site/tools/serve.py` NOT used — its isdir bug shadows /services + /resources; hubs served 200, unknown paths 404). Server stopped after the audit.
- **LCP/CLS:** localhost, unthrottled, via buffered PerformanceObserver (`performance.getEntriesByType('largest-contentful-paint')` returned nothing in this Chromium build, so the observer method was used for all 53 pages). These are lab numbers, not field data.
- **Footer map tiles:** iframe presence verified in the DOM on 33 pages; tile rendering NOT verified (iframes point at google.com, unreachable from this VM).
- **Google's Rich Results Test / Search Console** is the final word on schema — the local validators (jsonschema + structural + @id resolution) found 0 errors, but nothing here was run through Google's tester.
- **Auditor's tools:** `site/tools/verify_site.py` was NOT run (it overwrites FINDINGS-round1.md). No site file was changed.

## Per-page table (live track)

| slug | canon | title✓ | H1✓ | FAQ vis/sch/src | word Δ (live cb − full source) | defects |
|---|---|---|---|---|---|---|
| / | 200 | ✓ | ✓ | 6/6/6 | +494 | 0 |
| /services | 200 | ✓ | ✓ | 4/4/4 | −63 | 0 |
| /services/emergency-water-damage-restoration | 200 | ✓ | ✓ | 5/5/5 | −68 | 0 |
| /services/water-mitigation | 200 | ✓ | ✓ | 5/5/5 | −64 | 0 |
| /services/flood-damage-restoration | 200 | ✓ | ✓ | 5/5/5 | −82 | 0 |
| /services/mold-remediation | 200 | ✓ | ✓ | 5/5/5 | −86 | 0 |
| /services/commercial-water-damage | 200 | ✓ | ✓ | 5/5/5 | −79 | 0 |
| /service-areas/claremore-ok | 200 | ✓ | ✓ | 5/5/5 | −19 | 0 |
| /service-areas/owasso-ok | 200 | ✓ | ✓ | 5/5/5 | −39 | 0 |
| /service-areas/jenks-ok | 200 | ✓ | ✓ | 5/5/5 | −47 | 0 |
| /services/flooded-basement-cleanup | 200 | ✓ | ✓ | 5/5/5 | −76 | 0 |
| /resources/water-damage-restoration-cost-tulsa | 200 | ✓ | ✓ | 5/5/5 | −75 | 0 |
| /services/storm-damage-repair | 200 | ✓ | ✓ | 5/5/5 | −67 | 0 |
| /services/burst-pipe-water-damage | 200 | ✓ | ✓ | 5/5/5 | −77 | 0 |
| /services/sewage-backup-cleanup | 200 | ✓ | ✓ | 5/5/5 | −63 | 0 |
| /services/ceiling-water-damage | 200 | ✓ | ✓ | 4/4/4 | −64 | 0 |
| /services/hardwood-floor-drying | 200 | ✓ | ✓ | 5/5/5 | −86 | 0 |
| /service-areas/glenpool-ok | 200 | ✓ | ✓ | 4/4/4 | −26 | 0 |
| /service-areas/bixby-ok | 200 | ✓ | ✓ | 4/4/4 | −35 | 0 |
| /service-areas/broken-arrow-ok | 200 | ✓ | ✓ | 5/5/5 | −32 | 0 |
| /service-areas/sand-springs-ok | 200 | ✓ | ✓ | 4/4/4 | −41 | 0 |
| /resources/mold-after-water-damage-tulsa | 200 | ✓ | ✓ | 5/5/5 | −97 | 0 |
| /service-areas/skiatook-ok | 200 | ✓ | ✓ | 4/4/4 | −15 | 0 |
| /service-areas/coweta-ok | 200 | ✓ | ✓ | 4/4/4 | −46 | 0 |
| /service-areas/catoosa-ok | 200 | ✓ | ✓ | 4/4/4 | −39 | 0 |
| /service-areas/collinsville-ok | 200 | ✓ | ✓ | 4/4/4 | −35 | 0 |
| /service-areas/sapulpa-ok | 200 | ✓ | ✓ | 4/4/4 | −28 | 0 |
| /service-areas/midtown-tulsa | 200 | ✓ | ✓ | 4/4/4 | −21 | 0 |
| /about-us | 200 | ✓ | ✓ | 0/0/0 | −57 | 0 |
| /contact | 200 | ✓ | ✓ | 4/4/4 | −15 | 0 |
| /resources/how-to-file-water-damage-insurance-claim-tulsa | 200 | ✓ | ✓ | 4/4/4 | −63 | 0 |
| /resources/first-24-hours-after-water-damage | 200 | ✓ | ✓ | 5/5/5 | −84 | 0 |
| /service-areas/brookside-tulsa | 200 | ✓ | ✓ | 4/4/4 | −76 | 0 |
| /service-areas/south-tulsa | 200 | ✓ | ✓ | 4/4/4 | −14 | 0 |
| /service-areas/west-tulsa | 200 | ✓ | ✓ | 4/4/4 | −47 | 0 |
| /service-areas/north-tulsa | 200 | ✓ | ✓ | 4/4/4 | −44 | 0 |
| /services/ac-drain-line-overflow-cleanup | 200 | ✓ | ✓ | 3/3/3 | −86 | 0 |
| /services/appliance-leak-water-damage | 200 | ✓ | ✓ | 4/4/4 | −88 | 0 |
| /services/water-heater-leak-cleanup | 200 | ✓ | ✓ | 3/3/3 | −74 | 0 |
| /services/roof-leak-water-damage | 200 | ✓ | ✓ | 4/4/4 | −94 | 0 |
| /services/slab-leak-water-damage | 200 | ✓ | ✓ | 4/4/4 | −85 | 0 |
| /resources/oklahoma-water-damage-insurance-guide | 200 | ✓ | ✓ | 5/5/5 | −75 | 0 |
| /service-areas/east-tulsa | 200 | ✓ | ✓ | 4/4/4 | −53 | 0 |
| /services/smoke-soot-damage-cleanup | 200 | ✓ | ✓ | 4/4/4 | −95 | 0 |
| /resources/how-long-does-water-damage-take-to-dry | 200 | ✓ | ✓ | 4/4/4 | −82 | 0 |
| /resources/how-to-prevent-frozen-pipes-tulsa | 200 | ✓ | ✓ | 4/4/4 | −89 | 0 |
| /resources/water-damage-vs-flood-damage-insurance-oklahoma | 200 | ✓ | ✓ | 4/4/4 | −105 | 0 |
| /service-areas/cherry-street-tulsa | 200 | ✓ | ✓ | 4/4/4 | −8 | 0 |
| /commercial | 200 | ✓ | ✓ | 4/4/4 | −87 | 0 |
| /resources/water-damage-categories-and-classes-explained | 200 | ✓ | ✓ | 4/4/4 | −106 | 0 |
| /resources/signs-of-hidden-water-damage | 200 | ✓ | ✓ | 3/3/3 | −82 | 0 |
| /services/fire-damage-restoration | 200 | ✓ | ✓ | 5/5/5 | −94 | 0 |
| /resources | 200 | ✓ | ✓ | 0/0/0 | −9 | 0 |

## Render track (local, per-page)

H1 visible 53/53, overflow 0 at 390px 53/53 and at 1280px 53/53, CLS 0.0 every page both viewports. Worst LCP 428 ms desktop (homepage) / 492 ms mobile (/resources/water-damage-categories-and-classes-explained). Max mobile transfer 1,342.8 KB (/service-areas/bixby-ok). Full per-page render rows in `/tmp/a2z/render-audit.json` (`perf.json`, `render-raw.json`).

## Evidence files

- This file: `site/FINDINGS-technical-seo-a2z-2026-11-12.md`
- Live audit JSON: `/tmp/a2z/live-audit.json` (+ `/tmp/a2z/live-audit-summary.md`, script `/tmp/a2z/live_audit.py`)
- Render audit JSON: `/tmp/a2z/render-audit.json` (+ `/tmp/a2z/render-audit-summary.md`, raw `/tmp/a2z/render-raw.json`, `/tmp/a2z/perf.json`, `/tmp/a2z/reveal-probe.json`)
- Hero screenshots (12 desktop + sticky/contact shots): `/tmp/a2z/shots/`

## Open items (his call, NOT defects)

- **U5** — titles 52/53 >60 chars, descriptions 23/53 >160 chars (verbatim doc). Trim proposal already prepared (~/workspace/your_files/tulsa-repair-titles-descriptions-trimmed.txt); awaiting his choice.
- **18px micro-labels** — header "EMERGENCY?" (~11.2px), brand tagline (~10.88px), check-glyph spans (12px). His call.
- **Water-mitigation hero crop** — marginal desktop crop (vac at right edge); photo itself on-topic. Re-crop only if he wants it.
- **Footer map tiles + Google Rich Results Test** — not verifiable from this VM; his browser / Search Console is the final word.
