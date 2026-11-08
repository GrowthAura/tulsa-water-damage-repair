#!/usr/bin/env python3
"""Homepage-round probe: sitewide computed font-size audit (all 53 pages) +
homepage screenshots (desktop 1280 full-page, mobile 390 full-page).
Usage: python3 tools/probe_sitewide18.py <tag>   (tag = before | after)
Writes site/qa-home-round/<tag>-sizes.json + <tag>-home-1280.png + <tag>-home-390.png
+ <tag>-overflow.json. Serve out/ on :8317 first (python3 -m http.server 8317 -d out).
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
TAG = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = os.path.join(BASE, 'qa-home-round')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

pages = json.load(open(os.path.join(BASE, 'content/pages.json')))
SLUGS = [p['slug'] for p in pages]
# privacy/terms are in pages.json too; keep all 53 exactly as built.

SIZE_JS = """() => {
  const out = {};
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let el;
  while (el = walker.nextNode()) {
    const tag = el.tagName;
    if (['H1','H2','H3','H4','H5','H6','SCRIPT','STYLE','NOSCRIPT','SVG'].includes(tag)) continue;
    if (el.closest('h1,h2,h3,h4,h5,h6')) continue;
    // Recorded exceptions / icons (see findings): brand tagline, button micro-label, glyphs.
    if (el.closest('.check,.faq-toggle,.btn-small,.brand small')) continue;
    if (el.classList && (el.classList.contains('check') || el.classList.contains('faq-toggle') || el.classList.contains('btn-small'))) continue;
    let hasText = false;
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) { hasText = true; break; }
    }
    if (!hasText) continue;
    const cs = getComputedStyle(el);
    const size = parseFloat(cs.fontSize);
    if (Math.abs(size - 18) > 0.01) {
      const cls = (typeof el.className === 'string' && el.className) ? '.' + el.className.trim().split(/\\s+/).join('.') : '';
      const key = tag.toLowerCase() + cls + ' :: ' + size + 'px :: "' + el.textContent.trim().slice(0, 60) + '"';
      out[key] = (out[key] || 0) + 1;
    }
  }
  return out;
}"""

results = {}
overflow = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # Homepage screenshots first (desktop full + mobile full)
    for w, name in ((1280, 'home-1280'), (390, 'home-390')):
        ctx = browser.new_context(viewport={'width': w, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(ROOT + '/', wait_until='networkidle', timeout=60000)
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(OUT, f'{TAG}-{name}.png'), full_page=True)
        print(f'shot {name}: console errors {len(errs)} {errs[:3]}')
        ctx.close()
    # Sitewide size audit at desktop width
    for slug in SLUGS:
        ctx = browser.new_context(viewport={'width': 1280, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        try:
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=60000)
            pg.wait_for_timeout(300)
            ov = pg.evaluate("() => document.documentElement.scrollWidth - window.innerWidth")
            sizes = pg.evaluate(SIZE_JS)
            results[slug] = {'violations': sizes, 'consoleErrors': errs}
            overflow[slug] = ov
        except Exception as e:
            results[slug] = {'error': str(e)}
            overflow[slug] = None
        ctx.close()
    browser.close()

json.dump(results, open(os.path.join(OUT, f'{TAG}-sizes.json'), 'w'), indent=1)
json.dump(overflow, open(os.path.join(OUT, f'{TAG}-overflow.json'), 'w'), indent=1)
nviol = sum(len(v.get('violations', {})) for v in results.values() if isinstance(v, dict))
npages = sum(1 for v in results.values() if isinstance(v, dict) and v.get('violations'))
print(f'TAG={TAG} pages={len(results)} pages_with_violations={npages} distinct_violation_keys={nviol}')
for slug, v in results.items():
    if isinstance(v, dict) and v.get('violations'):
        print(' ', slug, '->', len(v['violations']), 'keys')
print('overflow != 0:', {k: v for k, v in overflow.items() if v not in (0, None)})
print('errors:', {k: v for k, v in results.items() if isinstance(v, dict) and (v.get('error') or v.get('consoleErrors'))})
