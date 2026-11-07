# Refinement round — findings (2026-11-07 ~14:40 PKT)

Scope: user's 4 ordered changes + "Learn more →" cut + favicon + crawlability
emphasis. Stack unchanged: Next.js 14 static export, no downgrade, no
plain-HTML shortcuts. LOCAL ONLY — no push/deploy/domain/DNS/token.

## 1. Images 101% — DONE (detail: site/FINDINGS-images-101.md)

- Full re-audit: all 60 slots re-viewed by pixels; p-hash duplicate check.
- Swapped (2): #11 flood body → flood-response crew with sandbags (Pexels
  28447787); #59 vs-flood hero → ROAD CLOSED sign in floodwater (Pexels
  13865778). Both viewed, 1200×800 WebP ≤150KB, 0 EXIF, honest alts.
- Emptied (3, branded panels render): #21 sewage body (pixel-dup of #20 +
  off-topic), #29 slab-leak hero (readable GRUNDFOS brand label, pump not a
  slab leak), #57 dry-time hero (pixel-dup of #16). No genuinely relevant
  free-stock photo exists for any of the three after repeated searches;
  social posts are other businesses' photos — not used.
- Kept as closest verified fits: #2 services-hub hero (B&W cleaning crew),
  #7 emergency body (technician), #16 basement hero (puddle, no basement
  context — no genuine flooded-basement stock photo on Pexels).
- First candidate for #59 (Pexels 28447774) turned out to BE the current #10
  hero (p-hash 1.00) — caught before use, not shipped.
- Final: 57 filled slots (48 heroes + 9 bodies), 57 unique files, max 149KB,
  0 duplicate pixel pairs, 0 same-shoot pairs on any page.

## 2. Footer — blogs out, just the Blog link — DONE

- `Footer.jsx`: Resources column (10 individual links) deleted entirely.
  Footer now has 4 columns: brand, Services, Service Area, Emergency Help.
- Footer-bottom nav is now: About Us · **Blog** · Contact · Sitemap.
  "Blog" → `/resources/`.
- New hub page `/resources/` (type `resources-hub`, added to
  `content/pages.json`): H1 "Water Damage Resources & Guides in Tulsa, OK",
  unique title/meta, self-canonical, one factual intro line only, and
  `ResourceCards` listing all 10 resource pages with their doc H1s + blurbs
  (zero invented copy). Hero is a branded panel (no image). No FAQs, so no
  FAQ schema on the hub (schema = visible Q&A holds).
- Orphan check: all 10 resource pages reachable via the hub; the previously
  orphaned vs-flood page is linked from the hub. Structural verifier: 0 orphans.

## 3. Maps — optimized, end-level — VERIFIED ALREADY CORRECT, no change needed

- Footer map (`loading="lazy"`, Google Maps `q=400 S 129th E Ave, Tulsa, OK
  74108&output=embed`) renders on every page EXCEPT area pages and contact.
- Area pages render ONLY their own body map (`MapBlock`, `q=<Area>, OK` —
  verified: Broken Arrow → `q=Broken%20Arrow%2C%20OK`).
- Contact renders ONLY its own body map (same business address).
- Iframe census of `out/`: 76 HTML files have exactly 1 iframe, 2 have 0
  (the 404 pages). No page has two maps. All iframe tags carry
  `loading="lazy"`; the map is below the fold and does not block LCP
  (homepage LCP 496ms, see §7).

## 4. Top bar removed — DONE

