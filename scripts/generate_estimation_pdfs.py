"""Create Sprint 2 PDFs from the same assignment text used by Jekyll.

Edit the plain HTML in _includes, then run this script. PDF and website
content share one source, including the tables, assumptions, and source links.
Requires reportlab and beautifulsoup4.
"""

from html import escape
from pathlib import Path
import shutil

from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf"
PUBLIC = ROOT / "assets/pdfs"
NAVY = colors.HexColor("#041e42")
MIST = colors.HexColor("#eef2f5")


def paragraph_text(element):
    """Keep readable text and clickable source links in the PDF."""
    if element.name == "a":
        return '<link href="' + escape(element["href"], quote=True) + '">' + escape(element.get_text()) + '</link>'
    if element.name is None:
        return escape(str(element))
    return "".join(paragraph_text(child) for child in element.children)


def make_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("DocumentTitle", fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=NAVY, spaceAfter=12))
    styles.add(ParagraphStyle("Team", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=16))
    styles.add(ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=16, spaceAfter=9, keepWithNext=True))
    styles.add(ParagraphStyle("Subsection", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=NAVY, spaceBefore=12, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle("Copy", fontName="Helvetica", fontSize=10, leading=14, spaceAfter=9))
    styles.add(ParagraphStyle("Note", parent=styles["Copy"], backColor=MIST, borderPadding=8, spaceBefore=7, spaceAfter=13))
    styles.add(ParagraphStyle("Cell", fontName="Helvetica", fontSize=9, leading=12))
    styles.add(ParagraphStyle("HeaderCell", parent=styles["Cell"], fontName="Helvetica-Bold", textColor=colors.white))
    styles.add(ParagraphStyle("Caption", fontName="Helvetica", fontSize=8, leading=11, textColor=colors.HexColor("#556272"), spaceBefore=8, spaceAfter=5, keepWithNext=True))
    return styles


def make_table(element, styles):
    rows = element.select("tr")
    cells = []
    for index, row in enumerate(rows):
        style = styles["HeaderCell"] if index == 0 else styles["Cell"]
        cells.append([Paragraph(paragraph_text(cell), style) for cell in row.find_all(["td", "th"], recursive=False)])
    columns = len(cells[0])
    caption = element.find("caption").get_text()
    # Short numeric columns leave more room for capability descriptions.
    if caption == "Release 1 capabilities and hidden work":
        widths = [25, 223, 154, 110]
    elif columns == 4:
        widths = [272, 80, 80, 80]
    elif columns == 3:
        widths = [280, 116, 116]
        if "stories" in caption:
            widths = [372, 85, 55]
        elif "Revisions" in caption:
            widths = [171, 171, 170]
    else:
        widths = [155, 357]
    table = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, MIST]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd2d8")),
    ]))
    return [Paragraph(escape(caption), styles["Caption"]), table, Spacer(1, 10)]


def page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#556272"))
    canvas.drawString(50, 27, "Team 10 | Campus Dining | Sprint 2")
    canvas.drawRightString(letter[0] - 50, 27, str(document.page))
    canvas.restoreState()


def create_pdf(source, filename, title, date):
    styles = make_styles()
    soup = BeautifulSoup((ROOT / "_includes" / source).read_text(), "html.parser")
    story = [Paragraph(title, styles["DocumentTitle"]), Paragraph("Team 10 | CS 4390/5388 | Campus Dining<br/>" + date, styles["Team"])]
    for section in soup.select("section"):
        # Keep the starter's comparison answers together on their own page.
        if section.get("id") == "starter-comparison":
            story.append(PageBreak())
        label = section.select_one(".document-label").get_text()
        heading = section.find("h2").get_text()
        story.append(Paragraph(escape(label + ": " + heading), styles["Section"]))
        # Classroom directions are already excluded from these shared includes.
        for element in section.select_one(".charter-section__content").children:
            if element.name == "h3":
                story.append(Paragraph(paragraph_text(element), styles["Subsection"]))
            elif element.name == "p":
                style = styles["Note"] if "charter-note" in element.get("class", []) else styles["Copy"]
                story.append(Paragraph(paragraph_text(element), style))
            elif element.name == "div" and element.find("table"):
                story.extend(make_table(element.find("table"), styles))
    path = OUTPUT / filename
    document = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=48, title=title + " - Campus Dining", author="Team 10")
    document.build(story, onFirstPage=page_number, onLaterPages=page_number)
    shutil.copyfile(path, PUBLIC / filename)
    print(f"Created {path} and public download")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    PUBLIC.mkdir(parents=True, exist_ok=True)
    create_pdf("sprint-2-starter.html", "sprint-2-estimation-starter.pdf", "Project Estimation Starter", "Portal record: September 29, 2026")
    create_pdf("sprint-2-activity.html", "sprint-2-estimation-activity-2.pdf", "Estimation Activity 2", "Estimate dated September 28, 2026")
    create_pdf("sprint-2-changes.html", "sprint-2-change-log.pdf", "Sprint 2 change log", "Updated September 29, 2026")


if __name__ == "__main__":
    main()
