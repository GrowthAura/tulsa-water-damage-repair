# A-to-Z Design Round — FINDINGS

- Date: 2026-11-07 ~16:00 PKT. Source of orders: Google Doc 1nLxqtvBybbb7Uq1VgsBqWoJENzGY_ZtQ6pWb0ELCCVs (title + 1 tab, saved ~/workspace/doc-1nLx/doc-1nLx-tabs.json).
- Scope: CSS + template + images only. No words/content changed except the one ordered cut (item 7). No links, schema, phone, address, header/footer touched.
- Build: `npm run export` green, 56/56 static pages. Served locally on 127.0.0.1:8317.
- Probes: `site/tools/probe_design.py` (H1 position, text sizes, overflow, console, screenshots), `site/tools/probe_a2z.py` (all 53 routes overflow/H1/console, card images, 148 internal refs, sitemap, FAQ schema). Screenshots: `site/qa-design/` (viewed by pixels).
- LOCAL ONLY — no push/deploy/domain/DNS/token.

## 1. H1 stylish (item 1)

- Before: H1 solid cream on the navy hero, no accent.
- After: `.hero h1` gets a cream → pale-cyan → cyan-light gradient (`#f7f3ea` → `#bfefff` → `#7fdbff`), guarded by `@supports (background-clip: text)` so browsers without support keep solid cream. Gradient stops all measure ≥7:1 on navy. No rotation, no text change, readable at 1440/390/320 (viewed).
- Applies to all pages (every H1 lives in the Hero component).

## 2. H2 stylish, no unjustified breaks (item 2)

- Before: H2 solid navy.
- After: H2 gets a navy → blue gradient (`#073B66` → `#0056A3`, both ≥6.6:1 on white), same `@supports` guard. H2s on navy (final-CTA card) keep solid cream via an explicit reset. No `<br>` or forced breaks exist in any heading; `text-wrap: balance` kept (it only balances natural wraps). Viewed on all sampled pages: H2s flow naturally, no awkward wraps.

## 3. Heroes shifted up (item 3)

- Before: hero media 26/30/34rem (mobile/640/1024), content pulled up −14/−16rem; homepage H1 top ≈428px @1440 (from qa-wide before-shots).
- After: media 21/24/28rem, content −11.5/−13rem, padding-bottom 4→3rem; short heroes 20/24→16/19rem, content −11/−12→−9/−10rem; brand-panel inner 26→21rem.
- Measured H1 top @1440: homepage 389px (−39px), hub/services 269px, resources 301px. Sticky header unchanged (81px); a small gap remains between header and hero content as ordered.

## 4. Background colour removed — white page (item 4)

