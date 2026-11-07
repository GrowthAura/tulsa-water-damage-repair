#!/usr/bin/env python3
"""Hero-fix round AFTER probe: H1 tops, H2 widow scan (per-word method),
overflow, console, commercial 2-link check, area cards + demand strips,
handle cards, phase grid, guide text sizes, resource card sizes, screenshots.
Usage: python3 tools/probe_after.py
Writes site/qa-hero-fix/after.json + screenshots.
"""
import json, os, re
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-hero-fix')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8317'
pages = json.load(open(os.path.join(BASE, 'content', 'pages.json')))
SLUGS = [p['slug'] for p in pages]
TYPES = {p['slug']: p.get('type') for p in pages}

H2_WORDS = """() => {
  const out = [];
  document.querySelectorAll('h2').forEach((h) => {
    const tn = [...h.childNodes].find(n => n.nodeType === 3 && n.textContent.trim());
    if (!tn) { out.push({id: h.id || null, text: h.innerText.trim().slice(0, 70), lines: ['?']}); return; }
    const words = tn.textContent.trim().split(/\\s+/);
    const lines = []; let cur = null; let off = 0;
    words.forEach((w) => {
      const range = document.createRange();
      range.setStart(tn, off); range.setEnd(tn, off + w.length);
      const rect = range.getBoundingClientRect();
      if (!cur || Math.abs(rect.top - cur.top) > 2) { cur = {top: Math.round(rect.top), words: []}; lines.push(cur); }
      cur.words.push(w); off += w.length + 1;
    });
    out.push({id: h.id || null, text: h.innerText.trim().slice(0, 70),
      lines: lines.map(l => l.words.join(' '))});
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

res = {'routes': {}, 'h2_widows': {}, 'commercial': {}, 'areas': {},
       'about': {}, 'home': {}, 'guides': {}, 'resources_hub': {}}

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    # --- per-route: H1 top @1440/390, overflow @1440/390/320, console ---
    for slug in SLUGS:
        row = {}
        for w in (1440, 390, 320):
            ctx = browser.new_context(viewport={'width': w, 'height': 900})
            pg = ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(400)
            m = pg.evaluate(MEASURE)
            row[f'w{w}'] = {'h1': m['h1count'], 'h1_top': m['h1_top'],
                            'badge_top': m['badge_top'], 'media_h': m['hero_media_h'],
                            'overflow': m['overflow']}
            if w == 390:
                row['console'] = sorted(set(errs))
            ctx.close()
        res['routes'][slug] = row
    # --- H2 widow scan @1440 + @1920 (all pages) ---
    for vw in (1440, 1920):
        widows = {}
        for slug in SLUGS:
            ctx = browser.new_context(viewport={'width': vw, 'height': 900})
            pg = ctx.new_page()
            pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
            pg.wait_for_timeout(300)
            for h in pg.evaluate(H2_WORDS):
                if len(h['lines']) >= 2 and len(h['lines'][-1].split()) == 1:
                    widows.setdefault(slug, []).append({'id': h['id'], 'text': h['text'], 'lines': h['lines']})
            ctx.close()
        res['h2_widows'][f'w{vw}'] = widows
    # --- commercial list: count <a> in the offer <ul> ---
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()
    pg.goto(ROOT + '/commercial/', wait_until='networkidle', timeout=30000)
    pg.wait_for_timeout(300)
    res['commercial'] = pg.evaluate("""() => {
      const h = document.getElementById('which-commercial-restoration-services-do-we-offer');
      let ul = h; while (ul && ul.tagName !== 'UL') ul = ul.nextElementSibling;
      const links = [...ul.querySelectorAll('a')].map(a => ({href: a.getAttribute('href'), text: a.innerText.trim().slice(0, 50)}));
      return {links, count: links.length};
    }""")
    # --- area pages: offer cards + demand strip ---
    for slug in SLUGS:
        if TYPES[slug] != 'area':
            continue
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(300)
        res['areas'][slug] = pg.evaluate("""() => {
          const h = [...document.querySelectorAll('h2')].find(x => /Services Do We Offer in/.test(x.innerText));
          let cards = 0, strip = null;
          if (h) {
            let n = h.nextElementSibling;
            while (n && !(n.classList && n.classList.contains('cards'))) n = n.nextElementSibling;
            if (n) cards = n.querySelectorAll('article.card').length;
            let s = h.parentElement.querySelector('.demand-strip');
            if (s) strip = {h3: s.querySelector('h3').innerText, items: [...s.querySelectorAll('li strong')].map(x => x.innerText)};
          }
          return {cards, strip};
        }""")
    # --- about handle cards ---
    pg.goto(ROOT + '/about-us/', wait_until='networkidle', timeout=30000)
    pg.wait_for_timeout(300)
    res['about'] = pg.evaluate("""() => {
      const h = document.getElementById('what-do-we-handle');
      let cards = 0, more = null;
      if (h) {
        let n = h.nextElementSibling;
        while (n && !(n.classList && n.classList.contains('cards'))) n = n.nextElementSibling;
        if (n) cards = n.querySelectorAll('article.card').length;
        const m = h.parentElement.querySelector('.handle-more a');
        if (m) more = {href: m.getAttribute('href'), text: m.innerText};
      }
      return {cards, more};
    }""")
    # --- homepage: phase grid + include h2 lines ---
    pg.goto(ROOT + '/', wait_until='networkidle', timeout=30000)
    pg.wait_for_timeout(300)
    res['home'] = pg.evaluate("""() => {
      const grid = document.querySelector('.phase-grid');
      const h = document.getElementById('what-does-water-damage-restoration-in-tulsa-include');
      return {phase_cards: grid ? grid.querySelectorAll('.phase-card').length : 0,
              phase_titles: grid ? [...grid.querySelectorAll('h3')].map(x => x.innerText) : [],
              include_h2_w: h ? Math.round(h.getBoundingClientRect().width) : null};
    }""")
    # --- guide text sizes ---
    for slug, label in [('/resources/first-24-hours-after-water-damage', 'guide'),
                        ('/services/burst-pipe-water-damage', 'service-control')]:
        pg.goto(ROOT + slug, wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(300)
        res['guides'][label] = pg.evaluate("""() => {
          const p = document.querySelector('.content-block > p');
          const li = document.querySelector('.content-block li');
          return {p_px: p ? getComputedStyle(p).fontSize : null,
                  li_px: li ? getComputedStyle(li).fontSize : null};
        }""")
    # --- resources hub card sizes ---
    pg.goto(ROOT + '/resources/', wait_until='networkidle', timeout=30000)
    pg.wait_for_timeout(300)
    res['resources_hub'] = pg.evaluate("""() => {
      const h3 = document.querySelector('.resource-cards .card-body h3');
      const p = document.querySelector('.resource-cards .card-body p');
      return {cards: document.querySelectorAll('.resource-cards article.card').length,
              h3_px: h3 ? getComputedStyle(h3).fontSize : null,
              p_px: p ? getComputedStyle(p).fontSize : null};
    }""")
    # --- screenshots ---
    def shot(path, vw, url, scroll_to=None, full=False):
        c = browser.new_context(viewport={'width': vw, 'height': 900})
        p = c.new_page()
        p.goto(ROOT + url, wait_until='networkidle', timeout=30000)
        p.wait_for_timeout(600)
        if scroll_to:
            p.evaluate(f"() => {{ const el = document.querySelector('{scroll_to}'); if (el) window.scrollTo(0, el.getBoundingClientRect().top + window.scrollY - 100); }}")
            p.wait_for_timeout(500)
        p.screenshot(path=os.path.join(OUT, path), full_page=full)
        c.close()
    shot('after-home-1440-top.png', 1440, '/')
    shot('after-home-390-top.png', 390, '/')
    shot('after-include-1440.png', 1440, '/', scroll_to='#what-does-water-damage-restoration-in-tulsa-include')
    shot('after-include-390.png', 390, '/', scroll_to='#what-does-water-damage-restoration-in-tulsa-include')
    shot('after-table-1440.png', 1440, '/', scroll_to='.table-wrap')
    shot('after-table-390.png', 390, '/', scroll_to='.table-wrap')
    shot('after-contact-1440.png', 1440, '/contact/')
    shot('after-contact-390.png', 390, '/contact/')
    shot('after-about-handle-1440.png', 1440, '/about-us/', scroll_to='#what-do-we-handle')
    shot('after-resources-1440.png', 1440, '/resources/')
    shot('after-bixby-1440.png', 1440, '/service-areas/bixby-ok/', scroll_to='.demand-strip')
    shot('after-bixby-390.png', 390, '/service-areas/bixby-ok/', scroll_to='.demand-strip')
    shot('after-broken-arrow-1440.png', 1440, '/service-areas/broken-arrow-ok/', scroll_to='.demand-strip')
    shot('after-broken-arrow-390.png', 390, '/service-areas/broken-arrow-ok/', scroll_to='.demand-strip')
    shot('after-owasso-1440.png', 1440, '/service-areas/owasso-ok/', scroll_to='.demand-strip')
    shot('after-guide-1440.png', 1440, '/resources/first-24-hours-after-water-damage')
    shot('after-guide-390.png', 390, '/resources/first-24-hours-after-water-damage')
    # inner hero samples
    shot('after-inner-sewage-1440.png', 1440, '/services/sewage-backup-cleanup')
    shot('after-inner-flood-1440.png', 1440, '/services/flood-damage-restoration')
    ctx.close()
    browser.close()

json.dump(res, open(os.path.join(OUT, 'after.json'), 'w'), indent=1)
print('written', os.path.join(OUT, 'after.json'))
