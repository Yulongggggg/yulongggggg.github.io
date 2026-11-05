# Yulong Liu — academic homepage

Single-page academic homepage retaining the September 17 template: blue navigation,
Verdana body text, Arial headings, and a large portrait beside the research
introduction, research directions, news, education, illustrated publications,
research support, and academic service. AI directions include differentiable
programming, neural PDE solvers, uncertainty-aware scientific AI, agentic AI, and
AI for Science and scientific discovery. Engineering directions include
homogenization, coupled multiphysics simulation, and subsurface energy systems
such as geothermal reservoirs and hydraulic fracturing. The page uses a white background,
responsive layouts, and real PDF first-page previews without text highlights.
Preserve this template when updating content unless a redesign is explicitly requested.
Research directions are two compact text lists, without diagrams, numbered items,
extra descriptions, or decorative cards. A separate Research highlights grid below
them shows four figures from published or public papers, each linked to its paper.
The main heading uses only “Yulong Liu”.

## Edit and preview

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
- `assets/pdf/Yulong_CV2026_V2.pdf`: downloadable CV.

Requires Node.js 22 or later. No npm dependencies or Ruby installation required.

```sh
npm run build
npm run preview
```

Open `http://127.0.0.1:8790/`. For a remote machine, forward port 8790 in your
editor or SSH client. Preview the built `dist/` directory, not the source template.

Publication and proposal statuses are retained from the previous website. Update
them when decisions are confirmed. The prior Jekyll Markdown pages remain as
source material; the new build does not use them. Common old page paths redirect
to the relevant section of the homepage.

## Alternative style: AcademicPages-like layout

`themes/academicpages/` holds a second, multi-page design modeled on the
AcademicPages Jekyll template (MIT License): a top navigation bar, a sticky profile
sidebar with avatar and links, and separate Research, Publications, CV, Talks,
Awards & Service and News pages, with a light-blue focus box, keyword chips, a grey
news bubble and a research-figure carousel on the home page. It is not deployed.

```sh
npm run build:academicpages
npm run preview:academicpages
```

Open `http://127.0.0.1:8791/`. The build writes `dist-academicpages/` with
`scripts/build-academicpages.mjs`.

- Shared with the main site: `site/publications.json` (Publications and Research
  pages), `assets/img/` figures and paper previews, the portrait and the CV PDF.
- Theme-only text, a snapshot from November 2026: `pages/home.html` (biography and
  interests), `pages/news-items.html` (one `<li>` per line; the home page shows the
  first six), `pages/talks.html`, `pages/awards.html`, `pages/cv.html`. Research
  groupings, figures and the three summaries missing from `publications.json` are
  set in the build script.
- `layout.html` is the shared shell (navigation, sidebar, footer); `style.css` and
  `main.js` hold the styles, mobile menu, carousel and figure viewer.

To switch the live site to this style, bring the theme pages up to date with
`site/index.html`, then in `.github/workflows/deploy.yml` change the build step to
`npm run build:academicpages` and the uploaded `path` to `./dist-academicpages`.
Old one-page anchors such as `/#publications` then land on the home page.

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
`assets/pdf/Yulong_CV2026_V2.pdf` and the legacy root `Yulong_CV2026_V2.pdf` with the
new PDF before rebuilding. Push website changes to the `pages` remote's `main`
branch; the `origin` remote is the earlier website repository.
