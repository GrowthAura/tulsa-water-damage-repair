# FINDINGS — Cross-Site Image Audit + Replacement
## Tulsa Water Damage Repair — 2026-11-07

**Site:** `~/workspace/tulsa-water-damage-repair/site/` (Next.js 14 static export)
**Live mapping:** `site/content/images.json` (52 entries) — read by `app/lib.js` pageImage().
`content/images-a.json` / `images-b.json` are STALE working files: **not used, not edited**.
**Scope:** LOCAL ONLY — no push / deploy / domain / DNS / token. No rebuild, `out/` untouched,
`content/pages.json`, `app/globals.css`, `app/[[...slug]]/page.js`, `app/components/Shared.jsx`,
header/footer untouched. All replacements IN PLACE (same filename in `public/images/`).

## Method

- **This site:** 57 files in `public/images/` (all WebP), md5-unique within site.
- **Pool:** every other site directory under `~/workspace/` — image files only under
  directories named `public/` / `images/` / `assets/` / `out/` (maxdepth 4), excluding this
  site, `node_modules`, `.next`, `qa-*`, `screenshots*`, `backups`, `tools`, `_build`, `tmp*`,
  `.git`, `gh-pages-staging`. **17,144 files, 4,061 unique md5s, 4,060 hashed**
  (1 unreadable: `gmb-videos/assets/dmc-logo.png`).
- **Hashes:** md5 + 16×16 aHash + 16×16 dHash (PIL + numpy; ImageHash not installed).
- **Judgement:** same-photo vs merely similar-scene decided by **viewed pixels only**, never by
  hash alone. Contact sheets in `/tmp/clash-sheets/`, `/tmp/borderline-*.jpg`,
  `/tmp/borderline-b*.jpg`, `/tmp/final-check-*.jpg`, `/tmp/check-*.jpg`, `/tmp/cand-*.jpg`.
- **Pexels method:** direct `images.pexels.com` URLs
  (`https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=1200&h=800&fit=crop`),
  search pages fetched with Windows Chrome UA + full headers. Blocklist of Pexels IDs already
  used anywhere (312 IDs from pool filenames + known Tulsa IDs + Sep-2024 flood series
  28447760–28447819).

### ⚠️ KEY LESSON — the aH≤20 threshold was TOO TIGHT (found in the deep re-check)

The first pass flagged only aH≤20 / dH≤20 and found 21 clashes. A second, deeper pass
pixel-checked the nearest pool neighbour of **every** file with aH≤75 — and found **1 more
genuine repeat among the "kept" files** (commercial body, aH=38) plus **3 of my own first
picks that were also repeats** (aH 22, 49, 60). Same-photo different-crop pairs observed:

| pair | aH | dH | what happened |
|---|---|---|---|
| water-heater pick 28479466 vs Lancaster sec2 | 22 | 42 | same laundry room, different crop |
| commercial body (kept) vs Lancaster water-extraction sec1 | 38 | 57 | same yellow vacuum, different crop |
| mold-hero pick 6141203 vs Lancaster mold-testing sec1 | 49 | 68 | same mold wall, different crop |
| burst-body pick 13726337 vs Lancaster slab-leak | 60 | 59 | same valve + black pipe, tighter crop |
| burst-body cand 8486978 vs Lancaster about-us | 72 | 106 | same worker, face-only crop vs half-body |
| wet-floor cand 7451918 vs Lancaster commercial sec2 | 31 | 55 | same sign + store, wider crop |

**Rule going forward: hash distance does NOT clear a photo. Every candidate and every kept
file's nearest pool neighbour must be pixel-checked.** In total 46 nearest-neighbour pairs
were pixel-checked in the deep re-check; 4 were repeats, 42 were different photos.

## Audit table — 22 confirmed cross-site repeats

