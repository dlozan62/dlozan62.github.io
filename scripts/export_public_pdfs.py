"""Export public document pages from the built Jekyll site as matching PDFs."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
OUTPUT = ROOT / "assets" / "pdfs"

DOCUMENTS = {
    "sprints/sprint-1/market-research/index.html": "sprint-1-market-research.pdf",
    "sprints/sprint-1/business-strategy/index.html": "sprint-1-business-strategy.pdf",
    "sprints/sprint-1/project-charter/index.html": "sprint-1-project-charter.pdf",
    "sprints/sprint-2/research-evidence/index.html": "sprint-2-research-evidence.pdf",
    "sprints/sprint-2/project-charter/index.html": "campus-dining-availability-system-project-charter.pdf",
    "sprints/sprint-2/change-log/index.html": "sprint-2-change-log.pdf",
}


def clean(value):
    return " ".join(
        value.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2011", "-")
        .split()
    )


class DocumentParser(HTMLParser):
    """Extract semantic blocks from one public document article."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_article = False
        self.depth = 0
        self.skip_depth = 0
        self.active = None
        self.buffer = []
        self.blocks = []
        self.in_table = False
        self.table_rows = []
        self.current_row = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        if not self.in_article and tag == "article" and "document-page" in classes:
            self.in_article = True
            self.depth = 1
            return
        if not self.in_article:
            return
        if tag == "br":
            if self.active:
                self.buffer.append("<br/>")
            return
        self.depth += 1
        if self.skip_depth:
            self.skip_depth += 1
            return
        if tag == "a" and "button" in classes:
            self.skip_depth = 1
            return
        if tag == "table":
            self.in_table = True
            self.table_rows = []
            return
        if tag == "tr" and self.in_table:
            self.current_row = []
            return
        if tag in {"h1", "h2", "h3", "p", "li", "th", "td"}:
            self.active = tag
            self.buffer = []

    def handle_endtag(self, tag):
        if not self.in_article:
            return
        if self.skip_depth:
            self.skip_depth -= 1
            self.depth -= 1
            return
        if tag == self.active:
            value = clean("".join(self.buffer).replace("<br/>", " | "))
            if value:
                if self.in_table and tag in {"th", "td"}:
                    self.current_row.append(value)
                else:
                    self.blocks.append((tag, value))
            self.active = None
            self.buffer = []
        if tag == "tr" and self.in_table and self.current_row:
            self.table_rows.append(self.current_row)
            self.current_row = None
        if tag == "table" and self.in_table:
            self.blocks.append(("table", self.table_rows))
            self.table_rows = []
            self.in_table = False
        self.depth -= 1
        if tag == "article" and self.depth == 0:
            self.in_article = False

    def handle_data(self, data):
        if self.in_article and self.active and not self.skip_depth:
            self.buffer.append(data)


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD2D8"))
    canvas.line(document.leftMargin, 0.48 * inch, LETTER[0] - document.rightMargin, 0.48 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#556272"))
    canvas.drawString(document.leftMargin, 0.3 * inch, "Campus Dining Availability System")
    canvas.drawRightString(LETTER[0] - document.rightMargin, 0.3 * inch, f"Page {document.page}")
    canvas.restoreState()


def export(source, destination):
    parser = DocumentParser()
    parser.feed(source.read_text(encoding="utf-8"))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=21, leading=24, textColor=colors.HexColor("#041E42"), alignment=TA_CENTER, spaceAfter=15))
    styles.add(ParagraphStyle(name="DocH2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=16, leading=18, textColor=colors.HexColor("#041E42"), spaceBefore=9, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle(name="DocH3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=colors.HexColor("#A84400"), spaceBefore=8, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle(name="DocBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#334155"), spaceAfter=5))
    styles.add(ParagraphStyle(name="DocBullet", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=11.5, leftIndent=16, firstLineIndent=-10, textColor=colors.HexColor("#334155"), spaceAfter=2.5))
    styles.add(ParagraphStyle(name="DocTableHeader", parent=styles["DocBody"], fontName="Helvetica-Bold", textColor=colors.white))

    story = []
    title_seen = False
    for kind, value in parser.blocks:
        if kind == "h1":
            if title_seen:
                story.append(PageBreak())
            story.append(Paragraph(escape(value), styles["DocTitle"]))
            title_seen = True
        elif kind == "h2":
            if value == "What could go wrong and how we would respond":
                story.append(PageBreak())
            story.append(Paragraph(escape(value), styles["DocH2"]))
        elif kind == "h3":
            story.append(Paragraph(escape(value), styles["DocH3"]))
        elif kind == "p":
            story.append(Paragraph(escape(value), styles["DocBody"]))
        elif kind == "li":
            story.append(Paragraph(escape(value), styles["DocBullet"], bulletText="-"))
        elif kind == "table":
            rows = [
                [
                    Paragraph(escape(cell), styles["DocTableHeader"] if row_index == 0 else styles["DocBody"])
                    for cell in row
                ]
                for row_index, row in enumerate(value)
            ]
            if rows:
                width = 7.1 * inch / max(len(row) for row in rows)
                table = Table(rows, colWidths=[width] * max(len(row) for row in rows), repeatRows=1)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#041E42")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD2D8")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]))
                story.extend([Spacer(1, 6), table, Spacer(1, 12)])

    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(destination),
        pagesize=LETTER,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.55 * inch,
        title=next((value for kind, value in parser.blocks if kind == "h1"), destination.stem),
        author="Team 10",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    for relative_source, filename in DOCUMENTS.items():
        source = SITE / relative_source
        if not source.is_file():
            raise FileNotFoundError(f"Build the site before exporting PDFs: {source}")
        destination = OUTPUT / filename
        export(source, destination)
        print(f"wrote {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