- `<div className="topbar">` deleted from `Header.jsx` on all pages; the
  `.topbar` CSS rules (4 rules) and the now-unused `.card-link` CSS rules
  removed from `globals.css` (re-read from disk at edit time; wide-pass
  agent's heading/intro width rules untouched — verified still in place).
- Header verified: height 81px at 1440 and 390, sticky, brand + nav + phone
  CTA + mobile call bar all intact (screenshots site/qa-refine/*-header.png).

## 5. "Learn more →" cut — DONE

- Both `card-link` blocks removed from `Shared.jsx` (ServiceCards + AreaCards).
  Cards stay linked via their H3 titles. New `ResourceCards` component was
  built without the label from the start.
- Verified in built HTML: 0 occurrences of "Learn more →" across `out/`.
- **NOT touched (user to decide separately):** the doc's own link anchor
  "Learn more about the mitigation phase:" in `content/pages.json` (line 643)
  — verbatim doc content with a doc link to `/services/water-mitigation`.
  It still renders on the `/services/` hub page. No change made.

## 6. Favicon — bigger and prettier — DONE

- Site had NO favicon. Created a clean water-drop mark in brand navy
  (#073B66) + cyan (#00BFFF) on a cream (#F7F3EA) rounded tile, matching the
  header brand-mark. Drawn as vector shapes (no AI image, no photo).
- Files in `public/`: `favicon.ico` (16+32), `favicon-32x32.png`,
  `favicon-16x16.png`, `apple-touch-icon.png` (180×180). All 0 EXIF.
- Wired via `app/layout.js` metadata `icons` (icon + apple) — every page
  emits the links: 78/78 HTML files contain `rel="icon"` and
  `apple-touch-icon`; all four files serve 200.
- Verified by viewed pixels at 180px, 32px (×3) and 16px (×6): droplet +
  cyan inner drop read clearly at every size.
- **Open:** a headless browser has no tab bar, so the tab-icon rendering
  itself could not be screenshotted here — needs one look in a real browser
  tab (user/parent check). Files + links are all verified.

## 7. Crawlability — full re-check, PASSED 0 problems

- Rebuild green: `npm run export`, 56 static pages (was 55, +1 hub),
  post-export 23 flat .html + 30 slash routes.
- Structural verifier (`tools/verify_site.py`, counts updated 52→53):
  **53 pages checked, 2,662 internal link fetches all 200, reachable from
  home 54/53, PROBLEMS: 0.** Sitemap 53 URLs, no image entries; robots OK
  (Allow /, Sitemap + Host lines). FAQ schema = visible Q&A on every page
  with FAQs (hub has none → no FAQ schema, correct). H1=1 on all 10 probed
  pages; titles/descriptions/canonicals/og:url unchanged vs doc.
- Overflow probe (`tools/probe_overflow.py`): **0 overflow pages at 390/320
  across all 53 pages.** Home card images 35/35 loaded, services hub 16/16
  (slab + sewage cards are branded panels, no `<img>` — expected).
- Visual probe (`tools/shots_refine.py` + metrics re-run, screenshots
  site/qa-refine/): 10 pages × 1440/390 — overflow 0, H1=1, topbar absent,
  "Learn more →" 0, 1 iframe each, console errors 0, header 81px both widths.
- LCP (PerformanceObserver, desktop localhost): homepage 496ms (hero IMG),
  resources hub 496ms (H1). Inside the <1.8s budget. Mobile LCP not
  measured in this round (same caveat as Round 2).
- Images re-checked after rebuild by viewed pixels: swapped flood body +
  vs-flood hero render correctly; nulled slots render branded panels;
  hub cards render (10/10 in DOM; reveal-on-scroll is the normal Tier 1
  behaviour — 9/10 visible after scrolling to the section, the 10th reveals
  when scrolled to).

## Process notes / things that went wrong and how they were handled

- `tools/verify_site.py` hardcodes its output to `site/FINDINGS-round1.md`
  and overwrote the original Round 1 log on this run. The original was
  reconstructed from PROGRESS.md (labelled as a reconstruction) and the fresh
  run's output is preserved here. Future runs should copy the file first or
  change the verifier's output path.
- First screenshot run crashed on `/services/` (Chromium renderer ran out of
  memory with 8GB RAM, full-page shots in one session). Re-ran with a fresh
  browser per page; all 10 pages captured.
- The full-page screenshot of `/resources/` showed an empty navy block where
  the cards belong — investigated and cleared: the cards are Tier 1
  `.reveal` elements at opacity 0 until scrolled into view (same behaviour
  as homepage cards in Round 1). After scrolling, 9/10 visible, titles +
  images correct. Not a defect.

## Open items (unchanged from before, still needing his word)

- Contact form not wired (no delivery email in doc).
- 7 doc phrases point at non-existent pages (left plain + flagged).
- Deploy note: verify no-slash canonicals serve 200 (not 308) on Vercel.
- Next.js 14.2.5 security advisory — consider patching before deploy.
- Favicon tab-bar rendering needs one real-browser look (see §6).
- Preview-photo decision from the theme preview still pending (generated
  scenes vs branded panels only on the real site).

Screenshots: site/qa-refine/ (52 files: 10 pages × 1440 full + 390 top +
390 footer + header close-ups, plus resources-hub cards scrolled).
Proof PDF: ~/workspace/your_files/tulsa-repair-refine-round-proof.pdf
