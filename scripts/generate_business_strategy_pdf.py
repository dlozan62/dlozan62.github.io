"""Generate the public Sprint 1 Business Strategy PDF.

The PDF is a printable companion to the page in
``sprints/sprint-1/business-strategy.html``. Keep the wording and source
references aligned when either document changes.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "pdfs" / "sprint-1-business-strategy.pdf"

NAVY = colors.HexColor("#041e42")
ORANGE = colors.HexColor("#ff8200")
INK = colors.HexColor("#101b2b")
MUTED = colors.HexColor("#556272")
MIST = colors.HexColor("#eef2f5")
LINE = colors.HexColor("#cbd2d8")


def make_styles():
    """Return the small set of paragraph styles used throughout the PDF."""
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="Kicker",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=11,
            textColor=ORANGE,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DocumentTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=31,
            alignment=TA_LEFT,
            textColor=NAVY,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=NAVY,
            spaceBefore=13,
            spaceAfter=7,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subheading",
            parent=styles["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=4,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCopy",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.2,
            textColor=INK,
            spaceAfter=7,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallCopy",
            parent=styles["BodyCopy"],
            fontSize=8,
            leading=11,
            textColor=MUTED,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardHeading",
            parent=styles["Subheading"],
            fontSize=11,
            leading=14,
            spaceBefore=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardCopy",
            parent=styles["BodyCopy"],
            fontSize=8.6,
            leading=12,
            spaceAfter=0,
        )
    )
    styles.add(
        ParagraphStyle(
            name="StatNumber",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=30,
            textColor=NAVY,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="StatLabel",
            parent=styles["BodyCopy"],
            fontSize=8,
            leading=10,
            textColor=MUTED,
            spaceAfter=0,
        )
    )
    return styles


def add_page_details(canvas, document):
    """Draw a simple running title and page number on every page."""
    canvas.saveState()
    page_width, page_height = letter
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(document.leftMargin, page_height - 0.42 * inch, "TEAM 10 / PROJECT STRATEGY")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.7)
    canvas.line(document.leftMargin, 0.55 * inch, page_width - document.rightMargin, 0.55 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(document.leftMargin, 0.36 * inch, "Campus Dining Availability System")
    canvas.drawRightString(page_width - document.rightMargin, 0.36 * inch, f"Page {document.page}")
    canvas.restoreState()


def paragraph(text, style):
    """Create a ReportLab paragraph from simple, source-grounded copy."""
    return Paragraph(text, style)


def section_heading(label, title, styles):
    """Return the small orange label and title used for a document section."""
    return [paragraph(label, styles["Kicker"]), paragraph(title, styles["SectionHeading"])]


def bullet_list(items, styles, numbered=False):
    """Format a plain list with hanging indents and consistent spacing."""
    prefix = "1." if numbered else "-"
    rows = []
    for index, item in enumerate(items, start=1):
        marker = f"{index}." if numbered else prefix
        rows.append(
            Table(
                [[Paragraph(marker, styles["BodyCopy"]), Paragraph(item, styles["BodyCopy"])]],
                colWidths=[0.28 * inch, 6.55 * inch],
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                        ("TEXTCOLOR", (0, 0), (0, 0), ORANGE),
                    ]
                ),
            )
        )
    return rows


def value_cards(styles):
    """Lay out the three groups with a possible, still unproven value."""
    cards = [
        (
            "For students",
            "The outcomes to examine are time, detours, meal substitutions, and unplanned spending.",
        ),
        (
            "For dining teams",
            "The project will explore whether an approved source could report and verify changes without excessive work. The interviews do not show that staff will adopt a reporting process or that it will reduce workload.",
        ),
        (
            "For the university",
            "Requirements and prototype tests can surface ownership, access, security, and integration questions before a pilot is considered. No savings, revenue, or meal-plan participation benefit has been established.",
        ),
    ]
    cells = []
    for heading, copy in cards:
        cells.append(
            [
                paragraph(heading, styles["CardHeading"]),
                Spacer(1, 5),
                paragraph(copy, styles["CardCopy"]),
            ]
        )
    table = Table([cells], colWidths=[2.23 * inch] * 3, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MIST),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def evidence_cards(styles):
    """Show interview counts while keeping the research groups distinct."""
    values = [
        ("12", "focused availability interviews used for the current direction"),
        ("13", "meal-plan preference responses kept separate from this project"),
        ("5", "candidate ideas compared before the team narrowed its scope"),
    ]
    cells = [
        [paragraph(number, styles["StatNumber"]), paragraph(label, styles["StatLabel"])]
        for number, label in values
    ]
    table = Table([cells], colWidths=[2.23 * inch] * 3, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def build_story(styles):
    """Build the document in the same order as the public strategy page."""
    story = [
        paragraph("SPRINT 1 / BUSINESS STRATEGY", styles["Kicker"]),
        paragraph("A trustworthy status before the walk", styles["DocumentTitle"]),
        paragraph(
            "This strategy explains what value the current Campus Dining Availability System will test, what the interview evidence can support, and what the team still needs to learn. It does not make a launch decision or estimate financial returns.",
            styles["BodyCopy"],
        ),
        Spacer(1, 5),
        *section_heading(
            "The current direction",
            "Help students choose where to eat with current information",
            styles,
        ),
        paragraph(
            "The team will find out whether current information about dining items, stations, and services can help students avoid wasted trips, delays, substitutions, and unexpected spending when choosing where to eat on campus.",
            styles["BodyCopy"],
        ),
        paragraph("Where the project stands", styles["Subheading"]),
        paragraph(
            "Team 10 compared five candidate ideas and selected a system for sharing current dining-item, station, kitchen, counter, and temporary-service status before students walk to a location. The current project stage is validation through prototype evaluation.",
            styles["BodyCopy"],
        ),
        paragraph(
            "The earlier flexible meal-plan idea is superseded. It is project history, not the current business objective. The 13 meal-plan preference responses in the Phase 2 packet answer a separate question; they do not validate the availability system.",
            styles["BodyCopy"],
        ),
        *section_heading(
            "User problem",
            "People sometimes learn about a change after they arrive",
            styles,
        ),
        paragraph(
            "A student may check a menu or posted hours, walk to a dining location, and then find that an item, station, kitchen service, counter, or required option is unavailable. When earlier information does not show the change, the student may lose time, switch meals, remain hungry, or spend more than planned.",
            styles["BodyCopy"],
        ),
    ]

    story.extend(
        bullet_list(
            [
                "One participant found a cafe open after its kitchen had closed, then spent about <b>$18</b> on delivery and waited roughly <b>40 minutes</b>.",
                "An empty grab-and-go case led one participant to take a <b>25-minute</b> walk across campus for pizza.",
                "After ribs were sold out, one participant spent about <b>$6 extra</b> on a snack and waited until after class for a full meal.",
            ],
            styles,
        )
    )
    story.extend(
        [
            paragraph(
                "The focused interviews also describe sold-out soup, missing sandwiches, unavailable oat milk, cleared stations, and equipment or service changes. Some posted hours and menus matched what participants found. The project therefore focuses on changes that regular menu and hours pages may not show; it is not intended to replace information that already works.",
                styles["BodyCopy"],
            ),
            paragraph(
                "Each example describes one participant's experience. These figures are not average costs or expected savings.",
                styles["SmallCopy"],
            ),
            KeepTogether(
                [
                    *section_heading(
                        "Value hypothesis",
                        "Useful information depends on trust and a workable update process",
                        styles,
                    ),
                    paragraph(
                        "If students can see an item's or service's status, location, and update time before leaving, they may avoid an unnecessary trip or choose another option earlier. This is a hypothesis, not a measured outcome.",
                        styles["BodyCopy"],
                    ),
                    value_cards(styles),
                ]
            ),
            Spacer(1, 10),
            KeepTogether(
                [
                    *section_heading(
                        "What the evidence can support",
                        "Early signals, not a forecast",
                        styles,
                    ),
                    evidence_cards(styles),
                ]
            ),
            Spacer(1, 7),
            paragraph(
                "These are small qualitative samples. The examples help describe specific experiences and possible user impact; they do not measure how common the problem is across the student population. The packet does not establish expected usage, adoption, operating cost, revenue, savings, or return on investment.",
                styles["BodyCopy"],
            ),
            *section_heading(
                "Business and operating assumptions",
                "What must be true for this idea to help",
                styles,
            ),
        ]
    )

    assumptions = [
        "Students will check availability before walking to a dining location. The team will test this through interviews and prototype tasks.",
        "A small set of labels will be clear enough to support a decision. The prototype will test Available, Low Stock, Sold Out, Closed, and Service Outage.",
        "Status changes can be updated often enough to remain useful. The team still needs to set a freshness expectation and define stale information.",
        "An approved source can report and verify changes without excessive staff work. This needs review with an operational stakeholder.",
        "Students in different situations experience this problem. The next interviews should include varied student groups, schedules, and dining locations.",
        "The system can show uncertainty honestly. The prototype will make the last-updated time and stale or unverified state visible.",
    ]
    story.extend(bullet_list(assumptions, styles))

    # Keep the validation heading with its complete numbered list when it
    # approaches a page boundary, so a later page never starts at item 4.
    validation_steps = bullet_list(
        [
            "Conduct 13 more focused availability interviews, bringing the project's interview target to 25. Include different student groups and dining locations, and look for examples that do not support the problem.",
            "Rank which status changes matter, define how fresh updates need to be, and identify who could report and verify each type of change.",
            "Build a prototype that shows a location, availability status, status details, and when information was last updated. Include a clear stale or unverified state.",
            "Test the main availability-checking task with at least five participants. The charter target is for at least four to complete the task without help.",
            "Review a realistic update owner, workflow, and data source with relevant stakeholders before recommending a pilot proposal.",
        ],
        styles,
        numbered=True,
    )
    story.append(
        KeepTogether(
            [
                *section_heading("Next validation", "Test usefulness before considering a pilot", styles),
                *validation_steps,
            ]
        )
    )
    story.extend(
        [
            paragraph(
                "The value measure is still open: the charter asks whether value should be measured through time saved, cost avoided, or fewer disrupted meals. Team 10 will decide after reviewing the evidence. This page does not make a continue, pause, or pilot decision.",
                styles["BodyCopy"],
            ),
            paragraph(
                "The current phase covers research, requirements, and prototype evaluation. It does not include a production launch, live university or vendor integrations, or a promise of perfectly current information. A pilot would be a later proposal requiring a credible operating path and stakeholder review.",
                styles["BodyCopy"],
            ),
            *section_heading("Source notes", "Read the evidence and current scope", styles),
            paragraph(
                '<link href="https://dlozan62.github.io/sprints/sprint-1/market-research/">Sprint 1 Market Research page</link> summarizes the research groups and the team\'s pivot.',
                styles["BodyCopy"],
            ),
            paragraph(
                '<link href="https://dlozan62.github.io/assets/pdfs/campus-dining-phase-2-final.pdf#page=3">Campus Dining Hall Research PDF</link>: candidate ideas on pages 1-2; focused availability interviews on pages 3-14; separate meal-plan preference responses on pages 16-22 and 24-29.',
                styles["BodyCopy"],
            ),
            paragraph(
                '<link href="https://dlozan62.github.io/sprints/sprint-1/project-charter/">Current Project Charter page</link> and the <link href="https://dlozan62.github.io/assets/pdfs/campus-dining-availability-system-project-charter.pdf">authoritative six-page charter PDF</link> define the active objective, scope, assumptions, and validation targets.',
                styles["BodyCopy"],
            ),
            paragraph(
                '<link href="https://dlozan62.github.io/assets/pdfs/sprint-1-project-document.pdf">Superseded Sprint 1 project document</link> records the earlier flexible meal-plan proposal. It is historical context, not the current project plan.',
                styles["BodyCopy"],
            ),
            paragraph(
                "The interview packet and charter are the sources for the examples, counts, assumptions, and project targets in this document. The value statements are hypotheses for the team to test.",
                styles["SmallCopy"],
            ),
        ]
    )
    return story


def main():
    """Write the PDF beside the other public project documents."""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, page_height = letter
    left = right = 0.8 * inch
    top = 0.72 * inch
    bottom = 0.78 * inch
    frame = Frame(
        left,
        bottom,
        page_width - left - right,
        page_height - top - bottom,
        id="content",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    document = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=left,
        rightMargin=right,
        topMargin=top,
        bottomMargin=bottom,
        title="Sprint 1 Business Strategy - Campus Dining Availability System",
        author="Team 10",
    )
    document.addPageTemplates([PageTemplate(id="strategy", frames=[frame], onPage=add_page_details)])
    document.build(build_story(make_styles()))
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
