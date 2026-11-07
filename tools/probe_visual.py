#!/usr/bin/env python3
"""Round 1 visual probe: for every page, at 1440 / 390 / 320 widths:
- full-page desktop screenshot + mobile top screenshot (homepage + a sample set)
- horizontal overflow (document.scrollWidth vs innerWidth)
- rendered image boxes (width x height, natural size) — height measured, never width alone
- hero image presence + hero box height
- console errors
Writes site/qa-round1/probe.json + screenshots. Usage: python3 tools/probe_visual.py
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-round1')
os.makedirs(OUT, exist_ok=True)
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
ROOT = 'http://127.0.0.1:8317'

# Screenshot set: homepage + hub + 1 of each type + contact + 2 areas + 2 resources
SHOT_SLUGS = ['/', '/services/', '/services/emergency-water-damage-restoration',
              '/services/flood-damage-restoration', '/services/mold-remediation',
              '/services/sewage-backup-cleanup', '/services/fire-damage-restoration',
              '/service-areas/broken-arrow-ok/', '/service-areas/midtown-tulsa/',
              '/resources/water-damage-restoration-cost-tulsa',
              '/resources/oklahoma-water-damage-insurance-guide',
              '/about-us/', '/contact/', '/commercial/']

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for p in pages:
        slug = p['slug']
        row = {'slug': slug, 'widths': {}}
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900},
                                      device_scale_factor=1)
            page = ctx.new_page()
            errors = []
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(800)
            m = page.evaluate("""() => {
              const imgs = [...document.querySelectorAll('img')].map(im => {
                const r = im.getBoundingClientRect();
                return {src: im.getAttribute('src'), alt: im.getAttribute('alt'),
                        w: Math.round(r.width), h: Math.round(r.height),
                        nw: im.naturalWidth, nh: im.naturalHeight,
                        loaded: im.complete && im.naturalWidth > 0};
              });
              const hero = document.querySelector('.hero img, .hero-brand-panel');
              let heroBox = null;
              if (hero) { const r = hero.getBoundingClientRect();
                heroBox = {tag: hero.tagName, w: Math.round(r.width), h: Math.round(r.height)}; }
              return {
                scrollW: document.documentElement.scrollWidth,
                innerW: window.innerWidth,
                overflow: document.documentElement.scrollWidth - window.innerWidth,
                h1: [...document.querySelectorAll('h1')].length,
                imgs: imgs,
                heroBox: heroBox,
                bodyH: document.body.scrollHeight,
              };
            }""")
            m['console_errors'] = errors
            row['widths'][w] = m
            if slug in SHOT_SLUGS:
                safe = slug.strip('/').replace('/', '_') or 'home'
                page.screenshot(path=os.path.join(OUT, f'{safe}-{w}.png'), full_page=(w == 1440))
                if w != 1440:
                    page.screenshot(path=os.path.join(OUT, f'{safe}-{w}-top.png'))
            ctx.close()
        results.append(row)
        print(f"{slug}: overflow1440={row['widths'][1440]['overflow']} "
              f"overflow390={row['widths'][390]['overflow']} "
              f"overflow320={row['widths'][320]['overflow']} "
              f"imgs={len(row['widths'][1440]['imgs'])} "
              f"hero={row['widths'][1440]['heroBox']} "
              f"err={sum(len(row['widths'][w]['console_errors']) for w in (1440,390,320))}")
    browser.close()

json.dump(results, open(os.path.join(OUT, 'probe.json'), 'w'), indent=1)
bad_overflow = [r['slug'] for r in results if any(r['widths'][w]['overflow'] > 0 for w in (1440, 390, 320))]
bad_imgs = []
for r in results:
    for im in r['widths'][1440]['imgs']:
        if not im['loaded']:
            bad_imgs.append((r['slug'], im['src']))
        if im['h'] == 0 and im['w'] > 0:
            bad_imgs.append((r['slug'], im['src'], 'zero-height'))
print(f'\nOVERFLOW pages: {bad_overflow}')
print(f'UNLOADED/ZERO-HEIGHT images: {bad_imgs}')
print(f'probe.json + screenshots in {OUT}')
