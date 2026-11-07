#!/usr/bin/env python3
"""Colour probe: computed H1/H2/H3 colours + effective background + WCAG contrast.
Usage: python3 tools/probe_colours.py — prints a table, writes site/qa-wide/colours.json.
"""
import json, os
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-wide')
ROOT = 'http://127.0.0.1:8317'

TARGETS = [
    ('/', '.hero h1', 'hero H1 (navy bg)'),
    ('/', '.content-block h2', 'home first H2 (cream bg)'),
    ('/', '.content-block h3', 'home first H3 (cream bg)'),
    ('/', '.section-navy h2', 'home navy-section H2'),
    ('/services/', '.section-navy h2', 'hub navy H2'),
    ('/services/', '.card-body h3 a', 'hub card-title link (cream card on navy)'),
    ('/services/emergency-water-damage-restoration', '.hero h1', 'service hero H1'),
    ('/services/emergency-water-damage-restoration', '.content-block h2', 'service first H2'),
    ('/services/emergency-water-damage-restoration', '.content-block h3', 'service first H3'),
    ('/services/emergency-water-damage-restoration', '.faq-list summary h3', 'service FAQ H3'),
    ('/services/emergency-water-damage-restoration', '.brand-panel h3', 'aside brand-panel H3 (navy panel)'),
    ('/service-areas/broken-arrow-ok/', '.content-block h2', 'area first H2'),
    ('/service-areas/broken-arrow-ok/', '.content-block h3', 'area first H3'),
    ('/contact/', '.form-card h3', 'contact form H3 (white card)'),
    ('/services/ceiling-water-damage', '.brand-panel h3', 'ceiling brand-panel H3 (navy panel, no body img)'),
    ('/', '.card-body h3', 'home card-title H3 element (cream card in navy section)'),
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
           fontSize: cs.fontSize, fontWeight: cs.fontWeight };
}"""

rows = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    seen = {}
    for slug, sel, label in TARGETS:
        if slug not in seen:
            page.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            page.evaluate("""async () => {
              for (let y = 0; y <= document.body.scrollHeight; y += 500) {
                window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
              window.scrollTo(0, 0); }""")
            page.wait_for_timeout(600)
            seen[slug] = True
        r = page.evaluate(JS, sel)
        rows.append({'page': slug, 'label': label, 'selector': sel, **(r or {'missing': True})})
        if r:
            print(f"{label:38s} {r['color']:22s} on {r['background']:22s} contrast {r['contrast']}:1  ({'PASS' if r['contrast'] >= 4.5 else 'FAIL'})")
        else:
            print(f"{label:38s} MISSING element {sel}")
    browser.close()

json.dump(rows, open(os.path.join(OUT, 'colours.json'), 'w'), indent=1)
bad = [r for r in rows if r.get('contrast', 99) < 4.5]
print(f"\nFAIL (<4.5:1): {len(bad)}  MISSING: {sum(1 for r in rows if r.get('missing'))}")
