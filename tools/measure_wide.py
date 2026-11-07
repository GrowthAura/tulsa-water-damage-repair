#!/usr/bin/env python3
"""Wide-pass measurement: rendered widths of headings + intro text at 1440/390.
Measures (per page, per width): container content width, hero h1, hero-intro,
navy-band lead, first content H2, split text column, sticky aside, call-strip p,
final-cta p, faq-list, overflow, h1 count, console errors.
Screenshots: desktop full-page + mobile top for the shot set.
Usage: python3 tools/measure_wide.py <tag>   (tag = before | after)
Writes site/qa-wide/<tag>-widths.json + screenshots.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
TAG = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = os.path.join(BASE, 'qa-wide')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'

SLUGS = ['/', '/services/emergency-water-damage-restoration',
         '/services/flood-damage-restoration',
         '/service-areas/broken-arrow-ok/']

JS = """() => {
  const q = (s) => document.querySelector(s);
  const w = (el) => el ? Math.round(el.getBoundingClientRect().width) : null;
  const heroH1 = q('.hero h1');
  const heroIntro = q('.hero .hero-intro');
  const navyLead = q('.section-navy .lead');
  const firstH2 = q('.content-block h2');
  const splitText = q('.split .content-block');
  const aside = q('.sticky-aside');
  const stripP = q('.call-strip p');
  const ctaP = q('.final-cta-card p');
  const faq = q('.faq-list');
  const container = q('.hero .container') || q('.container');
  const hero = q('.hero');
  return {
    scrollW: document.documentElement.scrollWidth,
    innerW: window.innerWidth,
    overflow: document.documentElement.scrollWidth - window.innerWidth,
    h1: [...document.querySelectorAll('h1')].length,
    containerW: w(container),
    heroW: w(hero),
    heroH1W: w(heroH1),
    heroH1Lines: heroH1 ? Math.round(heroH1.getBoundingClientRect().height / parseFloat(getComputedStyle(heroH1).lineHeight)) : null,
    heroIntroW: w(heroIntro),
    navyLeadW: w(navyLead),
    firstH2W: w(firstH2),
    splitTextW: w(splitText),
    asideW: w(aside),
    asideSticky: aside ? getComputedStyle(aside).position : null,
    stripPW: w(stripP),
    ctaPW: w(ctaP),
    faqW: w(faq),
  };
}"""

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for slug in SLUGS:
        row = {'slug': slug, 'widths': {}}
        for vw in (1440, 390):
            ctx = browser.new_context(viewport={'width': vw, 'height': 900}, device_scale_factor=1)
            page = ctx.new_page()
            errors = []
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            page.evaluate("""async () => {
              for (let y = 0; y <= document.body.scrollHeight; y += 500) {
                window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); }
              window.scrollTo(0, 0);
            }""")
            page.wait_for_timeout(800)
            m = page.evaluate(JS)
            m['console_errors'] = errors
            row['widths'][vw] = m
            safe = slug.strip('/').replace('/', '_') or 'home'
            page.screenshot(path=os.path.join(OUT, f'{TAG}-{safe}-{vw}.png'), full_page=(vw == 1440))
            if vw != 1440:
                page.screenshot(path=os.path.join(OUT, f'{TAG}-{safe}-{vw}-top.png'))
            ctx.close()
        results.append(row)
        for vw in (1440, 390):
            d = row['widths'][vw]
            print(f"{slug} @{vw}: container={d['containerW']} h1={d['heroH1W']} "
                  f"intro={d['heroIntroW']} navyLead={d['navyLeadW']} h2={d['firstH2W']} "
                  f"textCol={d['splitTextW']} aside={d['asideW']}({d['asideSticky']}) "
                  f"strip={d['stripPW']} cta={d['ctaPW']} faq={d['faqW']} "
                  f"overflow={d['overflow']} h1count={d['h1']} err={len(d['console_errors'])}")
    browser.close()

json.dump(results, open(os.path.join(OUT, f'{TAG}-widths.json'), 'w'), indent=1)
print(f'wrote {OUT}/{TAG}-widths.json')
