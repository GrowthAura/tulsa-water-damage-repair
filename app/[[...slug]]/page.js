import Link from 'next/link';
import { notFound } from 'next/navigation';
import { PAGES, PAGE_BY_SLUG, pageImage } from '../lib';
import {
  SITE,
  normSlug,
  shortName,
  parentOf,
  AREA_SLUGS,
  RESOURCE_SLUGS,
  TRUST_CHECKS,
  areaMapQuery,
} from '../lib-meta';
import Footer from '../components/Footer';
import { TrustBand, ServiceListCards, serviceListItems, AreaCards, ResourceCards, FaqList, FinalCta, MapBlock } from '../components/Shared';
import ContactForm from '../components/ContactForm';

export const dynamicParams = false;

const BY_NORM = Object.fromEntries(PAGES.map((p) => [normSlug(p.slug), p]));

export function generateStaticParams() {
  return PAGES.map((p) => ({
    slug: p.slug === '/' ? [] : p.slug.replace(/^\//, '').replace(/\/$/, '').split('/'),
  }));
}

function lookup(params) {
  const parts = params.slug || [];
  const path = '/' + parts.join('/');
  return BY_NORM[normSlug(path)] || null;
}

export function generateMetadata({ params }) {
  const page = lookup(params);
  if (!page) return {};
  const url = SITE.url + page.slug;
  const img = pageImage(page.slug).hero;
  // NOTE: canonical + og:url are rendered manually in the page component.
  // Next.js normalizes them to the trailingSlash form, which would break the
  // doc's exact mixed canonical forms (23 routes have no trailing slash).
  return {
    title: page.metaTitle,
    description: page.metaDescription,
    openGraph: {
      title: page.metaTitle,
      description: page.metaDescription,
      type: 'website',
      siteName: SITE.brand,
      ...(img ? { images: [{ url: SITE.url + img.file, width: 1200, height: 800, alt: img.alt }] } : {}),
    },
    twitter: {
      card: 'summary_large_image',
      title: page.metaTitle,
      description: page.metaDescription,
      ...(img ? { images: [SITE.url + img.file] } : {}),
    },
    robots: { index: true, follow: true },
  };
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

const SMALL_WORDS = new Set(['and', 'or', 'of', 'for', 'the', 'in', 'to', 'a', 'an']);
function titleCase(s) {
  return s
    .split(/\s+/)
    .map((w, i) => {
      if (/^[A-Z]{2,}$/.test(w)) return w; // AC, IICRC stay uppercase
      const lw = w.toLowerCase();
      if (i > 0 && SMALL_WORDS.has(lw)) return lw;
      return w.charAt(0).toUpperCase() + w.slice(1).toLowerCase();
    })
    .join(' ');
}

function parseHandleItem(html) {
  const href = (html.match(/<a href="([^"]+)"/) || [])[1] || '/services';
  const label = (html.match(/<strong>([\s\S]*?)<\/strong>/) || [])[1] || '';
  const body = html
    .replace(/^<a[^>]*><strong>[\s\S]*?<\/strong>/, '')
    .replace(/<\/a>/, '')
    .trim();
  return { href, titleHtml: label, descHtml: body };
}

// Group doc list paragraphs into card grids + the area-page SEO strip.
// - Homepage Phase 1/2 paragraphs -> phase-grid.
// - About "What Do We Handle?" paragraphs -> handle-grid (+ directory link).
// - Area offer <ul> -> demand-strip with that page's own services + city
//   (city taken from the offer H2 itself, exactly as written on the page).
function groupBlocks(blocks, page) {
  const out = [];
  let lastH2 = '';
  let i = 0;
  while (i < blocks.length) {
    const b = blocks[i];
    if (b.t === 'h2') lastH2 = b.text || '';
    // Phase cards (homepage only).
    if (page.type === 'homepage' && b.t === 'p' && /^<strong>Phase \d/.test(b.html || '')) {
      const items = [];
      while (i < blocks.length && blocks[i].t === 'p' && /^<strong>Phase \d/.test(blocks[i].html || '')) {
        items.push(blocks[i].html);
        i++;
      }
      out.push({ t: 'phase-grid', items });
      continue;
    }
    // About handle cards. (An intro paragraph sits between the h2 and the
    // list, so pass non-list blocks through first, then collect the run.)
    if (b.t === 'h2' && b.text === 'What Do We Handle?') {
      out.push(b);
      i++;
      while (
        i < blocks.length &&
        blocks[i].t !== 'h2' &&
        blocks[i].t !== 'hr' &&
        !(blocks[i].t === 'p' && /^<a href="[^"]+"><strong>/.test(blocks[i].html || ''))
      ) {
        out.push(blocks[i]);
        i++;
      }
      const items = [];
      while (i < blocks.length && blocks[i].t === 'p' && /^<a href="[^"]+"><strong>/.test(blocks[i].html || '')) {
        items.push(blocks[i].html);
        i++;
      }
      if (items.length) out.push({ t: 'handle-grid', items });
      if (
        i < blocks.length &&
        blocks[i].t === 'p' &&
        /^<a href="\/services">See the full services directory:/.test((blocks[i].html || '').trim())
      ) {
        out.push({ t: 'handle-more', html: blocks[i].html });
        i++;
      }
      continue;
    }
    out.push(b);
    // Area SEO strip, directly below the offer list (which renders as cards).
    if (page.type === 'area' && b.t === 'ul') {
      const cards = serviceListItems(b.items);
      const cityMatch = /Services Do We Offer in (.+)\?/.exec(lastH2);
      if (cards && cityMatch) {
        const city = cityMatch[1];
        out.push({
          t: 'demand-strip',
          city,
          items: cards.map((c) => `${titleCase(c.titleHtml.replace(/<[^>]*>/g, ''))} in ${city}`),
        });
      }
    }
    i++;
  }
  return out;
}

/* areaServed — shared by LocalBusiness and by each Service node: every real
   service area on the site (Tulsa + 12 suburb cities + 7 Tulsa neighborhoods,
   area-page H1s verbatim, location prefix stripped). No invented place. */
const AREA_SERVED = [
  { '@type': 'City', name: 'Tulsa' },
  { '@type': 'City', name: 'Broken Arrow' },
  { '@type': 'City', name: 'Bixby' },
  { '@type': 'City', name: 'Catoosa' },
  { '@type': 'City', name: 'Claremore' },
  { '@type': 'City', name: 'Collinsville' },
  { '@type': 'City', name: 'Coweta' },
  { '@type': 'City', name: 'Glenpool' },
  { '@type': 'City', name: 'Jenks' },
  { '@type': 'City', name: 'Owasso' },
  { '@type': 'City', name: 'Sand Springs' },
  { '@type': 'City', name: 'Sapulpa' },
  { '@type': 'City', name: 'Skiatook' },
  { '@type': 'Place', name: 'Midtown Tulsa' },
  { '@type': 'Place', name: 'Brookside, Tulsa' },
  { '@type': 'Place', name: 'South Tulsa' },
  { '@type': 'Place', name: 'West Tulsa' },
  { '@type': 'Place', name: 'North Tulsa' },
  { '@type': 'Place', name: 'East Tulsa' },
  { '@type': 'Place', name: 'Cherry Street & the Pearl District' },
];

/* Area-page "about" — the specific city/neighborhood each area page covers
   (same names as AREA_SERVED). Used as WebPage.about on area pages only. */
const AREA_ABOUT = {
  '/service-areas/broken-arrow-ok': { '@type': 'City', name: 'Broken Arrow' },
  '/service-areas/bixby-ok': { '@type': 'City', name: 'Bixby' },
  '/service-areas/catoosa-ok': { '@type': 'City', name: 'Catoosa' },
  '/service-areas/claremore-ok': { '@type': 'City', name: 'Claremore' },
  '/service-areas/collinsville-ok': { '@type': 'City', name: 'Collinsville' },
  '/service-areas/coweta-ok': { '@type': 'City', name: 'Coweta' },
  '/service-areas/glenpool-ok': { '@type': 'City', name: 'Glenpool' },
  '/service-areas/jenks-ok': { '@type': 'City', name: 'Jenks' },
  '/service-areas/owasso-ok': { '@type': 'City', name: 'Owasso' },
  '/service-areas/sand-springs-ok': { '@type': 'City', name: 'Sand Springs' },
  '/service-areas/sapulpa-ok': { '@type': 'City', name: 'Sapulpa' },
  '/service-areas/skiatook-ok': { '@type': 'City', name: 'Skiatook' },
  '/service-areas/midtown-tulsa': { '@type': 'Place', name: 'Midtown Tulsa' },
  '/service-areas/brookside-tulsa': { '@type': 'Place', name: 'Brookside, Tulsa' },
  '/service-areas/south-tulsa': { '@type': 'Place', name: 'South Tulsa' },
  '/service-areas/west-tulsa': { '@type': 'Place', name: 'West Tulsa' },
  '/service-areas/north-tulsa': { '@type': 'Place', name: 'North Tulsa' },
  '/service-areas/east-tulsa': { '@type': 'Place', name: 'East Tulsa' },
  '/service-areas/cherry-street-tulsa': { '@type': 'Place', name: 'Cherry Street & the Pearl District' },
};

function jsonLd(page) {
  const url = SITE.url + page.slug;
  const heroImg = pageImage(page.slug).hero;
  /* Offer catalog (homepage LocalBusiness only): the 18 real services,
     names = service H1s with the " in Tulsa, OK" suffix stripped. */
  const serviceCatalog = PAGES.filter((p) => p.type === 'service').map((p) => ({
    '@type': 'Offer',
    itemOffered: {
      '@type': 'Service',
      name: p.h1.replace(/ in Tulsa, OK$/, ''),
      url: SITE.url + p.slug,
      provider: { '@id': SITE.url + '/#business' },
    },
  }));
  const parent = parentOf(page);
  /* BreadcrumbList must match the visible breadcrumb trail exactly:
     - homepage: a single Home item (it renders no visible trail, and a
       second item pointing at the same URL was a duplicate);
     - last item name is shortName(page.slug), the same text the visible
       breadcrumb shows — NOT the full H1;
     - area pages have no parent (no /service-areas/ hub exists);
       resource pages parent to the real /resources/ hub. */
  const crumbs = [{ '@type': 'ListItem', position: 1, name: 'Home', item: SITE.url + '/' }];
  if (parent) crumbs.push({ '@type': 'ListItem', position: 2, name: parent.label, item: SITE.url + parent.href });
  if (page.type !== 'homepage') {
    crumbs.push({ '@type': 'ListItem', position: crumbs.length + 1, name: shortName(page.slug), item: url });
  }
  const localBusiness = {
    '@type': 'HomeAndConstructionBusiness',
    '@id': SITE.url + '/#business',
    name: SITE.brand,
    description:
      "We're a water damage restoration team based at 400 S 129th E Ave in Tulsa, OK 74108.",
    telephone: SITE.phone,
    url: SITE.url + '/',
    /* image = the business's main hero photo (homepage hero, real site asset);
       logo = the brand mark as a real image file (favicon-512 — the same Heavy
       A drop the header shows as inline SVG; no separate logo file exists). */
    image: SITE.url + '/images/home-tulsa-water-damage-repair.webp',
    logo: SITE.url + '/favicon-512x512.png',
    /* contactPoint: the doc's phone, the business's customer line.
       No email in the doc, so none here. */
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: SITE.phone,
      contactType: 'customer service',
      availableLanguage: 'English',
    },
    address: {
      '@type': 'PostalAddress',
      streetAddress: '400 S 129th E Ave',
      addressLocality: 'Tulsa',
      addressRegion: 'OK',
      postalCode: '74108',
      addressCountry: 'US',
    },
    /* GeoCoordinates from a real map lookup of the business address
       (36.15467, -95.83348 — FULL_ADDRESS match); hasMap is the exact
       Google Maps URL the site's own footer embed uses. */
    geo: { '@type': 'GeoCoordinates', latitude: 36.15467, longitude: -95.83348 },
    hasMap:
      'https://www.google.com/maps?q=400%20S%20129th%20E%20Ave%2C%20Tulsa%2C%20OK%2074108&output=embed',
    areaServed: AREA_SERVED,
    /* knowsAbout: the 18 real services — service-page H1s verbatim with
       only the " in Tulsa, OK" location suffix stripped. */
    knowsAbout: [
      'Emergency Water Damage Restoration',
      'Water Mitigation Services',
      'Flood Damage Restoration',
      'Mold Remediation',
      'Commercial Water Damage Restoration',
      'Flooded Basement & Crawlspace Cleanup',
      'Storm Damage Repair',
      'Burst Pipe Water Damage Repair',
      'Sewage Backup Cleanup',
      'Ceiling & Drywall Water Damage Repair',
      'Hardwood Floor Water Damage & Drying',
      'AC Drain Line Overflow Cleanup',
      'Appliance Leak Water Damage',
      'Water Heater Leak Cleanup',
      'Roof Leak Water Damage Repair',
      'Slab Leak Water Damage Restoration',
      'Smoke & Soot Damage Cleanup',
      'Fire Damage Restoration',
    ],
    openingHoursSpecification: {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      opens: '00:00',
      closes: '23:59',
    },
    /* hasOfferCatalog — homepage only (the full business profile): the 18
       real services with their page URLs. Inner pages carry the same business
       entity without the catalog (the Service node on service pages covers it). */
    ...(page.type === 'homepage'
      ? {
          hasOfferCatalog: {
            '@type': 'OfferCatalog',
            name: 'Water Damage Restoration Services',
            itemListElement: serviceCatalog,
          },
        }
      : {}),
  };
  /* HomeAndConstructionBusiness belongs on EVERY page, not just homepage/service pages:
     the 34 area/resource/hub/about/contact/commercial pages had no business
     entity at all. WebPage is likewise present on every page. */
  const webPage = {
    '@type': 'WebPage',
    '@id': url,
    url,
    name: page.h1,
    /* description = the page's own intro (doc text, entities already decoded
       by lib.js fixPage); inLanguage en-US; primaryImageOfPage = the page's
       real hero (every page has one). Area pages add about = that city/place. */
    description: page.intro,
    inLanguage: 'en-US',
    ...(heroImg ? { primaryImageOfPage: SITE.url + heroImg.file } : {}),
    ...(page.type === 'area' && AREA_ABOUT[page.slug] ? { about: AREA_ABOUT[page.slug] } : {}),
    isPartOf: { '@id': SITE.url + '/#website' },
  };
  const out = [
    {
      '@context': 'https://schema.org',
      '@graph': [
        { '@type': 'WebSite', '@id': SITE.url + '/#website', url: SITE.url + '/', name: SITE.brand, inLanguage: 'en-US', publisher: { '@id': SITE.url + '/#business' } },
        { '@type': 'BreadcrumbList', itemListElement: crumbs },
        ...(page.type === 'homepage'
          ? [localBusiness, webPage]
          : page.type === 'service'
            ? [
                {
                  '@type': 'Service',
                  name: page.h1,
                  /* serviceType = H1 minus the " in Tulsa, OK" suffix;
                     description = the page's own intro (doc text);
                     areaServed = the full 20-place list (this service is
                     offered across every area, not Tulsa alone);
                     image = the service's real hero. */
                  serviceType: page.h1.replace(/ in Tulsa, OK$/, ''),
                  description: page.intro,
                  url,
                  ...(heroImg ? { image: SITE.url + heroImg.file } : {}),
                  provider: { '@id': SITE.url + '/#business' },
                  areaServed: AREA_SERVED,
                },
                localBusiness,
                /* WebPage alongside Service: service pages previously had
                   no WebPage node at all (35/53); the page node is now
                   present on every page. */
                webPage,
              ]
            : [webPage, localBusiness]),
        ...(page.faqs && page.faqs.length
          ? [
              {
                '@type': 'FAQPage',
                mainEntity: page.faqs.map((f) => ({
                  '@type': 'Question',
                  name: f.q,
                  acceptedAnswer: { '@type': 'Answer', text: f.a_text },
                })),
              },
            ]
          : []),
        /* Article schema on guide pages only (type 'resource' — the 10
           /resources/ guides; the /resources/ hub is 'resources-hub').
           headline = H1 verbatim; author/publisher = the business itself
           (never a person name); dates from the sitemap lastmod
           (2026-11-07, the site publish date — pages.json carries no
           per-page dates, so no earlier date is invented). */
        ...(page.type === 'resource'
          ? [
              {
                '@type': 'Article',
                headline: page.h1,
                /* description = the guide's own intro (doc text). */
                description: page.intro,
                /* image = the guide's real hero (same file the page shows);
                   inLanguage + mainEntityOfPage tie the Article to its page. */
                ...(heroImg ? { image: SITE.url + heroImg.file } : {}),
                author: { '@id': SITE.url + '/#business' },
                publisher: { '@id': SITE.url + '/#business' },
                datePublished: '2026-11-07',
                dateModified: '2026-11-07',
                inLanguage: 'en-US',
                mainEntityOfPage: { '@id': url },
              },
            ]
          : []),
      ],
    },
  ];
  return out;
}

