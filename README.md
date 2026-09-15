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

Needs Ruby and Bundler.

```
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000

GitHub Pages builds from `main`. The main source pages are `index.html`,
`about.html`, `sprints.html`, and `sprint-1.html`. Each page keeps a small
Jekyll front matter block for its title, description, permalink, and shared
layout.

## Project structure

- `_layouts/default.html` contains the shared document shell, navigation, and footer.
- `_data/dining_locations.yml` stores the dining-location names and image filenames.
- `assets/css/style.css` contains the design tokens, components, page layouts, and responsive rules.
- `assets/js/site.js` contains small progressive enhancements. Core content remains available without JavaScript.
- `assets/images` and `assets/pdfs` contain the published media and downloadable document.

## AI use

AI tools support website design, development, and permitted grammar editing. The team authors the project research, analysis, and conclusions.
