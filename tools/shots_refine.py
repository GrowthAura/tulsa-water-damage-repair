#!/usr/bin/env python3
"""Refine-round visual probe: screenshots + console + H1 + overflow for the
changed pages. Writes site/qa-refine/*.png + site/qa-refine/probe.json.
Usage: python3 tools/shots_refine.py (serve.py must be running on :8317)."""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-refine')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

PAGES = [
    ('/', 'home'),
    ('/services/flood-damage-restoration', 'flood'),
    ('/resources/water-damage-vs-flood-damage-insurance-oklahoma', 'vs-flood'),
    ('/services/slab-leak-water-damage/', 'slab'),
    ('/resources/how-long-does-water-damage-take-to-dry', 'dry-time'),
    ('/services/sewage-backup-cleanup', 'sewage'),
    ('/service-areas/broken-arrow-ok/', 'broken-arrow'),
    ('/resources/', 'resources-hub'),
    ('/services/', 'services-hub'),
    ('/contact/', 'contact'),
]

rows = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug, safe in PAGES:
        row = {'slug': slug, 'widths': {}}
        for w in (1440, 390):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            errors = []
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(500)
            m = pg.evaluate("""() => {
              const h1s = [...document.querySelectorAll('h1')].map(h => h.textContent.trim());
              return {
                overflow: document.documentElement.scrollWidth - window.innerWidth,
                h1: h1s,
                title: document.title,
                canonical: (document.querySelector('link[rel=canonical]')||{}).href || null,
                icons: [...document.querySelectorAll('link[rel=icon], link[rel=apple-touch-icon]')].map(l => l.getAttribute('href')),
                topbar: !!document.querySelector('.topbar'),
                learnMore: [...document.querySelectorAll('a')].filter(a => a.textContent.trim() === 'Learn more →').length,
                iframes: [...document.querySelectorAll('iframe')].map(f => f.src),
                heroImg: (() => { const i = document.querySelector('.hero-media img, .hero img'); return i ? {src: i.getAttribute('src'), w: Math.round(i.getBoundingClientRect().width), h: Math.round(i.getBoundingClientRect().height), loaded: i.complete && i.naturalWidth > 0} : null; })(),
                heroPanel: !!document.querySelector('.hero-brand-panel'),
                bodyPanel: !!document.querySelector('.brand-panel'),
                headerH: Math.round(document.querySelector('.site-header').getBoundingClientRect().height),
              };
            }""")
            m['consoleErrors'] = errors
            row['widths'][w] = m
            # full-page desktop, top + footer mobile
            pg.screenshot(path=os.path.join(OUT, f'{safe}-{w}.png'), full_page=(w == 1440))
            if w == 390:
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(400)
                pg.screenshot(path=os.path.join(OUT, f'{safe}-{w}-footer.png'))
                pg.evaluate("() => window.scrollTo(0, 0)")
                pg.wait_for_timeout(300)
            # header close-up (desktop + mobile)
            hdr = pg.query_selector('.site-header')
            if hdr:
                hdr.screenshot(path=os.path.join(OUT, f'{safe}-{w}-header.png'))
            ctx.close()
        # footer close-up on home desktop
        if slug == '/':
            ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
            pg = ctx.new_page()
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(400)
            ftr = pg.query_selector('.site-footer')
            if ftr:
                ftr.screenshot(path=os.path.join(OUT, 'home-1440-footer.png'))
            ctx.close()
        rows.append(row)
        w1440 = row['widths'][1440]
        print(f"{slug}: ov1440={w1440['overflow']} ov390={row['widths'][390]['overflow']} "
              f"H1={len(w1440['h1'])} topbar={w1440['topbar']} learnMore={w1440['learnMore']} "
              f"iframes={len(w1440['iframes'])} heroImg={bool(w1440['heroImg'])} panel={w1440['heroPanel']} "
              f"consoleErr={len(w1440['consoleErrors'])} headerH={w1440['headerH']}")
    browser.close()

json.dump(rows, open(os.path.join(OUT, 'probe.json'), 'w'), indent=1)
print('wrote', OUT)
