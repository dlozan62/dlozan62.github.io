"""Build PDF copies of portal documents from the same HTML the website shows.

Each PDF is cut from the generated page in _site/, so the web text and the PDF
come from one source. Edit the page, rebuild the site, then rebuild the PDFs:

    bundle exec jekyll build
    python3 scripts/build_section_pdfs.py            # every document below
    python3 scripts/build_section_pdfs.py sprint-5   # only names containing "sprint-5"
    bundle exec jekyll build                         # copy the new PDFs into _site

Requirements (macOS):
  * LibreOffice (`soffice`) converts the extracted HTML to PDF.
  * Firefox renders the interactive wireframe for its screenshot PDF.
  * pypdf sets the PDF title and author.
  * A local server for the built site is started automatically for screenshots.

Only add documents here whose web text lives on a portal page. Team-submitted
PDFs that already exist (for example the Sprint 4 Service Levels PDF) are not
rebuilt by this script.
"""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import base64
import http.server
import mimetypes
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
PDFS = ROOT / "assets" / "pdfs"
SITE_URL = "https://dlozan62.github.io"
SOFFICE = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
FIREFOX = "/Applications/Firefox.app/Contents/MacOS/firefox"
AUTHOR = "Team 10"

# Wide tables print on landscape pages.
LANDSCAPE = {"sprint-4-agile-roadmap.pdf", "sprint-4-delivery-dashboard.pdf", "sprint-3-changelog.pdf",
             "sprint-4-changelog.pdf", "sprint-5-changelog.pdf"}

# output file, page route, section IDs (in order), sprint, document title
DOCUMENTS = [
    ("sprint-2-business-case.pdf", "/sprints/sprint-2/", ["business-case"], 2, "Business case"),
    ("sprint-2-roi-analysis.pdf", "/sprints/sprint-2/", ["roi"], 2, "ROI analysis"),
    ("sprint-3-changelog.pdf", "/sprints/sprint-3/", ["sprint3-changelog"], 3, "Sprint 3 changelog"),
    ("sprint-4-changelog.pdf", "/sprints/sprint-4/", ["sprint4-changelog-record"], 4, "Sprint 4 changelog"),
    ("sprint-4-agile-roadmap.pdf", "/sprints/sprint-4/", ["agile-roadmap"], 4, "Agile roadmap"),
    ("sprint-4-delivery-dashboard.pdf", "/sprints/sprint-4/", ["delivery-dashboard"], 4, "Delivery dashboard"),
    ("sprint-5-overview-review-tasks.pdf", "/sprints/sprint-5/",
     ["screens", "review-tasks", "wireframe-updates"], 5,
     "Wireframe overview and outside-user review tasks"),
    ("sprint-5-changelog.pdf", "/sprints/sprint-5/", ["sprint5-changelog"], 5,
     "Sprint 5 changelog"),
    ("sprint-5-contribution-statements.pdf", "/sprints/sprint-5/", ["sprint5-contributions"], 5,
     "Sprint 5 contribution statements"),
]

# output file, page route, window size, sprint, document title
SCREENSHOTS = [
    ("sprint-5-wireframe-screens.pdf", "/sprints/sprint-5/wireframe/", (1700, 1820), 5,
     "Four annotated wireframe screens"),
]

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
DROP = {"script", "style", "nav", "button", "svg", "iframe", "form", "input", "select", "label"}
DROP_CLASSES = {"button", "document-pdf", "research-download__links", "todo-skip-print", "skip-link"}

PRINT_CSS = """
@page { size: 8.5in 11in; margin: 0.75in; }
body, p, li, td, th, dt, dd, h1, h2, h3, h4, caption { font-family: Helvetica, Arial, sans-serif; }
body { color: #243746; font-size: 10.5pt; line-height: 1.4; }
.running { color: #526174; font-size: 9pt; border-bottom: 2px solid #ff8200; padding-bottom: 4pt; }
h1 { color: #041e42; font-size: 18pt; margin: 10pt 0 4pt; }
h2 { color: #041e42; font-size: 14pt; margin: 14pt 0 4pt; }
h3, h4 { color: #041e42; font-size: 11.5pt; margin: 10pt 0 3pt; }
.source { color: #526174; font-size: 8.5pt; }
caption { font-weight: bold; color: #041e42; text-align: left; }
th { background: #eef2f7; color: #041e42; text-align: left; }
dt { font-weight: bold; color: #041e42; margin-top: 6pt; }
.todo { color: #a84400; font-weight: bold; }
"""


