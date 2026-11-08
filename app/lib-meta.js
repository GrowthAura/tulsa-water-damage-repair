/* Client-safe site metadata — NO page data, NO JSON imports.
   This module is imported by 'use client' components (Header, ContactForm),
   so NOTHING in it may pull in content/pages.json (796 KB) or
   content/images.json: before this split, importing lib.js from a client
   component bundled the whole pages.json into the shared client chunk
   (986-…js = 694 KB, homepage transfer >1.1 MB).
   Server-only data (PAGES, PAGE_BY_SLUG, IMAGES, pageImage) lives in
   ./lib.js, which client components must NEVER import. */

export const SITE = {
  brand: 'Tulsa Water Damage Repair',
  domain: 'www.tulsawaterdamagerepair.com',
  url: 'https://www.tulsawaterdamagerepair.com',
  phone: '(918) 395-9320',
  phoneHref: 'tel:+19183959320',
  address: '400 S 129th E Ave, Tulsa, OK 74108',
  mapQuery: '400 S 129th E Ave, Tulsa, OK 74108',
};

export function normSlug(s) {
  if (!s) return '/';
  return s === '/' ? '/' : s.replace(/\/$/, '') || '/';
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
  if (page.type === 'service') return { label: 'Services', href: '/services' };
  /* No /service-areas/ hub route exists, so area pages have no parent crumb:
     linking "Service Areas" to "/" was a duplicate Home link with a wrong name. */
  if (page.type === 'area') return null;
  if (page.type === 'resource') return { label: 'Resources', href: '/resources' };
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
      '/services/slab-leak-water-damage',
      '/services/water-heater-leak-cleanup',
      '/services/appliance-leak-water-damage',
      '/services/ac-drain-line-overflow-cleanup',
      '/services/roof-leak-water-damage',
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
   are keyed because the doc mixes them.
   STATIC LITERAL (U1, 2026-11-08): previously computed at runtime by
   scanning PAGES (which forced the whole pages.json into the client
   bundle). Values are verbatim from the hub doc lists — including the
   <a> tags some carry (parseServiceItem strips those at render time,
   B1 fix). Regenerate from content/pages.json if the hub lists change:
   for each ul-block item in the /services/ hub page, map href -> <strong>
   inner HTML, plus the normSlug(href) key. */
export const SERVICE_TITLES = {
  '/services/burst-pipe-water-damage': '<a href="/services/burst-pipe-water-damage">Burst pipe water damage</a>',
  '/services/slab-leak-water-damage': '<a href="/services/slab-leak-water-damage">Slab leak water damage</a>',
  '/services/slab-leak-water-damage': '<a href="/services/slab-leak-water-damage">Slab leak water damage</a>',
  '/services/water-heater-leak-cleanup': '<a href="/services/water-heater-leak-cleanup">Water heater leak cleanup</a>',
  '/services/water-heater-leak-cleanup': '<a href="/services/water-heater-leak-cleanup">Water heater leak cleanup</a>',
  '/services/appliance-leak-water-damage': '<a href="/services/appliance-leak-water-damage">Appliance leak water damage</a>',
  '/services/appliance-leak-water-damage': '<a href="/services/appliance-leak-water-damage">Appliance leak water damage</a>',
  '/services/ac-drain-line-overflow-cleanup': '<a href="/services/ac-drain-line-overflow-cleanup">AC drain line overflow cleanup</a>',
  '/services/ac-drain-line-overflow-cleanup': '<a href="/services/ac-drain-line-overflow-cleanup">AC drain line overflow cleanup</a>',
  '/services/roof-leak-water-damage': '<a href="/services/roof-leak-water-damage">Roof leak water damage</a>',
  '/services/roof-leak-water-damage': '<a href="/services/roof-leak-water-damage">Roof leak water damage</a>',
  '/services/ceiling-water-damage': 'Ceiling and drywall water damage',
  '/services/hardwood-floor-drying': 'Hardwood floor drying',
  '/services/fire-damage-restoration': '<a href="/services/fire-damage-restoration">Fire damage restoration</a>',
  '/services/smoke-soot-damage-cleanup': '<a href="/services/smoke-soot-damage-cleanup">Smoke and soot cleanup</a>',
  /* Homepage service-list cards (2026-11-08): the 3 homepage groups have no
     <strong>, so parseServiceItem falls back to this map. Plain titles here —
     the card's <Link> is the single link; values are stripped of <a> at render. */
  '/services/emergency-water-damage-restoration': 'Emergency water damage restoration',
  '/services/water-mitigation': 'Water mitigation and structural drying',
  '/services/flood-damage-restoration': 'Flood damage restoration',
  '/services/flooded-basement-cleanup': 'Flooded basement and crawlspace cleanup',
  '/services/sewage-backup-cleanup': 'Sewage backup cleanup',
  '/services/mold-remediation': 'Mold remediation',
  '/services/storm-damage-repair': 'Storm damage repair',
  '/services/commercial-water-damage': 'Commercial water damage restoration',
};

export const AREA_GROUPS = [
  {
    label: 'Tulsa Neighborhoods',
    slugs: [
      '/service-areas/midtown-tulsa',
      '/service-areas/brookside-tulsa',
      '/service-areas/south-tulsa',
      '/service-areas/west-tulsa',
      '/service-areas/north-tulsa',
      '/service-areas/east-tulsa',
      '/service-areas/cherry-street-tulsa',
    ],
  },
  {
    label: 'Nearby Communities',
    slugs: [
      '/service-areas/broken-arrow-ok',
      '/service-areas/owasso-ok',
      '/service-areas/bixby-ok',
      '/service-areas/jenks-ok',
      '/service-areas/sand-springs-ok',
      '/service-areas/glenpool-ok',
      '/service-areas/claremore-ok',
      '/service-areas/catoosa-ok',
      '/service-areas/collinsville-ok',
      '/service-areas/skiatook-ok',
      '/service-areas/coweta-ok',
      '/service-areas/sapulpa-ok',
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
  '/service-areas/broken-arrow-ok',
  '/service-areas/owasso-ok',
  '/service-areas/bixby-ok',
  '/service-areas/jenks-ok',
  '/service-areas/sand-springs-ok',
  '/service-areas/midtown-tulsa',
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
