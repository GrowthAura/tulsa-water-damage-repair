# Testing Round 1 — structural verification (ORIGINAL RUN, 2026-11-07 ~13:25 PKT)

> NOTE (2026-11-07 ~14:40 PKT, refine round): tools/verify_site.py hardcodes its
> output path to this file, so re-running it for the refine round overwrote the
> original Round 1 log. This file is a reconstruction from PROGRESS.md, which
> records the Round 1 outcome in full. The fresh refine-round structural run
> now lives in site/FINDINGS-refine-round.md.

- Pages checked: 52/52, 200 both URL forms
- H1=1 on every page; titles/descriptions/canonicals/og:url verbatim vs doc
- 3,078 internal link fetches, all 200; 0 orphans; sitemap 52 URLs, no image entries; robots OK
- FAQ schema = visible Q&A
- Result: PASSED, 0 problems

Fixes made in-round:
1. Next.js forced canonical + og:url to slash form — now rendered manually with the doc's exact mixed forms.
2. Orphan resource page (/resources/water-damage-vs-flood-damage-insurance-oklahoma, zero inbound body links) fixed with a footer Resources column.
3. Verifier bugs fixed (JSON-LD list unwrap, entity-escaped descriptions, BFS slash normalization).

Round 1 visual (separate run, same day): 6 defects found + fixed + re-verified —
mobile overflow 37/52 → 0; 5 service cards wrong-slug/no-image → 17/17 loaded;
homepage reveal never mounted → 46/46 .in; double-escaped entities in 69 files → 0;
card blurb contrast fixed; image merge clobber → 50/52 heroes.
