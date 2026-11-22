import Link from 'next/link';
import { SITE, FOOTER_SERVICES, FOOTER_AREAS, RESOURCE_SLUGS, shortName } from '../lib-meta';

export default function Footer({ showMap = true }) {
  return (
    <footer className="site-footer">
      {showMap && (
        <div className="footer-map">
          <a
            href={`https://www.google.com/maps?q=${encodeURIComponent(SITE.mapQuery)}`}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`Open map - ${SITE.address} in Google Maps`}
          >
            <img src="/images/map-footer-tulsa.webp" alt={`Map - ${SITE.address}`} loading="eager" />
          </a>
          <p className="footer-map-attr">
            © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors
          </p>
        </div>
      )}
      <div className="container">
        <div className="footer-cols">
          <div className="footer-col">
            <div className="footer-brand">
              <span className="brand-mark" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="27" height="27" fill="none" aria-hidden="true">
                  <path
                    d="M12 1.9c0 0-7.4 8.7-7.4 13.7a7.4 7.4 0 0 0 14.9 0c0-5-7.4-13.7-7.4-13.7Z"
                    fill="#00BFFF"
                  />
                  <circle cx="9.0" cy="16.4" r="1.95" fill="#fff" />
                </svg>
              </span>
              <span>
                <strong>Tulsa Water Damage Repair</strong>
                <small>Tulsa, Oklahoma</small>
              </span>
            </div>
            <p>
              Water damage restoration across Tulsa County, day or night. We extract water, dry the
              structure to measured targets and document everything for your insurance claim.
            </p>
            <p className="footer-hours">Crews Standing By 24/7</p>
            <p>
              <strong>{SITE.address}</strong>
              <br />
              <a href={SITE.phoneHref}>{SITE.phone}</a>
            </p>
          </div>
          <div className="footer-col">
            <h3>Services</h3>
            <ul>
              {FOOTER_SERVICES.map((s) => (
                <li key={s}>
                  <Link href={s}>{shortName(s)}</Link>
                </li>
              ))}
              <li>
                <Link href="/services" className="footer-more">
                  View all services
                </Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h3>Service Areas</h3>
            <ul>
              {FOOTER_AREAS.map((s) => (
                <li key={s}>
                  <Link href={s}>{shortName(s)}</Link>
                </li>
              ))}
              <li>
                <Link href="/#which-tulsa-areas-do-you-serve" className="footer-more">
                  View all areas
                </Link>
              </li>
            </ul>
          </div>
          <div className="footer-col">
            <h3>Resources</h3>
            <ul>
              {RESOURCE_SLUGS.map((s) => (
                <li key={s}>
                  <Link href={s}>{shortName(s)}</Link>
                </li>
              ))}
              <li>
                <Link href="/resources" className="footer-more">
                  View all guides
                </Link>
              </li>
            </ul>
            {showMap && (
              <div className="footer-mini-map">
                <a
                  href={`https://www.google.com/maps?q=${encodeURIComponent(SITE.mapQuery)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`Open map - ${SITE.address} in Google Maps`}
                >
                  <img src="/images/map-footer-mini-tulsa.webp" alt={`Map - ${SITE.address}`} loading="eager" />
                </a>
                <p className="footer-map-attr">
                  © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors
                </p>
              </div>
            )}
          </div>
          <div className="footer-col">
            <h3>Emergency Help</h3>
            <p>Speak with Tulsa Water Damage Repair about your restoration needs.</p>
            <a className="btn btn-cyan" href={SITE.phoneHref}>
              <span>Call Now ·</span>
              <span>{SITE.phone}</span>
            </a>
            <br />
            <a className="btn btn-cream" href="/contact">
              Request Emergency Service
            </a>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} Tulsa Water Damage Repair</span>
          <span>
            <Link href="/about-us">About Us</Link>
            {' · '}
            <Link href="/resources">Blog</Link>
            {' · '}
            <Link href="/contact">Contact</Link>
            {' · '}
            {/* Plain <a>: /sitemap.xml is a static file, not a Next route — a
                next/link here makes the router prefetch /sitemap.xml.txt (RSC)
                and log a console 404. */}
            <a href="/sitemap.xml">Sitemap</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
