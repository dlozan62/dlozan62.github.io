# Campus Dining Availability System

A living project website for CS 4390/5388 Software Project Management. Sprint 1 records the team's move from meal-plan research to a campus dining availability system; Sprint 2 is a planned outline.

[View the website](https://dlozan62.github.io)

## Preview locally

GitHub Pages builds this site with Jekyll. To preview it locally:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Open <http://127.0.0.1:4000/>.

## Check changes

```sh
bundle exec jekyll build
bundle exec sass assets/css/style.css /tmp/site-check.css --no-source-map
python3 -m unittest discover -s tests -v
python3 scripts/check_site.py
```

## Publish

The [GitHub Actions workflow](.github/workflows/site-check.yml) checks the site before deploying changes from `main`. In repository settings, set **Pages → Build and deployment → Source** to **GitHub Actions**.

## AI use

AI assisted with website design, development, and drafts of the web summaries. The Sprint 1 source research and charter are linked on the site. Individual AI-use disclosures are pending.
