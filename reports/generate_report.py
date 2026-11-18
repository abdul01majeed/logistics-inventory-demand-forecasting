
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
import os

# ------------------------------------
# 1. CREATE DOCUMENT
# ------------------------------------

doc = Document()

section = doc.sections[0]
section.top_margin = Inches(0.8)
section.bottom_margin = Inches(0.8)
section.left_margin = Inches(1)
section.right_margin = Inches(1)

# ------------------------------------
# 2. DOCUMENT STYLES
# ------------------------------------

styles = doc.styles

normal = styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.paragraph_format.line_spacing = 1.5

for style_name, size in [
    ("Heading 1", 16),
    ("Heading 2", 13),
    ("Heading 3", 12)
]:
    style = styles[style_name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor(31, 78, 121)

# ------------------------------------
# 3. HEADER AND FOOTER
# ------------------------------------

header = section.header.paragraphs[0]
header.text = "LOGISTICS DATA ANALYTICS | STRATEGIC PLANNING"
header.alignment = WD_ALIGN_PARAGRAPH.CENTER

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER

footer.add_run("Page ")

field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer._p.append(field)

# ------------------------------------
# 4. TITLE PAGE
# ------------------------------------

for _ in range(3):
    doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("STRATEGIC PLANNING AND\nDATA EXPLORATION IN LOGISTICS")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run(
    "\nDATA-DRIVEN INVENTORY MANAGEMENT\n"
    "AND DEMAND FORECASTING USING PYTHON"
)
r.bold = True
r.font.size = Pt(17)

doc.add_paragraph("\n\n")

for line in [
    "WEEK 1 ASSIGNMENT REPORT",
    "",
    "Submitted by: [Your Full Name]",
    "Internship: Logistics Data Analytics",
    "Institution: [Institution Name]",
    "Submission Date: [DD/MM/YYYY]",
    "GitHub Repository: [Insert GitHub URL]"
]:
    p = doc.add_paragraph(line)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ------------------------------------
# 5. AUTOMATIC TABLE OF CONTENTS
# ------------------------------------

doc.add_heading("TABLE OF CONTENTS", level=1)

p = doc.add_paragraph()

fldChar1 = OxmlElement("w:fldChar")
fldChar1.set(qn("w:fldCharType"), "begin")

instrText = OxmlElement("w:instrText")
instrText.set(qn("xml:space"), "preserve")
instrText.text = 'TOC \\o "1-3" \\h \\z \\u'

fldChar2 = OxmlElement("w:fldChar")
fldChar2.set(qn("w:fldCharType"), "separate")

placeholder = OxmlElement("w:t")
placeholder.text = "Open in Microsoft Word and update the entire table."

fldChar3 = OxmlElement("w:fldChar")
fldChar3.set(qn("w:fldCharType"), "end")

p._p.append(fldChar1)
p._p.append(instrText)
p._p.append(fldChar2)
p._p.append(placeholder)
p._p.append(fldChar3)

doc.add_page_break()

# ------------------------------------
# 6. HELPER FUNCTIONS
# ------------------------------------

def heading(text, level=1):
    doc.add_heading(text, level=level)

def paragraph(text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, value in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = value

        shading = OxmlElement("w:shd")
        shading.set(qn("w:fill"), "D9EAF7")
        cell._tc.get_or_add_tcPr().append(shading)

        for run in cell.paragraphs[0].runs:
            run.bold = True

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    doc.add_paragraph("")

def code_block(code):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_after = Pt(6)

    run = p.add_run(code)
    run.font.name = "Consolas"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(40, 40, 40)

# ------------------------------------
# 7. REPORT CONTENT
# ------------------------------------

heading("1. EXECUTIVE SUMMARY")

paragraph(
    "This project proposes a data-driven inventory management and "
    "demand forecasting framework for a retail distribution business. "
    "It investigates how historical retail transaction data and Python "
    "data science techniques can improve inventory planning, purchasing "
    "decisions, and resource allocation."
)

paragraph(
    "The project uses the publicly available UCI Online Retail II dataset. "
    "Python libraries including Pandas, NumPy, Matplotlib, Seaborn, and "
    "Scikit-learn will support data cleaning, exploratory analysis, "
    "predictive modeling, and product segmentation."
)

paragraph(
    "The expected outcome is a practical framework for identifying "
    "demand patterns, forecasting product requirements, and supporting "
    "more informed inventory decisions."
)

heading("2. INTRODUCTION AND BACKGROUND RESEARCH")

heading("2.1 Background of the Project", 2)

paragraph(
    "Logistics management involves planning, implementing, and controlling "
    "the movement and storage of goods and related information. Inventory "
    "management is essential because excessive inventory increases storage "
    "costs, while insufficient inventory can cause stock shortages and "
    "delayed order fulfillment."
)

heading("2.2 Logistics Scenario", 2)

paragraph(
    "The proposed scenario involves a medium-sized online retail "
    "distribution company managing hundreds of consumer products through "
    "a central warehouse. The company experiences unpredictable demand, "
    "excess inventory, product shortages, and inefficient purchasing "
    "decisions."
)

heading("2.3 Problem Statement", 2)

paragraph(
    "The organization lacks a reliable analytical framework for predicting "
    "product demand and determining suitable inventory levels. This project "
    "investigates how Python-based analytics and machine learning can "
    "support improved inventory planning."
)

heading("2.4 Literature and Data Research", 2)

paragraph(
    "The primary dataset is Online Retail II from the UCI Machine Learning "
    "Repository. It contains historical retail transactions, including "
    "product codes, quantities, invoice dates, prices, and customer details."
)

paragraph(
    "Additional technical resources include Pandas documentation, "
    "Scikit-learn documentation, and Google OR-Tools documentation."
)

paragraph(
    "Dataset: https://archive.ics.uci.edu/dataset/502/online+retail+ii"
)

heading("3. PROJECT OBJECTIVES")

heading("3.1 Main Objective", 2)

paragraph(
    "To develop a data-driven strategic framework for improving inventory "
    "management and demand forecasting using Python and data science."
)

heading("3.2 Specific Objectives", 2)

for item in [
    "Collect and examine historical retail transaction data.",
    "Identify demand patterns across different products.",
    "Clean and prepare datasets using Python.",
    "Develop predictive models to estimate future demand.",
    "Segment products according to sales characteristics.",
    "Investigate inventory replenishment strategies.",
    "Evaluate the potential impact on logistics performance."
]:
    doc.add_paragraph(item, style="List Bullet")

heading("4. KEY PERFORMANCE INDICATORS")

add_table(
    ["KPI", "Formula / Measurement", "Desired Direction"],
    [
        ["Forecast Error (WAPE)",
         "Absolute forecast error / Total actual demand × 100",
         "Lower"],
        ["Inventory Turnover",
         "Cost of Goods Sold / Average Inventory Value",
         "Appropriate improvement"],
        ["Stockout Rate",
         "Stockout events / Total availability opportunities × 100",
         "Lower"],
        ["Order Fulfillment Rate",
         "Orders fulfilled completely / Total orders × 100",
         "Higher"],
        ["Inventory Holding Cost",
         "Average inventory value × Holding cost rate",
         "Lower"]
    ]
)

paragraph(
    "These KPIs provide a framework for evaluating forecasting performance, "
    "inventory efficiency, product availability, and service quality."
)

heading("5. APPLICATION OF DATA SCIENCE TECHNIQUES")

heading("5.1 Exploratory Data Analysis", 2)

paragraph(
    "Exploratory Data Analysis will identify missing values, duplicates, "
    "sales trends, top-selling products, and demand variability using "
    "Pandas, Matplotlib, and Seaborn."
)

heading("5.2 Regression and Demand Forecasting", 2)

paragraph(
    "Regression models, including Random Forest Regression, will estimate "
    "future demand using historical quantities, lag variables, rolling "
    "averages, and calendar features."
)

heading("5.3 Clustering Analysis", 2)

paragraph(
    "K-Means clustering will group products according to demand, revenue, "
    "and transaction characteristics. The intended groups are high, "
    "medium, and low demand."
)

heading("5.4 Inventory Optimization", 2)

paragraph(
    "Forecasting results can be combined with supplier lead times, "
    "inventory balances, and ordering costs to estimate reorder points "
    "and economic order quantities."
)

heading("6. STRATEGIC ROADMAP AND METHODOLOGY")

add_table(
    ["Stage", "Activity", "Tools", "Deliverable"],
    [
        ["1", "Data collection", "UCI Repository", "Raw dataset"],
        ["2", "Data cleaning", "Pandas, NumPy", "Clean dataset"],
        ["3", "Exploratory analysis", "Matplotlib, Seaborn", "Charts and insights"],
        ["4", "Feature engineering", "Pandas", "Model-ready data"],
        ["5", "Predictive modeling", "Scikit-learn", "Demand predictions"],
        ["6", "Product clustering", "K-Means", "Product segments"],
        ["7", "Inventory planning", "Statistical methods", "Replenishment proposals"],
        ["8", "Reporting", "Python, Word", "Final report"]
    ]
)

heading("7. PYTHON IMPLEMENTATION AND CODE ILLUSTRATIONS")

heading("7.1 Importing Libraries", 2)

code_block(
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "from sklearn.ensemble import RandomForestRegressor\n"
    "from sklearn.cluster import KMeans"
)

heading("7.2 Loading and Cleaning Data", 2)

code_block(
    'df = pd.read_excel("data/online_retail_II.xlsx")\n'
    'df = df.drop_duplicates()\n'
    'df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])\n'
    'df = df.dropna(subset=["StockCode", "InvoiceDate"])'
)

heading("7.3 Demand Forecasting", 2)

code_block(
    'model = RandomForestRegressor(\n'
    '    n_estimators=100,\n'
    '    random_state=42\n'
    ')\n'
    'model.fit(X_train, y_train)\n'
    'predictions = model.predict(X_test)'
)

heading("7.4 Product Clustering", 2)

code_block(
    'kmeans = KMeans(\n'
    '    n_clusters=3,\n'
    '    random_state=42,\n'
    '    n_init=10\n'
    ')\n'
    'product_clusters = kmeans.fit_predict(scaled_data)'
)

heading("8. EXPECTED PROJECT OUTCOMES")

add_table(
    ["Business Area", "Expected Improvement"],
    [
        ["Procurement", "Better demand-based purchasing decisions"],
        ["Inventory", "Reduced risk of stock shortages"],
        ["Warehousing", "Improved product space allocation"],
        ["Finance", "Better inventory cost control"],
        ["Customer service", "Improved product availability"]
    ]
)

paragraph(
    "These outcomes are proposed benefits and must be validated through "
    "actual operational data and model evaluation."
)

heading("9. PROJECT IMPLEMENTATION TIMELINE")

add_table(
    ["Week", "Activity", "Deliverable"],
    [
        ["1", "Research and strategic planning", "Project proposal"],
        ["2", "Data collection", "Raw dataset"],
        ["3", "Data cleaning", "Clean dataset"],
        ["4", "Exploratory analysis", "Visualizations"],
        ["5", "Predictive modeling", "Forecasting model"],
        ["6", "Model evaluation and clustering", "Evaluation results"],
        ["7", "Inventory optimization", "Recommendations"],
        ["8", "Documentation", "Final report"]
    ]
)

heading("10. PROJECT RISKS AND LIMITATIONS")

for item in [
    "Missing or inconsistent transaction records.",
    "Historical demand may not represent future demand.",
    "The dataset does not contain actual inventory balances.",
    "Supplier lead times and stockout records are unavailable.",
    "Forecasting models may produce inaccurate predictions.",
    "Business operating calendars must be validated before interpreting zero-sales days."
]:
    doc.add_paragraph(item, style="List Bullet")

heading("11. RECOMMENDATIONS")

for item in [
    "Adopt data-driven inventory planning.",
    "Monitor inventory performance using relevant KPIs.",
    "Use product segmentation to support warehouse allocation.",
    "Integrate supplier lead-time information.",
    "Maintain accurate inventory and transaction records.",
    "Regularly evaluate and update forecasting models."
]:
    doc.add_paragraph(item, style="List Number")

heading("12. CONCLUSION")

paragraph(
    "This project demonstrates how Python-based data analytics and "
    "machine learning can support more effective logistics and inventory "
    "management. Through exploratory analysis, demand forecasting, "
    "product clustering, and inventory planning, the proposed framework "
    "can help organizations make better-informed purchasing and resource "
    "allocation decisions."
)

paragraph(
    "The long-term objective is to integrate predictive analytics into "
    "inventory management processes and continuously evaluate operational "
    "performance using reliable business data."
)

heading("13. REFERENCES")

references = [
    "UCI Machine Learning Repository. Online Retail II Dataset. "
    "https://archive.ics.uci.edu/dataset/502/online+retail+ii",
    "Pandas Development Team. Pandas Documentation. https://pandas.pydata.org/docs/",
    "Scikit-learn Developers. Scikit-learn Documentation. https://scikit-learn.org/stable/",
    "Google OR-Tools. Optimization Documentation. https://developers.google.com/optimization",
    "Python Software Foundation. Python Documentation. https://docs.python.org/3/"
]

for ref in references:
    doc.add_paragraph(ref, style="List Number")

# ------------------------------------
# 8. SAVE REPORT
# ------------------------------------

os.makedirs("reports", exist_ok=True)

output = (
    "reports/Strategic_Planning_Logistics_Final.docx"
)

doc.save(output)

print("Professional report generated successfully!")
print("Saved to:", output)
