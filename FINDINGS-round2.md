# Testing Round 2 — structural + visual verification (FRESH)

## Structural (site/tools/verify_site.py, final run after all fixes: 0 problems)

- Pages checked: 52
- Internal link fetches by status: {200: 3078, 'home': 52}
- Reachable from home: 53 / 52 (53rd is /sitemap.xml)
- H1=1 on every page, titles/descriptions/canonicals/og:url verbatim vs doc, sitemap 52 URLs (no image entries), robots Allow `/` + Sitemap, FAQ schema = visible Q&A on all 51 FAQ pages, 0 orphans, 0 broken links, 0 self-links, no old-brand strings, no leftover link notation, 0 double-escaped entities (`&amp;#`) in out/.

## Visual probe (site/tools/probe_visual2.py, site/qa-round2/probe2.json)

- 52/52 pages, 1440/390/320, **0 console errors anywhere, 0 overflow pages at any width**.
- Homepage: 37 images in DOM (hero + 36 cards). The probe's fast scroll-through (100ms steps) reported 19 area-card images "unloaded" — re-checked with a slow scroll + 3s wait: **36/36 card images loaded**, 0 zero-height. The 19 were a probe-timing artifact, not a site defect.
- Hero boxes: home 1448×547, inner 1445×385, branded-panel heroes 1440×416 — all as designed.
- Viewed by pixels (site/qa-round2/): home hero desktop + mobile, home service cards, home area cards (Bixby/Jenks/Sand Springs), Broken Arrow hero, emergency hero + split, sewage split, categories branded-panel hero, cost page (numbered sections + Category table), contact page (contact table + brand panel + call card), footer (5 columns incl. Resources).

## DEFECT found in Round 2 (fixed + re-verified)

- **Footer buttons unreadable:** `.footer-col a` (specificity 0,1,1) overrode `.btn-cyan`/`.btn-cream` (0,1,0), so both footer buttons rendered pale text — the cream "Request Emergency Service" button was nearly invisible on cream (verified by zoomed screenshot). Fixed: scoped the rule to `.footer-col ul a` (nav links are all in `<ul>`; buttons are direct children). Re-verified: computed colors cyan button `rgb(7,50,79)` on cyan, cream button `rgb(7,59,102)` on cream + screenshot (qa-round2/check-footer-fixed.png).
- Post-fix re-verification (fresh): structural **0 problems**, home card images **36/36**, hub **17/17**, overflow **0 pages**.

## Speed (measured, homepage)

- LCP 860ms desktop (localhost). Transfer above-fold: 1.88MB uncompressed on the plain local server; realistic gzipped (as Vercel serves) ≈ **521KB worst case** (JS 368KB gzip + CSS 4KB + HTML 33KB + hero 60KB + fonts 53KB) — inside the <800KB budget. Full-scroll load 7.9MB uncompressed (all 35 card images + RSC payload) — lazy images only load on scroll.

## Images (final state)

- 50/52 heroes + 10/12 bodies merged (60 unique files, all 1200×800 WebP ≤150KB, 0 dupes, 0 missing files). Empty by the no-filler rule: heroes for `/services/sewage-backup-cleanup` + `/resources/water-damage-categories-and-classes-explained`; bodies for ceiling + flooded-basement — branded panels + call cards render there.
- Caveats (unchanged from Round 1, shown in screenshots and judged acceptable): flood hero/body same house/street (same Pexels series, different angle); slab-leak hero shows a small GRUNDFOS pump label; flooded-basement hero is a close-up puddle with no basement context; flood hero q50 / body q40 compression.
- All images are real stock photos (Pexels). No AI word in any filename/alt, no AI metadata, no geo-tag, no claim that any image is a real job photo.

## Flagged link mismatches / content gaps (from parse; unchanged, NOT invented)

- 7 doc phrases point at pages that do not exist (left plain + flagged in site/content/FINDINGS-parse.md): `/resources/mold-inspection-vs-mold-testing` (2x), `/resources/water-stain-on-ceiling-guide`, `/resources/can-wet-drywall-be-saved`, `/resources/is-sagging-ceiling-dangerous`, `/resources/hardwood-cupping-crowning-buckling`, `/resources/can-water-damaged-hardwood-be-saved`.
- 66 occurrences remapped to the unambiguous closest real page (e.g. `how-to-file-water-damage-claim-tulsa` → `…-insurance-claim-tulsa`); full list in site/content/link-report.json.
- Contact form has no delivery email in the doc — form UI present, NOT wired, never fakes a send; needs the owner's inbox (e.g. FormSubmit, same pattern as Tulsa Hardwood). No email address anywhere on the site.
- Deploy note: verify no-slash canonicals serve 200 directly (not 308 to slash) on Vercel; if Vercel redirects, the deploy config needs `trailingSlash: false` + the dual files. Next.js 14.2.5 carries a published security advisory (npm warning) — static export with no middleware is minimally exposed, but the parent may want to patch Next before deploy.
- Minor observation (not a defect): on mobile the sticky call bar overlaps the bottom edge of the hero's "Call Now" button at first paint — the bar is the same CTA, so nothing is lost.