Removed (now white #fff):
- `body` background cream → white (whole page).
- `.section-cream` (homepage, inner split, resources-hub crumbs) → white.
- `.section-tan` (AreaCards section, area map section) → white.
- `.section-blue` → white (was unused in JSX; neutralised anyway).
- `NavyBand` (inner-page intro band, was `.section-navy`) → plain white section; lead now navy, trust items ink with blue checks.
- `TrustBand` (homepage, was navy) → white with hairline rules; items ink, checks blue.
- `ResourceCards` section (was `.section-navy`) → white section; eyebrow plain blue.
- `AreaCards` section (was `.section-tan`) → white section.
- `ServiceCards` section (unused export, was `.section-navy`) → white for consistency.
- `.final-cta` outer background blue-gray → white (the navy card inside stays).

Kept, with reasons:
- Hero navy band — the hero itself; H1 lives here.
- `call-strip` cyan — the emergency CTA band (deliberate anchor).
- `.final-cta-card` navy — the final CTA anchor inside the now-white section.
- Footer navy — footer, not a content section; header/footer work already done, untouched.
- `brand-panel` navy — small component panel for empty image slots, not a section.
- Card cream background, FAQ cream items, aside-call cream, nav-drop/mobile-menu cream, table header navy — components, not section backgrounds; they give cards/controls distinction on the white page.
- `.section-navy` CSS rules left in place but no rendered section uses them anymore.

## 5. Cards top class (item 5)

- CSS: hover lift now also deepens the shadow; image zoom 1.04 → 1.06; card-body padding 1.25/1.4/1.5rem → 1.5/1.5/1.75rem (roomier).
- Card images loaded (fresh probe, after scroll, final build): homepage 34/34 (+1 branded panel: ceiling card, hero emptied this round), services hub 15/15 (+1 ceiling panel), resources hub 8/8 (+2 branded panels: dry-time + categories resource pages have no hero photo).
- The branded panels are now 3 service heroes (sewage, slab-leak, ceiling — no photo exists) + 2 resource heroes (dry-time, categories) + the /resources/ hub (no entry) = 6 panel-hero pages. All intentional per the no-filler rule; the double-eyebrow defect on these pages is fixed (see item 9).

## 6. Text 18 — all non-heading text (item 6)

- Rule applied: every non-heading text element below 18px raised to 1.125rem (18px). Text already ≥18px (body 18px, leads 23.2px, call-strip CTA 20–30px, H1/H2/H3) untouched.
- Raised to 18px: buttons, nav links, nav-drop links + labels, mobile-menu labels, eyebrows, hero badge, breadcrumbs, trust-band items, card blurbs, table cells, brand-panel text + list items, brand name, form labels/inputs/notes, footer text + links + bottom bar, mobile call bar, card-group labels.
- Measured computed sizes @1440 (probe_design.py): body paragraphs 18px (min across sampled pages), lists 18px, FAQ answers 18px, table cells 18px, card blurbs 18px, footer 18px, breadcrumbs 18px, form labels/notes 18px, trust items 18px, buttons 18px, eyebrows 18px. Leads stay 23.2px.
- Deliberately NOT raised (not reading text): `.btn .btn-small` (0.7rem caption inside the stacked header CTA — 18px would break the 5rem header) and `.brand small` (0.68rem brand-lockup caption "TULSA, OKLAHOMA"); footer-column `h3` labels (0.8rem) are heading elements, so they keep their size per the order ("except headings"). Icons (`+` toggles, check marks, dots) untouched.

## 7. Cut link (item 7)

- Ordered cut: "Read how the drying phase works in detail on our page."
- Found: homepage `/`, one block — the paragraph "The distinction matters because mitigation is time-critical every hour of delay increases the scope while restoration can be scheduled once the structure is verified dry." The phrase spanned TWO adjacent anchors to `/services/water-mitigation` ("Read how the drying phase works in detail on our" + " page"). Both anchors removed; the paragraph now ends cleanly "...verified dry." (the stray double period from the removal was fixed in the same pass).
- Verified: 0 occurrences of the phrase left in `content/pages.json` and in the built HTML. Nothing else cut — the doc's own "Learn more about the mitigation phase:" anchor and the separate "Full details on our page." link were left untouched.

## 8. Cross-site image audit + replacements (item 8)

Full detail: `site/FINDINGS-images-cross-site.md` (child agent, verified by me — see spot-checks below).

- **Method:** md5 + 16×16 aHash/dHash of all 57 files vs a 17,144-file pool from every other site under `~/workspace/` (public/images/assets/out dirs). Judgement by viewed pixels only, never hash alone — the deep re-check pixel-verified the nearest pool neighbour of every file with aH≤75 (46 pairs), because same-photo different-crop pairs reach aH=72 (e.g. burst-body candidate vs Lancaster, aH=72). **Lesson: hash distance alone never clears a photo.**
- **Found: 22 cross-site repeats** (21 first pass + 1 commercial body found only in the deep re-check, aH=38). Exact md5 clashes: 0 (all were re-encodes/different crops). Clashed with: Plano, Plano3, Lancaster, Texas, Cape Coral, Boynton Beach, Tulsa Hardwood, Tulsa Blackland, Biohazard, ts-spaces previews. Worst: home hero was on Plano3 + Lancaster; flood hero on 4 sites; burst hero/body on 3 sites each.
- **Replaced in place: 21** (same filename, fresh Pexels photo, 1200×800 WebP ≤150KB, 0 EXIF, no AI word in filename/alt/metadata, honest alt). **Emptied: 1** — ceiling hero deleted, hero set to `null` in `images.json` (branded panel renders): no genuine ceiling water-damage photo exists on Pexels after 3 search rounds; the only genuine collapsed-ceiling photos are the repeat itself and Pexels 30499666 (Plano 3's user-rejected destroyed-room gallery shot). Precedent: 3 slots emptied the same way in the 101% round.
- **Rejected picks caught by verification, never shipped: 11** — including 3 first picks that were themselves repeats (water-heater 28479466, mold-hero 6141203, burst-body 13726337 — all Lancaster, which uses descriptive filenames with no Pexels ID, so the ID blocklist couldn't catch them). Final picks are hash-clear AND pixel-checked.
- **Final state: 56 files, 0 remaining clashes, 0 within-site dupes, 35 kept files' md5s unchanged, 0 missing refs in images.json, no "AI" word in any alt.**
- **My spot-checks (independent):** 56 files in `public/images/`; ceiling hero `null` + file deleted; 0 missing refs (after fixing my own path bug — file values are `/images/...`); 0 AI-word alts; 0 format/dims/size/EXIF fails (all 1200×800 WebP, largest 152,872 B < 153,600); spot sizes match the log exactly (home 72,578 B, flood 122,466 B, mold hero 37,712 B, burst body 30,404 B); manifest + 22-file backup present (`/tmp/replacements_manifest.json`, `/tmp/old-clash-backup/`).
- **Known weaknesses (agent's, carried forward):** south-tulsa hero looks European (best available after 3 rounds); mold hero is a cleaning-action photo, not mold growth (growth still shown by the mold body on the same page); storm hero is palm trees in wind, not a destroyed room (per the gallery ban).
- **Hero-crop fixes (my follow-up, after viewing all 21 replaced heroes by pixels):** two photos were right but their subject sat outside the desktop hero's center-crop window (hero is `object-fit: cover`, ~28rem tall at 1440 — it shows the vertical middle of the file). Added an optional `pos` field to `images.json` + passthrough in `app/lib.js` `pageImage()` + `objectPosition` on the hero `<img>` in `page.js`:
  - Flood hero: `pos: "center 88%"` — the floodwater + wading people (bottom 27% of the file) were cropped out; now the flooded street and waders are visible in the hero (verified by screenshot).
  - Water-heater hero: `pos: "left 0%"` — the wall-mounted heater (top-left corner) was cropped out; now the boiler + pipes are visible in the hero (verified by screenshot).
  - The other 12 replaced heroes I viewed (frozen-pipes icicles, mold-after cracked wall, cost calculator + dollars, appliance laundry room, burst gushing water, commercial vacuuming, roof workers, storm palms, east/north/owasso/sapulpa houses) all frame their subject correctly — no further `pos` needed.

## 9. Defect caught in review (bonus)

- Double eyebrow on brand-panel heroes: on the 5 pages with no hero image (sewage, slab-leak, dry-time, categories, /resources/ hub) the eyebrow "TULSA WATER DAMAGE REPAIR" rendered TWICE — once centered inside the brand panel, once left-aligned in the hero content. Fixed: removed the eyebrow from the panel-inner (panel is now a plain navy band; the hero-content eyebrow is the single one). Pre-existing template defect, made prominent by the 18px eyebrow.

## 10. A-to-Z review checklist (item 9)

- Build green, 56/56 static pages; sitemap 53 URLs, all in pages.json.
- Overflow: 0 pages at 390/320 across all 53 routes (probe_a2z.py); 0 at 1440 on all 8 sampled pages.
- H1 = 1 on all 53 routes. Console errors: 0 on all 53 routes.
- Internal links: 147 distinct refs fetched, 0 broken. FAQ schema = visible Q&A on all pages, 0 mismatches.
- H1 stylish: gradient on all sampled pages, readable (viewed). Hero position: H1 tops 269–389px @1440, shifted up vs before.
- White sections: verified by pixels on homepage (full page), hub, service, area, contact, resources — one continuous white page; only hero navy, cyan call-strip, navy final-CTA card, navy footer remain as anchors.
- Cards: home 34/34, hub 15/15, resources 8/8 images loaded; ceiling/sewage/slab-leak cards are intentional panels (see item 5).
- Text 18: measured 18px across all sampled elements (see item 6).
- Cut link: 0 occurrences left (see item 7).
- Images cross-site: 22 clashes found, 21 replaced, 1 emptied, 0 remaining (see item 8). All 21 replaced heroes viewed by pixels; 2 hero-crop fixes applied + re-verified (flood, water-heater).
- Reveal check: after a slow scroll through the homepage, all 9 H2s and all 37 cards reach opacity 1 (an early probe that reported 3 hidden H2s was a smooth-scroll artifact of the probe itself, re-tested with instant scrolling: 0 hidden).
- Screenshots viewed: qa-design/ (home desktop top/full + mobile top, hub, emergency service, flood service, Broken Arrow area, contact, resources hub, about-us) + final replaced-hero set (home, flood v1+v2, mold, ceiling panel, south-tulsa, water-heater v1+v2, frozen, mold-after, cost, appliance, burst, commercial, roof, storm, east, north, owasso, sapulpa).

## Files changed

- `app/globals.css` (backgrounds, H1/H2 gradients, hero sizes, text-18 floor, card hover/padding)
- `app/[[...slug]]/page.js` (NavyBand white + ink text, section classes cream/tan → plain, brand-panel eyebrow removed)
- `app/components/Shared.jsx` (ResourceCards/AreaCards/ServiceCards sections navy/tan → white, eyebrows plain)
- `content/pages.json` (item 7 cut only — 1 block on `/`)
- `content/images.json` (item 8: 21 alts updated, ceiling hero → null, flood hero `pos: "center 88%"`, water-heater hero `pos: "left 0%"`)
- `app/lib.js` (pageImage passes hero/body objects through, so `pos` reaches the template)
- `public/images/` — 21 files replaced in place + 1 deleted (ceiling hero); 56 files now
- Probes: `site/tools/probe_design.py` (broken-arrow slug fixed to `/service-areas/broken-arrow-ok/` — the old slug 404'd and polluted one console count), `site/tools/probe_a2z.py`; screenshots `site/qa-design/`
