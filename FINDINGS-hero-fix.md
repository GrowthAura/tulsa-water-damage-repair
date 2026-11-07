# FINDINGS — Hero-fix round (2026-11-07)

Local only — no push/deploy/domain/DNS/token. Parent task: hero fix round + all
add-ons (sewage/slab/ceiling photos, table restyle, contact form restyle,
commercial 2-link list, "What Do We Handle?" cards, guides text, area-page
service cards, area SEO strips, full service-image audit + 2-3 images per
service page + branding, 2x A-to-Z testing).

## 0. Baseline (before this round, measured 2026-11-07 ~18:00 PKT)
- Home H1 top @1440 = **389px**, badge top 321px, hero media 448px.
- Inner pages H1 top @1440 = **269px**, eyebrow top 225px, media 304px.
- Overflow 0 @1440/390/320, console 0.
- Home hero = Pexels 3769711 (waiter mopping a restaurant floor — irrelevant).
- Sewage / slab-leak / ceiling heroes + bodies = null (navy panels).

## 1. MISS 1 — Home hero replaced (REAL photo, clash-cleared)
- **New: Pexels 21528760** — `public/images/home-tulsa-water-damage-repair.webp`
  (same filename, old waiter file overwritten), 1200x800 WebP, 64,610 B, 0 EXIF.
