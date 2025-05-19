from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def generate_pdf_report(data, startup_name="Startup"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceBefore=10,
        spaceAfter=6
    )

    elements = []

    # Title
    elements.append(Paragraph("Investment Thesis Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary
    summary = f"""
    <b>Investment Recommendation:</b> {data['recommendation']}<br/>
    <b>Overall Score:</b> {data['overall_score']}<br/>
    <b>Confidence Score:</b> {data['confidence_score']}<br/>
    <b>Processing Date:</b> {data['processing_date']}
    """
    elements.append(Paragraph("Summary", heading_style))
    elements.append(Paragraph(summary, body_style))

    # Category Analysis Table
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Category-wise Analysis", heading_style))

    table_data = [["Category", "Score", "Weight (%)", "Feedback"]]
    for cat in data["categories"]:
        table_data.append([
            cat["name"],
            str(cat["score"]),
            str(cat["weight"]),
            Paragraph(cat["feedback"], body_style)
        ])

    table = Table(table_data, colWidths=[60*mm, 20*mm, 25*mm, 70*mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("WORDWRAP", (0, 0), (-1, -1), True),
    ]))
    elements.append(table)

    # Strengths
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Strengths", heading_style))
    for item in data["strengths"]:
        elements.append(Paragraph(f"• {item}", body_style))

    # Weaknesses
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Weaknesses", heading_style))
    for item in data["weaknesses"]:
        elements.append(Paragraph(f"• {item}", body_style))

    # Recommendations
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Recommendations", heading_style))
    elements.append(Paragraph(data["recommendations"], body_style))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)

    date_str = datetime.utcnow().strftime("%d%m%Y")
    filename = f"Investment_Thesis_{startup_name}_{date_str}.pdf"
    return buffer, filename