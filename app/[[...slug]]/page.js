import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  SITE,
  PAGES,
  PAGE_BY_SLUG,
  pageImage,
  normSlug,
  shortName,
  parentOf,
  AREA_SLUGS,
  RESOURCE_SLUGS,
  TRUST_CHECKS,
  areaMapQuery,
} from '../lib';
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

function jsonLd(page) {
  const url = SITE.url + page.slug;
  const parent = parentOf(page);
  const crumbs = [{ '@type': 'ListItem', position: 1, name: 'Home', item: SITE.url + '/' }];
  if (parent) crumbs.push({ '@type': 'ListItem', position: 2, name: parent.label, item: SITE.url + parent.href });
  crumbs.push({ '@type': 'ListItem', position: crumbs.length + 1, name: page.h1, item: url });
  const localBusiness = {
    '@type': 'LocalBusiness',
    '@id': SITE.url + '/#business',
    name: SITE.brand,
    telephone: SITE.phone,
    url: SITE.url + '/',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '400 S 129th E Ave',
      addressLocality: 'Tulsa',
      addressRegion: 'OK',
      postalCode: '74108',
      addressCountry: 'US',
    },
    areaServed: { '@type': 'City', name: 'Tulsa' },
    openingHoursSpecification: {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      opens: '00:00',
      closes: '23:59',
    },
  };
  const out = [
    {
      '@context': 'https://schema.org',
      '@graph': [
        { '@type': 'WebSite', '@id': SITE.url + '/#website', url: SITE.url + '/', name: SITE.brand },
        { '@type': 'BreadcrumbList', itemListElement: crumbs },
        ...(page.type === 'homepage'
          ? [{ ...localBusiness, '@type': 'LocalBusiness' }]
          : page.type === 'service'
            ? [
                {
                  '@type': 'Service',
                  name: page.h1,
                  url,
                  provider: { '@id': SITE.url + '/#business' },
                  areaServed: { '@type': 'City', name: 'Tulsa' },
                },
                localBusiness,
              ]
            : [{ '@type': 'WebPage', '@id': url, url, name: page.h1, isPartOf: { '@id': SITE.url + '/#website' } }]),
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
              <a className="btn btn-cream" href="/contact/">
                Request Emergency Service
              </a>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

function NavyBand({ intro }) {
  return (
    <section className="section" style={{ padding: '2.5rem 0' }}>
      <div className="container">
        <p className="lead" style={{ color: 'var(--navy)' }}>
          {intro}
        </p>
        <ul
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
            <li key={c} style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', fontWeight: 700, fontSize: '1.125rem', color: 'var(--ink)' }}>
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
          <a className="btn btn-cream" href="/contact/">
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
        <h2 id={slugify(b.text)} className="reveal">
          {b.text}
        </h2>
      );
    case 'faq-heading':
      return (
        <>
          <h2 id="faq" className="reveal">
            {b.text}
          </h2>
          <FaqList faqs={page.faqs} />
        </>
      );
    case 'p':
      return <p dangerouslySetInnerHTML={{ __html: b.html }} />;
    case 'ul': {
      // Doc grouped service lists (hub + homepage) render as card grids, so
      // each service appears once as a card instead of twice (cards + list).
      // Any other list shape stays a plain bullet list.
      if (page.type === 'hub' || page.type === 'homepage') {
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

  // First normal paragraph is the intro: hero (home) or navy band (inner) shows it.
  const blocks = [...page.blocks];
  let intro = page.intro || '';
  const firstP = blocks.findIndex((b) => b.t === 'p');
  if (firstP >= 0) blocks.splice(firstP, 1);
  // Drop leading section dividers left over after the intro was consumed.
  while (blocks.length && blocks[0].t === 'hr') blocks.shift();

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
      {isHome ? <TrustBand /> : intro && <NavyBand intro={intro} />}
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
        <section className="section">
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