- Viewed by pixels (mine, not just the sourcing agent's): a carpeted room in a
  real home mid-restoration — opened wall exposing pipes/wiring, blue
  dehumidifier + grey air mover on the floor, power cord to an outlet, plastic
  sheeting taped on the left. Unmistakably water-damage drying work. NOT a
  waiter, NOT a restaurant.
- Alt (honest, no AI word, no em-dash): "Drying equipment, a dehumidifier and
  an air mover, in a carpeted room with an opened wall showing pipes and
  wiring, plastic sheeting on one side".
- Clash check vs rebuilt pool DB (`~/workspace/tulsa-water-damage-repair/pool_hashes.jsonl`,
  9,899 entries): md5 `fc5161e35443afea135c4728af4d2019` — 0 exact matches.
  Nearest neighbours pixel-checked side-by-side by me: Plano 3
  `bathroom-leak-12271457.webp` (B&W dripping-tap close-up) and
  `wet-carpet-4107278.webp` (person vacuuming a patterned rug) — both
  DIFFERENT photos. Cleared. Old clashed flooded-room hero 18302377 NOT used.
- Search terms tried (7): "flooded room standing water home", "pexels flooded
  room water damage", "pexels water extraction drying equipment home",
  "pexels wet floor water damage restoration", "pexels flooded basement
  water", "pexels flooded house interior water", "pexels water damage drying
  fan dehumidifier". Rejected near-misses: 12221947 / 30383694 (derelict),
  6471969 / 14823613 (aerial floods), 34801206 / 34801207 (flooded basement
  with Indonesian signage / commercial parking).

## 2. MISS 2 — Hero gap (FIXED, measured)
- CSS (`app/globals.css`): home media 28rem→20rem @1024 (21→16 base,
  24→18 @640); home content margin -13rem→-15rem @1024 (-11.5→-13 base);
  short media 19rem→14rem @1024 (16→12 base); short content margin
  -10rem→-11rem @1024 (-9→-9.5 base); brand-panel inner 21rem→12rem base,
  14rem @1024. No <hr> or divider exists between header and hero (verified in
  markup — the header's own 1px pale bottom border stays, subtle).
- Before → after (probe_after.py, `site/qa-hero-fix/after.json`):
  home H1 top @1440 **389px → 229px** (-160px), badge 321px → 161px, media
  448px → 320px; home H1 top @390 = 197px, badge 129px. Inner pages H1 top
  @1440 **269px → 173px** (-96px), eyebrow 225px → 129px, media 304px →
  224px; @390 = 165-196px. Overflow 0 @1440/390/320 on all 53 routes,
  console 0.
- Screenshots viewed by pixels: `after-home-1440-top.png` (badge sits just
  below the header, H1 right under it, the new drying-equipment photo fills
  the frame behind the H1 — opened wall + pipes visible) and
  `retake-home-390-top.png` (mobile: badge + H1 tight under the header, photo
  visible, sticky call bar below). Gap fixed.

## 3. MISS 3 — "Include?" H2 + section
- Measured the CURRENT build at 1440/1920/768/390 with a per-word line method:
  the H2 already wraps **"What Does Water Damage" / "Restoration in Tulsa
  Include?"** (4+4 words, no widow) at every desktop width, and 3 balanced
  lines at 390. The user's 7+1 screenshot ("Include?" alone) does NOT
  reproduce in the current build — it matches the pre-design-round live build.
  (The old probe's Range.getClientRects H2 measurement was flawed; the
  per-word method is the correct one.)
- Belt-and-braces fix anyway: `#what-does-water-damage-restoration-in-tulsa-include
  { max-width: 16em; }` — forces the 4+4 break even where `text-wrap: balance`
  is unsupported (line 1 ~590px, line 2 ~830px at 56px; 16em = 896px).
- Section made lovely: the Phase 1 / Phase 2 paragraphs are now two phase
  cards (`.phase-grid`, 2-col @1024; cream card, cyan top border, navy title).
  Words unchanged — the `<strong>` lead becomes the card title, the rest the
  card body. No other wording touched.
- H2 widow scan (all pages, per-word method, @1440 + @1920): exactly ONE
  other widow found sitewide — "/services/roof-leak-water-damage/" H2 "Why Is
  Roof Leak Damage Almost Always Underestimated?" wraps with "Underestimated?"
  alone on line 3 in the ~725px split column (both widths). Assessed, NOT
  force-fixed: `text-wrap: pretty` was tested and only moved the break (the
  last line stayed one word); no max-width can avoid it — the only non-widow
  split ("Why Is Roof Leak" / "Damage Almost" / "Always Underestimated?")
  needs a width ≥555px for line 3 but <516px to keep "Always" off line 2,
  impossible without changing words or font size (both off-limits). The last
  line is a 14-character word filling ~52% of the column — a substantial line,
  not a dangling short word like "Include?" was. It stays with `balance`.
  The "Include?" H2 itself is confirmed fixed (4+4, no widow).

## 4. Sewage / slab-leak / ceiling — no real photo exists (proven) → GENERATED
Photo child searched Pexels exhaustively (sewage 15 terms + web, slab 19 terms,
ceiling 11 terms + web): no genuinely relevant real photo exists for any of
the three. Per the user's standing rule ("jisk na mile khud bana lena"), all
six images (hero + body per page) were GENERATED and metadata-stripped:
- Sewage hero — basement laundry room, dark sewage water over the floor, worker
  with wet vacuum at a bubbling floor drain. 132,328 B q82.
- Sewage body — worker clearing a backed-up floor drain with a snake, dark
  water pooled around the drain. 126,138 B q77.
- Slab hero — worker kneeling at a jackhammered slab opening, leaking pipe +
  water inside. 128,796 B q82.
- Slab body — water seeping through a concrete crack, damp stain spreading.
  149,710 B q77.
- Ceiling hero — living-room ceiling, large brown stain + sagging peeling
  paint, drip falling into a bucket. 79,310 B q82.
- Ceiling body — stained peeling ceiling, drip into a bucket, fan + ladder.
  95,464 B q82.
- All six: 1200x800 WebP, ≤150KB, EXIF NONE (verified with PIL getexif),
  no AI word in filename/alt, honest alts describing exactly what the pixels
  show, no on-site claim they are real job photos. Viewed by pixels (contact
  sheets `/tmp/gen-sheet-1.jpg`, `/tmp/gen-sheet-2.jpg`) — all photorealistic
  and on-topic. NOT 30499666, NOT any destruction-gallery shot.
- Installed in `content/images.json` (sewage + ceiling entries filled; slab
  entry created under its exact slug `/services/slab-leak-water-damage/`).

## 5. Service-page image audit — every image judged by viewed pixels
Standard: the photo must unmistakably show the service's topic at first
glance (damage/water itself, restoration work/equipment in action, or the
specific appliance that is the service's subject). Rejected: generic cleaning,
a tool alone, a pristine real-estate room, place-wrong (palms, European old
town), destruction-gallery. 24 existing images audited (contact sheets
`/tmp/audit-sheet-1.png` … `/tmp/audit-sheet-4.jpg`):

KEPT (11): emergency hero (crew + extraction vacuum + van); water-mitigation
hero (wet/dry vacuum in a wet room); mold body (mold close-up);
flooded-basement hero (muddy standing water on concrete); storm body (fallen
tree in a US suburb); burst-pipe hero (water gushing from a broken pipe);
hardwood body (water droplets on wood); roof hero (roofers on a roof);
smoke-soot hero (charred beams); fire hero (fire-gutted room — fire damage
genuinely looks like this); fire body (fire-truck ladder spraying smoke).

REPLACED (13 — real Pexels first, generate only if none exists; sourcing
child's verdict `/tmp/hero-fix-replacements/VERDICT.md`, 8 image-search
rounds, ~60 queries + Pexels pages):
- **Real picks installed (3):** mold hero = Pexels 4176061 (hazmat worker
  fogging a living room with a misting wand — remediation/PPE work; honest
  caveat: no mold visible, it is fogging work); storm hero = Pexels 32394147
  (uprooted tree across a residential street, suburban houses, overcast — no
  palms, no European old town; houses possibly Australian but no
  place-identifying markers); roof body (new 2nd image) = Pexels 37623613
  (roofer in a red hard hat prying a wavy roof sheet; corrugated sheet, not
  US shingles — roof repair work, clearly relevant). All three pixel-checked
  by me (`/tmp/picks-sheet.jpg`), clash-cleared (0 md5 matches; nearest
  neighbours pixel-checked different), 1200x800, ≤150KB, 0 EXIF.
- **Burst-pipe body — real pick REJECTED by me, generated instead:** Pexels
  8678665 existed (rusty pipe in a concrete wall, water dripping from a
  joint) but the child flagged it borderline (a drip, not a burst; dark
  industrial room, no home context). Per the user's 1001% standard I
  generated a stronger one: water spraying from a broken copper pipe in a
  laundry room, plumber reaching for the valve. Reported plainly here.
- **Generated (11 of the 13):** emergency body (dehumidifier + air mover on
  a wet living-room floor), mitigation body (air movers + dehumidifier along
  a damp wall), flood hero (flooded living room, standing water around sofa
  and coffee table), flood body (worker with wet vacuum in a flooded living
  room), commercial hero (flooded office, standing water + sagging ceiling
  tiles), commercial body (air movers + dehumidifier on a wet office
  carpet), hardwood hero (cupped/buckled wet planks + drying mats), AC hero
  (water dripping from a wall-mounted AC into a bucket, stained wall),
  appliance hero (washing machine leaking water onto the laundry room
  floor), water-heater hero (tank in a garage, water pooling at its base),
  plus burst-pipe body (see the bullet above).
  All pixel-checked by me (`/tmp/gen2-sheet-1.jpg` … `-3.jpg`) —
  photorealistic, on-topic, no text/watermark, faces small/partial.
  The real-photo search for each is documented in the child's VERDICT.md
  (near-misses + why each failed: derelict, place-wrong, pool-blocked,
  size-fail, or no water visible).
- All 16 new images: 1200x800 WebP, ≤150KB, 0 EXIF (verified per file with
  PIL getexif after optimize), no AI word in filename/alt, honest alts
  describing exactly what the pixels show, no on-site claim they are real
  job photos. Generated files carry no AI-generator metadata (the generator
  output had 0 EXIF; re-encode strips everything).

NEW BODIES (6 — hero-only pages now get a 2nd image; 1 real + 5 generated):
flooded-basement body (GENERATED: dehumidifier + air movers + wet vacuum on
a wet concrete basement floor), AC body (GENERATED: water-stained ceiling and
wall under an AC drain line, towel on the wet floor), appliance body
(GENERATED: technician pulling out a leaking dishwasher, water on the kitchen
floor), water-heater body (GENERATED: hands tightening a valve on a leaking
heater with a wrench, water dripping into a bucket), roof body (REAL Pexels
37623613, see above), smoke-soot body (GENERATED: worker in a mask wiping
black soot from a wall, half cleaned).
Per-service image count after this round: every service page now has 2-3
images (hero + body; the 6 sewage/slab/ceiling pages also have hero + body
from section 4). No service page is left with a panel or a single image.

## 6. Branding on service images — DONE
Tasteful brand mark baked into every service-page image file (heroes +
bodies): the header's own mark — navy rounded square + cyan water drop with
white highlight + thin cyan ring — 72px (6% of width), bottom-right, 20px
margin, never over the subject's centre. Applied by
`site/tools/optimize_brand_images.py --brand` — **36 service images branded**
(18 service pages x hero + body). Verified by pixels (`/tmp/brand-check.jpg`):
the mark is small, premium, not gaudy, on both a dark photo (flood hero) and
a bright one (mold hero). The home hero is NOT branded (it is not a
service-page image). Final audit after branding: all 36 files 1200x800,
**≤150,000 B** (largest: commercial hero 147,424 B), 0 EXIF. (Two files came
out of the optimizer at 151,974 B / 150,022 B — over a strict 150,000 B cap —
the branding re-encode brought them to 147,424 B / 144,528 B, under the cap.)

## 7. Tables restyled (homepage "Tulsa County and nearby communities" + all tables)
- `.table-wrap`: card border + shadow kept; header now a navy→blue gradient
  with a 3px cyan rule underneath; zebra rows (cream), hover row tint
  (blue-gray); cells roomier (0.95rem 1.25rem); city links blue, bold, no
  underline until hover (pale underline → cyan on hover). Same treatment
  applies sitewide (services-hub "Which Service Do I Need?" table shares
  `.table-wrap`). No word/link/URL/ZIP changed.
- **Defect found by pixel-checking the retake and FIXED:** the header labels
  ("City / Zip codes / Page") were INVISIBLE — dark navy text on the navy
  gradient. Cause: the cells are `<th><strong>City</strong></th>` and the
  global `.content-block strong { color: var(--navy); }` rule beat the
  inherited cream on the `<strong>`. Fix: `.table-wrap thead th strong
  { color: var(--cream); }` (globals.css). Rebuilt + re-shot:
  `retake-table-1440c.png` — header labels now clearly readable in cream on
  the gradient, cyan rule below, zebra rows, bold blue links. Verified by
  pixels. (Lesson: computed style on the `th` looked right — the `<strong>`
  inside was the culprit; always check the inner element.)

## 8. Contact form restyled (/contact/)
- `.form-card`: 16px radius, deeper shadow, padding 2rem (2.25/2.5 @640);
  title 1.5rem navy; labels 1rem navy; fields white (was cream), 1.5px
  #c9d6e3 border, 10px radius, 0.85rem 1rem padding; hover border darkens;
  focus = blue border + 3px cyan ring (no outline); textarea min-height 8rem,
  vertical resize; submit = navy→blue gradient, 1rem padding, 1.2rem font.
- Labels, wording, fields UNCHANGED; form still NOT wired to any inbox (the
  "not connected to an inbox yet" note is kept verbatim — no fake send).
- Screenshot verified by pixels (`retake-contact-1440.png`): white card, navy
  labels, white fields with borders, large textarea, gradient "Send Message"
  button. The left column's map iframe is present in the built HTML (Google
  Maps embed for 400 S 129th E Ave, Tulsa, OK 74108) but renders as an empty
  white card in this sandbox's headless browser (Google unreachable from the
  probe) — not a styling defect; maps were verified live in the earlier
  refine round.

## 9. Commercial list — exactly 2 links kept (CORRECTED instruction)
- `/commercial/` "Which Commercial Restoration Services Do We Offer?" list
  (`content/pages.json`, block 6): links KEPT on (1) Commercial water damage
  restoration → `/services/commercial-water-damage`, (2) Flood damage
  restoration → `/services/flood-damage-restoration`. Links REMOVED from the
  other five (Sewage backup cleanup, Mold remediation, Storm damage repair,
  Fire damage restoration, Smoke and soot cleanup) — bold names kept as plain
  text, all other wording unchanged. Scope: ONLY this list. Similar linked
  service lists elsewhere (homepage grouped lists, services hub) NOT changed —
  pending his call. **Built-HTML verification: PASSED** — probe counted
  exactly 2 links in the list, the right two (Commercial water damage
  restoration → /services/commercial-water-damage, Flood damage restoration →
  /services/flood-damage-restoration).

## 10. "What Do We Handle?" → cards (/about-us/)
- Note: the section lives on **/about-us/** (blocks 11-20), not the homepage.
- Blocks 13-19 (7 category paragraphs) now render as a `ServiceListCards`
  grid (same premium card language as the services hub, each with its own
  service hero image; sewage/slab/ceiling cards use the panel until their new
  photos land, then the photo automatically). Block 20 ("See the full services
  directory:") renders as a bold link below the grid (`.handle-more`).
- Labels + descriptions verbatim (including the trailing colon on labels);
  each card's title links to the same target the paragraph's first link
  pointed to; multi-link paragraphs (By water source / By damage type) keep
  their inner service links inside the card body.
- **Defect found by the after-probe and FIXED:** the grid rendered 0 cards —
  `groupBlocks` collected the list paragraphs only when they came IMMEDIATELY
  after the h2, but an intro paragraph (block 12) sits between the h2 and the
  list, so the run collected zero items. Fix: the handle branch now passes
  non-list blocks through first (stopping at the next h2/hr), then collects
  the list run. Rebuilt + re-measured: **7 cards** (titles verbatim with
  colons) + the "See the full services directory:" link → /services/.
  Screenshot verified by pixels (`retake-about-handle-1440.png`): 7 premium
  cards with images, inner links intact inside the "By water source" /
  "By damage type" cards.

## 11. Guides text bigger (pages + hub cards)
- Guide (resource) pages: body paragraphs + list text 18px → **20px**
  (`.page-resource .content-block > p/li/.faq-answer p { font-size: 1.25rem }`),
  scoped by a new `page-{type}` class on the inner section — sitewide text
  untouched, headings unchanged. **Measured: 20px** on a resource page
  (probe: p 20px, li 20px) vs 18px on the service-page control. Screenshot
  verified by pixels (`retake-guide-1440.png`): body + list text clearly
  larger, H2 unchanged, no overflow.
- /resources/ hub cards (`ResourceCards` + `.resource-cards`): titles
  1.25rem → **1.5rem**, blurbs 1.125rem → **1.25rem**. **Measured: h3 24px,
  p 20px** on the hub (10 cards). Screenshot verified by pixels
  (`retake-resources-1440.png`): titles + blurbs clearly larger, no awkward
  wraps at 1440.
- Interpretation note: "guides" = the 10 `resource`-type pages under
  /resources/ (there is no `guide` page type). If he meant something else,
  he can correct it.

## 12. Area pages — offer lists → image cards + SEO strip
- Block `ul` case now converts service-shaped lists on `area` pages too
  (`serviceListItems` guard: every item must have exactly one `/services/`
  href). Verified in data first: exactly ONE such list per area page (the
  offer list, 5-8 items); all other area-page lists fail the guard and stay
  plain bullets. **Brookside has no offer list at all** (its page is
  causes/drying/areas/lead-paint/cost) — so no cards and no strip there;
  nothing was invented for it.
- Cards use each service's own hero image via `ServiceListCards` (sewage /
  slab / ceiling cards get the panel until their new photos land, then the
  photo automatically). Wording verbatim, links preserved as card links.
- NEW SEO strip below the cards on all 18 area pages with an offer list:
  H3 **"Most In-Demand Services in [City]"** (chosen over "Hot Services" —
  more professional, same meaning) + that page's own services as
  "Service Name in City" (title-cased per his examples, e.g. "Emergency Water
  Damage Restoration in Bixby"; source list text untouched elsewhere), each
  BOLD blue with a cyan check, in a cream strip card, 2-col @1024. Plain text
  ONLY — no links. City name taken from the page's own offer H2
  ("... in South Tulsa?" → "South Tulsa"), never from the slug.
- **Verified by the probe (all 19 area pages):** 18 pages with offer lists
  have cards (5-8 each, matching their list counts) + the strip with the
  correct H3 and item count (Bixby 7, Broken Arrow 6, South Tulsa 8, Coweta 5,
  Collinsville 5, the rest 6-7). Brookside: 0 cards, no strip (no offer list
  — as expected, nothing invented). Screenshots verified by pixels:
  `retake-bixby-cards-1440.png` (cards with images — emergency, mitigation,
  flood, sewage with the new generated basement photo), `retake-bixby-strip-390.png`
  + `retake-broken-arrow-strip-390.png` (mobile: single-column strip, all
  items with city names, clean). Cherry Street's city reads "Cherry Street and
  the Pearl District" — taken verbatim from that page's own offer H2, as briefed.

## 13. Testing — Round 1 + Round 2 (BOTH DONE, both clean)
Two separate fresh A-to-Z passes on the FINAL build (after all images +
branding installed), each run independently — not one recycled report.

**Round 1** (2026-11-07 ~18:36 PKT): `tools/probe_a2z.py` — 53 routes,
overflow 0, H1=1 everywhere, console 0, card images home 37/37, services hub
18/18, resources 8/8, internal refs 159, broken 0, sitemap 53, FAQ mismatches
0. `tools/verify_site.py` — 53 pages, 2,576 internal link fetches all 200,
PROBLEMS 0. Fresh screenshots viewed by pixels: flood, mold, commercial,
storm, AC, hardwood, sewage, ceiling heroes all render correctly on their
pages (r1-*.png). **Defects found: 0.**

**Round 2** (2026-11-07 ~18:38 PKT): fresh re-run of both tools, identical
clean results (probe_a2z: same lines; verify_site: 2,576 fetches all 200,
PROBLEMS 0). Plus a focused re-check of every round-specific item on the
final build: H1 tops home 229 / inner 173 (unchanged), commercial list
exactly 2 links (the right two), about handle 7 cards + more link, home
phase cards 2 + Include H2 width 896px, guide body 20px, Bixby 7 cards +
7 strip items, Broken Arrow 6+6, Owasso 6+6, and all 18 service pages render
their hero + body images (DOM check: no missing/broken). **Defects found: 0.**

**Defects found and fixed during this round (before testing):**
1. Handle cards rendered 0 — intro paragraph between the h2 and the list
   broke the grouping (fixed: pass non-list blocks through first).
2. Table header labels invisible — `.content-block strong` navy beat the
   inherited cream on the `<strong>` inside `<th>` (fixed: `.table-wrap
   thead th strong { color: var(--cream); }`).
3. Roof-leak H2 widow — assessed, no fix possible without changing words or
   font size (see section 3); `text-wrap: pretty` tested and reverted.

**1-hour window:** the round is complete inside it (ordered ~18:11 PKT,
testing done ~18:40 PKT). Nothing left half-done from this round's brief.
