"""
Générateur de rapport PDF officiel pour le Data Challenge Burkina (Défi 2).
Convertit la documentation en un PDF structuré et professionnel.
"""

import os
from fpdf import FPDF

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(DOCS_DIR, "RAPPORT_OFFICIEL_DEFI2.md")
PDF_PATH = os.path.join(DOCS_DIR, "RAPPORT_OFFICIEL_DEFI2.pdf")

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"
FONT_ITALIC_PATH = "C:/Windows/Fonts/ariali.ttf"


class OfficialReportPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_x(self.l_margin)
            self.set_font("ArialCustom", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(self.epw / 2, 8, "FocusEduc - Data Challenge Burkina 2026 (Défi 2)", align="L")
            self.cell(self.epw / 2, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(200, 200, 200)
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_x(self.l_margin)
        self.set_font("ArialCustom", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(self.epw, 8, "Solution d'Aide à la Décision Éducative - Évaluation à l'aveugle", align="C")


def build_pdf():
    pdf = OfficialReportPDF(orientation="P", unit="mm", format="A4")
    
    # Polices système
    pdf.add_font("ArialCustom", fname=FONT_PATH)
    pdf.add_font("ArialCustom", style="B", fname=FONT_BOLD_PATH)
    pdf.add_font("ArialCustom", style="I", fname=FONT_ITALIC_PATH)

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Couverture
    pdf.set_font("ArialCustom", "B", 24)
    pdf.set_text_color(46, 125, 50)
    pdf.ln(35)
    pdf.multi_cell(pdf.epw, 12, "FocusEduc", align="C")
    
    pdf.set_font("ArialCustom", "B", 13)
    pdf.set_text_color(50, 50, 50)
    pdf.ln(6)
    pdf.multi_cell(pdf.epw, 8, "Plateforme Intelligente pour Mesurer et Réduire les Inégalités d'Accès à l'Éducation au Burkina Faso", align="C")

    pdf.set_font("ArialCustom", "I", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.ln(8)
    pdf.multi_cell(pdf.epw, 6, "Data Challenge Burkina 2026 - Édition Éducation\n21e Semaine du Numérique", align="C")

    pdf.ln(25)
    pdf.set_draw_color(46, 125, 50)
    pdf.set_line_width(0.8)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())
    pdf.ln(20)

    pdf.set_font("ArialCustom", "B", 11)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(pdf.epw, 7, "Dossier de Documentation Technique et Décisionnelle\nDéfi 2 : Parité fille-garçon et fracture urbain-rural\nÉvaluation à l'aveugle (Anonymat certifié)", align="C")

    pdf.add_page()

    # Corps du texte
    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    pdf.set_text_color(20, 20, 20)

    for line in lines:
        raw = line.strip()
        if not raw:
            pdf.ln(2)
            continue
        
        if raw.startswith("# FocusEduc") or raw.startswith("> **Data Challenge") or raw.startswith("> **Défi 2") or raw.startswith("*Dossier"):
            continue

        pdf.set_x(pdf.l_margin)

        if raw.startswith("## "):
            pdf.ln(4)
            pdf.set_font("ArialCustom", "B", 13)
            pdf.set_text_color(46, 125, 50)
            clean_title = raw.replace("## ", "").replace("*", "")
            pdf.multi_cell(pdf.epw, 7, clean_title)
            pdf.set_text_color(20, 20, 20)
            pdf.ln(1)
        elif raw.startswith("### "):
            pdf.ln(2)
            pdf.set_font("ArialCustom", "B", 10.5)
            pdf.set_text_color(60, 60, 60)
            clean_subtitle = raw.replace("### ", "").replace("*", "")
            pdf.multi_cell(pdf.epw, 6, clean_subtitle)
            pdf.set_text_color(20, 20, 20)
            pdf.ln(1)
        elif raw.startswith("* ") or raw.startswith("- "):
            pdf.set_font("ArialCustom", "", 9.5)
            bullet_text = "  • " + raw[2:].replace("**", "").replace("`", "")
            pdf.multi_cell(pdf.epw, 5, bullet_text)
        elif raw.startswith("1. ") or raw.startswith("2. ") or raw.startswith("3. "):
            pdf.set_font("ArialCustom", "", 9.5)
            num_text = "  " + raw[:3] + " " + raw[3:].replace("**", "").replace("`", "")
            pdf.multi_cell(pdf.epw, 5, num_text)
        elif raw.startswith("> "):
            pdf.set_font("ArialCustom", "I", 9.5)
            pdf.set_text_color(60, 60, 60)
            quote_text = raw.replace("> ", "").replace("**", "")
            pdf.multi_cell(pdf.epw, 5, quote_text)
            pdf.set_text_color(20, 20, 20)
        elif raw.startswith("```"):
            continue
        else:
            pdf.set_font("ArialCustom", "", 9.5)
            clean_p = raw.replace("**", "").replace("`", "")
            pdf.multi_cell(pdf.epw, 5, clean_p)

    pdf.output(PDF_PATH)
    print(f"-> Rapport PDF généré avec succès : {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
