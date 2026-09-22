"""Check the generated GitHub Pages site without third-party Python packages."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
REQUIRED_PAGES = (
    "index.html",
    "about/index.html",
    "sprints/index.html",
    "sprints/sprint-1/index.html",
    "sprints/sprint-2/index.html",
    "sprints/sprint-1/market-research/index.html",
    "sprints/sprint-1/business-strategy/index.html",
    "sprints/sprint-1/project-charter/index.html",
    "sprints/sprint-2/research-evidence/index.html",
    "sprints/sprint-2/project-charter/index.html",
    "sprints/sprint-2/change-log/index.html",
)
PUBLIC_DOCUMENTS = {
    "sprints/sprint-1/market-research/index.html": "assets/pdfs/sprint-1-market-research.pdf",
    "sprints/sprint-1/business-strategy/index.html": "assets/pdfs/sprint-1-business-strategy.pdf",
    "sprints/sprint-1/project-charter/index.html": "assets/pdfs/sprint-1-project-charter.pdf",
    "sprints/sprint-2/research-evidence/index.html": "assets/pdfs/sprint-2-research-evidence.pdf",
    "sprints/sprint-2/project-charter/index.html": "assets/pdfs/campus-dining-availability-system-project-charter.pdf",
    "sprints/sprint-2/change-log/index.html": "assets/pdfs/sprint-2-change-log.pdf",
}
PRIVATE_PUBLIC_TARGET = re.compile(r"(?:retrospective|peer-evaluation|individual-estimation-memo)", re.IGNORECASE)
CONFLICT_MARKER = re.compile(r"^(?:<{7}|={7}|>{7})(?:\s|$)", re.MULTILINE)
ORPHAN_HEADING_TEXT = re.compile(r"</h[1-6]>\s*[A-Za-z](?=\s*<)")
CSS_URL = re.compile(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)")
SOURCE_TYPES = {".css", ".html", ".js", ".md", ".yml", ".py"}
IGNORED_SOURCE_DIRS = {".git", "_site", ".jekyll-cache", "vendor", "node_modules", ".venv"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.references = []
        self.images_without_alt = 0

    def handle_starttag(self, tag, attributes):
        values = dict(attributes)
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        if values.get("id"):
            self.ids.append(values["id"])
        for attribute in ("href", "src", "poster"):
            if values.get(attribute):
                self.references.append(values[attribute])


def target_for(page_path, reference):
    url = urlparse(reference)
    if url.scheme or url.netloc or reference.startswith("//"):
        return None
    path = unquote(url.path)
    target = SITE / path.lstrip("/") if path.startswith("/") else page_path.parent / path
    if not path:
        target = page_path
    if target.is_dir() or path.endswith("/"):
        target /= "index.html"
    return target, url.fragment


def main():
    errors = []

    for source in ROOT.rglob("*"):
        if not source.is_file() or source.suffix not in SOURCE_TYPES:
            continue
        if IGNORED_SOURCE_DIRS & set(source.relative_to(ROOT).parts):
            continue
        contents = source.read_text(encoding="utf-8")
        if CONFLICT_MARKER.search(contents):
            errors.append(f"{source.relative_to(ROOT)} contains a merge-conflict marker")
        if source.suffix == ".html" and ORPHAN_HEADING_TEXT.search(contents):
            errors.append(f"{source.relative_to(ROOT)} contains text outside a heading")

    for relative_path in REQUIRED_PAGES:
        if not (SITE / relative_path).is_file():
            errors.append(f"missing generated page: {relative_path}")

    parsed_pages = {}
    for page_path in SITE.rglob("*.html"):
        relative_path = page_path.relative_to(SITE)
        page = Page()
        page.feed(page_path.read_text(encoding="utf-8"))
        parsed_pages[page_path] = page
        duplicates = [identifier for identifier, count in Counter(page.ids).items() if count > 1]
        if duplicates:
            errors.append(f"{relative_path} has duplicate IDs: {', '.join(duplicates)}")
        if page.images_without_alt:
            errors.append(f"{relative_path} has {page.images_without_alt} image(s) without alt text")

    for page_path, page in parsed_pages.items():
        for reference in page.references:
            if PRIVATE_PUBLIC_TARGET.search(unquote(urlparse(reference).path)):
                errors.append(
                    f"{page_path.relative_to(SITE)} links to a private sprint artifact: {reference}"
                )
            resolved = target_for(page_path, reference)
            if resolved is None:
                continue
            target, fragment = resolved
            if not target.is_file():
                errors.append(f"{page_path.relative_to(SITE)} has missing target: {reference}")
            elif fragment and target in parsed_pages and fragment not in parsed_pages[target].ids:
                errors.append(f"{page_path.relative_to(SITE)} has missing anchor: {reference}")

    css_path = SITE / "assets/css/style.css"
    if not css_path.is_file():
        errors.append("missing generated stylesheet")
    else:
        for reference in CSS_URL.findall(css_path.read_text(encoding="utf-8")):
            resolved = target_for(css_path, reference)
            if resolved and not resolved[0].is_file():
                errors.append(f"stylesheet has missing target: {reference}")

    for relative_page, relative_pdf in PUBLIC_DOCUMENTS.items():
        page_path = SITE / relative_page
        pdf_path = SITE / relative_pdf
        expected_reference = "/" + relative_pdf
        page = parsed_pages.get(page_path)
        if page and expected_reference not in page.references:
            errors.append(f"{relative_page} does not link to its matching PDF: {expected_reference}")
        if not pdf_path.is_file():
            errors.append(f"missing public document PDF: {relative_pdf}")

    if errors:
        print("Site check failed:\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print(f"Site check passed: {len(parsed_pages)} pages, internal targets, and IDs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
