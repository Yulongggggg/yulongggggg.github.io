// Alternative AcademicPages-style site (top navigation, profile sidebar, multiple pages).
// Builds into dist-academicpages/. Publications come from site/publications.json;
// the other page text lives in themes/academicpages/pages/.
import { cp, mkdir, readFile, writeFile, rm, access } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { createHash } from 'node:crypto';

const root = fileURLToPath(new URL('../', import.meta.url));
const theme = path.join(root, 'themes/academicpages');
const out = path.join(root, 'dist-academicpages');
const origin = 'https://yulongggggg.github.io';
const read = file => readFile(path.join(theme, file), 'utf8');
const escape = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const papers = JSON.parse(await readFile(path.join(root, 'site/publications.json'), 'utf8'));
const byId = Object.fromEntries(papers.map(p => [p.id, p]));
const authorsHtml = p => escape(p.authors.replace(/\.$/, '')).replace('Yulong Liu', '<strong>Yulong Liu</strong>');
const linksHtml = links => links.map(l => `<a href="${escape(l.url)}">[${escape(l.label)}]</a>`).join(' ');

// Research page: projects grouped by primary focus.
const extraLinks = { belief: [{ label: 'Code', url: 'https://github.com/HaningZS/Bayesian-Belief-Tracking' }] };
const summaries = {
  bilayer: 'A physics-informed neural network surrogate for stress and displacement around pressurized cavities in homogeneous and bilayered elastic media. It combines the governing equations with finite-element data and runs up to 160 times faster than finite-element simulation.',
  microtunnelling: 'Harvester ants widen their tunnels in several passes. Finite-element simulations compare the plastic zone and the excavation force, torque and energy of single-pass and five-stage excavation of small unsupported tunnels in moist sand.',
  belief: 'Sequential Bayesian Belief Tracking updates, during generation, the probability that a long reasoning trace will end in a correct answer. Scalar scores mainly improve calibration, while structure-aware prefix signals are needed to improve ranking.',
};
const areas = [
  { id: 'geothermal', title: 'Scientific AI for Geothermal Energy', projects: [['operator', 'geothermal-operator']] },
  { id: 'rock-mechanics', title: 'Physics-Informed Rock Mechanics', projects: [['pinn', 'pinn-cavity'], ['bilayer', null]] },
  { id: 'reliable-ai', title: 'Reliable AI for Scientific Computing', projects: [['intent', 'pde-refine'], ['belief', null]] },
  { id: 'geomechanics', title: 'Computational Geomechanics', projects: [['microtunnelling', 'microtunnelling']] },
];
const assets = new Set(['assets/pdf/Yulong_Liu_CV.pdf']);
function projectHtml(id, figure) {
  const p = byId[id];
  if (!p) throw new Error(`Unknown paper id in research page: ${id}`);
  const full = figure ? `assets/img/research/${figure}.webp` : p.image;
  const thumb = figure ? `assets/img/research/${figure}-thumb.webp` : p.image;
  assets.add(full); assets.add(thumb);
  const summary = p.summary || summaries[id];
  if (!summary) throw new Error(`Missing research summary: ${id}`);
  return `<article class="project">
  <h3>${escape(p.title)}</h3>
  <p class="project-meta">${authorsHtml(p)}. <em>${escape(p.venue)}</em>.</p>
  <div class="project-row">
    <a class="project-figure${figure ? '' : ' project-figure--page'}" href="/${full}" data-figure aria-label="Enlarge figure: ${escape(p.title)}"><img src="/${thumb}" alt="${escape(p.alt)}" loading="lazy"${figure ? '' : ` width="${p.imageWidth}" height="${p.imageHeight}"`}></a>
    <div class="project-box"><p>${escape(summary)}</p><div class="project-links">${linksHtml([...p.links, ...(extraLinks[id] || [])])}</div></div>
  </div>
</article>`;
}
const research = `<p>This page gives an overview of my research in scientific AI, computational geomechanics, and subsurface energy systems. Use the buttons below to jump to projects by their primary focus; select a figure to enlarge it.</p>
<nav class="section-nav" aria-label="Research sections">${areas.map(a => `<a href="#${a.id}">${escape(a.title)}</a>`).join('')}</nav>
${areas.map(a => `<h2 class="research-area" id="${a.id}">${escape(a.title)}</h2>\n${a.projects.map(([id, fig]) => projectHtml(id, fig)).join('\n<hr class="project-sep">\n')}`).join('\n')}`;

// Publications page.
const pubGroups = [['Preprints', 'preprint'], ['Refereed Journal Articles', 'journal'], ['Conference Proceedings', 'conference']];
const publications = pubGroups.map(([title, category]) => {
  const rows = papers.filter(p => p.category === category);
  return `<h2 class="pub-heading">${title}</h2>
<ul class="archive-list">
${rows.map(p => `  <li>${authorsHtml(p)}. “${escape(p.title)}”. <em>${escape(p.venue)}</em>. <span class="pub-links">${linksHtml(p.links)}</span></li>`).join('\n')}
</ul>`;
}).join('\n');

