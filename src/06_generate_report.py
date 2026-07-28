"""
06_generate_report.py
Genera un reporte PDF automatico con los KPIs principales de rotacion de personal.
Uso: python src/06_generate_report.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- Rutas: relativas a la carpeta del proyecto 
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "HR-Employee-Attrition-clean.csv"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

fecha_hoy = datetime.now().strftime("%Y-%m-%d")
pdf_path = REPORTS_DIR / f"reporte_rotacion_{fecha_hoy}.pdf"
chart1_path = REPORTS_DIR / "_tmp_chart_depto.png"
chart2_path = REPORTS_DIR / "_tmp_chart_overtime.png"

# --- 1. Cargar datos ---
df = pd.read_csv(DATA_PATH)

# --- 2. Calcular los mismos KPIs 
total_empleados = len(df)
total_renuncias = (df["Attrition"] == "Yes").sum()
tasa_rotacion = total_renuncias / total_empleados
ingreso_promedio = df["MonthlyIncome"].mean()

# --- 3. Grafico: rotacion por departamento ---
rot_depto = df.groupby("Department")["Attrition"].apply(lambda x: (x == "Yes").mean()).sort_values(ascending=False)
plt.figure(figsize=(6, 4))
rot_depto.plot(kind="bar", color="#1f77b4")
plt.title("Tasa de Rotacion por Departamento")
plt.ylabel("Tasa de Rotacion")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(chart1_path, dpi=150)
plt.close()

# --- 4. Grafico: rotacion segun overtime ---
rot_overtime = df.groupby("OverTime")["Attrition"].apply(lambda x: (x == "Yes").mean())
plt.figure(figsize=(6, 4))
rot_overtime.plot(kind="bar", color="#ff7f0e")
plt.title("Tasa de Rotacion segun Horas Extra")
plt.ylabel("Tasa de Rotacion")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(chart2_path, dpi=150)
plt.close()

# --- 5. Armar el PDF con ReportLab
styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleCustom", parent=styles["Title"], fontSize=20)
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=11, textColor=colors.grey)

doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
elements = []

elements.append(Paragraph("Reporte de Rotacion de Personal", title_style))
elements.append(Paragraph(f"Generado automaticamente el {fecha_hoy}", subtitle_style))
elements.append(Spacer(1, 20))

kpi_data = [
    ["Total Empleados", f"{total_empleados:,}"],
    ["Total Renuncias", f"{total_renuncias:,}"],
    ["Tasa de Rotacion", f"{tasa_rotacion:.1%}"],
    ["Ingreso Mensual Promedio", f"${ingreso_promedio:,.0f}"],
]
tabla = Table(kpi_data, colWidths=[250, 150])
tabla.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("FONTSIZE", (0, 0), (-1, -1), 11),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
]))
elements.append(tabla)
elements.append(Spacer(1, 25))

elements.append(Paragraph("Rotacion por Departamento", styles["Heading2"]))
elements.append(Image(str(chart1_path), width=5*inch, height=3.3*inch))
elements.append(Spacer(1, 15))

elements.append(Paragraph("Rotacion segun Horas Extra", styles["Heading2"]))
elements.append(Image(str(chart2_path), width=5*inch, height=3.3*inch))

doc.build(elements)

# --- 6. Borrar las imagenes temporales, ya quedaron incrustadas en el PDF ---
chart1_path.unlink()
chart2_path.unlink()

print(f"Reporte generado: {pdf_path}")