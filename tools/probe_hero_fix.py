#!/usr/bin/env python3
"""Hero-fix probe: H1 tops, H2 line/widow analysis, overflow, console, screenshots.
Usage: python3 tools/probe_hero_fix.py [before|after]
Writes site/qa-hero-fix/<mode>.json + screenshots.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
MODE = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = os.path.join(BASE, 'qa-hero-fix')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

H2_ANALYZE = """() => {
  const out = [];
  document.querySelectorAll('h2').forEach((h) => {
    const range = document.createRange();
    range.selectNodeContents(h);
    const rects = [...range.getClientRects()].map(r => ({w: Math.round(r.width), t: h.innerText}));
    const words = h.innerText.trim().split(/\\s+/);
    const lines = rects.length;
    const lastW = rects.length ? rects[rects.length - 1].w : 0;
    const maxW = rects.length ? Math.max(...rects.map(r => r.w)) : 0;
    const lastWords = (() => {
      // approximate last-line words by width: walk words from the end
      const all = h.innerText.trim();
      return all;
    })();
    out.push({id: h.id || null, text: h.innerText.trim().slice(0, 70),
      lines, lastLineWidth: lastW, maxLineWidth: maxW,
      lastRatio: maxW ? +(lastW / maxW).toFixed(2) : 0,
      words: words.length});
  });
  return out;
}"""

MEASURE = """() => {
  const h1 = document.querySelector('h1');
  const r = h1 ? h1.getBoundingClientRect() : null;
  const hero = document.querySelector('.hero-media, .hero-brand-panel');
  const hr = hero ? hero.getBoundingClientRect() : null;
  const badge = document.querySelector('.hero-badge, .hero-content .eyebrow');
  const br = badge ? badge.getBoundingClientRect() : null;
  return {
    h1count: document.querySelectorAll('h1').length,
    h1_top: r ? Math.round(r.top + window.scrollY) : null,
    hero_media_h: hr ? Math.round(hr.height) : null,
    badge_top: br ? Math.round(br.top + window.scrollY) : null,
    overflow: document.documentElement.scrollWidth - window.innerWidth,
  };
}"""

PAGES = ['/', '/services/emergency-water-damage-restoration',
         '/services/flood-damage-restoration', '/contact/', '/services/']

results = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in PAGES:
        tag = slug.strip('/').replace('/', '_') or 'home'
        row = {'slug': slug}
        errors = []
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(600)
            m = pg.evaluate(MEASURE)
            row[f'w{w}'] = m
            if w == 1440:
                pg.screenshot(path=os.path.join(OUT, f'{MODE}-{tag}-1440-top.png'))
                h2s = pg.evaluate(H2_ANALYZE)
                row['h2_1440'] = h2s
                pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                pg.wait_for_timeout(700)
                pg.screenshot(path=os.path.join(OUT, f'{MODE}-{tag}-1440-full.png'), full_page=True)
            if w == 390:
                pg.screenshot(path=os.path.join(OUT, f'{MODE}-{tag}-390-top.png'))
                row['h2_390'] = pg.evaluate(H2_ANALYZE)
            ctx.close()
        row['console_errors'] = sorted(set(errors))
        results[slug] = row
        print(slug, '| h1_top@1440:', row['w1440']['h1_top'],
              '| badge_top:', row['w1440']['badge_top'],
              '| media_h:', row['w1440']['hero_media_h'],
              '| overflow:', {w: row[f'w{w}']['overflow'] for w in (1440, 390, 320)},
              '| console:', len(row['console_errors']))
    browser.close()
json.dump(results, open(os.path.join(OUT, f'{MODE}.json'), 'w'), indent=1)
print('written', os.path.join(OUT, f'{MODE}.json'))
