"""
analysis/reports.py
Generates monthly executive summaries, financial performance reports,
and professional PDF export capabilities for CanteenWise.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from utils.csv_handler import CSVHandler
from analysis.profit_analysis import ProfitAnalyzer

# Import ReportLab for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ReportGenerator:
    def __init__(self, data_dir="data"):
        if not os.path.isabs(data_dir):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            data_dir = os.path.join(base_dir, data_dir)
        self.data_dir = data_dir
        self.sales_handler = CSVHandler(os.path.join(data_dir, "sales.csv"), id_column=None)
        self.waste_handler = CSVHandler(os.path.join(data_dir, "waste.csv"), id_column=None)
        self.purchases_handler = CSVHandler(os.path.join(data_dir, "purchases.csv"), id_column=None)
        self.profit_analyzer = ProfitAnalyzer(data_dir)

    def generate_monthly_summary(self) -> pd.DataFrame:
        """
        Aggregates sales revenue, purchase expenses, and waste costs by month
        to generate a comprehensive financial executive report.
        """
        sales_df = self.sales_handler.load()
        waste_df = self.waste_handler.load()
        purchases_df = self.purchases_handler.load()

        # 1. Ensure date columns are formatted as datetime
        sales_df["date"] = pd.to_datetime(sales_df["date"])
        waste_df["date"] = pd.to_datetime(waste_df["date"])
        purchases_df["date"] = pd.to_datetime(purchases_df["date"])

        # Extract Year-Month (e.g., '2026-01')
        sales_df["month"] = sales_df["date"].dt.to_period("M")
        waste_df["month"] = waste_df["date"].dt.to_period("M")
        purchases_df["month"] = purchases_df["date"].dt.to_period("M")

        # 2. Monthly Revenue Calculation
        sales_df["revenue"] = sales_df["quantity_sold"] * sales_df["selling_price"]
        monthly_revenue = sales_df.groupby("month")["revenue"].sum().reset_index()

        # 3. Monthly Purchasing Expenses Calculation
        monthly_purchases = purchases_df.groupby("month")["total_cost"].sum().reset_index().rename(columns={"total_cost": "total_purchases"})

        # 4. Monthly Waste Cost Calculation
        monthly_waste = waste_df.groupby("month")["waste_cost"].sum().reset_index().rename(columns={"waste_cost": "total_waste_cost"})

        # 5. Merge all metrics into a single monthly report DataFrame
        report_df = monthly_revenue.merge(monthly_purchases, on="month", how="outer")
        report_df = report_df.merge(monthly_waste, on="month", how="outer").fillna(0.0)

        # Calculate Net Operating Cashflow / Profit estimate per month
        report_df["net_performance"] = report_df["revenue"] - (report_df["total_purchases"] + report_df["total_waste_cost"])
        
        # Convert Period back to string for clean presentation
        report_df["month"] = report_df["month"].astype(str)
        report_df = report_df.sort_values(by="month").reset_index(drop=True)

        return report_df

    def export_monthly_summary_pdf(self, output_pdf_path: str = "CanteenWise_Executive_Report.pdf") -> str:
        """
        Generates the monthly summary dataframe and exports it as a clean,
        professional executive PDF document.
        """
        report_df = self.generate_monthly_summary()

        # Setup document geometry
        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=letter,
            rightMargin=40, leftMargin=40,
            topMargin=40, bottomMargin=40
        )
        
        story = []
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=15
        )

        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2B6CB0"),
            spaceBefore=10,
            spaceAfter=8
        )

        cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#2D3748")
        )

        header_cell_style = ParagraphStyle(
            'TableHeaderCell',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=colors.white,
            fontName="Helvetica-Bold"
        )

        # Header Title block
        story.append(Paragraph("CanteenWise Executive Financial Report", title_style))
        story.append(Paragraph("Monthly Performance Summary: Revenue, Procurement, Waste, and Net Margins", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=15))

        story.append(Paragraph("Monthly Financial Breakdown", section_heading))

        # Build Table Data
        table_data = [[
            Paragraph("<b>Month</b>", header_cell_style),
            Paragraph("<b>Revenue (Rs.)</b>", header_cell_style),
            Paragraph("<b>Purchases (Rs.)</b>", header_cell_style),
            Paragraph("<b>Waste Cost (Rs.)</b>", header_cell_style),
            Paragraph("<b>Net Profit (Rs.)</b>", header_cell_style)
        ]]

        for _, row in report_df.iterrows():
            table_data.append([
                Paragraph(str(row["month"]), cell_style),
                Paragraph(f"{row['revenue']:,.2f}", cell_style),
                Paragraph(f"{row['total_purchases']:,.2f}", cell_style),
                Paragraph(f"{row['total_waste_cost']:,.2f}", cell_style),
                Paragraph(f"{row['net_performance']:,.2f}", cell_style)
            ])

        # Create Table and apply professional styling
        summary_table = Table(table_data, colWidths=[90, 105, 105, 105, 105])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ]))

        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Add footer or explanatory note
        note_style = ParagraphStyle('NoteStyle', parent=styles['Italic'], fontSize=8, textColor=colors.HexColor("#718096"))
        story.append(Paragraph("Note: Net Profit is computed as Gross Revenue minus total purchase expenses and recorded waste costs.", note_style))

        # Build PDF
        doc.build(story)
        return output_pdf_path

if __name__ == "__main__":
    generator = ReportGenerator()
    pdf_file = generator.export_monthly_summary_pdf()
    print(f"--- Monthly Executive PDF Report generated successfully: {pdf_file} ---")