import { cp, mkdir, readFile, writeFile, access, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createHash } from 'node:crypto';

const root = fileURLToPath(new URL('../', import.meta.url));
const out = path.join(root, 'dist');
const origin = 'https://yulongggggg.github.io';
const papers = JSON.parse(await readFile(path.join(root, 'site/publications.json'), 'utf8'));
const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);
const colors = new Set(['', 'blue', 'red', 'muted']);
const color = value => colors.has(value) ? value : '';
const ids = new Set();
for (const paper of papers) {
  if (!/^[a-z0-9-]+$/.test(paper.id) || ids.has(paper.id)) throw new Error(`Invalid or duplicate paper id: ${paper.id}`);
  ids.add(paper.id);
  if (!['journal', 'conference', 'preprint'].includes(paper.category)) throw new Error(`Invalid category: ${paper.id}`);
  if (!paper.image.startsWith('assets/img/') || paper.image.includes('..')) throw new Error(`Invalid image path: ${paper.id}`);
  await access(path.join(root, paper.image));
  if (paper.pdfFile) {
    if (!paper.pdfFile.startsWith('assets/pdf/') || !paper.pdfFile.endsWith('.pdf') || paper.pdfFile.includes('..')) throw new Error(`Invalid PDF path: ${paper.id}`);
    await access(path.join(root, paper.pdfFile));
  }
  for (const link of paper.links) if (new URL(link.url).protocol !== 'https:') throw new Error(`Invalid paper URL: ${link.url}`);
}
function renderPaper(p, featured) {
  const isPaperPage = p.imageType === 'paper-page';
  const ribbon = p.ribbon && !isPaperPage ? `<span class="ribbon ${color(p.ribbonColor)}"><span>${escape(p.ribbon)}</span></span>` : '';
  const tags = featured ? `<div class="tags">${(p.tags || []).map((tag, i) => `<span${i ? ' class="green"' : ''}>${escape(tag)}</span>`).join('')}</div>` : '';
  const links = `<div class="paper-links">${p.links.map(link => `<a class="badge ${color(link.color)}" href="${escape(link.url)}">${escape(link.label)}</a>`).join('')}</div>`;
  const authors = escape(p.authors).replace('Yulong Liu', '<strong>Yulong Liu</strong>');
  return `<article class="paper ${featured ? 'featured' : 'compact'}" id="${featured ? 'paper' : 'list'}-${escape(p.id)}">
    <a class="paper-image${isPaperPage ? ' paper-image--page' : ''}" href="${escape(p.image)}" data-figure aria-label="${isPaperPage ? 'View first page' : 'Enlarge figure'}: ${escape(p.title)}">${ribbon}<img src="${escape(p.image)}" alt="${escape(p.alt)}" loading="lazy" width="${p.imageWidth || (featured ? 300 : 230)}" height="${p.imageHeight || (featured ? 240 : 150)}"></a>
    <div class="paper-copy">${tags}<h3>${escape(p.title)}</h3>${featured ? links : ''}${featured && p.summary ? `<p class="paper-summary">${escape(p.summary)}</p>` : ''}<p class="authors">${authors}</p><p class="venue">${escape(p.venue)}</p>${featured ? '' : links}</div>
  </article>`;
}
const groups = [
  ['publications', 'Selected Recent Publications', papers.filter(p => p.selected), true],
  ['conference-papers', 'Conference Papers', papers.filter(p => p.category === 'conference'), false],
  ['journal-publications', 'Journal Publications', papers.filter(p => p.category === 'journal'), false],
  ['preprints', 'Preprints & Manuscripts', papers.filter(p => p.category === 'preprint'), false],
];
const publications = groups.map(([id, title, rows, featured]) => `<section class="home-section" id="${id}" aria-labelledby="${id}-title"><h2 class="publication-heading" id="${id}-title">${escape(title)}</h2>${rows.map(p => renderPaper(p, featured)).join('\n')}</section>`).join('\n');
const template = await readFile(path.join(root, 'site/index.html'), 'utf8');
const stylesheetVersion = createHash('sha256').update(await readFile(path.join(root, 'site/style.css'))).digest('hex').slice(0, 12);
if (!template.includes('<!-- PUBLICATIONS -->')) throw new Error('Missing publications marker.');
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const file of ['style.css', 'main.js', 'favicon.svg']) await cp(path.join(root, 'site', file), path.join(out, file));
await cp(path.join(root, 'site/cat'), path.join(out, 'cat'), { recursive: true });
await writeFile(path.join(out, 'index.html'), template.replace('<!-- PUBLICATIONS -->', publications).replace('href="style.css"', `href="style.css?v=${stylesheetVersion}"`));
const assets = new Set(['assets/pdf/Yulong_CV2026_V2.pdf', 'assets/fonts/yulong-name-kai.woff', 'assets/fonts/OFL.txt', ...papers.map(p => p.image), ...papers.map(p => p.pdfFile).filter(Boolean)]);
for (const asset of assets) {
  await mkdir(path.dirname(path.join(out, asset)), { recursive: true });
  await cp(path.join(root, asset), path.join(out, asset));
}
// This existing portrait is a PNG with a historical .jpeg filename.
await cp(path.join(root, 'assets/img/yulong-liu-portrait.jpeg'), path.join(out, 'assets/img/yulong-liu-portrait.png'));
await writeFile(path.join(out, '.nojekyll'), '');
await writeFile(path.join(out, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
await writeFile(path.join(out, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc></url></urlset>\n`);
for (const [route, target] of Object.entries({ research: '#about', publications: '#publications', education: '#education', awards: '#others', talks: '#talks', contact: '#contact', cv: 'assets/pdf/Yulong_CV2026_V2.pdf' })) {
  await mkdir(path.join(out, route), { recursive: true });
  const href = `../${target}`;
  await writeFile(path.join(out, route, 'index.html'), `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=${href}"><title>Yulong Liu</title><p><a href="${href}">Continue to Yulong Liu’s homepage</a></p></html>\n`);
}
await writeFile(path.join(out, '404.html'), `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found · Yulong Liu</title><body style="font:18px/1.6 Arial,sans-serif;max-width:650px;margin:15vh auto;padding:24px"><h1>Page not found</h1><p>This page may have moved.</p><a href="${origin}/">Return to Yulong Liu’s homepage →</a></body></html>\n`);
console.log(`Built ${papers.length} publications into ${out}`);
