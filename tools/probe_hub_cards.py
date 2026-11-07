#!/usr/bin/env python3
"""Hub-cards fix probe: /services/ hub + homepage at 1440/390/320.
Screenshots (scroll-through so .reveal fires) + H1 + overflow + console +
card counts + group headings + no plain group lists + no duplicate grid.
Writes site/qa-hub-cards/*.png + site/qa-hub-cards/probe.json.
Usage: python3 tools/probe_hub_cards.py (serve.py must run on :8317)."""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-hub-cards')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

PAGES = [('/services/', 'hub'), ('/', 'home'), ('/resources/', 'resources-hub')]

JS = """() => {
  const cards = [...document.querySelectorAll('article.card')].map(c => {
    const a = c.querySelector('h3 a');
    return {href: a ? a.getAttribute('href') : null,
            title: a ? a.textContent.trim() : null,
            img: !!(c.querySelector('.card-media img') || {}).src,
            panel: !!c.querySelector('.media-fallback'),
            w: Math.round(c.getBoundingClientRect().width),
            h: Math.round(c.getBoundingClientRect().height)};
  });
  const groups = [...document.querySelectorAll('.content-block h2')].map(h => h.textContent.trim());
  const labels = [...document.querySelectorAll('.content-block p strong')].map(s => s.textContent.trim());
  const contentUls = [...document.querySelectorAll('.content-block ul')].map(u =>
    u.textContent.trim().slice(0, 60));
  return {
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()),
    dupGrid: document.body.textContent.includes('Our Water Damage Services'),
    cards, groups, labels, contentUls,
    cardImgsLoaded: [...document.querySelectorAll('.card img')]
      .filter(im => im.complete && im.naturalWidth > 0).length + '/' +
      document.querySelectorAll('.card img').length,
  };
}"""

rows = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug, safe in PAGES:
        row = {'slug': slug, 'widths': {}}
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            errors = []
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            # scroll through so .reveal elements fire
            pg.evaluate("""async () => {
              const h = document.body.scrollHeight;
              for (let y = 0; y <= h; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
              window.scrollTo(0, 0);
            }""")
            pg.wait_for_timeout(600)
            m = pg.evaluate(JS)
            m['consoleErrors'] = errors
            row['widths'][w] = m
            if w in (1440, 390):
                pg.screenshot(path=os.path.join(OUT, f'{safe}-{w}.png'), full_page=True)
            ctx.close()
        rows.append(row)
    browser.close()

json.dump(rows, open(os.path.join(OUT, 'probe.json'), 'w'), indent=2)
for r in rows:
    print('===', r['slug'])
    for w, m in r['widths'].items():
        print(f"  {w}px overflow={m['overflow']} h1={m['h1']} console={m['consoleErrors']}")
        print(f"    cards={len(m['cards'])} imgs={m['cardImgsLoaded']} dupGrid={m['dupGrid']}")
        print(f"    groups={m['groups'][:8]}")
        print(f"    contentUls={m['contentUls']}")
