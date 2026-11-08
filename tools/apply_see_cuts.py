#!/usr/bin/env python3
"""Apply the ordered 'See and' / dangling 'See'/'see' cuts to content/pages.json.

Rules (user-ordered, 2026-11-08):
- Cut 'See <a>and</a>' (18) wherever it dangles at the end of a paragraph.
- Cut a lone dangling 'See'/'see' that ends a bullet/paragraph/FAQ/table cell
  with no continuation after it.
- DO NOT cut: burst-pipe block 16 ('...larger than what you can see.' — the
  'see' is the last word of a real sentence), and the water-heater-leak
  'Related services: and' bare anchor (report only, needs his word).
- Collinsville offer list item 3: restore the doc's Mold remediation link
  (doc has 'Mold remediation ... (/services/mold-remediation)'; the parse
  dropped it). This is a restore, not an added link.
Every cut is recorded to qa-home-round/see-cuts-applied.json with before/after.
"""
import json, re, sys

BASE = '/home/hatch/workspace/tulsa-water-damage-repair/site'
d = json.load(open(f'{BASE}/content/pages.json'))
by_slug = {p['slug']: p for p in d}
cls = json.load(open(f'{BASE}/qa-home-round/see-classification.json'))
cuts = []

def parse_entry(entry):
    slug, rest = entry.split(' | ', 1)
    m = re.search(r'block (\d+)', rest)
    bi = int(m.group(1)) if m else None
    field = 'p'
    idx = None
    row = cell = None
    m2 = re.search(r'item (\d+)', rest)
    m3 = re.search(r'FAQ (\d+)', rest)
    m4 = re.search(r'row (\d+) cell (\d+)', rest)
    if m2:
        field, idx = 'item', int(m2.group(1))
    elif m3:
        field, idx = 'faq', int(m3.group(1))
    elif m4:
        field, row, cell = 'table', int(m4.group(1)), int(m4.group(2))
    return slug, bi, field, idx, row, cell

def get_field(slug, bi, field, idx, row, cell):
    page = by_slug[slug]
    if field == 'faq':
        return page['faqs'][idx]['a_html']
    blk = page['blocks'][bi]
    if field == 'item':
        return blk['items'][idx]
    if field == 'table':
        return blk['rows'][row][cell]
    return blk['html']

def set_field(slug, bi, field, idx, row, cell, value):
    page = by_slug[slug]
    if field == 'faq':
        page['faqs'][idx]['a_html'] = value
        return
    blk = page['blocks'][bi]
    if field == 'item':
        blk['items'][idx] = value
        return
    if field == 'table':
        blk['rows'][row][cell] = value
        return
    blk['html'] = value

# --- 1. 'See and' cuts (18) ---
for entry in cls['cut_seeand']:
    slug, bi, field, idx, row, cell = parse_entry(entry)
    assert field == 'p', entry
    html = get_field(slug, bi, field, idx, row, cell)
    pat = re.compile(r' ?See +<a[^>]*>and</a> ?')
    matches = pat.findall(html)
    assert len(matches) == 1, f'{slug} block {bi}: expected 1 See-and, found {len(matches)} :: {html[-180:]}'
    new = pat.sub('', html, count=1)
    assert '..' not in new[-30:], f'{slug} block {bi}: double period after cut :: {new[-120:]}'
    set_field(slug, bi, field, idx, row, cell, new)
    cuts.append({'type': 'see-and', 'slug': slug, 'block': bi, 'before': html[-140:], 'after': new[-140:]})

