# College Dining Meal Plan Initiative

Project website for CS 4390/5388 Software Project Management.

Live site: https://dlozan62.github.io

This repo is the public record of our campus dining research. We started with meal-plan value and flexibility. The current question is what happens when students cannot trust dining information: menus, hours, sold-out items, and dietary details.

Sprint 1 is published. Sprints 2 through 6 will be added as they close.

## Team

- Zachary Carrejo
- Salvador Rodarte
- Team member
- Team member

## Local preview

This is a Jekyll site, so use Jekyll's development server instead of the VS
Code/Cursor **Live Server** extension. Live Server only serves the source files;
it does not process Liquid, front matter, or `_layouts`.

The project uses Ruby 3.3.12. On this Apple Silicon Mac, select the installed
Homebrew Ruby before running Bundler:

```sh
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
ruby -v
bundle check || bundle install
bundle exec jekyll serve --livereload
```

Open <http://127.0.0.1:4000>. In VS Code or Cursor, the same URL can be opened
inside the editor with **Simple Browser: Show** from the command palette.

If port 4000 is already occupied, either use the existing preview or choose a
different port:

```sh
bundle exec jekyll serve --livereload --port 4001
```

The main source pages are `index.html`,
`about.html`, `sprints.html`, and `sprint-1.html`. Each page keeps a small
Jekyll front matter block for its title, description, permalink, and shared
layout.

## Project structure

- `_layouts/default.html` contains the shared document shell, navigation, and footer.
- `assets/css/style.css` contains the design tokens, components, page layouts, and responsive rules.
- `assets/js/site.js` handles only the mobile navigation. Core content remains available without JavaScript.
- `assets/images` and `assets/pdfs` contain the published media and downloadable document.

## Before publishing

Run the same checks used by GitHub Actions:

```sh
bundle exec jekyll build
bundle exec sass assets/css/style.css /tmp/site-check.css --no-source-map
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
```

The checks catch CSS syntax errors, merge-conflict markers, missing pages and
assets, broken internal links, duplicate IDs, and missing image alt text on
every generated HTML page, including future sprints.

The workflow builds and checks pull requests, then deploys the checked `_site`
artifact after a successful push to `main`. To make this workflow the publishing
gate, set **Settings → Pages → Build and deployment → Source** to **GitHub
Actions**. If Source remains **Deploy from a branch**, GitHub Pages can publish
from `main` before these checks finish.

## AI use

AI tools support website design, development, and permitted grammar editing. The team authors the project research, analysis, and conclusions.
