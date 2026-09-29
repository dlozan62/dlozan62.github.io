# Campus Dining Availability System

A living project website for CS 4390/5388 Software Project Management. Sprint 1 records the team's move from meal-plan research to a campus dining availability system. Sprint 2 presents the estimation starter and worked Activity 2 on one page, with a PDF for each assignment and a separate change log.

The Sprint 2 assignment text lives in `_includes/sprint-2-starter.html` and `_includes/sprint-2-activity.html`. The change log lives in `_includes/sprint-2-changes.html`. The PDF generator reads these same files so the page and downloads stay consistent. After changing the text, run `python3 scripts/generate_estimation_pdfs.py` with ReportLab and Beautiful Soup installed, then inspect the PDFs. The original starter worksheet remains archived as `assets/pdfs/sprint-2-estimation-starter-team10.pdf`; the page links the version containing only project work.

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
