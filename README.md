# DineCheck

DineCheck is Team 10's campus dining availability project for CS 4390 / CS 5388 Software Project Management. This repository is the team's project portal: it presents the research, scope, estimates, budget, and decisions behind the proposed system.

[Visit DineCheck](https://dlozan62.github.io)

## Project records

- **Sprint 1:** market research, business strategy, current project charter, and individual contribution statements.
- **Sprint 2:** business case and recommendation, estimation appendix, one-page budget, and a separate project changelog.
- **Sprints 3–6:** planned; pages are added when the team has work to publish.

Research statements and cost figures come from the team's existing records. Sprint 1 retains the earlier project name where it belongs to that historical record. The PDFs and Word files remain available under `assets/`.

## Website structure

| File or folder | Purpose |
| --- | --- |
| `_layouts/default.html` | Shared document metadata, header, navigation, breadcrumbs, and footer |
| `assets/css/style.css` | The complete responsive design system; no separate override stylesheet |
| `assets/js/site.js` | Mobile menu, keyboard-accessible table scrolling, and active report links |
| `index.html` | Project introduction, illustrative product preview, evidence, and progress |
| `demo.html` | Browser-only concept demo with fictional data, filters, and simulated staff updates |
| `about.html` | Team portraits, responsibilities, and biographies |
| `sprints.html` | Published and planned sprint archive |
| `sprint-1.html`, `sprint-2.html` | Sprint overviews and reports |
| `market-research.html` | Research evidence and its limitations |
| `sprints/` | Business strategy, charter, and changelog pages |
| `assets/documents/`, `assets/pdfs/` | Original downloadable project records |
| `scripts/check_site.py`, `tests/` | Generated-page and internal-link validation |
| `.github/workflows/site-check.yml` | Build, validation, and GitHub Pages deployment |

## Local development

Use Ruby from `.ruby-version` and Bundler compatible with `Gemfile.lock`.

```sh
bundle install
bundle exec jekyll serve --livereload
```

Open `http://127.0.0.1:4000`. Pages use Jekyll front matter and Liquid filters; opening a source HTML file directly does not reproduce the deployed site.

## Check changes

```sh
python3 -m unittest discover -s tests -v
node --check assets/js/site.js
bundle exec jekyll build --strict_front_matter
python3 scripts/check_site.py
```

The checker validates the required routes, local links, anchor targets, CSS assets, unique IDs, and image alternative text.

## Publish

In the repository's **Settings → Pages**, set the build source to **GitHub Actions**. Push reviewed changes to `main`; the workflow publishes only after its checks pass. Pull requests run the same checks without publishing.

## Editing guidelines

- Add shared styles to the named sections of `style.css` rather than stacking override files.
- Keep source research, historical records, and assumptions distinct from proven outcomes.
- Preserve existing permalink routes and section IDs so document links continue to work.
- Add alternative text to meaningful images. Decorative images use an empty `alt` attribute.
- Wide report tables scroll within their own container on small screens.
- Keep downloadable files aligned with their source documents. The optional PDF generators require `reportlab`; they are not run during website deployment.

## AI use

AI assisted with website design, development, and drafts of the web summaries. Source research and the current charter are linked on Sprint 1. The team's contribution statements describe its use of AI.

## Concept demo

`/demo/` is an illustrative concept, not a released product or live campus feed. Its location names, menus, hours, and timestamps are fictional. Staff controls simulate updates only in the current browser page; reload or Reset demo restores the initial scenario. The demo works without JavaScript as a static sample; its controls appear when JavaScript is available.
