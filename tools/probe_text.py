#!/usr/bin/env python3
"""Text-size + colour probe: computed font-size/line-height/colour/background/contrast
for body text elements at 1440 and 390. Screenshots: desktop full + mobile top.
Usage: python3 tools/probe_text.py <tag>   (tag = before | after)
Writes site/qa-text/<tag>-text.json + screenshots.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
TAG = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = os.path.join(BASE, 'qa-text')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8321'

SLUGS = ['/', '/services/emergency-water-damage-restoration',
         '/service-areas/broken-arrow-ok/', '/contact/']

TARGETS = [
    ('.content-block > p', 'body paragraph'),
    ('.content-block p.lead', 'lead paragraph (content)'),
    ('.hero .hero-intro', 'hero intro (home)'),
    ('.section-navy .lead', 'navy-band lead (inner)'),
    ('.content-block ul li', 'list item'),
    ('.table-wrap td', 'table cell'),
    ('.faq-answer', 'FAQ answer'),
    ('.card-body p', 'card blurb'),
    ('.card-body h3 a', 'card title link'),
    ('.content-block > p a', 'body link'),
    ('.brand-panel p', 'brand-panel text'),
    ('.footer-col p', 'footer text'),
    ('.footer-col ul a', 'footer link'),
    ('.crumbs', 'breadcrumb'),
    ('.form-card label', 'form label'),
]

JS = """(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const cs = getComputedStyle(el);
  let bg = null, node = el;
  while (node && node !== document.body) {
    const b = getComputedStyle(node).backgroundColor;
    if (b && !b.startsWith('rgba(0, 0, 0, 0') && b !== 'transparent') { bg = b; break; }
    node = node.parentElement;
  }
  if (!bg) bg = getComputedStyle(document.body).backgroundColor;
  const parse = (s) => s.match(/[\\d.]+/g).map(Number);
  const lum = (rgb) => {
    const [r, g, b] = rgb.slice(0, 3).map(v => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const fg = parse(cs.color), bgRgb = parse(bg);
  const l1 = lum(fg), l2 = lum(bgRgb);
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  return { color: cs.color, background: bg, contrast: Math.round(ratio * 100) / 100,
           fontSize: cs.fontSize, lineHeight: cs.lineHeight, fontWeight: cs.fontWeight };
}"""

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in SLUGS:
        row = {'slug': slug, 'widths': {}}
        for vw in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': vw, 'height': 900}, device_scale_factor=1)
            page = ctx.new_page()
            errors = []
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            page.evaluate("""async () => {
              for (let y = 0; y <= document.body.scrollHeight; y += 500) {
                window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
              window.scrollTo(0, 0); }""")
            page.wait_for_timeout(700)
            m = {
                'scrollW': page.evaluate("document.documentElement.scrollWidth"),
                'innerW': vw,
                'overflow': page.evaluate("document.documentElement.scrollWidth - window.innerWidth"),
                'h1': page.evaluate("document.querySelectorAll('h1').length"),
                'console_errors': errors,
            }
            for sel, label in TARGETS:
                r = page.evaluate(JS, sel)
                m[label] = r
                if r:
                    print(f"{slug} @{vw} {label:28s} {r['fontSize']:>6s} / lh {r['lineHeight']:>6s}  {r['color']:20s} on {r['background']:20s} {r['contrast']}:1 {'PASS' if r['contrast'] >= 4.5 else 'FAIL'}")
                else:
                    print(f"{slug} @{vw} {label:28s} MISSING")
            row['widths'][vw] = m
            safe = slug.strip('/').replace('/', '_') or 'home'
            if vw == 1440:
                page.screenshot(path=os.path.join(OUT, f'{TAG}-{safe}-1440.png'), full_page=True)
            elif vw == 390:
                page.screenshot(path=os.path.join(OUT, f'{TAG}-{safe}-390-top.png'))
            ctx.close()
        results.append(row)
    browser.close()

json.dump(results, open(os.path.join(OUT, f'{TAG}-text.json'), 'w'), indent=1)
bad = [ (r['slug'], vw, lab) for r in results for vw, m in r['widths'].items()
        for lab, v in m.items() if isinstance(v, dict) and v.get('contrast', 99) < 4.5 ]
print(f"\nCONTRAST FAIL (<4.5:1): {len(bad)} {bad}")
print(f"wrote {OUT}/{TAG}-text.json")
