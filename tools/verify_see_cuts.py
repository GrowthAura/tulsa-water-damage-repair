#!/usr/bin/env python3
"""Re-verify 0 dangling 'See and' / dangling 'See'/'see' remain in pages.json
after the cuts. Expected survivors: burst-pipe block 16 (real sentence
'...what you can see.') and the water-heater 'Related services: and' bare
anchor (report-only, needs his word)."""
import json, re

BASE = '/home/hatch/workspace/tulsa-water-damage-repair/site'
d = json.load(open(f'{BASE}/content/pages.json'))

seeand = []
dangling = []
bare_and = []

def check_text(slug, where, text):
    if text is None:
        return
    t = re.sub(r'<[^>]+>', '', text)  # strip tags for the text check
    t = t.replace('&quot;', '"').replace('&#x27;', "'").strip()
    if re.search(r'\bSee\s+and\b', t):
        seeand.append((slug, where, t[-100:]))
    # dangling See/see at end (allow optional trailing period)
    m = re.search(r'\b([Ss]ee)\.?\s*$', t)
    if m:
        dangling.append((slug, where, t[-100:]))
    # bare <a>and</a> with no surrounding sentence
    if re.search(r'<a[^>]*>\s*and\s*</a>', text):
        bare_and.append((slug, where, text[-160:]))

for p in d:
    slug = p['slug']
    for bi, blk in enumerate(p.get('blocks', [])):
        if 'html' in blk:
            check_text(slug, f'block {bi} (p)', blk['html'])
        if 'items' in blk:
            for ii, it in enumerate(blk['items']):
                check_text(slug, f'block {bi} item {ii}', it)
        if blk.get('t') == 'table':
            for ri, row in enumerate(blk.get('rows', [])):
                for ci, cell in enumerate(row):
                    check_text(slug, f'block {bi} row {ri} cell {ci}', cell)
    for fi, f in enumerate(p.get('faqs', [])):
        check_text(slug, f'FAQ {fi}', f.get('a_html', ''))

print('dangling "See and":', len(seeand))
for x in seeand:
    print('  ', x)
print('dangling "See"/"see" endings:', len(dangling))
for x in dangling:
    print('  ', x)
print('bare "<a>and</a>":', len(bare_and))
for x in bare_and:
    print('  ', x)

# Collinsville mold link present?
col = [x for x in d if x['slug'] == '/service-areas/collinsville-ok/'][0]
print('Collinsville offer items with hrefs:',
      sum(1 for it in col['blocks'][16]['items'] if 'href=' in it), '/', len(col['blocks'][16]['items']))
print('Collinsville mold item:', col['blocks'][16]['items'][3][:120])
