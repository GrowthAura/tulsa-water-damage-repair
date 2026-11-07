#!/usr/bin/env python3
"""Retake screenshots with instant scroll + long reveal wait.
Usage: python3 tools/shots_retake.py
Writes site/qa-hero-fix/retake-*.png
"""
import os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-hero-fix')
ROOT = 'http://127.0.0.1:8317'

SHOTS = [
    ('retake-table-1440.png', 1440, '/', "zip"),
    ('retake-table-390.png', 390, '/', "zip"),
    ('retake-contact-1440.png', 1440, '/contact/', '.form-card'),
    ('retake-contact-390.png', 390, '/contact/', '.form-card'),
    ('retake-bixby-cards-1440.png', 1440, '/service-areas/bixby-ok/', '#what-water-damage-services-do-we-offer-in-bixby'),
    ('retake-bixby-strip-1440.png', 1440, '/service-areas/bixby-ok/', '.demand-strip'),
    ('retake-bixby-strip-390.png', 390, '/service-areas/bixby-ok/', '.demand-strip'),
    ('retake-broken-arrow-strip-1440.png', 1440, '/service-areas/broken-arrow-ok/', '.demand-strip'),
    ('retake-broken-arrow-strip-390.png', 390, '/service-areas/broken-arrow-ok/', '.demand-strip'),
    ('retake-resources-1440.png', 1440, '/resources/', '.resource-cards .cards'),
    ('retake-about-handle-1440.png', 1440, '/about-us/', '#what-do-we-handle'),
    ('retake-guide-1440.png', 1440, '/resources/first-24-hours-after-water-damage', '.content-block'),
    ('retake-guide-390.png', 390, '/resources/first-24-hours-after-water-damage', '.content-block'),
    ('retake-home-390-top.png', 390, '/', None),
]

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for path, vw, url, sel in SHOTS:
        ctx = browser.new_context(viewport={'width': vw, 'height': 900})
        pg = ctx.new_page()
        pg.goto(ROOT + url, wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(600)
        pg.evaluate("() => { document.documentElement.style.scrollBehavior = 'auto'; }")
        if sel == 'zip':
            pg.evaluate("""() => {
              const w = [...document.querySelectorAll('.table-wrap')].find(x => x.innerText.includes('Zip codes'));
              if (w) window.scrollTo(0, w.getBoundingClientRect().top + window.scrollY - 120);
            }""")
        elif sel:
            pg.evaluate(f"""() => {{
              const el = document.querySelector('{sel}');
              if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 90);
            }}""")
        pg.wait_for_timeout(1300)
        pg.screenshot(path=os.path.join(OUT, path))
        print('saved', path)
        ctx.close()
    browser.close()