"Distance" is aHash / dHash Hamming distance (16×16 = 256 bits). Old Pexels ID is given
only where it is known (from FINDINGS-images-101.md or from the other site's filename);
"unknown" means the other site's filename carries no Pexels ID.

| # | This file (slot) | Other site + file it matched | aH / dH | Old Pexels ID |
|---|---|---|---|---|
| 1 | `home-tulsa-water-damage-repair.webp` (home hero) | Plano3 `public/images/flooded-floor-18302377.webp` **and** Lancaster `public/assets/img/emergency-water-damage-restoration-lancaster-ca-sec1.webp` (same photo, different crop) | 0 / 0 and 25 / 19 | 18302377 |
| 2 | `resources-how-to-prevent-frozen-pipes-tulsa-tulsa-water-damage-repair.webp` (frozen-pipes hero) | Texas `assets/img/dumas-snow-icicles-brick-house.jpg` | 1 / 1 | unknown |
| 3 | `resources-mold-after-water-damage-tulsa-tulsa-water-damage-repair.webp` (mold-after hero) | Boynton Beach `site/public/images/mold-wall-growth-1200.jpg` (+600 variant) | 2 / 8 | unknown |
| 4 | `resources-water-damage-restoration-cost-tulsa-tulsa-water-damage-repair.webp` (cost hero) | Cape Coral `public/images/img-cost.jpg` | 0 / 11 | unknown |
| 5 | `service-areas-east-tulsa-tulsa-water-damage-repair.webp` (east-tulsa hero) | Cape Coral `public/images/img-roof-house.jpg` | 0 / 5 | unknown |
| 6 | `service-areas-north-tulsa-tulsa-water-damage-repair.webp` (north-tulsa hero) | Plano `public/images/contact-areas-plano-street-photo.webp` (+480/600/800 variants) | 0 / 1 | unknown |
| 7 | `service-areas-owasso-ok-tulsa-water-damage-repair.webp` (owasso hero) | Tulsa Hardwood `site-wilson/public/img/tulsa-suburban-house-porch-lawn.jpg` | 1 / 2 | unknown |
| 8 | `service-areas-sapulpa-ok-tulsa-water-damage-repair.webp` (sapulpa hero) | Tulsa Hardwood `site-wilson/public/img/sapulpa-suburban-house-driveway.jpg` **and** Plano3 `public/images/suburban-house-exterior-8583638.webp` (+400/800) | 0 / 1 and 1 / 0 | 8583638 |
| 9 | `service-areas-south-tulsa-tulsa-water-damage-repair.webp` (south-tulsa hero) | Texas `assets/img/texas-home-driveway.jpg` (+ `ts-spaces/texas-water-damage-site-preview` copy) | 0 / 5 | unknown |
| 10 | `services-appliance-leak-water-damage-tulsa-water-damage-repair.webp` (appliance hero) | Plano `public/images/laundry-leak-photo.webp` (+480/600/800) | 1 / 2 | unknown |
| 11 | `services-burst-pipe-water-damage-tulsa-water-damage-repair-drying-equipment.webp` (burst body) | Plano `public/images/about-contact-photo.webp` **and** Plano3 `public/images/plumber-work-6419128.webp` **and** Texas `assets/img/andrews-plumber-pipe-repair.jpg` | 0 / 0, 1 / 0 | 6419128 |
| 12 | `services-burst-pipe-water-damage-tulsa-water-damage-repair.webp` (burst hero) | Plano3 `public/images/burst-pipe-15206136.webp` **and** Boynton `site/public/images/leaking-pipe-plastic-1200.jpg` | 0 / 0 and 0 / 1 | 15206136 |
| 13 | `services-ceiling-water-damage-tulsa-water-damage-repair.webp` (ceiling hero) | Boynton `site/public/images/collapsed-ceiling-room-1200.jpg` | 0 / 1 | unknown |
| 14 | `services-commercial-water-damage-tulsa-water-damage-repair.webp` (commercial hero) | `ts-spaces/lynnwood-water-damage-website-preview/assets/img/img-drying-cleanup.jpg` | 0 / 1 | unknown |
| 15 | `services-flood-damage-restoration-tulsa-water-damage-repair.webp` (flood hero) | Plano Blackland `site/assets/img/flood-damage-restoration-plano-tx.jpg` **and** Plano `public/images/flood-different-street-water-photo.webp` **and** Cape Coral `public/images/photo-flood-house.jpg` **and** `state-site-build/site/assets/hero.jpg` | 0 / 2, 1 / 1 | 28447774 |
| 16 | `services-mold-remediation-tulsa-water-damage-repair-drying-equipment.webp` (mold body) | Plano3 `public/images/indoor-mold-18063447.webp` **and** Cape Coral `public/images/svc-mold.jpg` | 0 / 6, 1 / 11 | 18063447 |
| 17 | `services-mold-remediation-tulsa-water-damage-repair.webp` (mold hero) | Plano3 `public/images/mold-wall-18351809.webp` | 0 / 1 | 18351809 |
| 18 | `services-roof-leak-water-damage-tulsa-water-damage-repair.webp` (roof hero) | Cape Coral `public/images/img-roof.jpg` **and** Texas `assets/img/keller-roof-replacement-brick-home.jpg` | 1 / 7, 1 / 8 | unknown |
| 19 | `services-storm-damage-repair-tulsa-water-damage-repair.webp` (storm hero) | Cape Coral `public/images/split-how.jpg` | 0 / 5 | unknown |
| 20 | `services-water-heater-leak-cleanup-tulsa-water-damage-repair.webp` (water-heater hero) | Plano `public/images/attic-water-heater-photo.webp` (+480/800) | 1 / 0 | unknown |
| 21 | `services-water-mitigation-tulsa-water-damage-repair-drying-equipment.webp` (mitigation body) | Texas `assets/img/henderson-water-extraction-technician.jpg` **and** Plano3 `public/images/water-extraction-6195949.webp` | 1 / 1, 1 / 2 | 6195949 |
| 22 | `services-commercial-water-damage-tulsa-water-damage-repair-drying-equipment.webp` (commercial body) — **found only in the deep re-check** | Lancaster `public/assets/img/water-extraction-services-lancaster-ca-sec1.webp` (same yellow wet/dry vacuum + hose + nozzle on grey tiles, different crop) | 38 / 57 | unknown |

Exact md5 clashes: **0** (all repeats were re-encodes / different crops, not byte-identical files).
Within-site dupes before the round: **0**.

## Replacements — 21 replaced in place + 1 emptied

Every replacement: fresh real photo from Pexels, 1200×800 WebP ≤150KB, 0 EXIF, no AI-related
word in filename/alt/metadata, honest alt text (only what the pixels show). Alt updated in
`content/images.json` only; `content/pages.json` words untouched. Old files backed up to
`/tmp/old-clash-backup/` (22 files: the 21 originals + the commercial-body original).

| # | Slot / file | Old Pexels ID / scene | New Pexels ID | New size | Q | New alt (in `images.json`) |
|---|---|---|---|---|---|---|
| 1 | home hero `home-tulsa-water-damage-repair.webp` | 18302377 / flooded room | **3769711** | 72,578 B | 82 | A man mopping a wet wooden floor in a dining room with chairs stacked on tables |
| 2 | frozen-pipes hero | unknown / snow house + icicles | **11118906** | 40,734 B | 82 | Long icicles hanging from the eaves of a house roof under a blue sky |
| 3 | mold-after hero | unknown / mold on brick | **30397833** | 148,212 B | 60 | A cracked wall with peeling paint and dark damp patches after water damage |
| 4 | cost hero | unknown / calculator + dollars | **6694916** | 65,406 B | 82 | A calculator showing figures beside a stack of dollar bills and printed cost documents on a wooden desk |
| 5 | east-tulsa hero | unknown / beige house | **20296321** | 141,998 B | 75 | A light blue-grey two-story suburban house with white-trimmed windows behind a trimmed hedge |
| 6 | north-tulsa hero | unknown / brick townhouses | **10628470** | 151,128 B | 82 | A row of modern three-story townhouses with garages and concrete driveways under a blue sky |
| 7 | owasso hero | unknown / blue house + porch | **4682075** | 152,144 B | 70 | A light grey two-story house with a double front porch and balcony, green lawn and trees behind |
| 8 | sapulpa hero | 8583638 / green house | **35742592** | 50,280 B | 82 | A blue-grey two-story suburban house with white trim and a garage, neighbouring houses on both sides |
| 9 | south-tulsa hero | unknown / beige house + stone base | **24524484** | 143,750 B | 82 | A white house with blue double garage doors, paved driveway and garden beds under a cloudy sky |
| 10 | appliance hero | unknown / laundry leak | **17181948** | 107,974 B | 82 | A home laundry room with a white washing machine and dryer under wooden wall cabinets |
| 11 | burst body | 6419128 / gloved hands + pipe fittings | **35869441** (round 2) | 30,404 B | 82 | A red pipe wrench on a black background |
| 12 | burst hero | 15206136 / dripping pipe joint | **4406593** | 61,028 B | 82 | Water gushing out of a broken pipe |
| 13 | ceiling hero | unknown / collapsed ceiling room | **EMPTIED to branded panel** (see below) | — | — | hero: null in `images.json` |
| 14 | commercial hero | unknown / red coveralls + vacuum | **9462135** | 68,488 B | 82 | A cleaner vacuuming a hard floor with a red vacuum cleaner beside a wall radiator |
| 15 | commercial body | unknown / yellow wet/dry vacuum | **9462766** (round 2) | 33,218 B | 82 | A hand in a pink rubber glove scrubbing white wall tiles with a green brush |
| 16 | flood hero | 28447774 / flooded house | **35249003** (re-pick) | 122,466 B | 82 | People wading through floodwater on a flooded residential street between rows of houses |
| 17 | mold body | 18063447 / mold spots | **36458949** | 62,740 B | 82 | A close-up of pale mould growth with fine stalks spreading across a dark surface |
| 18 | mold hero | 18351809 / mold wall | **28576635** (round 2) | 37,712 B | 82 | A person in yellow rubber gloves spraying and wiping a wall with a cleaning spray |
| 19 | roof hero | unknown / roofers + shingles | **38749872** | 94,920 B | 82 | Two roofing workers on a house roof carrying buckets under a clear blue sky |
| 20 | storm hero | unknown / collapsed ceiling room | **16313103** | 48,680 B | 82 | Palm trees bending in strong wind under a grey storm sky |
| 21 | water-heater hero | unknown / heater in cabinet | **8142983** (round 2) | 44,460 B | 82 | A white wall-mounted water heater above a washing machine in a white tiled bathroom with a mirror and sink |
| 22 | mitigation body | 6195949 / worker + vacuum | **6195274** (re-pick) | 56,124 B | 82 | Two cleaners vacuuming and mopping a living room floor in a black-and-white photo |

### Ceiling hero — emptied, not replaced
`services-ceiling-water-damage-tulsa-water-damage-repair.webp` (99,232 B) **deleted**; hero set
to `null` in `images.json` (branded panel renders instead). Reason: no genuine ceiling
water-damage photo exists on Pexels after 3 search rounds ("collapsed ceiling room",
"water stain ceiling", "water damaged drywall", "ceiling stain"); the only genuine
collapsed-ceiling photos are the current hero itself (Boynton repeat) and Pexels 30499666
(Plano 3's user-rejected destroyed-room gallery shot, also a repeat). Precedent: 3 slots
emptied the same way in the 101% round (sewage body, slab-leak hero, dry-time hero).
Backup candidate 11427055 (gloved hand sealing drywall) was judged filler, not used.

## Rejected picks — caught by verification, never shipped

| Slot | Rejected Pexels ID | Why (pixel-confirmed) |
|---|---|---|
| flood hero | 17682749 | pixel-identical to Texas `assets/img/dickinson-flooded-street-homes.jpg` (aH=0/dH=1) |
| mitigation body | 6195129 | pixel-identical to Biohazard `public/images/cleaning-team-equipment-oklahoma.jpg` (aH=0/dH=1) |
| water-heater hero | 28479466 | same laundry room + same two washers + same heater as Lancaster `water-heater-leak-cleanup-lancaster-sec2.webp` (aH=22/dH=42, different crop) |
| mold hero | 6141203 | same mold wall as Lancaster `mold-testing-lancaster-ca-sec1.webp` (aH=49/dH=68, different crop) |
| burst body | 13726337 | same valve + black pipe as Lancaster `slab-leak-water-damage-lancaster-ca.webp` (aH=60/dH=59, tighter crop) |
| commercial body (candidate) | 7451918 | same "CAUTION WET FLOOR" sign + store as Lancaster `commercial-water-damage-restoration-lancaster-ca-sec2.webp` (aH=31/dH=55) |
| burst body (candidate) | 8486978 | same worker (hi-vis + green gaiter) as Lancaster `about-us.webp` (aH=72/dH=106, face-only crop) |
| burst body (candidate) | 33388390 | exact pool match: Plano3 `public/images/plumber-work-33388390.webp` (aH=1/dH=0) |
| burst body (candidate) | 35290675 | exact pool match: Plano3 `public/images/plumber-work-35290675-400.webp` (aH=0/dH=4) |
| burst body (candidate) | 8488035 | exact pool match: Boynton `site/public/images/exposed-plumbing-pipes-1200.jpg` (aH=0/dH=7) |
| commercial body (candidate) | 6196694 | **not** a cross-site repeat (pool nearest aH=73, pixel-checked different) — NOT USED because it is the same photoshoot (same person, red coveralls, yellow vacuum) as the removed commercial hero; would look like the old photo to the user |

Rejected first picks are backed up in `/tmp/bad-picks-backup/` (water-heater, mold-hero, burst-body).
The filename-based Pexels-ID blocklist did **not** catch these: the other sites use descriptive
filenames with no Pexels ID in them (notably the Lancaster site, which shares many Pexels
photos with this site's picks). Hash-checking every candidate against the pool **before**
selecting, plus pixel-checking the nearest neighbour, is what caught them.

## Known weaknesses / judgement calls

- **South-tulsa hero (24524484):** European look (tiled roof, blue garage doors) — best
  available after 3 search rounds; place-fit is weaker than the other area heroes.
- **Mold hero (28576635):** a cleaning-action photo (gloves spraying/wiping a wall), not mold
  growth itself — the mold-growth candidates on Pexels were all repeats on Lancaster/Plano3.
  Mold growth is still shown on the same page by the mold body (36458949).
- **Storm hero (16313103):** palm trees in wind, chosen over a destroyed-room photo (35531302)
  to avoid the destruction-gallery category the user banned.
- **Mold hero first pick (6141203)** needed WebP q30 to fit under 150KB (152,068 B); the
  round-2 replacement (28576635) fits at q82 (37,712 B), so the q30 file is gone.
- **Services hub image** (`services-tulsa-water-damage-repair.webp`, B&W cleaning team of 3)
  and the mitigation body (6195274, B&W cleaners) are from the same photoshoot series but
  are **different photos** — within-site pairwise check: 0 near-dupe pairs.
- **8142983 vs 8142971 (water-heater candidates):** two different angles of the same bathroom
  (same heater, same tiles) — different photos, only 8142983 used.

## Final verification (re-run 2026-11-07, logs `/tmp/verify_final_r2.log` + `/tmp/verify_tail.py`)

- **56 files** (57 − 1 deleted ceiling file): **0 format/dims/size/EXIF fails** — all 1200×800
  WebP, ≤150KB (largest: hardwood body 152,872 B, owasso 152,144 B, sand-springs 151,676 B,
  fire hero 151,450 B, north-tulsa 151,128 B), 0 EXIF tags.
- **21 files changed** vs the pre-round md5 list (`/tmp/tulsa57.md5`) — exactly the 21
  replaced clash files; the other **35 kept files' md5s are unchanged**.
- **Replaced files vs the ORIGINAL photo:** aH 111–161 / dH 108–152 (clearly different photos).
  Round-2 files vs their rejected first pick: aH 134–149 / dH 118–130.
- **Nearest pool neighbour for all 56 files:** every file with aH≤75 was pixel-checked
  (46 pairs in the deep re-check + 3 final pairs + candidate checks) — **all different
  photos; 0 remaining clashes**. Closest remaining: sapulpa aH=27 (vs Lancaster desert
  landscape — different), storm aH=30 (same desert — different), burst body aH=44 (vs
  Plano3 copper pipes — different), frozen-pipes aH=45 (vs Plano3 fire sprinkler — different).
- **Within-site near-dupe pairs: 0.**
- **`images.json`:** 52 entries, ceiling hero null, 0 missing-file references, 0 alt mismatches,
  no standalone "AI" word in any alt.
- **Not touched:** `content/images-a.json` / `images-b.json` (mtime 2026-11-07 09:36),
  `content/pages.json` (mtime 2026-11-07 11:01), `out/`, CSS, page code, header/footer.
  No other file under `site/` changed during this round.

## Final counts

| | |
|---|---|
| Slots audited | **57** |
| Cross-site repeats found | **22** (21 in first pass + 1 commercial body in deep re-check) |
| Replaced in place | **21** |
| Emptied to branded panel | **1** (ceiling hero) |
| Kept (md5 unchanged) | **35** |
| Unique files now | **56** |
| Remaining cross-site clashes | **0** |
| Within-site dupes | **0** |

## Working files (not part of the site)

- Manifest: `/tmp/replacements_manifest.json`
- Originals backup: `/tmp/old-clash-backup/` (22 files)
- Rejected first picks backup: `/tmp/bad-picks-backup/` (3 files)
- Pool hashes: `/tmp/pool_hashes.json`
- Verification logs: `/tmp/verify_final.log`, `/tmp/verify_final2.log`, `/tmp/verify_final_r2.log`
- Contact / check sheets: `/tmp/clash-sheets/`, `/tmp/borderline-*.jpg`, `/tmp/borderline-b*.jpg`,
  `/tmp/final-check-*.jpg`, `/tmp/check-*.jpg`, `/tmp/cand-*.jpg`