// News: the home page shows the six most recent items.
const newsItems = (await read('pages/news-items.html')).trim().split('\n').filter(Boolean);
const pages = [
  { route: '/', nav: null, title: "Yulong Liu's Homepage", heading: null, file: 'pages/home.html' },
  { route: '/research/', nav: 'Research', title: 'Research', heading: 'Research', html: research },
  { route: '/publications/', nav: 'Publications', title: 'Publications', heading: 'Publications', html: publications },
  { route: '/cv/', nav: 'CV', title: 'CV', heading: 'Curriculum Vitae', file: 'pages/cv.html' },
  { route: '/talks/', nav: 'Talks', title: 'Talks', heading: 'Talks and Presentations', file: 'pages/talks.html' },
  { route: '/awards/', nav: 'Awards & Service', title: 'Awards and Service', heading: 'Awards, Research Support, and Service', file: 'pages/awards.html' },
  { route: '/news/', nav: 'News', title: 'News', heading: 'News', file: 'pages/news.html' },
];
const layout = await read('layout.html');
const versionOf = async file => createHash('sha256').update(await readFile(path.join(theme, file))).digest('hex').slice(0, 12);
const cssVersion = await versionOf('style.css');
const jsVersion = await versionOf('main.js');
const cvVersion = createHash('sha256').update(await readFile(path.join(root, 'assets/pdf/Yulong_Liu_CV.pdf'))).digest('hex').slice(0, 12);
const description = 'Yulong Liu, Ph.D. candidate at Cornell University: scientific AI, computational geomechanics, and subsurface energy systems.';

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const page of pages) {
  let content = page.html ?? await read(page.file);
  content = content.replace('{{RECENT_NEWS}}', newsItems.slice(0, 6).join('\n')).replace('{{ALL_NEWS}}', newsItems.join('\n'));
  const nav = pages.filter(p => p.nav).map(p => `        <li><a href="${p.route}"${p === page ? ' aria-current="page"' : ''}>${escape(p.nav)}</a></li>`).join('\n');
  const html = layout
    .replaceAll('{{TITLE}}', escape(page.route === '/' ? page.title : `${page.title} · Yulong Liu`))
    .replaceAll('{{DESCRIPTION}}', escape(description))
    .replaceAll('{{PATH}}', page.route)
    .replace('{{NAV}}', nav)
    .replace('{{PAGE_TITLE}}', page.heading ? `      <h1 class="page__title">${escape(page.heading)}</h1>` : '')
    .replace('{{CONTENT}}', content)
    .replace('href="/style.css"', `href="/style.css?v=${cssVersion}"`)
    .replace('src="/main.js"', `src="/main.js?v=${jsVersion}"`)
    .replaceAll('/assets/pdf/Yulong_Liu_CV.pdf', `/assets/pdf/Yulong_Liu_CV.pdf?v=${cvVersion}`);
  for (const [, asset] of html.matchAll(/(?:src|href)="\/(assets\/[^"?#]+)/g)) assets.add(asset);
  const dir = path.join(out, page.route);
  await mkdir(dir, { recursive: true });
  await writeFile(path.join(dir, 'index.html'), html);
}

// Copy theme files and every referenced asset.
await cp(path.join(theme, 'style.css'), path.join(out, 'style.css'));
await cp(path.join(theme, 'main.js'), path.join(out, 'main.js'));
await cp(path.join(root, 'site/favicon.svg'), path.join(out, 'favicon.svg'));
for (const asset of assets) {
  // The portrait is a PNG stored under a historical .jpeg file name.
  const source = asset === 'assets/img/yulong-liu-portrait.png' ? 'assets/img/yulong-liu-portrait.jpeg' : asset;
  await access(path.join(root, source));
  await mkdir(path.dirname(path.join(out, asset)), { recursive: true });
  await cp(path.join(root, source), path.join(out, asset));
}
for (const p of papers.filter(p => p.pdfFile)) {
  await mkdir(path.dirname(path.join(out, p.pdfFile)), { recursive: true });
  await cp(path.join(root, p.pdfFile), path.join(out, p.pdfFile));
}
// The CV used to be published as Yulong_CV2026_V2.pdf; keep that URL working for links already shared.
await cp(path.join(root, 'assets/pdf/Yulong_Liu_CV.pdf'), path.join(out, 'assets/pdf/Yulong_CV2026_V2.pdf'));
await writeFile(path.join(out, '.nojekyll'), '');
await writeFile(path.join(out, 'robots.txt'), `User-agent: *\nAllow: /\nSitemap: ${origin}/sitemap.xml\n`);
await writeFile(path.join(out, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${pages.map(p => `<url><loc>${origin}${p.route}</loc></url>`).join('')}</urlset>\n`);
await writeFile(path.join(out, '404.html'), `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found · Yulong Liu</title><body style="font:18px/1.6 -apple-system,'Segoe UI',Roboto,Arial,sans-serif;max-width:650px;margin:15vh auto;padding:24px"><h1>Page not found</h1><p>This page may have moved.</p><a href="${origin}/">Return to Yulong Liu’s homepage →</a></body></html>\n`);
console.log(`Built ${pages.length} AcademicPages-style pages and ${assets.size} assets into ${out}`);
