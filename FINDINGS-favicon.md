# Favicon — end-level round — 2026-11-07 ~20:00 PKT (local only)

## 1. Before — inspected at real size (viewed by pixels)

| File | Size | Verdict |
|---|---|---|
| favicon-master.png | 512×512, 4,970 B | Decent at large size, weak at tiny sizes |
| favicon-16x16.png | 16×16, 762 B | Navy drop reads, but cyan inner drop is a ~4px blob and the white highlight is a 1px speck straddling the navy/cyan boundary — reads as dirt/noise |
| favicon-32x32.png | 32×32, 1,591 B | Same: small cyan blob, muddy white speck |
| apple-touch-icon.png | 180×180, 10,198 B | Fine at that size |
| favicon.ico | 2,377 B — 16 + 32 only | Missing 48px entry |
| site.webmanifest | — | Did not exist |
| theme-color meta | — | Did not exist |

Other before-defects:
- Drop point blunt/soft; drop slightly lopsided (not the header's clean teardrop).
- Cream tile has no edge definition — on a white tab bar the tile boundary vanishes.
- The mark did not use the header's exact teardrop geometry (header SVG: cyan drop + white highlight on a navy tile).

## 2. After — redrawn from scratch (site/tools/make_favicon.py, PIL, supersampled)

Kept the brand per brief: cream rounded-square tile (#F7F3EA) + navy drop (#073B66) + cyan inner drop (#00BFFF). Refinements:
- **Drop = header's exact teardrop path** (symmetric, crisp point, circular bottom), slightly bolder for 16px legibility. First render had a bug (arc swept through the top of the circle, y-down coords) — produced an arch shape; caught by viewing the render, fixed (sweep 180°→90°→0°), re-rendered and re-viewed.
- **Cyan inner drop enlarged** (~48% of navy drop vs ~35% before) so it reads as a drop at 16px, not a blob.
- **White highlight moved fully INSIDE the cyan drop** (upper-left, like the header mark). Old one straddled the navy/cyan edge.
- **Hairline navy edge on the cream tile** (~15% navy) so the tile reads on white tab bars.
- **16×16 and 32×32 hand-tuned native renders** (not downscales): 16px has no highlight (a 1px speck reads as dirt) and a larger cyan drop; 32px has a clean 2px highlight.

Full set now (all in public/, all in out/ after export):

| File | Size | Bytes |
|---|---|---|
| favicon-master.png | 512×512 | 36,206 |
| favicon-512x512.png | 512×512 | 36,206 |
| favicon-512x512-maskable.png | 512×512 (drop at 78% for safe zone) | 31,556 |
| favicon-192x192.png | 192×192 | 11,862 |
| apple-touch-icon.png | 180×180 | 11,346 |
| favicon-48x48.png | 48×48 | 2,730 |
| favicon-32x32.png | 32×32 | 372 |
| favicon-16x16.png | 16×16 | 242 |
| favicon.ico | 16 + 32 + 48, 32bpp | 3,398 |
| site.webmanifest | — | 484 |

Head setup (app/layout.js): `manifest: '/site.webmanifest'` in metadata + `export const viewport = { themeColor: '#073B66' }`. No words/content/links/phone changed.

## 3. Verification (fresh final build)

- Rebuild green (static export, 23 flat + 30 slash routes).
- Built HTML head: `<link rel="manifest" href="/site.webmanifest">`, `<meta name="theme-color" content="#073B66">`, icon links (ico + 32 + 16), apple-touch-icon — all present.
- Manifest parses; all 3 declared icons exist at the declared sizes.
- .ico verified: 3 entries (16/32/48, 32bpp).
- Local HTTP serve: all 8 icon/manifest files 200.
- Tab-bar legibility test (16px + 32px composited on white / light-grey / navy, enlarged 8×, viewed by pixels): navy drop + cyan inner drop read clearly on all three backgrounds; tile edge visible on white; 32px highlight reads as a highlight, not dirt. Screenshot: /tmp/favicon-tab-test.png (scratch, not committed).
- Apple-touch-icon viewed at real size: clean.

## 4. NOT verified — needs the parent (live browser)

A subagent cannot operate a live browser, so the real tab-bar check was NOT done: open the live preview (or local build) in a real browser and confirm the tab actually shows the new favicon (hard refresh / clear favicon cache — browsers cache favicons aggressively, so a stale tab icon does not mean the files are wrong). Parent to arrange via browser.browse.
