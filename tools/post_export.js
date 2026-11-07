#!/usr/bin/env node
/**
 * Post-export: with trailingSlash:true every route exports as <path>/index.html.
 * For routes whose canonical form has NO trailing slash, also emit <path>.html
 * (same content) so BOTH /path and /path/ serve 200 directly with no redirect
 * hop on the canonical URL. Slash-canonical routes already serve from index.html.
 */
const fs = require('fs');
const path = require('path');

const pages = require('../content/pages.json');
const out = path.join(__dirname, '..', 'out');
let made = 0;
let skipped = 0;
for (const p of pages) {
  if (p.slug === '/' || p.slug.endsWith('/')) {
    skipped++;
    continue;
  }
  const dir = path.join(out, p.slug.replace(/^\//, ''));
  const indexFile = path.join(dir, 'index.html');
  const flatFile = dir + '.html';
  if (!fs.existsSync(indexFile)) {
    console.error('MISSING index.html for', p.slug);
    process.exitCode = 1;
    continue;
  }
  fs.copyFileSync(indexFile, flatFile);
  made++;
}
console.log(`post-export: ${made} flat .html copies made, ${skipped} slash routes use index.html`);
