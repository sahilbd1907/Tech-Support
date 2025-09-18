from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
import tempfile
from datetime import datetime
from typing import Dict

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.temp_dir = 'temp_pdfs'
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Company information
        self.company_name = "Precision CNC Solutions"
        self.company_address = "123 Industrial Way, Manufacturing District"
        self.company_city = "Tech City, TC 12345"
        self.company_phone = "(555) 123-4567"
        self.company_email = "info@precisioncnc.com"
        self.company_website = "www.precisioncnc.com"
    
    def generate_quotation(self, geometry_data: Dict, material: str, thickness: float, 
                          machining_time: float, total_cost: float) -> str:
        """
        Generate a professional PDF quotation
        
        Args:
            geometry_data: CAD geometry information
            material: Material type
            thickness: Material thickness
            machining_time: Estimated machining time
            total_cost: Total cost
        """
        # Create temporary PDF file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quotation_{timestamp}.pdf"
        filepath = os.path.join(self.temp_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Build PDF content
        story = []
        
        # Header
        story.extend(self._create_header())
        story.append(Spacer(1, 20))
        
        # Quotation details
        story.extend(self._create_quotation_details(geometry_data, material, thickness))
        story.append(Spacer(1, 20))
        
        # Cost breakdown
        story.extend(self._create_cost_breakdown(geometry_data, material, thickness, 
                                               machining_time, total_cost))
        story.append(Spacer(1, 20))
        
        # Terms and conditions
        story.extend(self._create_terms_conditions())
        
        # Build PDF
        doc.build(story)
        
        return filename
    
    def _create_header(self):
        """Create company header section"""
        elements = []
        
        # Company name
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=TA_CENTER,
            spaceAfter=12
        )
        elements.append(Paragraph(self.company_name, title_style))
        
        # Company details
        details_style = ParagraphStyle(
            'CompanyDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=6
        )
        
        elements.append(Paragraph(self.company_address, details_style))
        elements.append(Paragraph(self.company_city, details_style))
        elements.append(Paragraph(f"Phone: {self.company_phone}", details_style))
        elements.append(Paragraph(f"Email: {self.company_email}", details_style))
        elements.append(Paragraph(f"Web: {self.company_website}", details_style))
        
        # Quotation title
        elements.append(Spacer(1, 20))
        quote_title_style = ParagraphStyle(
            'QuoteTitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.darkred,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        elements.append(Paragraph("CNC MACHINING QUOTATION", quote_title_style))
        
        return elements
    
    def _create_quotation_details(self, geometry_data: Dict, material: str, thickness: float):
        """Create quotation details section"""
        elements = []
        
        # Section title
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        elements.append(Paragraph("Project Details", section_style))
        
        # Project information table
        project_data = [
            ['Date:', datetime.now().strftime("%B %d, %Y")],
            ['Material:', material.capitalize()],
            ['Thickness:', f"{thickness} mm"],
            ['Total Cutting Length:', f"{geometry_data['total_length']:.2f} mm"],
            ['Line Entities:', str(geometry_data['line_count'])],
            ['Arc Entities:', str(geometry_data['arc_count'])],
            ['Circle Entities:', str(geometry_data['circle_count'])],
            ['Polyline Entities:', str(geometry_data['polyline_count'])]
        ]
        
        project_table = Table(project_data, colWidths=[2*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(project_table)
        
        return elements
    
    def _create_cost_breakdown(self, geometry_data: Dict, material: str, thickness: float,
                              machining_time: float, total_cost: float):
        """Create cost breakdown section"""
        elements = []
        
        # Section title
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        elements.append(Paragraph("Cost Breakdown", section_style))
        
        # Calculate individual costs
        from cost_calculator import CostCalculator
        calc = CostCalculator()
        material_cost = calc.calculate_material_cost(geometry_data['total_length'], thickness, material)
        labor_cost = calc.calculate_labor_cost(machining_time, material)
        
        # Cost breakdown table
        cost_data = [
            ['Item', 'Details', 'Amount'],
            ['Material Cost', f"{material.capitalize()} ({thickness}mm)", f"${material_cost:.2f}"],
            ['Labor Cost', f"{machining_time:.1f} minutes @ ${calc.machine_rates.get(material.lower(), 40.0):.2f}/hour", f"${labor_cost:.2f}"],
            ['Setup & Tooling', 'Standard setup and tool change', '$5.00'],
            ['', '', ''],
            ['TOTAL', '', f"${total_cost:.2f}"]
        ]
        
        cost_table = Table(cost_data, colWidths=[1.5*inch, 2.5*inch, 1*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -2), (-1, -2), colors.lightgrey),
            ('FONTNAME', (0, -2), (-1, -2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -2), (-1, -2), 12)
        ]))
        
        elements.append(cost_table)
        
        # Additional information
        elements.append(Spacer(1, 12))
        info_style = ParagraphStyle(
            'InfoText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_LEFT
        )
        
        elements.append(Paragraph(f"Estimated Machining Time: {machining_time:.1f} minutes", info_style))
        elements.append(Paragraph(f"Feed Rate: {calc.feed_rates.get(material.lower(), 300)} mm/min", info_style))
        elements.append(Paragraph(f"Quote Valid For: 30 days", info_style))
        
        return elements
    
    def _create_terms_conditions(self):
        """Create terms and conditions section"""
        elements = []
        
        # Section title
        section_style = ParagraphStyle(
            'SectionTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=12
        )
        elements.append(Paragraph("Terms & Conditions", section_style))
        
        # Terms text
        terms_style = ParagraphStyle(
            'TermsText',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            alignment=TA_LEFT,
            spaceAfter=6
        )
        
        terms = [
            "• Payment terms: Net 30 days from invoice date",
            "• Lead time: 2-3 weeks from order confirmation",
            "• Minimum order quantity: 1 piece",
            "• Material availability subject to stock",
            "• Tolerances: ±0.1mm unless specified otherwise",
            "• Surface finish: As machined (Ra 3.2)",
            "• This quote is valid for 30 days from date of issue"
        ]
        
        for term in terms:
            elements.append(Paragraph(term, terms_style))
        
        return elements