# --- 2. Dangling See/see cuts ---
remove_blocks = []  # (slug, bi) of <p> blocks whose ONLY content is 'See' — removed at the end
for entry in cls['cut_see']:
    slug, bi, field, idx, row, cell = parse_entry(entry)
    # SKIP: burst-pipe block 16 — real sentence ending '...what you can see.'
    if slug == '/services/burst-pipe-water-damage' and bi == 16:
        cuts.append({'type': 'KEPT-real-sentence', 'slug': slug, 'block': bi,
                     'before': get_field(slug, bi, field, idx, row, cell)[-140:], 'after': '(unchanged)'})
        continue
    # SPECIAL: burst-pipe block 31 — two dangling 'see's, one before <br>, one inside an <a>.
    if slug == '/services/burst-pipe-water-damage' and bi == 31:
        html = get_field(slug, bi, field, idx, row, cell)
        assert html == ('<strong>For <a href="/services/ceiling-water-damage">ceiling damage</a> '
                        'from attic bursts:</strong> see <br><a href="/services/hardwood-floor-drying">'
                        '<strong>For hardwood floors:</strong> see</a> '), f'unexpected burst-31: {html!r}'
        new = ('<strong>For <a href="/services/ceiling-water-damage">ceiling damage</a> '
               'from attic bursts:</strong><br><a href="/services/hardwood-floor-drying">'
               '<strong>For hardwood floors:</strong></a>')
        set_field(slug, bi, field, idx, row, cell, new)
        cuts.append({'type': 'see-x2-special', 'slug': slug, 'block': bi, 'before': html, 'after': new})
        continue
    text = get_field(slug, bi, field, idx, row, cell)
    stripped = text.rstrip()
    # SPECIAL: a <p> block whose ONLY content is 'See' — the whole block is the
    # dangling word. Defer removal to the end (descending index order, so no
    # other block index is invalidated).
    if field == 'p' and stripped.rstrip('.') in ('See', 'see'):
        remove_blocks.append((slug, bi))
        cuts.append({'type': 'see-only-block-REMOVE', 'slug': slug, 'block': bi,
                     'before': text, 'after': '(block removed — its only content was the dangling See)'})
        continue
    # SPECIAL: sewage bullet is a LINK whose text is 'Basement backups: see'.
    # Cut ': see' (the colon only introduced the removed 'see') so the bullet
    # becomes 'Basement backups' — the user's stated result. Link target unchanged.
    if slug == '/services/sewage-backup-cleanup' and bi == 40 and field == 'item':
        assert text == ('<a href="/services/flooded-basement-cleanup"><strong>Basement backups:'
                        '</strong> see</a> '), f'unexpected sewage bullet: {text!r}'
        new = '<a href="/services/flooded-basement-cleanup"><strong>Basement backups</strong></a> '
        set_field(slug, bi, field, idx, row, cell, new)
        cuts.append({'type': 'see-colon', 'slug': slug, 'block': bi, 'item': idx,
                     'before': text, 'after': new})
        continue
    # GENERAL: trailing ' See' / ' see' (optional trailing period/space).
    m = re.search(r'\s+([Ss]ee)\.?\s*$', stripped)
    assert m, f'{slug} block {bi} {field}: no trailing See/see :: {stripped[-140:]}'
    # The 'See' must be a dangling fragment: preceded by a sentence end ('.',
    # optionally followed by a closing quote, e.g. ...dries." See) or be a lone
    # bullet/table/FAQ fragment — never part of a real clause.
    before_see = stripped[:m.start()]
    tail = before_see.rstrip()
    tail = re.sub(r"(&quot;|&#x27;|&apos;|[\"'])+$", '', tail).rstrip()
    assert tail.endswith('.') or field in ('item', 'table', 'faq'), \
        f'{slug} block {bi} {field}: See not after a period :: {stripped[-140:]}'
    new = before_see.rstrip()
    set_field(slug, bi, field, idx, row, cell, new)
    cuts.append({'type': 'see', 'slug': slug, 'block': bi, 'field': field, 'idx': idx,
                 'before': text[-140:], 'after': new[-140:]})

# --- 3. Collinsville Mold remediation link restore (doc link, parse dropped it) ---
col = by_slug['/service-areas/collinsville-ok/']
item3 = col['blocks'][16]['items'][3]
assert item3 == '<strong>Mold remediation</strong> containment and removal under IICRC S520 guidelines ', \
    f'unexpected Collinsville item 3: {item3!r}'
new3 = ('<strong><a href="/services/mold-remediation">Mold remediation</a></strong> '
        'containment and removal under IICRC S520 guidelines ')
col['blocks'][16]['items'][3] = new3
cuts.append({'type': 'collinsville-mold-link-restore', 'slug': '/service-areas/collinsville-ok/',
             'block': 16, 'item': 3, 'before': item3, 'after': new3})

# --- 4. Deferred removal of 'See'-only blocks (descending index per page) ---
from collections import defaultdict
by_page = defaultdict(list)
for slug, bi in remove_blocks:
    by_page[slug].append(bi)
for slug, bis in by_page.items():
    for bi in sorted(bis, reverse=True):
        blk = by_slug[slug]['blocks'][bi]
        assert blk.get('html', '').strip().rstrip('.') in ('See', 'see'), \
            f'removal target changed: {slug} block {bi}: {blk.get("html", "")!r}'
        del by_slug[slug]['blocks'][bi]
print('See-only blocks removed:', dict(by_page))

json.dump(d, open(f'{BASE}/content/pages.json', 'w'), indent=2, ensure_ascii=False)
json.dump(cuts, open(f'{BASE}/qa-home-round/see-cuts-applied.json', 'w'), indent=2, ensure_ascii=False)

from collections import Counter
print('cuts by type:', dict(Counter(c['type'] for c in cuts)))
print('total records:', len(cuts))
print('pages.json written.')
