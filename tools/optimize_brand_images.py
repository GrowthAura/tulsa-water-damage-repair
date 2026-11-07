#!/usr/bin/env python3
"""Optimize + brand service-page images (hero-fix round).
Usage:
  python3 tools/optimize_brand_images.py --optimize-generated
      Resize the 6 generated images (sewage/slab/ceiling hero+body) from
      1920x1280 to 1200x800 WebP <=150KB, 0 EXIF, into /tmp/hero-fix-final/.
  python3 tools/optimize_brand_images.py --brand
      Composite the site brand mark (navy rounded square + cyan water drop,
      matching the header .brand-mark) bottom-right of EVERY service-page
      image file in public/images/, re-encode WebP <=150KB, 0 EXIF.
      Run ONLY on the final installed files (after replacements land).
Brand badge: 72px on a 1200px-wide image (6%), 20px margin, never covers
the subject's centre; cyan ring keeps it visible on the hero's navy gradient.
"""
import argparse, json, os, sys
from PIL import Image, ImageDraw

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
GEN = '/tmp/hero-fix-generated'
FINAL = '/tmp/hero-fix-final'

# media results, in call order (snapshot ids in the tool results)
GENERATED = [
    ('media-generation-services-sewage-backup-cleanup-0-69e0fd86-6311-4b08-ae8d-138040aea54a.webp',
     'services-sewage-backup-cleanup-tulsa-water-damage-repair.webp'),
    ('media-generation-services-sewage-backup-cleanup-0-c6e85ac5-1089-485d-b86f-c15e1a1a32e1.webp',
     'services-sewage-backup-cleanup-tulsa-water-damage-repair-sewage-cleanup.webp'),
    ('media-generation-services-slab-leak-water-damag-0-db462075-d804-402c-bfa0-9761632a85d6.webp',
     'services-slab-leak-water-damage-tulsa-water-damage-repair.webp'),
    ('media-generation-services-slab-leak-water-damag-0-708f7db8-f9ee-40d7-84df-41ab66cbd267.webp',
     'services-slab-leak-water-damage-tulsa-water-damage-repair-slab-repair.webp'),
    ('media-generation-services-ceiling-water-damage-0-819e784c-ec80-48cb-8f3b-14a4b4403d0d.webp',
     'services-ceiling-water-damage-tulsa-water-damage-repair.webp'),
    ('media-generation-services-ceiling-water-damage-0-ce8b89ab-a10f-470a-b680-7120749852a4.webp',
     'services-ceiling-water-damage-tulsa-water-damage-repair-ceiling-repair.webp'),
]

def webp_bytes(im, quality):
    import io
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=quality, method=6)
    return buf.getvalue()

def save_optimized(im, path, max_bytes=150 * 1024):
    """Save 1200x800 WebP <= max_bytes, stepping quality down from 82."""
    im = im.convert('RGB').resize((1200, 800), Image.LANCZOS)
    q = 82
    data = webp_bytes(im, q)
    while len(data) > max_bytes and q > 55:
        q -= 5
        data = webp_bytes(im, q)
    with open(path, 'wb') as f:
        f.write(data)
    chk = Image.open(path)
    assert chk.size == (1200, 800), chk.size
    assert not chk.getexif(), 'EXIF present!'
    return len(data), q

def brand_badge(size=72):
    """Navy rounded square + cyan water drop (header .brand-mark), 4x supersampled."""
    S = size * 4
    badge = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle([4, 4, S - 4, S - 4], radius=int(S * 0.22),
                        fill=(7, 59, 102, 255), outline=(0, 191, 255, 220), width=8)
    # water drop: triangle apex + circle body, cyan #00BFFF
    cx = S // 2
    d.polygon([(cx, int(S * 0.16)), (int(S * 0.24), int(S * 0.52)),
               (int(S * 0.76), int(S * 0.52))], fill=(0, 191, 255, 255))
    d.ellipse([int(S * 0.24), int(S * 0.34), int(S * 0.76), int(S * 0.86)],
              fill=(0, 191, 255, 255))
    # white highlight dot (as in the header SVG)
    d.ellipse([int(S * 0.33), int(S * 0.60), int(S * 0.44), int(S * 0.71)],
              fill=(255, 255, 255, 255))
    return badge.resize((size, size), Image.LANCZOS)

def apply_brand(path):
    im = Image.open(path).convert('RGB')
    assert im.size == (1200, 800), (path, im.size)
    badge = brand_badge(72)
    im_rgba = im.convert('RGBA')
    im_rgba.alpha_composite(badge, (1200 - 72 - 20, 800 - 72 - 20))
    q = 82
    data = webp_bytes(im_rgba.convert('RGB'), q)
    while len(data) > 150 * 1024 and q > 55:
        q -= 5
        data = webp_bytes(im_rgba.convert('RGB'), q)
    with open(path, 'wb') as f:
        f.write(data)
    chk = Image.open(path)
    assert not chk.getexif(), 'EXIF present!'
    return len(data), q

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--optimize-generated', action='store_true')
    ap.add_argument('--brand', action='store_true')
    args = ap.parse_args()
    if args.optimize_generated:
        os.makedirs(FINAL, exist_ok=True)
        for src, target in GENERATED:
            sp = os.path.join(GEN, src)
            tp = os.path.join(FINAL, target)
            im = Image.open(sp)
            assert im.size == (1920, 1280), (src, im.size)
            assert not im.getexif(), 'source EXIF!'
            n, q = save_optimized(im, tp)
            print(f'{target}: {n} B q{q} 1200x800 0-EXIF')
    if args.brand:
        d = json.load(open(os.path.join(BASE, 'content', 'images.json')))
        pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
        pages = pages if isinstance(pages, list) else pages.get('pages', [])
        files = set()
        for p in pages:
            if p.get('type') != 'service':
                continue
            e = d.get(p['slug']) or {}
            for kind in ('hero', 'body'):
                ent = e.get(kind) if isinstance(e, dict) else None
                if ent:
                    files.add(ent['file'].lstrip('/'))
        print(f'branding {len(files)} service images')
        for f in sorted(files):
            path = os.path.join(BASE, 'public', f)
            n, q = apply_brand(path)
            print(f'{f}: {n} B q{q} branded')
    if not (args.optimize_generated or args.brand):
        ap.print_help()
        sys.exit(2)

if __name__ == '__main__':
    main()
