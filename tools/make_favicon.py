#!/usr/bin/env python3
"""Lovely favicon generator — Tulsa Water Damage Repair (round 2).

Redraws the brand mark from scratch (PIL, supersampled) using the header's
teardrop geometry, refined for tiny-size legibility AND warmth:
  - cream rounded-square tile with a whisper of radial glow (bright warm
    centre fading to cream at the edges) + hairline navy edge (tile reads on
    white tab bars)
  - navy drop with a soft vertical gradient: brand navy #073B66 at the tip
    flowing to a luminous deep blue at the belly — like light through water
  - cyan inner drop with its own gentle gradient (bright sky top, deeper
    cyan bottom) so it reads as water, not a flat sticker
  - drop silhouette a touch more graceful than the header path: slightly
    fuller belly + a softly rounded tip (tiny quadratic at the apex instead
    of a needle point)
  - white highlight: a SOFT sheen (radial alpha disc, bright core fading to
    transparent, fully inside the cyan drop) at 48px and up; a clean 2px
    hard disc at 32px; none at 16px (a 1px speck reads as dirt)

Legibility guardrails (unchanged from round 1):
  - 16px is a hand-tuned native render, flat fills, no highlight, slightly
    larger cyan so both drops read at real size
  - no text, no letters, no extra icons — cream tile + navy drop + cyan drop

Outputs (into site/public/):
  favicon-master.png (512), favicon-192x192.png, favicon-512x512.png (manifest),
  favicon-512x512-maskable.png, apple-touch-icon.png (180),
  favicon-48x48.png, favicon-32x32.png, favicon-16x16.png, favicon.ico (16/32/48)
"""
import math
import os
from PIL import Image, ImageDraw

NAVY_TOP = (7, 59, 102, 255)      # brand navy #073B66
NAVY_BOT = (15, 110, 168, 255)    # luminous deep blue
CYAN_TOP = (31, 200, 255, 255)    # bright sky cyan
CYAN_BOT = (0, 168, 232, 255)     # deeper cyan
CREAM = (247, 243, 234, 255)
GLOW_CENTRE = (252, 250, 243, 255)  # warm bright centre of the tile
GLOW_EDGE = (245, 241, 229, 255)    # tile edge, a whisper darker than cream
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
    """Teardrop path (header geometry, gently refined): point at top,
    circular bottom, slightly fuller belly + softly rounded tip.
    tip_round=False gives the original sharp apex (used at 16px, where a
    rounded tip blunts into a flat top). Mirrors the header SVG:
    M12 2.5 ... 6.5 12a6.5 ... (viewBox 24x24)."""
    s = width / 13.0          # drop width 13 units, height 18.5 units in viewBox
    top = top_y
    left = (cx - 6.5 * s, top_y + 12.0 * s)
    right = (cx + 6.5 * s, top_y + 12.0 * s)
    # rounded tip: flanks at +/-0.85s, quadratic control just above the apex
    lf = (cx - 0.85 * s, top + 1.2 * s) if tip_round else (cx, top)
    rf = (cx + 0.85 * s, top + 1.2 * s) if tip_round else (cx, top)
    apex_c = (cx, top - 0.15 * s)
    # left side cubic: P0=lf, C1=lf, C2=(cx-6.7s, top+8.0s) fuller belly, end=left
    pts = cubic(lf, lf, (cx - 6.7 * s, top_y + 8.0 * s), left)
    # bottom semicircle: center (cx, top+12s), radius 6.5s.
    # Image coords are y-DOWN, so the BOTTOM of the circle is at angle 90deg:
    # sweep 180deg (left) -> 90deg (bottom) -> 0deg (right).
    cy = top_y + 12.0 * s
    r = 6.5 * s
    for deg in range(180, -1, -3):
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    # right side cubic back up: P0=right, C1=(cx+6.7s, top+8.0s), C2=rf, end=rf
    pts += cubic(right, (cx + 6.7 * s, top_y + 8.0 * s), rf, rf)
    # rounded tip back to the left flank (skipped when the apex is sharp)
    if tip_round:
        pts += quad(rf, apex_c, lf)
    return pts


def drop_mask(size, cx, top, w, tip_round=True):
    """L-mode mask of the drop shape at canvas `size`."""
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.polygon(drop_polygon(cx, top, w, w * 18.5 / 13.0, tip_round), fill=255)
    return m


def soft_disc(diameter):
    """White disc with a radial alpha falloff (bright core, fading to
    transparent at the edge) — a sheen, not a sticker. Built small and
    upscaled: smooth, and its fading edge never leaves a grey fringe where
    it crosses a colour boundary."""
    g0 = 128
    g = Image.new("RGBA", (g0, g0), (0, 0, 0, 0))
    px = g.load()
    cx = cy = (g0 - 1) / 2.0
    r = (g0 - 1) / 2.0
    for y in range(g0):
        for x in range(g0):
            t = min(1.0, math.hypot(x - cx, y - cy) / r)
            a = int(255 * max(0.0, 1.0 - t * t))
            px[x, y] = (255, 255, 255, a)
    return g.resize((max(1, diameter), max(1, diameter)), Image.BICUBIC)


