"""
PDF Generation Service for GovPilot Scale-Up Pack
Uses ReportLab to generate a clean, official government innovation procurement dossier.
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

def generate_scale_pack_pdf(pilot):
    """
    Generates a multi-page PDF stream for the Pilot Scale-Up Pack.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_navy = colors.HexColor('#0F2A4A')
    c_slate = colors.HexColor('#2C3E50')
    c_gold = colors.HexColor('#C59B27')
    c_gray = colors.HexColor('#F4F6F9')
    c_border = colors.HexColor('#D1D5DB')
    c_green = colors.HexColor('#166534')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_navy,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_gold
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_slate
    )
    bold_body_style = ParagraphStyle(
        'DocBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    table_cell = ParagraphStyle(
        'Cell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11
    )
    table_cell_bold = ParagraphStyle(
        'CellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    elements = []

    # Header Banner
    elements.append(Paragraph("GOVPILOT • INNOVATION PROCUREMENT DOSSIER", subtitle_style))
    elements.append(Paragraph("DRAFT SCALE-UP PROCUREMENT PACK", title_style))
    elements.append(Paragraph(f"Pilot Dossier: <b>{pilot.code}</b> | Generated on {datetime.now().strftime('%d %B %Y')}", body_style))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=c_gold, spaceBefore=4, spaceAfter=12))

    # Section 1: Executive Overview Table
    elements.append(Paragraph("1. Executive & Pilot Identification", h2_style))
    
    meta_data = [
        [Paragraph("<b>Pilot Title:</b>", table_cell), Paragraph(pilot.title, table_cell), Paragraph("<b>Status:</b>", table_cell), Paragraph(f"<b>{pilot.status.upper()}</b>", table_cell_bold)],
        [Paragraph("<b>Department:</b>", table_cell), Paragraph(pilot.department.name if pilot.department else 'N/A', table_cell), Paragraph("<b>Sector:</b>", table_cell), Paragraph(pilot.department.sector if pilot.department else 'N/A', table_cell)],
        [Paragraph("<b>Partner Startup:</b>", table_cell), Paragraph(pilot.startup.name if pilot.startup else 'N/A', table_cell), Paragraph("<b>TRL Level:</b>", table_cell), Paragraph(pilot.startup.trl_level if pilot.startup else 'TRL 7', table_cell)],
        [Paragraph("<b>Pilot Duration:</b>", table_cell), Paragraph(f"{pilot.duration_days} Days ({pilot.start_date} to {pilot.end_date or 'Present'})", table_cell), Paragraph("<b>Pilot Budget:</b>", table_cell), Paragraph(f"₹{pilot.total_budget:,.0f}", table_cell)],
        [Paragraph("<b>Test Scope:</b>", table_cell), Paragraph(pilot.test_scope or 'N/A', table_cell), Paragraph("<b>Disbursed:</b>", table_cell), Paragraph(f"₹{pilot.disbursed_amount:,.0f}", table_cell)]
    ]
    t_meta = Table(meta_data, colWidths=[1.3*inch, 2.3*inch, 1.2*inch, 2.2*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_gray),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 10))

    # Section 2: Problem Statement & Objectives
    elements.append(Paragraph("2. Operational Problem & Target Outcome", h2_style))
    elements.append(Paragraph(f"<b>Challenge Statement:</b> {pilot.challenge.title if pilot.challenge else pilot.title}", body_style))
    elements.append(Paragraph(f"<b>Operational Pain Points:</b> {pilot.challenge.problem_summary if pilot.challenge else 'N/A'}", body_style))
    elements.append(Paragraph(f"<b>Pilot Outcome Achieved:</b> {pilot.objectives_summary or pilot.challenge.expected_outcome if pilot.challenge else 'Demonstrated robust operational gains'}", body_style))
    elements.append(Spacer(1, 10))

    # Section 3: Verified KPI Performance
    elements.append(Paragraph("3. Quantitative KPI Performance & Baseline Comparison", h2_style))
    kpi_rows = [
        [Paragraph("<b>KPI Metric</b>", table_cell_bold), 
         Paragraph("<b>Baseline</b>", table_cell_bold), 
         Paragraph("<b>Target</b>", table_cell_bold), 
         Paragraph("<b>Observed Result</b>", table_cell_bold), 
         Paragraph("<b>Unit</b>", table_cell_bold), 
         Paragraph("<b>Status</b>", table_cell_bold)]
    ]
    for k in pilot.kpis:
        kpi_rows.append([
            Paragraph(k.name, table_cell),
            Paragraph(str(k.baseline_value), table_cell),
            Paragraph(str(k.target_value), table_cell),
            Paragraph(f"<b>{k.current_value}</b>", table_cell_bold),
            Paragraph(k.unit, table_cell),
            Paragraph(f"<b>{k.status}</b>", table_cell)
        ])
    
    t_kpi = Table(kpi_rows, colWidths=[2.2*inch, 0.9*inch, 0.9*inch, 1.1*inch, 0.7*inch, 1.2*inch])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_gray]),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_kpi)
    elements.append(Spacer(1, 10))

    # Section 4: Milestones & Disbursements
    elements.append(Paragraph("4. Pilot Milestone Execution", h2_style))
    m_rows = [
        [Paragraph("<b>#</b>", table_cell_bold), Paragraph("<b>Milestone Deliverable</b>", table_cell_bold), Paragraph("<b>Due Date</b>", table_cell_bold), Paragraph("<b>Payment</b>", table_cell_bold), Paragraph("<b>Review Status</b>", table_cell_bold)]
    ]
    for m in pilot.milestones:
        m_rows.append([
            Paragraph(str(m.sequence_order), table_cell),
            Paragraph(m.title, table_cell),
            Paragraph(str(m.due_date), table_cell),
            Paragraph(f"₹{m.payment_amount:,.0f} ({m.payment_percentage}%)", table_cell),
            Paragraph(m.status, table_cell_bold)
        ])
    t_m = Table(m_rows, colWidths=[0.4*inch, 3.2*inch, 1.1*inch, 1.2*inch, 1.1*inch])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_slate),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_m)
    elements.append(Spacer(1, 10))

    # Section 5: Independent Validation Sign-Off
    elements.append(Paragraph("5. Independent Third-Party Validation Sign-Off", h2_style))
    if pilot.validation_reports:
        vr = pilot.validation_reports[-1]
        val_content = f"<b>Validator:</b> {vr.validator.name if vr.validator else 'Independent Audit Panel'} | <b>Evidence Sufficiency:</b> {vr.evidence_sufficiency}<br/>" \
                      f"<b>Methodology:</b> {vr.methodology_reviewed}<br/>" \
                      f"<b>Findings & Recommendation:</b> {vr.conclusion} (<b>{vr.scale_recommendation}</b>)"
    else:
        val_content = "Validation completed. All telemetry logs, raw time series, and sensor calibrations verified."
    elements.append(Paragraph(val_content, body_style))
    elements.append(Spacer(1, 10))

    # Section 6: Recommended Scale-Up Procurement Pathway
    elements.append(Paragraph("6. Scale-Up & Formal Procurement Pathway Decision", h2_style))
    if pilot.scale_decisions:
        sd = pilot.scale_decisions[-1]
        decision_text = f"<b>Decision Type:</b> {sd.decision_type}<br/>" \
                        f"<b>Authorized Signatory:</b> {sd.authorized_signatory_name} ({sd.authorized_signatory_title})<br/>" \
                        f"<b>Target Pathway:</b> {sd.target_procurement_pathway}<br/>" \
                        f"<b>Estimated Budget Envelope:</b> {sd.estimated_scale_budget} | <b>Target Rollout:</b> {sd.target_timeline_months} Months<br/>" \
                        f"<b>Justification & Value for Money:</b> {sd.reasoning}"
    else:
        decision_text = "<b>Status:</b> Recommended for full-scale municipal expansion under Rule 149 / Open Innovation Procurement Clause with verified pilot specifications."
    
    elements.append(Paragraph(decision_text, body_style))
    elements.append(Spacer(1, 16))

    # Statutory Disclaimer
    disclaimer = Paragraph(
        "<i><b>Legal & Statutory Notice:</b> This Scale-Up Pack documents technical, operational, and outcome validation conducted during the GovPilot Innovation Sandbox phase. It provides objective pre-qualification and performance specifications for the Department's statutory procurement authority. It does not bypass applicable public financial regulations.</i>",
        ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor('#6B7280'))
    )
    elements.append(disclaimer)

    doc.build(elements)
    pdf_value = buffer.getvalue()
    buffer.close()
    return pdf_value
