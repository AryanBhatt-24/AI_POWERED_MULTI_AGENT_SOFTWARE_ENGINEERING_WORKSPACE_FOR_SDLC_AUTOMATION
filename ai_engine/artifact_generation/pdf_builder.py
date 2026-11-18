from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    ListFlowable,
    ListItem,
    HRFlowable
)


def build_pdf(
    title: str,
    sections: list[dict],
    output_path: str
) -> str:

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=55,
        leftMargin=55,
        topMargin=60,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="DocumentTitle",
        parent=styles["Title"],
        fontSize=22,
        alignment=TA_CENTER,
        spaceAfter=25
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=15,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=16,
        spaceAfter=10
    ))

    story = []

    story.append(Paragraph(title, styles["DocumentTitle"]))
    story.append(HRFlowable(width="100%", color=colors.grey))
    story.append(Spacer(1, 20))

    for section in sections:

        heading = section.get("heading", "")
        content = section.get("content", "")
        diagram_path = section.get("diagram_path")

        if heading:
            story.append(
                Paragraph(heading, styles["SectionHeading"])
            )

        if isinstance(content, list):

            items = [
                ListItem(
                    Paragraph(str(item), styles["BodyText"])
                )
                for item in content
            ]

            story.append(
                ListFlowable(items, bulletType="bullet")
            )

        elif content:
            story.append(
                Paragraph(str(content), styles["BodyText"])
            )

        if diagram_path:
            image_path = Path(diagram_path)

            if image_path.exists():
                diagram = Image(str(image_path))
                diagram._restrictSize(
                    6.2 * inch,
                    4.5 * inch
                )
                story.append(Spacer(1, 10))
                story.append(diagram)

        story.append(Spacer(1, 12))

    document.build(story)

    return str(output_file)