def vgrad(size, top_rgb, bot_rgb):
    """Vertical RGBA gradient image, size x size."""
    g = Image.new("RGBA", (1, size))
    px = g.load()
    for y in range(size):
        t = y / max(1, size - 1)
        px[0, y] = tuple(int(top_rgb[i] + (bot_rgb[i] - top_rgb[i]) * t)
                         for i in range(3)) + (255,)
    return g.resize((size, size))


def radial_glow(size, centre_rgb, edge_rgb):
    """Radial glow: bright warm centre fading to the edge colour.
    Computed small (256px) and upscaled — a smooth radial gradient
    upscales invisibly, and the per-pixel loop at full size is slow."""
    g0 = 256
    g = Image.new("RGBA", (g0, g0))
    px = g.load()
    cx = cy = (g0 - 1) / 2.0
    maxd = math.hypot(cx, cy)
    for y in range(g0):
        for x in range(g0):
            t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
            # ease the falloff so the glow hugs the centre
            t = t * t * (3 - 2 * t)
            px[x, y] = tuple(int(centre_rgb[i] + (edge_rgb[i] - centre_rgb[i]) * t)
                             for i in range(3)) + (255,)
    return g.resize((size, size), Image.BICUBIC)


def tile(img, size, radius_frac=0.22):
    """Paint the glowing cream tile onto RGBA image `img` (in place)."""
    glow = radial_glow(size, GLOW_CENTRE, GLOW_EDGE)
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=size * radius_frac, fill=255)
    img.paste(glow, (0, 0), mask)
    d2 = ImageDraw.Draw(img)
    d2.rounded_rectangle([0, 0, size - 1, size - 1], radius=size * radius_frac,
                         outline=EDGE, width=max(1, size // 256))


def render(size, highlight="soft", cyan_scale=0.48, drop_scale=1.0, ss=4):
    """Render one favicon at `size` px (supersampled ss× then downsampled).
    highlight: 'soft' (blurred sheen), 'hard' (clean disc), 'none'."""
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    tile(img, S)
    # navy drop: vertical gradient through the drop mask
    w = S * 0.52 * drop_scale
    top = S * 0.115
    navy_h = w * 18.5 / 13.0
    img.paste(vgrad(S, NAVY_TOP, NAVY_BOT), (0, 0),
              drop_mask(S, S / 2, top, w))
    # cyan inner drop: scaled, centre ~63% down the navy drop
    cw = w * cyan_scale
    cheight = cw * 18.5 / 13.0
    ctop = top + navy_h * 0.63 - cheight * 0.42
    img.paste(vgrad(S, CYAN_TOP, CYAN_BOT), (0, 0),
              drop_mask(S, S / 2, ctop, cw))
    # white highlight: fully inside cyan drop, upper-left — a soft sheen
    # (radial alpha disc: bright core fading to transparent, so no grey
    # fringe where it meets the cyan edge). Small and deep inside the cyan.
    if highlight != "none":
        hr = cw * 0.14
        hcx = S / 2 - cw * 0.13
        hcy = ctop + cheight * 0.33
        if highlight == "soft":
            disc = soft_disc(int(hr * 2))
            img.paste(disc, (int(hcx - hr), int(hcy - hr)), disc)
        else:
            d = ImageDraw.Draw(img)
            d.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], fill=WHITE)
    return img.resize((size, size), Image.LANCZOS)


def render_16():
    """Hand-tuned 16px: no highlight (1px speck reads as dirt); bolder drop,
    larger cyan so both read at real size. Drawn natively, pixel-aligned.
    Flat fills stay — gradients would muddy at this size."""
    S = 16
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=3, fill=CREAM,
                        outline=(7, 59, 102, 45), width=1)
    w = 9.0
    top = 1.0
    # sharp apex here: the rounded tip blunts into a flat top at 16px
    d.polygon(drop_polygon(S / 2, top, w, w * 18.5 / 13.0, tip_round=False), fill=NAVY_TOP)
    cw = w * 0.55
    cheight = cw * 18.5 / 13.0
    navy_h = w * 18.5 / 13.0
    ctop = top + navy_h * 0.63 - cheight * 0.42
    d.polygon(drop_polygon(S / 2, ctop, cw, cheight, tip_round=False), fill=(0, 191, 255, 255))
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    master = render(512)
    master.save(f"{OUT}/favicon-master.png")
    master.save(f"{OUT}/favicon-512x512.png")
    render(192).save(f"{OUT}/favicon-192x192.png")
    render(180).save(f"{OUT}/apple-touch-icon.png")
    render(48).save(f"{OUT}/favicon-48x48.png")
    render(32, highlight="hard").save(f"{OUT}/favicon-32x32.png")
    render_16().save(f"{OUT}/favicon-16x16.png")
    # maskable: same tile, drop at 78% scale for the safe zone
    mask = render(512, drop_scale=0.78)
    mask.save(f"{OUT}/favicon-512x512-maskable.png")
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
