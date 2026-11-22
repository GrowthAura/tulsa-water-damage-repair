import Link from 'next/link';
import { SITE } from './lib-meta';
import Footer from './components/Footer';
import { FinalCta } from './components/Shared';

export default function NotFound() {
  return (
    <>
      <section className="hero hero-short">
        <div className="hero-brand-panel">
          <div className="panel-inner">
            <span className="panel-drop" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path
                  d="M12 1.9c0 0-7.4 8.7-7.4 13.7a7.4 7.4 0 0 0 14.9 0c0-5-7.4-13.7-7.4-13.7Z"
                  fill="#00BFFF"
                />
                <circle cx="9.0" cy="16.4" r="1.95" fill="#fff" />
              </svg>
            </span>
          </div>
        </div>
        <div className="hero-content">
          <div className="container">
            <p className="eyebrow on-navy">Tulsa Water Damage Repair</p>
            <h1>Page Not Found</h1>
            <p className="hero-intro">That page does not exist or was moved.</p>
            <div className="hero-ctas">
              <Link className="btn btn-cyan" href="/">
                Back to Homepage
              </Link>
              <Link className="btn btn-cream" href="/services">
                Browse Services
              </Link>
              <a className="btn btn-cream" href={SITE.phoneHref}>
                Call {SITE.phone}
              </a>
            </div>
          </div>
        </div>
      </section>
      <FinalCta />
      <Footer showMap={false} />
    </>
  );
}
