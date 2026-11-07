# "See"-Link + Technical SEO Round — Findings
## Tulsa Water Damage Repair — 2026-11-07 ~18:55 PKT (local only)

User order (upset, his screenshot of the "Documentation before removal" step ending in a bare
"See" link): wherever the word "See" carries an internal link, correct it. Then internal links
400% OK, 3x deepest technical SEO + schema, footer best level (remove the "→" arrows he hates),
UI/UX A-to-Z proper end level. 1 hour, relaxed pace, 10x lovely. LOCAL ONLY.

---

## 1. "See" links — ALL UNLINKED (done, verified)

### Method
- Audited every anchor in content/pages.json (all strings, blocks + FAQs) and in the built
  HTML of all 53 pages (scripts stripped, flat .html copies deduped to canonical routes).
- Pattern: any `<a>` whose visible text is exactly "See" or begins with "See" (word boundary).
- Fix: removed the `<a ...>...</a>` tags only; the words stay as plain text, wording 100%
  unchanged. No other anchor touched.
- Trap avoided: a previous direct fix attempt FAILED on JSON escaping. Verified ground
  truth (repr-checked): the raw file stores standard JSON escaping, and json.load()
  gives REAL quotes in the loaded strings (0 backslashes) — the brief was correct.
  The unlink regex was quote-agnostic (`<a` + backslash-b + `[^>]*>(See` + backslash-b
  + `[^<]*)</a>`), which is why it worked regardless. The unlink asserted 277
  replacements + 0 remaining and was re-verified in the rebuilt HTML (0 See anchors).

### Count correction (important)
- First audit counted **248** — WRONG. It used `startswith('See ')` (See + space) and missed
  the **29× "See:"** anchors (colon, no space). The correct total is **277**.
- Final: **277 anchors unlinked** (242 × bare "See", 29 × "See:", 6 × "See..." phrases).
  All had plain-text inner content (no nested tags). 0 remain in pages.json, 0 remain in
  built HTML (re-audited after rebuild). Plain "See" words still present as text
  (20 on the homepage — wording unchanged).

### The 6 "See..." phrases unlinked
| Page (pages.json path) | Anchor text | Target |
|---|---|---|
| [0] homepage, blocks[22] | "See every service organized in one place on our" | /services/ |
| [0] homepage, blocks[51] | "See our insurance claim guide:" | /resources/how-to-file-water-damage-insurance-claim-tulsa |
| [0] homepage, faqs[2] | "See the full drying timeline guide:" | /resources/how-long-does-water-damage-take-to-dry |
| [1] services hub, faqs[2] | "See the full list with zip codes on our" | / |
| [28] about-us, blocks[20] | "See the full services directory:" | /services/ |
| [38] cost guide, faqs[1] | "See the cost table above and the full cost guide:" | /resources/water-damage-restoration-cost-tulsa |

### The 242 bare "See" anchors (by target — full per-page list in /tmp/see_pagesjson.txt)
- Bare "See" occurred on: homepage (7: storm, slab-leak, AC drain, water-heater, flood,
  emergency, +1), about-us (6), commercial (1), all 10 resources guides, all 18 service
  pages (heroes/bodies/FAQs), and area pages. Full 277-row list (page path, anchor text,
  target): site/SEE-LINKS-UNLINKED-277.txt (generated from the pre-unlink pages.json).
- Spot checks (verified in rebuilt HTML):
  - Homepage blocks[40]: "...equipment already on the truck. See" — anchor gone, word kept.
  - Homepage blocks[22]: "See every service organized in one place on our [hub page]" —
    "See..." phrase plain, the separate "hub page" link KEPT (its text is not a See anchor).
  - "See the full services directory:" (about-us) — plain text now; the "What Do We Handle?"
    cards built from it are unaffected.

### Diff
- content/pages.json: 277 insertions + 277 deletions (554 lines — exactly the 277 anchors,
  one line each). No reformat, no other change. Rebuild green
  ("23 flat .html copies, 30 slash routes").

## 2. Internal links — 400% audit (done, fresh)
- tools/verify_site.py (fresh run after the unlink): **53 pages checked, 2,390 internal
  link fetches all 200, reachable from home 53/53.**