class SectionExtractor(HTMLParser):
    """Copy the elements with the requested IDs, minus screen-only controls."""

    def __init__(self, ids):
        super().__init__(convert_charrefs=True)
        self.ids = set(ids)
        self.sections = {}
        self.current = None
        self.depth = 0
        self.skip_depth = 0
        self.out = []

    def _attrs(self, attrs):
        return dict(attrs)

    def handle_starttag(self, tag, attrs):
        values = self._attrs(attrs)
        if self.current is None:
            if values.get("id") in self.ids and tag not in VOID:
                self.current = values["id"]
                self.depth = 1
                self.out = []
            return
        if tag not in VOID:
            self.depth += 1
        classes = set((values.get("class") or "").split())
        if self.skip_depth:
            if tag not in VOID:
                self.skip_depth += 1
            return
        if tag in DROP or classes & DROP_CLASSES:
            if tag not in VOID:
                self.skip_depth = 1
            return
        if "todo-tag" in classes:
            self.out.append('<span class="todo">[')
            return
        if tag == "img":
            src = values.get("src", "")
            local = SITE / src.lstrip("/") if src.startswith("/") else None
            if local and local.is_file():
                width = values.get("width")
                size = ' width="420"' if not width or int(width) > 420 else f' width="{width}"'
                self.out.append(f'<p><img src="{data_uri(local)}" alt="{escape(values.get("alt", ""))}"{size}></p>')
            return
        if tag == "table":
            self.out.append('<table border="1" cellpadding="5" cellspacing="0" width="100%">')
            return
        if tag == "details":
            self.out.append("<div>")
            return
        if tag == "summary":
            self.out.append("<h4>")
            return
        if tag == "a":
            self.out.append("<span>")
            return
        keep = {k: v for k, v in attrs if k in ("colspan", "rowspan", "scope")}
        rendered = "".join(f' {k}="{escape(v or "")}"' for k, v in keep.items())
        self.out.append(f"<{tag}{rendered}>")

    def handle_startendtag(self, tag, attrs):
        if self.current is not None and not self.skip_depth:
            self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self.current is None:
            return
        if tag not in VOID:
            self.depth -= 1
        if self.skip_depth:
            if tag not in VOID:
                self.skip_depth -= 1
            return
        if self.depth == 0:
            self.sections[self.current] = "".join(self.out)
            self.current = None
            return
        mapping = {"details": "</div>", "summary": "</h4>", "a": "</span>"}
        if tag == "span" and self.out and self.out[-1].endswith("TODO"):
            self.out.append("]</span>")
            return
        self.out.append(mapping.get(tag, f"</{tag}>"))

    def handle_data(self, data):
        if self.current is not None and not self.skip_depth:
            self.out.append(escape(data))

    def handle_comment(self, data):
        pass


def data_uri(path):
    """LibreOffice only embeds images in imported HTML when they are inline data."""
    kind = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{kind};base64,{base64.b64encode(path.read_bytes()).decode()}"


def page_file(route):
    return SITE / route.strip("/") / "index.html"


def wrap(title, sprint, route, ids, body, landscape=False):
    anchor = f"{SITE_URL}{route}#{ids[0]}"
    css = PRINT_CSS.replace("size: 8.5in 11in", "size: 11in 8.5in") if landscape else PRINT_CSS
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{escape(title)}</title><style>{css}</style></head><body>
<p class="running">Team 10 · DineCheck · CS 4390/5388 Software Project Management · Sprint {sprint}</p>
<h1>{escape(title)}</h1>
<p class="source">This PDF is built from the same text as the portal page: {escape(anchor)}</p>
{body}
</body></html>"""


def convert(html_path, out_dir):
    subprocess.run(
        [SOFFICE, "--headless", '--infilter=HTML (StarWriter)', "--convert-to", "pdf:writer_pdf_Export",
         "--outdir", str(out_dir), str(html_path)],
        check=True, capture_output=True,
    )
    return out_dir / (html_path.stem + ".pdf")


def set_metadata(source, target, title, sprint):
    reader = PdfReader(source)
    writer = PdfWriter()
    writer.append(reader)
    writer.add_metadata({
        "/Title": f"{title} (Sprint {sprint})",
        "/Author": AUTHOR,
        "/Subject": f"DineCheck, Team 10, Sprint {sprint}",
        "/Creator": "DineCheck portal",
    })
    with open(target, "wb") as handle:
        writer.write(handle)


def build_document(name, route, ids, sprint, title, work):
    source = page_file(route)
    parser = SectionExtractor(ids)
    parser.feed(source.read_text(encoding="utf-8"))
    missing = [i for i in ids if i not in parser.sections]
    if missing:
        raise SystemExit(f"{name}: section(s) not found in {source}: {', '.join(missing)}")
    body = "\n".join(parser.sections[i] for i in ids)
    html_path = work / (Path(name).stem + ".html")
    html_path.write_text(wrap(title, sprint, route, ids, body, name in LANDSCAPE), encoding="utf-8")
    set_metadata(convert(html_path, work), PDFS / name, title, sprint)


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, *args):
        pass


def build_screenshot(name, route, size, sprint, title, work, port):
    png = work / (Path(name).stem + ".png")
    profile = work / "firefox-profile"
    profile.mkdir(exist_ok=True)
    subprocess.run(
        [FIREFOX, "--headless", "--no-remote", "--profile", str(profile),
         f"--window-size={size[0]},{size[1]}", "--screenshot", str(png), f"http://127.0.0.1:{port}{route}"],
        check=True, capture_output=True, timeout=120,
    )
    html_path = work / (Path(name).stem + ".html")
    body = f'<p><img src="{data_uri(png)}" width="640" alt="{escape(title)}"></p>'
    html_path.write_text(wrap(title, sprint, route, ["top"], body).replace("#top", ""), encoding="utf-8")
    set_metadata(convert(html_path, work), PDFS / name, title, sprint)


def main(argv):
    if not SITE.is_dir():
        raise SystemExit("Build the site first: bundle exec jekyll build")
    wanted = argv[1] if len(argv) > 1 else ""
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for name, route, ids, sprint, title in DOCUMENTS:
            if wanted in name:
                build_document(name, route, ids, sprint, title, work)
                print(f"built assets/pdfs/{name}")
        shots = [s for s in SCREENSHOTS if wanted in s[0]]
        if shots:
            with socketserver.TCPServer(("127.0.0.1", 0), QuietHandler) as server:
                port = server.server_address[1]
                threading.Thread(target=server.serve_forever, daemon=True).start()
                for name, route, size, sprint, title in shots:
                    build_screenshot(name, route, size, sprint, title, work, port)
                    print(f"built assets/pdfs/{name}")
                server.shutdown()


if __name__ == "__main__":
    main(sys.argv)
