"""Build the downloadable Sprint 1 market research summary PDF.

The text in this small script follows market-research.html. Keeping the layout
in a few named sections makes it easier for a new developer to update later.
Run with the bundled Codex Python that includes ReportLab:

    python3 scripts/generate_market_research_pdf.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# These colors match the site's navy, orange, and light gray palette.
NAVY = colors.HexColor("#041E42")
ORANGE = colors.HexColor("#FF8200")
ORANGE_INK = colors.HexColor("#A84400")
MIST = colors.HexColor("#EEF2F5")
PAPER = colors.HexColor("#F7F8F8")
INK = colors.HexColor("#101B2B")
MUTED = colors.HexColor("#556272")
LINE = colors.HexColor("#CBD2D8")

OUTPUT_PATH = Path(__file__).resolve().parents[1] / "assets/pdfs/sprint-1-market-research.pdf"


# The stats are the small interview counts shown on the web page.
STATS = [
    ("13", "meal-plan response sheets, including one staff response"),
    ("8", "respondents preferred a dollar balance"),
    ("5", "respondents preferred set meals"),
]
AVAILABILITY_STAT = ("12", "focused availability response sheets")

MEAL_PLAN_PARAGRAPHS = [
    "The 13 meal-plan response sheets include one response from a staff member. "
    "Eight respondents preferred a dollar balance, while five preferred a set number "
    "of meals. In their comments, respondents tied a dollar balance to changing "
    "day-to-day spending; one respondent said set meals would be easier to track.",
    "Other answers mentioned rollover, discounts, food variety, portion size, and being "
    "able to use a plan at different locations. These responses describe a small "
    "interview group, not a campus-wide estimate.",
]

AVAILABILITY_INTRO = (
    "The focused availability response sheets ask what people checked before leaving, what "
    "they found at arrival, and what happened when an item or service differed. The "
    "responses include cases with a clear cost in time or money, as well as substitutions "
    "with no added cost. Some respondents said the hours or menu they checked matched "
    "what they found; the group did not report a problem on every trip."
)

EXAMPLES = [
    (
        "Empty grab-and-go case",
        "One participant walked to the Union for pizza; the detour took about 25 minutes "
        "(packet p. 10).",
    ),
    (
        "Kitchen closed while the cafe was open",
        "One participant ordered delivery to a lab for about $18 and waited roughly 40 "
        "minutes (packet p. 12).",
    ),
    (
        "Sold-out ribs",
        "One participant bought a snack for about $6 more and waited until after class "
        "for a full meal (packet p. 9).",
    ),
]

OTHER_EXAMPLES = (
    "Other sheets describe sold-out soup, unavailable milk, and changed stations. People "
    "sometimes chose a substitute, skipped an item, or learned about the change from a "
    "sign or staff member only after they arrived."
)

CANDIDATES = [
    (
        "Real-Time Food Availability System",
        "Show whether food items and dining stations are available, low in stock, or sold out.",
    ),
    (
        "Dining Hours and Service Status Tracker",
        "Show separate kitchen and counter hours, temporary closures, equipment outages, and service changes.",
    ),
    (
        "Flexible Meal Plan with Rollover Balance",
        "Carry unused funds into the next semester and make balances and spending easy to see.",
    ),
    (
        "Customizable Meal Plan Options",
        "Offer dollar-balance, set-meal, or combined plan structures for different needs and budgets.",
    ),
    (
        "Campus Dining Alerts and Notifications",
        "Notify students about sold-out items, equipment failures, or restocking problems.",
    ),
]

DECISION_TEXT = (
    "After comparing the five candidates with the availability interview evidence, the "
    "team selected a system that shows current item and station availability before "
    "students walk to a dining location. The packet points to repeated surprises and "
    "concrete effects such as substitutions, delays, and extra spending."
)

EVIDENCE_LIMIT = (
    "These 12 response sheets document interview examples. They do not measure how often "
    "each problem occurs across campus, establish its campus-wide financial impact, or "
    "prove that a particular system is feasible or effective."
)

SOURCE_NOTE = (
    "Source: campus-dining-phase-2-final.pdf. The packet contains five candidate ideas "
    "and the scoping decision on pages 1-2; 12 focused availability response sheets on pages "
    "3-14; and 13 meal-plan response sheets on pages 16-22 and 24-29. The meal-plan "
    "responses include one staff respondent. In the source, \"Phase 2\" names the "
    "research round; it does not mean Sprint 2 has started."
)


def make_styles():
    """Return the small set of text styles used in the report."""
    base = getSampleStyleSheet()
    return {
        "eyebrow": ParagraphStyle(
            "Eyebrow", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8, leading=10, textColor=ORANGE_INK, spaceAfter=8,
        ),
        "decision_eyebrow": ParagraphStyle(
            "DecisionEyebrow", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8, leading=10, textColor=NAVY, spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=27, leading=29, textColor=NAVY, alignment=TA_LEFT,
            spaceAfter=11,
        ),
        "lead": ParagraphStyle(
            "Lead", parent=base["BodyText"], fontName="Helvetica",
            fontSize=11.5, leading=16, textColor=MUTED, spaceAfter=15,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=17, leading=20, textColor=NAVY, spaceBefore=5, spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9.6, leading=14, textColor=INK, spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Helvetica",
            fontSize=8.3, leading=11.5, textColor=MUTED,
        ),
        "stat_number": ParagraphStyle(
            "StatNumber", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=22, leading=24, textColor=NAVY, spaceAfter=5,
        ),
        "stat_label": ParagraphStyle(
            "StatLabel", parent=base["Normal"], fontName="Helvetica",
            fontSize=7.3, leading=9, textColor=MUTED,
        ),
        "candidate_number": ParagraphStyle(
            "CandidateNumber", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=ORANGE_INK,
        ),
        "candidate_title": ParagraphStyle(
            "CandidateTitle", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.5, leading=12, textColor=NAVY,
        ),
        "candidate_body": ParagraphStyle(
            "CandidateBody", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.8, leading=12, textColor=MUTED,
        ),
        "decision_title": ParagraphStyle(
            "DecisionTitle", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=17, leading=19, textColor=NAVY, spaceAfter=7,
        ),
        "decision_body": ParagraphStyle(
            "DecisionBody", parent=base["BodyText"], fontName="Helvetica",
            fontSize=9.4, leading=13.5, textColor=NAVY,
        ),
    }


def paragraph(text, style):
    """Escape plain text before placing it in a ReportLab paragraph."""
    return Paragraph(escape(text), style)


def make_stats_table(styles, width):
    """Make one short row of evidence cards."""
    card_width = width / len(STATS)
    cards = []
    for value, label in STATS:
        cards.append([
            [paragraph(value, styles["stat_number"])],
            [paragraph(label, styles["stat_label"])],
        ])

    table = Table(
        [[Table(card, colWidths=[card_width]) for card in cards]],
        colWidths=[card_width] * len(STATS),
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LINEBEFORE", (1, 0), (-1, -1), 0.6, LINE),
    ]))
    return table


def make_availability_stat(styles, width):
    """Keep the availability count beside its own interview description."""
    table = Table(
        [[
            paragraph(AVAILABILITY_STAT[0], styles["stat_number"]),
            paragraph(AVAILABILITY_STAT[1], styles["stat_label"]),
        ]],
        colWidths=[65, width - 65],
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MIST),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def make_example_table(styles, width):
    """Lay out the three specific stories with their source page numbers."""
    rows = []
    for title, detail in EXAMPLES:
        rows.append([
            paragraph(title, styles["candidate_title"]),
            paragraph(detail, styles["candidate_body"]),
        ])

    table = Table(rows, colWidths=[width * 0.32, width * 0.68], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return table


def make_candidate_table(styles, width):
    """Show the five candidate ideas in the same order as the web page."""
    rows = []
    for index, (title, detail) in enumerate(CANDIDATES, start=1):
        rows.append([
            paragraph(f"{index:02d}", styles["candidate_number"]),
            paragraph(title, styles["candidate_title"]),
            paragraph(detail, styles["candidate_body"]),
        ])

    table = Table(rows, colWidths=[32, width * 0.34, width - 32 - width * 0.34], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def draw_page_frame(canvas, doc):
    """Add the small site label and page number to every PDF page."""
    canvas.saveState()
    width, height = letter
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.7)
    canvas.line(doc.leftMargin, height - 34, width - doc.rightMargin, height - 34)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(NAVY)
    canvas.drawString(doc.leftMargin, height - 25, "COLLEGE DINING  /  SPRINT 1")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - doc.rightMargin, 27, f"Market research  /  {doc.page}")
    canvas.restoreState()


def build_pdf():
    """Create the two-page, print-ready research summary."""
    styles = make_styles()
    document = SimpleDocTemplate(
        str(OUTPUT_PATH), pagesize=letter,
        leftMargin=0.68 * inch, rightMargin=0.68 * inch,
        topMargin=0.6 * inch, bottomMargin=0.58 * inch,
        title="Sprint 1 Market Research",
        author="College Dining Meal Plan Initiative",
        subject="Meal-plan preferences, availability interviews, and project scope",
    )
    story = [
        paragraph("SPRINT 1 / MARKET RESEARCH", styles["eyebrow"]),
        paragraph("The research moved from meal plans to availability.", styles["title"]),
        paragraph(
            "We first heard different preferences about campus meal-plan formats. Later, "
            "focused interviews recorded what people found when dining information did "
            "not match the food or service available on arrival.",
            styles["lead"],
        ),
        make_stats_table(styles, document.width),
        Spacer(1, 17),
        paragraph("01 / EARLIER MEAL-PLAN FINDINGS", styles["eyebrow"]),
        paragraph("Flexibility and structure both mattered", styles["section"]),
    ]
    story.extend(paragraph(text, styles["body"]) for text in MEAL_PLAN_PARAGRAPHS)
    story.extend([
        Spacer(1, 5),
        paragraph("02 / FOCUSED AVAILABILITY INTERVIEWS", styles["eyebrow"]),
        paragraph("What people found on arrival", styles["section"]),
        make_availability_stat(styles, document.width),
        Spacer(1, 8),
        paragraph(AVAILABILITY_INTRO, styles["body"]),
        make_example_table(styles, document.width),
        PageBreak(),
        paragraph(OTHER_EXAMPLES, styles["small"]),
        Spacer(1, 12),
        paragraph("FROM INTERVIEW EVIDENCE TO SCOPE", styles["eyebrow"]),
        paragraph("Five candidate needs", styles["section"]),
        make_candidate_table(styles, document.width),
        Spacer(1, 17),
    ])

    decision_box = Table([
        [paragraph("RESEARCH-LED SCOPING DECISION", styles["decision_eyebrow"])],
        [paragraph("Real-Time Campus Dining Availability System", styles["decision_title"])],
        [paragraph(DECISION_TEXT, styles["decision_body"])],
    ], colWidths=[document.width])
    decision_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([
        KeepTogether(decision_box),
        Spacer(1, 13),
        paragraph("WHAT THESE INTERVIEWS CAN SHOW", styles["eyebrow"]),
        paragraph(EVIDENCE_LIMIT, styles["body"]),
        paragraph("SOURCE PACKET AND PAGE RANGES", styles["eyebrow"]),
        paragraph(SOURCE_NOTE, styles["small"]),
    ])

    document.build(story, onFirstPage=draw_page_frame, onLaterPages=draw_page_frame)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
