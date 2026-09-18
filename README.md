# Yulong Liu — academic homepage

Single-page academic homepage with a navy navigation bar, portrait and biography,
news, education, illustrated publications, research support, and academic service.
The layout follows https://chenliu-1996.github.io/. The biography, portrait, CV,
publication metadata, and scientific figures come from Yulong's existing website.
The HTML, CSS, and JavaScript are independently implemented.

## Edit and preview

- `site/index.html`: biography, news, education, service, and links.
- `site/publications.json`: publication metadata; selected and categorized lists share this source.
- `site/style.css`: layout, colors, typography, and mobile styles.
- `site/main.js`: mobile navigation and the research-figure viewer.
- `site/cat/`: the reference site's pixel cat artwork; source credit is in `ATTRIBUTION.txt`.
- `assets/img/`: portrait and scientific figures.
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

The CV source lives in https://github.com/Yulongggggg/Yulong_CV2026_V2.
Replace `assets/pdf/Yulong_CV2026_V2.pdf` with the newly compiled PDF, then rebuild.
