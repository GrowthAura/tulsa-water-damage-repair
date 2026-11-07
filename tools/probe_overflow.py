#!/usr/bin/env python3
"""Fast re-probe: mobile overflow at 390/320 for all 52 pages + homepage/hub
card image counts. Usage: python3 tools/probe_overflow.py"""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
ROOT = 'http://127.0.0.1:8317'
bad = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for p in pages:
        row = {}
        for w in (390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            pg.goto(ROOT + p['slug'], wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(400)
            row[w] = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            ctx.close()
        if row[390] > 0 or row[320] > 0:
            bad.append((p['slug'], row))
    # card images on home + hub
    for slug in ('/', '/services/'):
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(1200)
        n = pg.evaluate("() => [...document.querySelectorAll('.card img')].filter(im => im.complete && im.naturalWidth > 0).length + '/' + document.querySelectorAll('.card img').length")
        print(f'{slug} card imgs loaded: {n}')
        ctx.close()
    browser.close()
print(f'\nOVERFLOW pages (390/320): {len(bad)}')
for s, r in bad:
    print('  -', s, r)
