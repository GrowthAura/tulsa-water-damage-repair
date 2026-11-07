#!/usr/bin/env python3
"""Round 1 (post-fix) screenshots: scroll through each page gradually so
reveal animations fire and lazy images load, then capture full-page desktop
+ mobile top. Writes site/qa-round1/r2-<slug>-<w>.png"""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-round2')
ROOT = 'http://127.0.0.1:8317'
SHOTS = ['/', '/services/', '/services/emergency-water-damage-restoration',
         '/services/sewage-backup-cleanup', '/services/ceiling-water-damage',
         '/service-areas/broken-arrow-ok/', '/service-areas/midtown-tulsa/',
         '/resources/water-damage-restoration-cost-tulsa',
         '/resources/water-damage-categories-and-classes-explained',
         '/about-us/', '/contact/', '/commercial/']

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in SHOTS:
        safe = slug.strip('/').replace('/', '_') or 'home'
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.evaluate("""async () => {
          for (let y = 0; y <= document.body.scrollHeight; y += 500) {
            window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
          window.scrollTo(0, 0);
        }""")
        pg.wait_for_timeout(1200)
        pg.screenshot(path=os.path.join(OUT, f'r2-{safe}-1440.png'), full_page=True)
        ctx.close()
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        pg = ctx.new_page()
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(OUT, f'r2-{safe}-390-top.png'))
        ctx.close()
        print('shot', slug)
    browser.close()
print('done')
