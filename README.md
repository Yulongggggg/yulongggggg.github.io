# Yulong Liu — academic homepage

The live site, https://yulongggggg.github.io/, uses a multi-page design modeled on the
AcademicPages Jekyll template (MIT License): a top navigation bar, a sticky profile sidebar
with portrait and links, and separate Research, Publications, CV, Talks, Awards & Service and
News pages. The home page has the biography, a light-blue research-focus box, keyword chips,
a grey Recent News bubble and a research-figure carousel. AI directions include differentiable
programming, neural PDE solvers, uncertainty-aware scientific AI, agentic AI, and AI for
Science and scientific discovery; engineering directions include homogenization, coupled
multiphysics simulation, and subsurface energy systems such as geothermal reservoirs and
hydraulic fracturing. The main heading uses only “Yulong Liu”.

The earlier single-page design is kept in `site/` (see “Classic single-page design” below).

## Edit and preview

- `themes/academicpages/layout.html`: shared shell (navigation, profile sidebar, footer).
- `themes/academicpages/pages/home.html`: biography, research focus, interests and figure carousel.
- `themes/academicpages/pages/news-items.html`: one `<li>` per line, newest first; the home page shows all of them in a scrollable Recent News box and `/news/` lists them all.
- `themes/academicpages/pages/talks.html`, `awards.html` (research support, awards, academic service) and `cv.html` (education and the embedded CV).
- `site/publications.json`: publication metadata shared by both designs. `scripts/build-academicpages.mjs` generates the Publications and Research pages from it; research groupings, figures and the three summaries missing from the JSON are set in the script.
- `themes/academicpages/style.css` and `main.js`: styles, mobile menu, figure carousel and figure viewer.
- `assets/img/`: portrait, scientific figures and paper previews. `assets/img/research/` holds WebP copies of the research figures (`*-thumb.webp` for previews; full-resolution originals stay in `assets/img/research-results/`). `assets/img/paper-pages/` holds real PDF first-page screenshots.
- `assets/pdf/Yulong_Liu_CV.pdf`: downloadable CV. The build also publishes it at the old `assets/pdf/Yulong_CV2026_V2.pdf` path so earlier links keep working.

Requires Node.js 22 or later. No npm dependencies or Ruby installation required.

```sh
npm run build
npm run preview
```

Open `http://127.0.0.1:8790/`. `npm run build` writes `dist/`, which the GitHub Pages
workflow deploys. For a remote machine, forward port 8790 in your editor or SSH client.
Paths from the single-page site keep working: `/research/`, `/publications/`, `/talks/`,
`/awards/` and `/cv/` are real pages, `/contact/` redirects to the home page and
`/education/` to `/cv/`.

Update publication and proposal statuses when decisions are confirmed. The older
Jekyll Markdown pages in the repository root remain as source material; neither build
uses them.

## Classic single-page design

The previous design (blue navigation, Verdana body text, a large portrait beside the research
introduction, research-direction lists, a Research highlights figure grid, news with a pinned
item and a carousel, education timeline, illustrated publications and a pixel Shiba Inu
companion) is kept but no longer deployed. Its text lives separately from the live design and
was last synchronized in November 2026.

- `site/index.html`: biography, news, education, service, and links.
- Pinned news: the `news-pinned` box at the top of News holds the single most important item. A `news-carousel` list item holds related items as a swipeable card (arrows, dots, keyboard; slow auto-advance that pauses on hover/focus and under reduced motion); `site/main.js` builds the dots.
- `site/publications.json`: publication metadata; selected and categorized lists share this source.
- `site/style.css`: layout, colors, typography, and mobile styles.
- `site/main.js`: mobile navigation, research-figure viewer, and desktop pixel dog (CSS classes keep the older corner-cat names).
- `site/dog/`: Shiba Inu sprites by kyafu (free licence; re-laid out by `scripts/build_dog_sprites.py`) and an original tennis ball; see `ATTRIBUTION.txt`.
- `assets/img/`: portrait, scientific figures, and paper previews.
- `assets/img/research/`: WebP copies of the Research highlights figures. The grid shows `*-thumb.webp` (1100 px wide; the geothermal thumbnail shows the first three of six cases) and the figure viewer opens the full image. Full-resolution originals stay in `assets/img/research-results/`; the build copies this folder to `dist/`.
- `assets/img/paper-pages/`: actual PDF first-page screenshots. `imageSource` in publication metadata records their source; `imageWidth` and `imageHeight` preserve the page proportions.
- `pdfFile` in publication metadata includes an uploaded paper PDF in the deployment. Public paper links point to the publisher, arXiv, or the hosted PDF.
- `assets/pdf/Yulong_Liu_CV.pdf`: downloadable CV. The build also publishes it at the old `assets/pdf/Yulong_CV2026_V2.pdf` path so earlier links keep working.

Build it with `npm run build:classic` (it also writes `dist/`) and preview with `npm run preview`.
To make it the live site again, update `site/index.html` from the theme pages, then change the
`build` script in `package.json` back to `node scripts/build-site.mjs`.

## GitHub Pages root address

The intended public address is **https://yulongggggg.github.io/**. This requires
the repository **Yulongggggg/yulongggggg.github.io**. The `yulong_website` repository
by itself serves a project path, not that root address.

1. Create an empty public repository named `yulongggggg.github.io` under `Yulongggggg`.
2. Push this site to its `main` branch.
3. In Settings → Pages → Build and deployment, select **GitHub Actions**.
4. Run **Deploy to GitHub Pages** if it did not already run.

The workflow uploads only `dist/`, excluding archived source and development files.
No custom domain or CNAME is needed. See [GitHub's Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## CV updates

The CV source lives in https://github.com/Yulongggggg/Yulong_CV2026_V2. Keep its original template; update content without changing the typography or layout unless requested.
The local checkout is `../Yulong_CV2026_V2`. Edit `cv_content.tex` for content and
`main.tex` for typography. Compile with Tectonic, XeLaTeX or pdfLaTeX, then replace
`assets/pdf/Yulong_Liu_CV.pdf` and the legacy root `Yulong_Liu_CV.pdf` with the
new PDF before rebuilding. Push website changes to the `pages` remote's `main`
branch; the `origin` remote is the earlier website repository.
