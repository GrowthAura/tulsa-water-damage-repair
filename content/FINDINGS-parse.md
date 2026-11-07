# Tulsa Water Damage Repair — Parse Findings (Round 0)

Source: Google Doc 1iMayAVFlZk5WYxULJ_h-On6BvTQBhubLjLim7Q4NOB4, parsed from the
raw tabs JSON (doc-1iMay-tabs.json) — bold runs, real FEMA link annotations and
real tables preserved. Parser: tools/parse_doc.py. Output: site/content/pages.json.
Verification: tools/verify_content.py — **4,969 sentences checked, 0 missing.**

## Doc structure (verified, not assumed)

- 52 pages, each exactly 1 HEADING_2 (visible H1, all 52 unique), 321 H3s,
  630 bullets (all nesting level 0), 51 real tables (288 rows), 20 FEMA link
  runs (= 10 FEMA link instances, anchor "FEMA's Flood Map Service Center"),
  1,842 bold runs, 2 italic runs, 478 HR section dividers.
- Meta: all 52 pages have exactly 1 Meta Title + 1 Meta Description (used verbatim).
- Phone: only (918) 395-9320 (245 mentions). No email anywhere in the doc.
  No old-brand/phone/domain contamination (0 hits).
- FAQ: 51 of 52 pages have a "Frequently Asked Questions" section (222 Q&As
  total). Only /about-us/ has no FAQ — that is the doc's own structure.
- Em dashes: 0 in doc. En dashes: 70 (ranges like 24–48) — replaced with "-"
  at build. Double spaces collapsed. Words unchanged.
- Bold lead-in + vertical-tab = lead-in paragraph pattern (544 paras):
  rendered as <strong>lead-in</strong><br>body. FAQ questions are the bold
  lead-in of FAQ-section paras.

## Links — 833 occurrences logged (site/content/link-report.json)

| Disposition | Count |
|---|---|
| valid (matches a real route) | 742 |
| remapped to unambiguous closest real page | 66 |
| city-table re-anchored (path-only Page cell) | 7 |
| city-table blank Page cell linked (city name) | 5 |
| left plain — no real page exists | 6 |
| left plain — points at its own page's topic | 1 |
| remapped by sentence context (Midtown hardwood) | 1 |
| path-only table cell anchored to row label | 5 |

- Self-links in body content: **0** (checked after remapping too).
- Anchor rule: full phrase since last sentence boundary (or \x0b lead-in break);
  if the phrase ends with a dangling word (on/our/See/etc.) up to 3 following
  words from the SAME sentence are included, never crossing another link or a
  sentence end. Short anchors (e.g. bare "See" lines — the doc's own
  cross-reference style) keep the doc's words verbatim and get a title=""
  attribute with the target page's H1 for usability.
- Internal links are plain <a href> (no target=_blank). FEMA links are the only
  external links: target=_blank + rel=noopener, exact URL kept.
- **Remaps (unambiguous, same topic, near-identical slug):**
  how-to-file-water-damage-claim-tulsa → …-insurance-claim-tulsa (27x);
  how-long-water-damage-takes-to-dry → how-long-does-water-damage-take-to-dry (11x);
  water-damage-categories → …-and-classes-explained (9x);
  preventing-frozen-pipes-tulsa → how-to-prevent-frozen-pipes-tulsa (9x);
  10-signs-hidden-water-damage → signs-of-hidden-water-damage (5x);
  ceiling-drywall-water-damage → ceiling-water-damage (3x);
  smoke-soot-cleanup → smoke-soot-damage-cleanup (2x).
  Context remap: can-water-damaged-hardwood-be-saved on Midtown page →
  /services/hardwood-floor-drying (paired with it in the same sentence).
- **Left plain + flagged (no real page; do NOT invent the page):**
  /resources/mold-inspection-vs-mold-testing (2x: mold-remediation page,
  mold-after-water-damage FAQ); /resources/water-stain-on-ceiling-guide (1x,
  ceiling page); /resources/can-wet-drywall-be-saved (1x, ceiling page);
  /resources/is-sagging-ceiling-dangerous (1x, ceiling page);
  /resources/hardwood-cupping-crowning-buckling (1x, hardwood page);
  /resources/can-water-damaged-hardwood-be-saved (1x, hardwood page itself).
  The "(/…)" notation was stripped; the sentence stays as plain text.
- Homepage city table (City | Zip codes | Page): Page column blank for
  Catoosa, Collinsville, Skiatook, Coweta, Sapulpa — the city name in the
  first column is linked to its existing area page (the column is a link
  column and the pages exist). Path-only Page cells are linked with the city
  name as anchor.
- Homepage path "(/)" (2x) = homepage link, resolved to "/".

## Excluded from page content (logged, NOT published)

- 5 batch delivery notes at tab boundaries — notes to the builder, not
  homeowner content ("Here are all 10 pages rewritten at absolute peak
  level…", "All 10 pages done…"): cost page ×1, mold-after page ×2,
  first-24-hours ×1, oklahoma insurance guide ×1.
- 1 bracket instruction para on /contact/: "[Embed Google Map of 400 S 129th
  E Ave, Tulsa, OK 74108] / [Non-emergency contact form here]" — rendered as
  a map embed + form UI (see gap below), never as visible text.

## Content gaps — flagged, NOT invented

1. **Contact form has no delivery email in the doc.** Form UI will be present
   on /contact/ with a clear notice that delivery is not connected yet; it
   must NOT pretend to submit. Needs the owner's inbox (e.g. FormSubmit, same
   pattern as Tulsa Hardwood) before it can receive messages.
2. **7 dead-link phrases point at pages that do not exist** (list above).
   If the owner wants them, those pages must be written as new doc content.
3. **No email address anywhere** — footer/contact show phone + street address
   only (both from the doc: 400 S 129th E Ave, Tulsa, OK 74108).
4. **Meta titles run 50–108 chars** (several over 60) — used verbatim per
   order; not shortened.

## Parser bugs found and fixed during this round

- Internal links rendered with target=_blank (fixed: only FEMA opens new tab).
- Forward anchor extension crossed the next link and cut words mid-word
  ("drywal l") — fixed with token-span math + never crossing a sentence end
  or another link; \x0b now counts as an anchor boundary so bold lead-ins
  are never swallowed into a link.
- En dashes survived in text runs (cleaning was only applied to the
  emptiness check) — fixed by cleaning inside runs_of().
- Contact table's blank header row rendered as an empty row — dropped.
- City-table header comparison failed on <strong>-wrapped headers — fixed.
