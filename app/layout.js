import { DM_Sans } from 'next/font/google';
import './globals.css';
import Header from './components/Header';
import { Reveal } from './components/Reveal';
import { SITE } from './lib-meta';

const dmSans = DM_Sans({ subsets: ['latin'], weight: ['400', '500', '700'], display: 'swap' });

export const metadata = {
  metadataBase: new URL(SITE.url),
  robots: { index: true, follow: true },
  manifest: '/site.webmanifest',
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
    ],
    apple: '/apple-touch-icon.png',
  },
};

export const viewport = {
  themeColor: '#073B66',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={dmSans.className}>
        <noscript>
          <style>{`.reveal{opacity:1 !important;transform:none !important;}`}</style>
        </noscript>
        <Header />
        <main>{children}</main>
        <Reveal />
        <a className="mobile-call-bar" href={SITE.phoneHref} aria-label={`Call Now ${SITE.phone}`}>
          <span className="mobile-call-icon" aria-hidden="true">☎</span>
          <span>Call Now · {SITE.phone}</span>
        </a>
        <div className="mobile-call-spacer" aria-hidden="true" />
      </body>
    </html>
  );
}
