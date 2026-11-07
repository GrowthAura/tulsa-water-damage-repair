#!/usr/bin/env python3
"""Menu-scroller verification (menu-scroll + orphan round):
- Desktop 1440x900: open Services + Service Areas dropdowns, measure
  .nav-drop scrollHeight vs clientHeight (must scroll), computed max-height
  and overflow-y, every link reachable via scrollIntoView, no page overflow.
- Mobile 390x844: open the mobile menu overlay, same checks for .mobile-menu.
- Screenshots into site/qa-menu-orphans/ (viewed by pixels).
Usage: python3 tools/probe_menu_scroll.py   (serves out/ on :8319 itself)
"""
import json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright

BASE = os.path.expanduser('~/workspace/tulsa-water-damage-repair/site')
OUT = os.path.join(BASE, 'qa-menu-orphans')
os.makedirs(OUT, exist_ok=True)
ROOT = 'http://127.0.0.1:8319'
res = {}

srv = subprocess.Popen([sys.executable, os.path.join(BASE, 'tools', 'serve.py'), '8319'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # ---------- desktop dropdowns ----------
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(ROOT + '/', wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(400)
        for name, label in (('services', 'Services'), ('areas', 'Service Areas')):
            pg.click(f'.main-nav details summary:has-text("{label}")')
            pg.wait_for_timeout(350)
            m = pg.evaluate("""() => {
              const drops = [...document.querySelectorAll('.nav-drop')];
              const d = drops.find(x => x.offsetParent !== null) || drops[0];
              const cs = getComputedStyle(d);
              const links = [...d.querySelectorAll('a')];
              return {scrollH: d.scrollHeight, clientH: d.clientHeight,
                      maxH: cs.maxHeight, overflowY: cs.overflowY,
                      scrollbarWidth: cs.scrollbarWidth,
                      scrollbarColor: cs.scrollbarColor,
                      links: links.length,
                      lastLink: links.length ? links[links.length-1].textContent.trim() : ''};
            }""")
            # every link reachable: scrollIntoView the last link, it must end up visible inside the drop
            reach = pg.evaluate("""() => {
              const drops = [...document.querySelectorAll('.nav-drop')];
              const d = drops.find(x => x.offsetParent !== null) || drops[0];
              const links = [...d.querySelectorAll('a')];
              let bad = [];
              for (const a of links) {
                a.scrollIntoView({block: 'nearest'});
                const r = a.getBoundingClientRect(), dr = d.getBoundingClientRect();
                if (r.bottom < dr.top || r.top > dr.bottom) bad.push(a.textContent.trim());
              }
              return {unreachable: bad, scrollTopAfterLast: d.scrollTop,
                      pageOverflow: document.documentElement.scrollWidth - window.innerWidth};
            }""")
            m.update(reach)
            m['console'] = sorted(set(errs))
            res[f'desktop_{name}'] = m
            pg.screenshot(path=os.path.join(OUT, f'desktop-drop-{name}.png'))
            print(f"desktop {name}: scroll {m['scrollH']} vs client {m['clientH']}, links {m['links']}, "
                  f"unreachable {m['unreachable']}, pageOverflow {m['pageOverflow']}, console {m['console']}")
            pg.keyboard.press('Escape')
            pg.wait_for_timeout(200)
        ctx.close()
        # ---------- mobile menu ----------
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        pg = ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(ROOT + '/', wait_until='networkidle', timeout=30000)
        pg.wait_for_timeout(400)
        pg.click('.mobile-head details summary')
        pg.wait_for_timeout(400)
        m = pg.evaluate("""() => {
          const d = document.querySelector('.mobile-menu');
          const cs = getComputedStyle(d);
          const links = [...d.querySelectorAll('a')];
          return {scrollH: d.scrollHeight, clientH: d.clientHeight,
                  maxH: cs.maxHeight, overflowY: cs.overflowY,
                  scrollbarWidth: cs.scrollbarWidth,
                  scrollbarColor: cs.scrollbarColor,
                  links: links.length,
                  pageOverflow: document.documentElement.scrollWidth - window.innerWidth};
        }""")
        reach = pg.evaluate("""() => {
          const d = document.querySelector('.mobile-menu');
          const links = [...d.querySelectorAll('a')];
          let bad = [];
          for (const a of links) {
            a.scrollIntoView({block: 'nearest'});
            const r = a.getBoundingClientRect(), dr = d.getBoundingClientRect();
            if (r.bottom < dr.top || r.top > dr.bottom) bad.push(a.textContent.trim());
          }
          return {unreachable: bad, scrollTopAfterLast: d.scrollTop};
        }""")
        m.update(reach)
        m['console'] = sorted(set(errs))
        res['mobile_menu'] = m
        pg.screenshot(path=os.path.join(OUT, 'mobile-menu-open.png'))
        print(f"mobile menu: scroll {m['scrollH']} vs client {m['clientH']}, links {m['links']}, "
              f"unreachable {m['unreachable']}, pageOverflow {m['pageOverflow']}, console {m['console']}")
        ctx.close()
        browser.close()
finally:
    srv.terminate()
json.dump(res, open(os.path.join(OUT, 'menu-scroll.json'), 'w'), indent=2)
print('wrote', os.path.join(OUT, 'menu-scroll.json'))
