# Images 101% — full re-audit (refine round, 2026-11-07)

Every image slot re-viewed by actual pixels (6 labelled contact sheets,
`/tmp/audit-sheets/sheet1-6.jpg`, manifest `/tmp/audit-manifest.json`), judged
against its exact section, not just page topic. Perceptual-hash (16×16 average
hash) used for duplicate detection. Source: Pexels free stock only — the
image-search results for restoration-company websites were NOT used
(licensing / misattribution). No AI images. No AI word in any filename / alt /
metadata. No geo-tag. No image is claimed to be a real job photo. All files
1200×800 WebP ≤150KB, 0 EXIF.

## Swaps made this round (2)

| # | Slot | Old verdict | New file | New alt (only what the pixels show) |
|---|---|---|---|---|
| 11 | `/services/flood-damage-restoration` body | Same shoot as the page hero (#10: same white house, red fence, different angle) — rejected | `services-flood-damage-restoration-tulsa-water-damage-repair-flood-response.webp` (Pexels 28447787, "Flood Response Team in Residential Area") | "Flood response workers in rain gear stacking sandbags on a flooded residential street" |
| 59 | `/resources/water-damage-vs-flood-damage-insurance-oklahoma` hero | Pixel-identical to #10 flood hero (p-hash 1.00) — rejected | `resources-water-damage-vs-flood-damage-insurance-oklahoma-tulsa-water-damage-repair.webp` (Pexels 13865778, "Road Closed Signage on Street") | "A ROAD CLOSED sign standing in floodwater on a tree-lined street" |

Notes on the two swaps:
- A first candidate for #59 (Pexels 28447774, "Flooded suburban house during
  heavy rain") turned out to BE the current #10 hero (p-hash 1.00) — caught
  before use, not shipped. It is the same photo, not a look-alike.
- #11's new photo is from the same photographer/event as #10 (same flood,
  Sep 2024) but a different street, different houses, different subject
  (response crew + sandbags, not the house). Houses are European-style
  (tile roofs) — a place-fit weakness, logged honestly; the subject is
  exactly flood response, which is what the body section is about.
- #59's new photo: flooded US street, ROAD CLOSED sign, trees — on-topic
  for "water damage vs flood damage" (street flooding = flood, not a pipe leak).

## Slots emptied this round (3) — branded panel renders, no forced filler

| # | Slot | Why emptied |
|---|---|---|
| 21 | `/services/sewage-backup-cleanup` body | Pixel-identical to #20 burst-pipe body (p-hash 1.00) AND off-topic for sewage (hands on pipes/valves). No genuinely relevant free-stock sewage photo found in 3 searches (Pexels has no sewage-cleanup stock; social posts are other businesses' photos — unusable). File deleted. |
| 29 | `/services/slab-leak-water-damage/` hero | Gloved hands adjusting a pump: GRUNDFOS brand label clearly readable at full size, plus a boiler control panel. Subject is a pump, not a slab leak. No slab/foundation-water stock photo found. File deleted. |
| 57 | `/resources/how-long-does-water-damage-take-to-dry` hero | Pixel-identical to #16 flooded-basement hero (p-hash 1.00). No drying-equipment stock photo found on Pexels (air movers / dehumidifiers only exist as other companies' social posts — unusable). File deleted. |

## Closest-fit keeps (flagged, not perfect — pool-limited)

| # | Slot | Verdict |
|---|---|---|
| 2 | `/services/` hub hero | KEEP. Black-and-white cleaning crew with vacuum/mop. Loosely on-topic for a services hub; no better extraction-crew stock photo found. Alt is honest about what it shows. |
| 7 | `/services/emergency-water-damage-restoration` body | KEEP. Technician face close-up at work — on-topic for emergency response. |
| 16 | `/services/flooded-basement-cleanup` hero | KEEP as closest verified fit. Standing-water puddle on cracked concrete, no basement context in frame. No genuine flooded-basement stock photo exists on Pexels (searched 3 ways); the flooded-basement photos that exist are other businesses' social posts — unusable. |

## All other slots — KEEP (53)

Every other filled slot was viewed and is on-topic for its exact section:
heroes for all 17 services (except the two emptied above), all 19 area heroes
(representative US suburban houses — plausible Oklahoma, no false town claim
anywhere on site), all 10 remaining resource heroes, and the 7 remaining
body slots. No duplicate file across pages (p-hash re-run after swaps: 0
duplicate pixel pairs), no same-shoot pair on any one page.

## Empty-by-rule slots (unchanged)

- Sewage hero + categories hero: empty (no genuinely relevant photo) — branded panel.
- Ceiling body + flooded-basement body: empty — branded panel.
- Plus the 3 newly emptied slots above (#21 body, #29 hero, #57 hero).

## Final counts

- Filled: **57 slots (48 heroes + 9 bodies)**, 57 unique files, 0 dupes.
- Before this round: 60 slots (50 heroes + 10 bodies).
- All files 1200×800 WebP, max 149KB, 0 EXIF.
- Re-verified after rebuild: swapped images render on their pages
  (see site/FINDINGS-refine-round.md), nulled slots render branded panels.