function Hero({ page }) {
  const img = pageImage(page.slug).hero;
  const isHome = page.type === 'homepage';
  const isShort = !isHome;
  return (
    <section className={`hero ${isShort ? 'hero-short' : ''}`}>
      {img ? (
        <div className="hero-media">
          <img
            src={img.file}
            alt={img.alt}
            width={1200}
            height={800}
            style={img.pos ? { objectPosition: img.pos } : undefined}
          />
        </div>
      ) : (
        <div className="hero-brand-panel">
          <div className="panel-inner" aria-hidden="true" />
        </div>
      )}
      <div className="hero-content">
        <div className="container">
          {isHome && (
            <span className="hero-badge">
              <span className="dot" aria-hidden="true" />
              24/7 Emergency Response
            </span>
          )}
          {page.type !== 'homepage' && (
            <p className="eyebrow on-navy">
              {page.type === 'service'
                ? 'Water damage restoration · Tulsa, OK'
                : page.type === 'area'
                  ? 'Service area · Tulsa, OK'
                  : page.type === 'resource'
                    ? 'Guide · Tulsa, OK'
                    : 'Tulsa Water Damage Repair'}
            </p>
          )}
          <h1>{page.h1}</h1>
          {isHome && <p className="hero-intro">{page.intro}</p>}
          {isHome && (
            <div className="hero-ctas">
              <a className="btn btn-cyan" href={SITE.phoneHref}>
                Call Now · {SITE.phone}
              </a>
              <a className="btn btn-cream" href="/contact">
                Request Emergency Service
              </a>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

function NavyBand({ intro, pageClass }) {
  // Intro can be two paragraphs (split on a blank line). Single-paragraph
  // intros (every other page) still render exactly one <p className="lead">.
  const paras = String(intro || '')
    .split(/\n\s*\n/)
    .map((s) => s.trim())
    .filter(Boolean);
  return (
    <section className={`section navy-band${pageClass ? ` ${pageClass}` : ''}`}>
      <div className="container">
        {paras.map((p, i) => (
          <p key={i} className="lead" style={{ color: 'var(--navy)' }}>
            {p}
          </p>
        ))}
        <ul
          className="navy-trust"
          style={{
            listStyle: 'none',
            margin: '1.5rem 0',
            padding: 0,
            display: 'flex',
            flexWrap: 'wrap',
            gap: '0.75rem 2rem',
          }}
        >
          {TRUST_CHECKS.map((c) => (
            <li key={c} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', fontWeight: 700, color: 'var(--ink)' }}>
              <span className="check" aria-hidden="true" style={{ width: 20, height: 20, borderRadius: '50%', border: '1px solid var(--blue)', color: 'var(--blue)', display: 'grid', placeItems: 'center', fontSize: '0.75rem' }}>
                ✓
              </span>
              {c}
            </li>
          ))}
        </ul>
        <div className="hero-ctas" style={{ marginTop: 0 }}>
          <a className="btn btn-cyan" href={SITE.phoneHref}>
            Call Now · {SITE.phone}
          </a>
          <a className="btn btn-cream" href="/contact">
            Request Emergency Service
          </a>
        </div>
      </div>
    </section>
  );
}

function StickyAside({ page }) {
  const body = pageImage(page.slug).body;
  return (
    <aside className="sticky-aside" aria-label="About this page">
      {body ? (
        <figure className="sticky-figure" style={{ margin: 0 }}>
          <img src={body.file} alt={body.alt} width={1200} height={800} loading="lazy" />
        </figure>
      ) : (
        <div className="brand-panel">
          <h3>{SITE.brand}</h3>
          <p>Water damage restoration across Tulsa County, day or night.</p>
          <ul>
            {TRUST_CHECKS.map((c) => (
              <li key={c}>{c}</li>
            ))}
          </ul>
          <a className="btn btn-cyan" href={SITE.phoneHref} style={{ width: '100%' }}>
            Call Now · {SITE.phone}
          </a>
        </div>
      )}
      <div className="aside-call">
        <p>Water damage right now?</p>
        <a className="btn btn-cyan" href={SITE.phoneHref}>
          Call Now · {SITE.phone}
        </a>
      </div>
    </aside>
  );
}

function Block({ b, page }) {
  switch (b.t) {
    case 'hr':
      return <hr className="doc-divide" />;
    case 'h2':
      return (
        <h2 id={slugify(b.text)}>
          {b.text}
        </h2>
      );
    case 'faq-heading':
      return (
        <>
          <h2 id="faq">
            {b.text}
          </h2>
          <FaqList faqs={page.faqs} />
        </>
      );
    case 'p':
      return <p dangerouslySetInnerHTML={{ __html: b.html }} />;
    case 'ul': {
      // Doc grouped service lists (hub + homepage + area offer lists) render
      // as card grids, so each service appears once as a card instead of a
      // bullet list. serviceListItems returns null for any other list shape,
      // so plain lists (documentation, checklists, areas covered) stay lists.
      if (page.type === 'hub' || page.type === 'homepage' || page.type === 'area') {
        const cards = serviceListItems(b.items);
        if (cards) return <ServiceListCards items={cards} />;
      }
      return (
        <ul>
          {b.items.map((it, i) => (
            <li key={i} dangerouslySetInnerHTML={{ __html: it }} />
          ))}
        </ul>
      );
    }
    case 'table':
      return (
        <div className="table-wrap">
          <table>
            {b.headers && (
              <thead>
                <tr>
                  {b.headers.map((h, i) => (
                    <th key={i} dangerouslySetInnerHTML={{ __html: h }} />
                  ))}
                </tr>
              </thead>
            )}
            <tbody>
              {b.rows.map((row, i) => (
                <tr key={i}>
                  {row.map((cell, j) => (
                    <td key={j} dangerouslySetInnerHTML={{ __html: cell }} />
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    case 'phase-grid':
      return (
        <div className="phase-grid">
          {b.items.map((html, i) => {
            const title = (html.match(/<strong>([\s\S]*?)<\/strong>/) || [])[1] || '';
            const body = html.replace(/<strong>[\s\S]*?<\/strong>/, '').trim();
            return (
              <article className="phase-card" key={i}>
                <h3>{title}</h3>
                <p dangerouslySetInnerHTML={{ __html: body }} />
              </article>
            );
          })}
        </div>
      );
    case 'handle-grid':
      return <ServiceListCards items={b.items.map(parseHandleItem)} />;
    case 'handle-more':
      return <p className="handle-more" dangerouslySetInnerHTML={{ __html: b.html }} />;
    case 'demand-strip':
      return (
        <div className="demand-strip">
          <h3>Most In-Demand Services in {b.city}</h3>
          <ul className="demand-list">
            {b.items.map((name, i) => (
              <li key={i}>
                <strong>{name}</strong>
              </li>
            ))}
          </ul>
        </div>
      );
    case 'cta':
      return (
        <section className="call-strip">
          <div className="container">
            <p>{b.plain}</p>
            <a className="btn btn-outline" href={SITE.phoneHref}>
              Call Now · {SITE.phone}
            </a>
          </div>
        </section>
      );
    case 'contact-extras':
      return (
        <div className="contact-grid">
          <div>
            <MapBlock query={SITE.mapQuery} title={`Map — ${SITE.address}`} />
          </div>
          <ContactForm />
        </div>
      );
    default:
      return null;
  }
}

export default function Page({ params }) {
  const page = lookup(params);
  if (!page) notFound();
  const isHome = page.type === 'homepage';
  const isResourcesHub = page.type === 'resources-hub';
  const isArea = page.type === 'area';
  const isContact = page.type === 'contact';

  // Slug-derived class for page-scoped styling (e.g. one page's larger text).
  const slugClass =
    page.slug && page.slug !== '/'
      ? `page-${page.slug.replace(/[^a-z0-9]+/gi, '-').replace(/^-+|-+$/g, '')}`
      : '';

  // First normal paragraph is the intro: hero (home) or navy band (inner) shows it.
  let blocks = [...page.blocks];
  let intro = page.intro || '';
  const firstP = blocks.findIndex((b) => b.t === 'p');
  if (firstP >= 0) blocks.splice(firstP, 1);
  // Drop leading section dividers left over after the intro was consumed.
  while (blocks.length && blocks[0].t === 'hr') blocks.shift();
  // Group list paragraphs into card grids + the area-page SEO strip.
  blocks = groupBlocks(blocks, page);

  const parent = parentOf(page);
  const crumbs = (
    <nav className="crumbs" aria-label="Breadcrumb">
      <Link href="/">Home</Link>
      {parent && (
        <>
          <span aria-hidden="true">›</span>
          <Link href={parent.href}>{parent.label}</Link>
        </>
      )}
      <span aria-hidden="true">›</span>
      <span aria-current="page">{shortName(page.slug)}</span>
    </nav>
  );

  // Homepage: insert area cards after the section they belong to.
  // (Service lists render as their own card grids in Block; no separate
  // builder grid — the services must not appear twice.)
  const renderHomeBlocks = () => {
    const out = [];
    let section = '';
    let areasInserted = false;
    blocks.forEach((b, i) => {
      if (b.t === 'h2') section = b.text;
      out.push(<Block key={i} b={b} page={page} />);
      if (b.t === 'hr' && section === 'Which Tulsa Areas Do You Serve?' && !areasInserted) {
        areasInserted = true;
        out.push(<AreaCards key="area-cards" slugs={AREA_SLUGS} />);
      }
    });
    if (!areasInserted) out.push(<AreaCards key="area-cards-fallback" slugs={AREA_SLUGS} />);
    return out;
  };

  const bodyBlocks = isHome ? (
    renderHomeBlocks()
  ) : (
    blocks.map((b, i) => <Block key={i} b={b} page={page} />)
  );

  return (
    <>
      <link rel="canonical" href={SITE.url + page.slug} />
      <meta property="og:url" content={SITE.url + page.slug} />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd(page)) }}
      />
      <Hero page={page} />
      {isHome ? <TrustBand /> : intro && <NavyBand intro={intro} pageClass={slugClass} />}
      {isResourcesHub ? (
        <>
          <section className="section" style={{ paddingBottom: 0 }}>
            <div className="container">{crumbs}</div>
          </section>
          <ResourceCards slugs={RESOURCE_SLUGS} heading="Guides and Cost Information" eyebrow="Resources" />
        </>
      ) : isHome ? (
        <section className="section">
          <div className="container content-block">
            {bodyBlocks}
          </div>
        </section>
      ) : (
        <section className={`section page-${page.type}${slugClass ? ` ${slugClass}` : ''}`}>
          <div className="container">
            {crumbs}
            <div className="split">
              <div className="content-block">
                {bodyBlocks}
              </div>
              <StickyAside page={page} />
            </div>
          </div>
        </section>
      )}
      {isArea && (
        <section className="section" aria-label="Service area map">
          <div className="container">
            <MapBlock query={areaMapQuery(page.slug)} title={`Map — ${shortName(page.slug)}, Tulsa, OK`} />
          </div>
        </section>
      )}
      <FinalCta />
      <Footer showMap={!isArea && !isContact} />
    </>
  );
}
