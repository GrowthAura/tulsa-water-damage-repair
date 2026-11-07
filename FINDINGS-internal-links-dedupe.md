# Internal links dedupe — 45 repeat pairs (2026-11-08 ~00:40 PKT)

User order: "bus ap nye 1 dfa krna hey yaar 2 linsk 1 page ko nahi denye"
(One link per target per page, in body copy.) Local only until push; part of the
pending bundle (homepage table + FAQ 18px + favicon lovely + doc audit + this dedupe).

## Scope
- 50 pages (homepage /, /about-us/, /contact/ EXCLUDED per his scope — untouched,
  byte-identical to pre-dedupe backup).
- Body copy only: content blocks + FAQ answers (pages.json). Header/footer/dropdowns,
  related-service/area cards and hub cards are template navigation — untouched.
- Rule: keep ONE link per target per page; words stay plain verbatim where unlinked.

## Keep decision (his "mind use karo" — strongest anchor, not blind first)
- Default: keep first occurrence, unlink the rest.
- Keep LATER (stronger) instead: /services/ -> insurance-claim guide kept the FAQ
  "Our step-by-step insurance claim guide:" (not the p "Walk through the full process:");
  /service-areas/owasso-ok/ -> frozen-pipes kept FAQ "Full prevention checklist:"
  (not the p "Full checklist:").
- NARROW-KEEP (first occurrence kept, anchor narrowed to the clean name, unlink later):
  storm-damage-repair "South Tulsa and Bixby" -> "Bixby"; ac-drain-line "and Glenpool"
  -> "Glenpool"; cherry-street "and Brookside" -> "Brookside"; sewage "and Bixby" -> "Bixby".
- Judgment fixes: north-tulsa mold kept the offer-list "Mold remediation" (NOT the
  leftover "and" anchor from the See round — "See <a>and</a>" unlinked); east-tulsa
  kept ul "Commercial water damage", unlinked table "Varies by scale see" (a "see"
  remnant); flood-damage FAQ "Our" + "explains each scenario" both unlinked (kept
  p "Full breakdown:"); sewage FAQ kept "growth", unlinked " process within the";
  sapulpa FAQ "More:" unlinked; midtown FAQ "and" unlinked.
- Services hub (/services/): kept the table links (blocks[6]), unlinked the ul
  duplicates + p "mitigation phase" + FAQ "how we structure mitigation".

## Result
- 45 repeat pairs -> 0. 93 anchor edits (45 keeps incl. 4 narrow-keeps, 48 unlinks).
- Built-HTML audit (.content-block incl. nested .faq-list, 52 pages, 514 links):
  0 repeat targets, 0 anchors >5 words on the 50 in-scope pages.
- Remaining repeats/long anchors exist ONLY on the 3 excluded pages (homepage 15/11
  — mostly whole service cards as one link; about-us 3/2; contact 2/1 — the 6 known
  long anchors) — per his exclusion, untouched.
- verify_site.py: 53 pages, 2,500 internal fetches all 200, PROBLEMS 0.
- /commercial/ inbound FAQ link intact. 278 "See" anchors NOT restored.