- PROBLEMS: **1 — orphan page: /commercial/**
  - Cause (verified): /commercial/'s ONLY inbound link sitewide was the FAQ "See" link on
    /services/fire-damage-restoration ("Do you handle commercial fire damage?" — answer ends
    "See" → /commercial/). The unlink removed it, per the user's explicit order.
  - /commercial/ is still in the sitemap (2 mentions) and directly accessible; it simply has
    no internal link pointing to it now. The services hub links only to
    /services/commercial-water-damage (the service page, not the hub).
  - NOT fixed unilaterally: restoring the See link would violate his explicit unlink order,
    and inventing a replacement link would violate the doc-only link rule. **His call needed:**
    (a) leave it orphaned, (b) restore that one FAQ link, or (c) add a non-"See" link to
    /commercial/ somewhere (he names the place/anchor).
  - 0 broken links, 0 body self-links, every remaining target a real route.

## 3. Technical SEO + schema — 3x deepest passes (DONE, child agent; parent-verified diffs)
Evidence: site/qa-see-seo/seo-FINDINGS.md, seo-pass1.json, seo-pass2.json, seo-pass3.json,
seo-cwv-pass2.json, seo-cwv-pass3.json. Probes: site/tools/seo_probe.py, site/tools/seo_cwv.py.
All builds ran in an isolated copy (~/workspace/seo-build-tmp, removed after); the real
site/out/ was never rebuilt by the child. Scope respected: only app/lib.js + page.js
(metadata/JSON-LD only) changed; content/pages.json untouched; sitemap/robots needed no change.

### Pass 1 — 194 defects found, ALL FIXED (except the orphan)
1. LocalBusiness missing on 34/53 pages (all area/resource/hub/about/contact/commercial pages
   had no business entity at all).
2. Breadcrumb parent URLs wrong on 29 pages — area "Service Areas" → `/` (duplicate Home
   link); resource "Resources" → `/` instead of the real `/resources/` hub.
3. Breadcrumb last-item name ≠ visible trail on 52 pages — JSON-LD used the full H1, the
   visible breadcrumb uses shortName.
4. Homepage breadcrumb duplicated Home — 2 items, both pointing at `/`.
- Fixes (verified in the diff by the parent): lib.js `parentOf()` — area → null (no
  `/service-areas/` hub exists), resource → `/resources/`; page.js `jsonLd()` — homepage
  breadcrumb = single Home item, last crumb = `shortName()` (matches visible),
  LocalBusiness + WebPage added to every page's `@graph`.
- (4 Pass-1 "defects" were probe bugs — `&` in H1s, address `@type`, FAQ `<h3>` scoping,
  Chrome CTA links — fixed in the probe, not the site.)

### Pass 2 — 1 defect (fresh rebuild + probe + CWV)
Only the /commercial/ orphan remained. Everything else 0: "See" anchors 0, broken internal
links 0, body self-links 0, canonical/og/twitter exactly 1x each and self-matching on 53/53,
titles/descriptions verbatim, FAQ schema Q/A exact vs doc on all 222 FAQs (51 FAQ pages),
sitemap 53 locs = canonical set with lastmod 53/53.

### Pass 3 — 1 defect (from-scratch rebuild + probe + CWV + independent checks)
Same result. Independent re-check (different code, straight from built files): LocalBusiness
53/53, BreadcrumbList 53/53, FAQPage 51/51, WebSite 53/53, Service 18/18, WebPage 35/35,
0 unparseable JSON-LD; sitemap XML parses, 53 entries, all loc+lastmod (2026-11-07);
`www.` refs 0, `http://` refs 0; og:image files all exist, all 1200x800 as declared; alts
present, no "AI" word anywhere in filenames/alts.

### CWV — MEASURED (real Chromium, unthrottled localhost; baseline, not field data)
| Page | Desktop LCP / CLS | Mobile 390 LCP / CLS |
|---|---|---|
| `/` | 512ms / 0 (P2), 508ms / 0 (P3) | 316ms / 0, 308ms / 0 |
| `/services/emergency-water-damage-restoration` | 336 / 0, 340 / 0 | 244 / 0, 244 / 0 |
| `/service-areas/broken-arrow-ok/` | 356 / 0, 336 / 0 | 268 / 0, 272 / 0 |
Overflow 0 on all 53 pages at 1440/390/320; console errors 0. (Pass 1 CWV run returned nulls
due to an init-script bug in the child's probe — fixed, measured properly in Passes 2–3.)

### Open / could not fix (report only, no wording/fact changes)
- Title/description lengths (verbatim doc): 52/53 titles >60 chars (longest 108, South Tulsa),
  23/53 descriptions >160 (longest 191, Midtown Tulsa); no duplicates. Needs his wording call.
- robots.txt `Host:` line kept — Yandex-only, ignored by Google, harmless.
- Trailing-slash forms: mixed forms are the doc's exact canonicals and match everywhere
  (sitemap = canonical = og:url; 23 no-slash, 30 slash). Not changed. Note: the python test
  server 301s no-slash URLs to slash form, but all 23 no-slash canonicals have both
  `path.html` and `path/index.html` in out/, so GitHub Pages serves the canonical form 200.
- LocalBusiness has no geo/image/logo/priceRange/sameAs — not added; geo is not in the doc
  (would be invented data), the rest are optional.

## 4. Footer best level — arrows removed (DONE, child agent; parent-verified by pixels)
- BEFORE: all 5 footer link groups carried `<span class="arrow">→</span>` with a slide-right
  hover (Services list, "View all services", Areas list, "View all areas", "Blog").
- AFTER (Edmond palette only): plain links, no glyph. Hover lifts the text to cream, fades
  in a 2px cyan underline, nudges 2px right. "View all services" / "View all areas" / "Blog"
  got `className="footer-more"`: bold cream with a PERMANENT 2px cyan underline, so they still
  read as the column's action links — no arrow needed. Dead `.footer-col a .arrow` CSS rules
  removed. Header's "View every service →" (Header.jsx:62) untouched, as ordered.
- All footer links, wording, NAP (400 S 129th E Ave, Tulsa, OK 74108), phone (918) 395-9320
  unchanged. Parent verified by pixels: Footer.jsx 0 arrows, globals.css 0 `.arrow` rules,
  footer screenshot shows the cyan underlines + stacked Call Now button (see below).
- Evidence: site/qa-see-seo/uiux-fix-footer-d1440.png,
  site/qa-see-seo/uiux-fix-footer-m390-buttons.png.

## 5. UI/UX A-to-Z (DONE, child agent; parent spot-verified)
- FIXED 1 — Footer "Call Now" button split the phone number (desktop): the narrow 5th column
  wrapped it into 3 lines, breaking mid-number ("Call Now ·" / "(918) 395–" / "9320"). Fixed
  by splitting the button into two spans with `.footer-col .btn` stacked (column, 1rem gap).
  Bonus: "Request Emergency Service" went from 3 lines to 2 (desktop) / 1 (mobile).
- FIXED 2 — Brand-panel ✓ floated beside the 2nd line: `.brand-panel li` used
  `align-items: center`, so on wrapped items like "Insurance Claim Documentation" the ✓ sat
  beside "Documentation". Changed to `flex-start` + matching line-height; ✓ now pins to the
  first line (verified on /services/).
- CHECKED AND PASSING (no change): hero + trust chips, home/hub/resources/area cards, all
  tables incl. the contact NAP/ZIP table (gradient header, zebra rows; on mobile they scroll
  inside their card, no page overflow), contact form, FAQ, phase cards, demand strip, final
  CTA, mobile menu overlay, sticky mobile call bar. Probe: 0 console errors, 0 page overflow
  on all 14 page/viewport combos.
- NOT A DEFECT — map iframes: footer/contact map iframes show a broken-frame icon only in
  this VM's headless Chrome (net::ERR_TUNNEL_CONNECTION_FAILED, VM proxy); curl reaches
  google.com/maps fine. No site change made.
- Defects needing page.js edits: none. Two cosmetic notes only, no action: hero trust chips
  wrap 3+1 on desktop (natural flex wrap); mobile tables show 1–2 columns until scrolled
  sideways (deliberate overflow-x pattern).
- Evidence: site/qa-see-seo/UIUX-FINDINGS.md + 55 screenshots in site/qa-see-seo/ (uiux-*
  prefix: 28 full/footer shots + 17 scrolled-viewport shots + 4 fix-verification shots).
  Note: full-page captures alone leave below-fold cards invisible (`.reveal` animation) —
  a capture artifact, not a defect; the child used step-scrolled viewport shots for cards.

## Verification (FINAL, parent — fresh final build, after both children)
- Rebuild green (static export, 23 flat .html copies, 30 slash routes).
- probe_a2z.py (fresh): routes 53 | overflow pages 0 | H1 != 1: [] | console errors: [] |
  card imgs / 37/37, /services/ 18/18, /resources/ 8/8 | internal refs 157, broken [] |
  sitemap 53 (in pages.json 53) | FAQ mismatches [].
- verify_site.py (fresh): 53 pages, 2,390 internal link fetches all 200, reachable from home
  53/53. PROBLEMS: 1 — orphan /commercial/ (known, flagged in §2, needs his call).
- "See" anchors: 0 in pages.json, 0 in built HTML (re-audited post-rebuild).
- Footer screenshot viewed by the parent by pixels: 0 arrows, cyan underlines on Blog /
  View all services / View all areas, Call Now button stacked with the number intact.
- FINDINGS-round1.md: verify_site.py overwrote it AGAIN during the final audit (known trap —
  the script hardcodes its output path to that file); restored from git afterwards
  (reconstructed original Round 1 log intact).
- Changed files this round: content/pages.json (277 See unlinks), app/lib.js (parentOf),
  app/[[...slug]]/page.js (JSON-LD), app/components/Footer.jsx (arrows out, footer-more in),
  app/globals.css (footer treatment, Call Now stack, brand-panel check). New: this findings
  file, SEE-LINKS-UNLINKED-277.txt, tools/seo_probe.py, tools/seo_cwv.py,
  site/qa-see-seo/ (evidence). LOCAL ONLY — no push/deploy/domain/DNS/token.
