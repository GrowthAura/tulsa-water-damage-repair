#!/usr/bin/env python3
"""Design-round probe: H1 Y position (hero shift), computed text sizes (18px
floor), overflow at 1440/390/320, H1 count, console errors, screenshots.
Usage: python3 tools/probe_design.py
Writes site/qa-design/design.json + screenshots.
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-design')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'
SLUGS = ['/', '/services/', '/services/emergency-water-damage-restoration',
         '/services/flood-damage-restoration', '/service-areas/broken-arrow-ok/',
         '/contact/', '/resources/', '/about-us/']
SIZE_SEL = {
    'body_p': '.content-block p',
    'btn': '.btn',
    'crumbs': '.crumbs',
    'footer_p': '.footer-col p',
    'footer_link': '.footer-col ul a',
    'footer_bottom': '.footer-bottom',
    'card_p': '.card-body p',
    'table_td': '.table-wrap td',
    'trust_li': '.trust-band li',
    'eyebrow': '.eyebrow',
    'hero_badge': '.hero-badge',
    'brand_panel_li': '.brand-panel li',
    'form_label': '.form-card label',
    'form_note': '.form-note',
    'mobile_call_bar': '.mobile-call-bar',
}
results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in SLUGS:
        tag = slug.strip('/').replace('/', '_') or 'home'
        row = {'slug': slug}
        errors = []
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(500)
            m = pg.evaluate("""() => {
              const h1 = document.querySelector('h1');
              const r = h1 ? h1.getBoundingClientRect() : null;
              const cs = (sel) => { const el = document.querySelector(sel);
                return el ? parseFloat(getComputedStyle(el).fontSize) : null; };
              const out = { h1count: document.querySelectorAll('h1').length,
                h1_top: r ? Math.round(r.top + window.scrollY) : null,
                h1_text: h1 ? h1.innerText.slice(0, 60) : null,
                overflow: document.documentElement.scrollWidth - window.innerWidth,
                sizes: {} };
              const sels = %s;
              for (const [k, sel] of Object.entries(sels)) out.sizes[k] = cs(sel);
              return out;
            }""" % json.dumps(SIZE_SEL))
            row[f'w{w}'] = m
            if w == 1440:
                pg.screenshot(path=os.path.join(OUT, f'{tag}-1440-top.png'))
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(900)
                pg.screenshot(path=os.path.join(OUT, f'{tag}-1440-full.png'), full_page=True)
            if w == 390:
                pg.evaluate("() => window.scrollTo(0, 0)")
                pg.wait_for_timeout(300)
                pg.screenshot(path=os.path.join(OUT, f'{tag}-390-top.png'))
            ctx.close()
        row['console_errors'] = sorted(set(errors))
        results[slug] = row
        print(slug, '| h1_top@1440:', row['w1440']['h1_top'], '| overflow:', {w: row[f'w{w}']['overflow'] for w in (1440, 390, 320)}, '| h1:', row['w1440']['h1count'], '| console:', len(row['console_errors']))
    browser.close()
json.dump(results, open(os.path.join(OUT, 'design.json'), 'w'), indent=1)
print('written', os.path.join(OUT, 'design.json'))
