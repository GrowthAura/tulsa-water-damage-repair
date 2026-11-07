#!/usr/bin/env python3
"""End-level favicon generator — Tulsa Water Damage Repair.

Redraws the brand mark from scratch (PIL, supersampled) using the header's
exact teardrop geometry, refined for tiny-size legibility:
  - cream rounded-square tile (#F7F3EA) + hairline navy edge (tile reads on
    white tab bars)
  - navy drop (#073B66), header teardrop path, slightly bolder
  - cyan inner drop (#00BFFF), larger than the old mark so it reads at 16px
  - white highlight disc, fully INSIDE the cyan drop (old one straddled the
    navy/cyan boundary and read as dirt at 16px)
  - 16px/32px are hand-tuned native renders (no highlight at 16px — a 1px
    speck reads as noise; cyan drop enlarged instead)

Outputs (into site/public/):
  favicon-master.png (512), favicon-192x192.png, favicon-512x512.png (manifest),
  favicon-512x512-maskable.png, apple-touch-icon.png (180),
  favicon-48x48.png, favicon-32x32.png, favicon-16x16.png, favicon.ico (16/32/48)
"""
import math
import os
from PIL import Image, ImageDraw

NAVY = (7, 59, 102, 255)
CYAN = (0, 191, 255, 255)
CREAM = (247, 243, 234, 255)
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


def drop_polygon(cx, top_y, width, height):
    """Header teardrop path, scaled: point at top, circular bottom.
    Mirrors the header SVG: M12 2.5 ... 6.5 12a6.5 ... (viewBox 24x24)."""
    s = width / 13.0          # drop width 13 units, height 18.5 units in viewBox
    top = (cx, top_y)
    left = (cx - 6.5 * s, top_y + 12.0 * s)
    right = (cx + 6.5 * s, top_y + 12.0 * s)
    # left side cubic: P0=top, C1=top, C2=(cx-6.5s, top+7.6s), end=left
    pts = cubic(top, top, (cx - 6.5 * s, top_y + 7.6 * s), left)
    # bottom semicircle: center (cx, top+12s), radius 6.5s.
    # Image coords are y-DOWN, so the BOTTOM of the circle is at angle 90deg:
    # sweep 180deg (left) -> 90deg (bottom) -> 0deg (right).
    cy = top_y + 12.0 * s
    r = 6.5 * s
    for deg in range(180, -1, -3):
        a = math.radians(deg)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    # right side cubic back up: P0=right, C1=(cx+6.5s, top+7.6s), C2=top, end=top
    pts += cubic(right, (cx + 6.5 * s, top_y + 7.6 * s), top, top)
    return pts


def tile(draw, size, radius_frac=0.22, fill=CREAM, edge=EDGE):
    draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=size * radius_frac,
                           fill=fill, outline=edge, width=max(1, size // 256))


def render(size, highlight=True, cyan_scale=0.48, drop_scale=1.0, ss=4):
    """Render one favicon at `size` px (supersampled ss× then downsampled)."""
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    tile(d, S)
    # navy drop: width ~52% of tile, top ~12%, height = width*18.5/13
    w = S * 0.52 * drop_scale
    top = S * 0.115
    d.polygon(drop_polygon(S / 2, top, w, w * 18.5 / 13.0), fill=NAVY)
    # cyan inner drop: scaled, centre ~63% down the navy drop
    cw = w * cyan_scale
    cheight = cw * 18.5 / 13.0
    navy_h = w * 18.5 / 13.0
    ctop = top + navy_h * 0.63 - cheight * 0.42
    d.polygon(drop_polygon(S / 2, ctop, cw, cheight), fill=CYAN)
    # white highlight: fully inside cyan drop, upper-left
    if highlight:
        hr = cw * 0.17
        hcx = S / 2 - cw * 0.20
        hcy = ctop + cheight * 0.30
        d.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], fill=WHITE)
    return img.resize((size, size), Image.LANCZOS)


def render_16():
    """Hand-tuned 16px: no highlight (1px speck reads as dirt); bolder drop,
    larger cyan so both read at real size. Drawn natively, pixel-aligned."""
    S = 16
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=3, fill=CREAM,
                        outline=(7, 59, 102, 45), width=1)
    w = 9.0
    top = 1.0
    d.polygon(drop_polygon(S / 2, top, w, w * 18.5 / 13.0), fill=NAVY)
    cw = w * 0.52
    cheight = cw * 18.5 / 13.0
    navy_h = w * 18.5 / 13.0
    ctop = top + navy_h * 0.63 - cheight * 0.42
    d.polygon(drop_polygon(S / 2, ctop, cw, cheight), fill=CYAN)
    return img


def render_32():
    """Hand-tuned 32px: native render, small clean highlight (2px)."""
    S = 32
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=7, fill=CREAM,
                        outline=(7, 59, 102, 40), width=1)
    w = 17.0
    top = 3.0
    d.polygon(drop_polygon(S / 2, top, w, w * 18.5 / 13.0), fill=NAVY)
    cw = w * 0.50
    cheight = cw * 18.5 / 13.0
    navy_h = w * 18.5 / 13.0
    ctop = top + navy_h * 0.63 - cheight * 0.42
    d.polygon(drop_polygon(S / 2, ctop, cw, cheight), fill=CYAN)
    hr = 1.6
    hcx = S / 2 - cw * 0.20
    hcy = ctop + cheight * 0.30
    d.ellipse([hcx - hr, hcy - hr, hcx + hr, hcy + hr], fill=WHITE)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    master = render(512)
    master.save(f"{OUT}/favicon-master.png")
    master.save(f"{OUT}/favicon-512x512.png")
    render(192).save(f"{OUT}/favicon-192x192.png")
    render(180).save(f"{OUT}/apple-touch-icon.png")
    render(48).save(f"{OUT}/favicon-48x48.png")
    render_32().save(f"{OUT}/favicon-32x32.png")
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
