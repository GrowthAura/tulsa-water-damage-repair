# Favicon — Lovely round (2026-11-07 ~23:01 PKT, local only)

User: "favicon thora lovely aur end-level, perfect, best-ever banao — maza aye bhari wala."
Generator: `site/tools/make_favicon.py` (updated, re-runnable, ~4s). No push/deploy.

## Before (end-level round, viewed by pixels)
Clean and legible, but FLAT: solid navy drop, solid cyan drop, flat cream
tile, hard white disc highlight that read like a stuck-on bubble. Correct,
but no warmth — it looked drawn, not delightful.

## After — what changed and why it is lovelier
- **Navy drop, soft vertical gradient** — brand navy #073B66 at the tip
  flowing to a luminous deep blue #0F6EA8 at the belly. Reads like light
  travelling through water instead of a flat sticker.
- **Cyan inner drop, its own gentle gradient** — bright sky #1FC8FF at the
  top to deeper cyan #00A8E8 at the bottom. The inner drop now glows
  instead of sitting flat.
- **Tile, whisper of radial glow** — warm bright centre #FCFAF3 fading to
  cream #F5F1E6 at the edges. The tile feels warm and lit, not blank.
  Hairline navy edge kept (tile still reads on white tab bars).
- **Drop silhouette, a touch more graceful** — slightly fuller belly
  (cubic control 6.5s→6.7s, 7.6s→8.0s) + a softly rounded tip (tiny
  quadratic at the apex instead of a needle point). Same header teardrop
  family, just plumper and kinder.
- **Highlight, soft sheen not a sticker** — radial alpha disc (bright core
  fading to transparent), smaller (0.14× cyan width) and deeper inside the
  cyan drop. First attempt used a blurred ellipse: it spread white over
  the navy and read as a grey smudge/fog — caught by viewing, replaced
  with the alpha disc. At 32px the highlight stays a clean 2px hard disc;
  at 16px there is none (a 1px speck reads as dirt).
- **16px kept flat and sharp** — native hand-tuned render, flat fills,
  sharp apex (the rounded tip blunted into a flat top at 16px, so the
  16px render uses the sharp tip). Cyan bumped 0.52→0.55 so both drops
  stay bold at real size. Gradients would muddy at 16px — deliberately
  not applied there.
- Brand kept: cream tile + navy drop + cyan inner drop. No text, no
  letters, no extra icons.

## Verification (viewed by pixels, fresh final build)
- Master 512: gradient flows cleanly tip→belly on both drops; sheen is a
  soft glow fully inside the cyan, no grey fringe; tile warm, edge crisp.
- 16px + 32px composited on white / light-grey / navy, enlarged 8×,
  viewed by pixels: clean drop reads on all three backgrounds at both
  sizes; tile edge visible on white; 32px highlight reads as a shine,
  not dirt.
- Apple-touch-icon viewed clean at real size (180px).
- PNGs carry ZERO metadata (no EXIF/text/AI metadata, verified per file).
- favicon.ico verified: 3 entries, 16/32/48, 32bpp.
- site.webmanifest parses; all icons match declared sizes; theme #073b66.
- Rebuild green (`npm run export`, 53 routes); built HTML has favicon.ico
  + 16/32 PNG + apple-touch-icon + manifest links and theme-color #073B66.
- Generator runtime: ~60s → ~4s (radial glow now computed at 256px and
  upscaled — a smooth radial gradient upscales invisibly).

## Files
- Changed: `public/favicon-*` (master/512/512-maskable/192/48/32/16),
  `public/apple-touch-icon.png`, `public/favicon.ico`,
  `tools/make_favicon.py`. `site.webmanifest` + theme-color unchanged.
- NOT touched: `app/globals.css`, `content/pages.json` (parent agent's
  in-progress table + FAQ work — left alone).

## Still open
- Real tab-bar check happens on the live Vercel deploy (browsers cache
  favicons aggressively — hard refresh needed to see the new mark).
- Not pushed — local only, goes with the next push on the user's word +
  fresh token.
