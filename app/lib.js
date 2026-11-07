import pagesDataRaw from '../content/pages.json';
import imagesData from '../content/images.json';

/* The parser HTML-escapes plain-text fields (blurb, intro, h1, FAQ questions,
   h2 text, schema answer text) because it also builds HTML strings from them.
   Those fields are rendered as JSX text or JSON strings, where React/JSON
   would escape the & a second time and the page would show literal &#x27;.
   Decode entities in PLAIN-TEXT fields only — `html`/`a_html` fields stay
   escaped because they are injected as HTML via dangerouslySetInnerHTML. */
const NAMED = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
  ndash: '–', mdash: '—', rsquo: '’', lsquo: '‘', rdquo: '”', ldquo: '“',
  hellip: '…', copy: '©', reg: '®', trade: '™',
};
function unescapeEntities(s) {
  if (typeof s !== 'string' || !s.includes('&')) return s;
  return s
    .replace(/&#x([0-9a-fA-F]+);/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(parseInt(d, 10)))
    .replace(/&([a-zA-Z]+);/g, (_, n) => (NAMED[n] !== undefined ? NAMED[n] : `&${n};`));
}
function fixPage(p) {
  const q = { ...p };
  for (const f of ['h1', 'metaTitle', 'metaDescription', 'blurb', 'intro']) {
    if (q[f]) q[f] = unescapeEntities(q[f]);
  }
  if (Array.isArray(q.faqs)) {
    q.faqs = q.faqs.map((f) => ({ ...f, q: unescapeEntities(f.q), a_text: unescapeEntities(f.a_text) }));
  }
  if (Array.isArray(q.blocks)) {
    q.blocks = q.blocks.map((b) => {
      const nb = { ...b };
      if (nb.text) nb.text = unescapeEntities(nb.text);
      if (nb.plain) nb.plain = unescapeEntities(nb.plain);
      return nb;
    });
  }
  return q;
}
const pagesData = pagesDataRaw.map(fixPage);

export const SITE = {
  brand: 'Tulsa Water Damage Repair',
  domain: 'tulsawaterdamagerepair.com',
  url: 'https://tulsawaterdamagerepair.com',
  phone: '(918) 395-9320',
  phoneHref: 'tel:+19183959320',
  address: '400 S 129th E Ave, Tulsa, OK 74108',
  mapQuery: '400 S 129th E Ave, Tulsa, OK 74108',
};

export const PAGES = pagesData;
export const IMAGES = imagesData && typeof imagesData === 'object' ? imagesData : {};
export const PAGE_BY_SLUG = Object.fromEntries(PAGES.map((p) => [p.slug, p]));

export function normSlug(s) {
  if (!s) return '/';
  return s === '/' ? '/' : s.replace(/\/$/, '') || '/';
}

export function pageImage(slug) {
  const entry = IMAGES[slug] || {};
  return {
    hero: entry.hero ? { ...entry.hero } : null,
    body: entry.body ? { ...entry.body } : null,
  };
}

export function shortName(slug) {
  const last = slug.replace(/\/$/, '').split('/').filter(Boolean).pop() || 'home';
  return last
    .replace(/-ok$/, '')
    .replace(/-tulsa$/, '')
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

export function parentOf(page) {
  if (page.type === 'service') return { label: 'Services', href: '/services/' };
  /* No /service-areas/ hub route exists, so area pages have no parent crumb:
     linking "Service Areas" to "/" was a duplicate Home link with a wrong name. */
  if (page.type === 'area') return null;
  if (page.type === 'resource') return { label: 'Resources', href: '/resources/' };
  return null;
}

/* Service groups for nav dropdown + cards — order follows the doc's homepage groups. */
export const SERVICE_GROUPS = [
  {
    label: 'Emergency & Water Removal',
    slugs: [
      '/services/emergency-water-damage-restoration',
      '/services/water-mitigation',
      '/services/flood-damage-restoration',
      '/services/flooded-basement-cleanup',
      '/services/sewage-backup-cleanup',
    ],
  },
  {
    label: 'Water Damage by Source',
    slugs: [
      '/services/burst-pipe-water-damage',
      '/services/slab-leak-water-damage/',
      '/services/water-heater-leak-cleanup/',
      '/services/appliance-leak-water-damage/',
      '/services/ac-drain-line-overflow-cleanup/',
      '/services/roof-leak-water-damage/',
    ],
  },
  {
    label: 'Water Damage by Material',
    slugs: ['/services/ceiling-water-damage', '/services/hardwood-floor-drying'],
  },
  {
    label: 'Mold, Fire & Storm',
    slugs: [
      '/services/mold-remediation',
      '/services/storm-damage-repair',
      '/services/fire-damage-restoration',
      '/services/smoke-soot-damage-cleanup',
    ],
  },
  {
    label: 'Commercial',
    slugs: ['/services/commercial-water-damage'],
  },
];

export const SERVICE_SLUGS = SERVICE_GROUPS.flatMap((g) => g.slugs);

/* Doc service names per href, taken from the /services/ hub's grouped lists
   (the <strong> service name in each item). The homepage's grouped lists
   carry the same 18 services as single links with no <strong> separator, so
   the hub names give the title/description boundary there. Both slash forms
   are keyed because the doc mixes them. */
export const SERVICE_TITLES = (() => {
  const map = {};
  const hub = PAGES.find((p) => p.slug === '/services/');
  if (hub) {
    for (const b of hub.blocks || []) {
      if (b.t !== 'ul') continue;
      for (const it of b.items || []) {
        const href = (it.match(/href="([^"]+)"/) || [])[1];
        const strong = it.match(/<strong>([\s\S]*?)<\/strong>/);
        if (href && strong) {
          map[href] = strong[1];
          map[normSlug(href)] = strong[1];
        }
      }
    }
  }
  return map;
})();

export const AREA_GROUPS = [
  {
    label: 'Tulsa Neighborhoods',
    slugs: [
      '/service-areas/midtown-tulsa/',
      '/service-areas/brookside-tulsa/',
      '/service-areas/south-tulsa/',
      '/service-areas/west-tulsa/',
      '/service-areas/north-tulsa/',
      '/service-areas/east-tulsa/',
      '/service-areas/cherry-street-tulsa/',
    ],
  },
  {
    label: 'Nearby Communities',
    slugs: [
      '/service-areas/broken-arrow-ok/',
      '/service-areas/owasso-ok/',
      '/service-areas/bixby-ok/',
      '/service-areas/jenks-ok/',
      '/service-areas/sand-springs-ok/',
      '/service-areas/glenpool-ok/',
      '/service-areas/claremore-ok/',
      '/service-areas/catoosa-ok/',
      '/service-areas/collinsville-ok/',
      '/service-areas/skiatook-ok/',
      '/service-areas/coweta-ok/',
      '/service-areas/sapulpa-ok/',
    ],
  },
];

export const AREA_SLUGS = AREA_GROUPS.flatMap((g) => g.slugs);

/* Footer best-ever service picks (theme rule: header/footer carry only the best). */
export const FOOTER_SERVICES = [
  '/services/emergency-water-damage-restoration',
  '/services/water-mitigation',
  '/services/flood-damage-restoration',
  '/services/mold-remediation',
  '/services/burst-pipe-water-damage',
  '/services/commercial-water-damage',
];

export const FOOTER_AREAS = [
  '/service-areas/broken-arrow-ok/',
  '/service-areas/owasso-ok/',
  '/service-areas/bixby-ok/',
  '/service-areas/jenks-ok/',
  '/service-areas/sand-springs-ok/',
  '/service-areas/midtown-tulsa/',
];

/* Resource pages, in doc order. The /resources/ hub lists all ten, so no
   resource page is an orphan: /resources/water-damage-vs-flood-damage-
   insurance-oklahoma has zero inbound body links in the doc; the other nine
   are linked from body copy (several via the parser's remapped paths).
   Footer chrome (header/footer links are exempt from the doc-only link
   rule) links only the hub, not the individual pages. */
export const RESOURCE_SLUGS = [
  '/resources/water-damage-restoration-cost-tulsa',
  '/resources/mold-after-water-damage-tulsa',
  '/resources/how-to-file-water-damage-insurance-claim-tulsa',
  '/resources/first-24-hours-after-water-damage',
  '/resources/oklahoma-water-damage-insurance-guide',
  '/resources/how-long-does-water-damage-take-to-dry',
  '/resources/how-to-prevent-frozen-pipes-tulsa',
  '/resources/water-damage-vs-flood-damage-insurance-oklahoma',
  '/resources/water-damage-categories-and-classes-explained',
  '/resources/signs-of-hidden-water-damage',
];

/* Trust-band checks — verbatim fragments from the homepage doc text. */
export const TRUST_CHECKS = [
  'Crews Standing By 24/7',
  'IICRC S500 Drying Standards',
  'Readings Logged Daily',
  'Insurance Claim Documentation',
];

export function areaMapQuery(slug) {
  const seg = slug.replace(/\/$/, '').split('/').pop() || '';
  const tulsaHoods = ['midtown', 'brookside', 'south', 'west', 'north', 'east', 'cherry-street'];
  const base = seg.replace(/-ok$/, '').replace(/-tulsa$/, '').replace(/-/g, ' ');
  const name = base.replace(/\b\w/g, (c) => c.toUpperCase());
  if (tulsaHoods.includes(seg.replace(/-tulsa$/, ''))) return `${name}, Tulsa, OK`;
  return `${name}, OK`;
}
