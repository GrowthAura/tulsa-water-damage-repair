#!/usr/bin/env python3
"""Classic favicon generator — Tulsa Water Damage Repair (round 4: HEAVY classic).

The user asked for a CLASSIC favicon (2026-11-08): the "lovely" round-2
mark (navy gradient drop + cyan inner drop + warm glow + soft sheen) was
too decorative. The classic mark is the HEADER's own brand mark, flat:
  - flat cream tile (solid #F7F3EA, NO radial glow) + hairline navy edge
    (tile reads on white tab bars)
  - ONE flat cyan drop (#00BFFF, solid, NO gradient) — the header SVG path
    exactly: M12 2.5 ... 6.5 12a6.5 ... (viewBox 24x24)
  - small SOLID white circle highlight (header: cx 9.4, cy 15.2, r 1.7 in
    viewBox units) — a flat disc, never a soft sheen; at 32px a clean 2px
    disc; none at 16px (a 1px speck reads as dirt)

ROUND 4 — HEAVY (2026-11-08, his order: "bhtu heavy sa koi classic"):
same mark, same geometry, same flat rules — the drop is simply BIGGER so it
fills more of the tile and reads bolder at every size:
  - drop width 0.56S -> 0.62S, top 0.10S -> 0.08S (height 0.882S, bottom
    margin ~0.04S; cyan coverage 27.6% -> 33.8% at 32px, 42.2% -> 46.1% at
    16px). Candidate 0.66S was REJECTED (drop touched the tile top AND
    bottom edges — cramped, corners cut).
  - 16px hand-tune: width 9.5 -> 10.0, top 1.0 -> 0.5 (apex near the top
    edge, bottom margin ~1.3px; the w10/t1.0 variant was REJECTED — its
    round bottom merged flat into the tile's bottom edge).
  - white dot scales with the drop (r = 0.131w, same proportions); the
    HEADER SVG got the same heavier drop (see app/components/Header.jsx).
    The header tile stays NAVY and the wordmark is unchanged — only the
    drop inside got heavier, so header icon and favicon are the same mark.

Legibility guardrails (unchanged):
  - 16px is a hand-tuned native render, flat fills, no highlight, sharp apex
    (a rounded tip blunts into a flat top at 16px)
  - no text, no letters, no extra icons — cream tile + cyan drop + white dot

Outputs (into site/public/):
  favicon-master.png (512), favicon-192x192.png, favicon-512x512.png (manifest),
  favicon-512x512-maskable.png, apple-touch-icon.png (180),
  favicon-48x48.png, favicon-32x32.png, favicon-16x16.png, favicon.ico (16/32/48)
"""
import math
import os
from PIL import Image, ImageDraw

CYAN = (0, 191, 255, 255)        # header brand cyan #00BFFF, flat
CREAM = (247, 243, 234, 255)     # flat cream tile #F7F3EA
WHITE = (255, 255, 255, 255)
EDGE = (7, 59, 102, 38)          # hairline tile edge, ~15% navy
OUT = os.path.expanduser("~/workspace/tulsa-water-damage-repair/site/public")


def cubic(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def quad(p0, c, p2, n=10):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt * mt * p0[0] + 2 * mt * t * c[0] + t * t * p2[0]
        y = mt * mt * p0[1] + 2 * mt * t * c[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def drop_polygon(cx, top_y, width, height, tip_round=True):
    """Teardrop path — the header SVG geometry exactly: point at top,
    circular bottom, drop width 13 units, height 18.5 units in viewBox.
    tip_round=False gives the original sharp apex (used at 16px)."""
    s = width / 13.0
    top = top_y
    left = (cx - 6.5 * s, top_y + 12.0 * s)
    right = (cx + 6.5 * s, top_y + 12.0 * s)
    lf = (cx - 0.85 * s, top + 1.2 * s) if tip_round else (cx, top)
    rf = (cx + 0.85 * s, top + 1.2 * s) if tip_round else (cx, top)
    apex_c = (cx, top - 0.15 * s)
    pts = cubic(lf, lf, (cx - 6.7 * s, top_y + 8.0 * s), left)
    cy = top_y + 12.0 * s
    r = 6.5 * s
    for deg in range(180, -1, -3):
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts += cubic(right, (cx + 6.7 * s, top_y + 8.0 * s), rf, rf)
    if tip_round:
        pts += quad(rf, apex_c, lf)
    return pts


def render(size, highlight=True, drop_scale=1.0, ss=4):
    """Render one classic favicon at `size` px (supersampled ssx then
    downsampled). Flat fills only — no gradients, no glow, no sheen."""
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # flat cream tile
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=CREAM,
                        outline=EDGE, width=max(1, S // 256))
    # single flat cyan drop (header mark) — HEAVY round 4: width 0.62S
    # (was 0.56S), top 0.08S (was 0.10S); same exact teardrop geometry,
    # just scaled up so the drop fills more of the tile.
    w = S * 0.62 * drop_scale
    top = S * 0.08
    h = w * 18.5 / 13.0
    d.polygon(drop_polygon(S / 2, top, w, h), fill=CYAN)
    # solid white circle, header proportions: centre (-2.6u, 0.686h) from
    # the drop apex, radius 0.131w (viewBox: cx 9.4, cy 15.2, r 1.7)
    if highlight:
        s = w / 13.0
        hcx = S / 2 - 2.6 * s
        hcy = top + 0.686 * h
        hr = 0.131 * w
        d.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], fill=WHITE)
    return img.resize((size, size), Image.LANCZOS)


def render_16():
    """Hand-tuned 16px: flat fills, sharp apex, no highlight."""
    S = 16
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=3, fill=CREAM,
                        outline=(7, 59, 102, 45), width=1)
    w = 10.0  # HEAVY round 4 (was 9.5); top 0.5 (was 1.0) — see docstring
    top = 0.5
    d.polygon(drop_polygon(S / 2, top, w, w * 18.5 / 13.0, tip_round=False), fill=CYAN)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    master = render(512)
    master.save(f"{OUT}/favicon-master.png")
    master.save(f"{OUT}/favicon-512x512.png")
    render(192).save(f"{OUT}/favicon-192x192.png")
    render(180).save(f"{OUT}/apple-touch-icon.png")
    render(48).save(f"{OUT}/favicon-48x48.png")
    render(32).save(f"{OUT}/favicon-32x32.png")
    render_16().save(f"{OUT}/favicon-16x16.png")
    # maskable: same mark, drop at 78% scale for the safe zone
    render(512, drop_scale=0.78).save(f"{OUT}/favicon-512x512-maskable.png")
    # .ico with 16/32/48
    im16 = Image.open(f"{OUT}/favicon-16x16.png")
    im32 = Image.open(f"{OUT}/favicon-32x32.png")
    im48 = Image.open(f"{OUT}/favicon-48x48.png")
    im48.save(f"{OUT}/favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)],
              append_images=[im32, im16])
    for f in sorted(os.listdir(OUT)):
        if f.startswith("favicon") or f.startswith("apple-touch"):
            p = os.path.join(OUT, f)
            im = Image.open(p)
            print(f"{f}: {im.size} {im.format} {os.path.getsize(p)}B")
    print("ico entries:")
    import struct
    data = open(f"{OUT}/favicon.ico", "rb").read()
    _, _, count = struct.unpack("<HHH", data[:6])
    for i in range(count):
        w, h, _, _, _, bpp, size, _ = struct.unpack("<BBBBHHII", data[6 + i * 16:6 + (i + 1) * 16])
        print(f"  {w or 256}x{h or 256} bpp={bpp} {size}B")


if __name__ == "__main__":
    main()
