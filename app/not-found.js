import Link from 'next/link';
import { SITE } from './lib';
import Footer from './components/Footer';
import { FinalCta } from './components/Shared';

export default function NotFound() {
  return (
    <>
      <section className="hero hero-short">
        <div className="hero-brand-panel">
          <div className="panel-inner">
            <p className="eyebrow on-navy">Tulsa Water Damage Repair</p>
          </div>
        </div>
        <div className="hero-content">
          <div className="container">
            <h1>Page Not Found</h1>
            <p className="hero-intro">That page does not exist or was moved.</p>
            <div className="hero-ctas">
              <Link className="btn btn-cyan" href="/">
                Back to Homepage
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
