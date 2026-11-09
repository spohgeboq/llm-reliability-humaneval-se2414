import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def build_docx(markdown_path: str, output_docx_path: str):
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    with open(markdown_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if not table_lines:
            in_table = False
            return

        rows_data = []
        for tl in table_lines:
            if '\t' in tl:
                cols = [c.strip() for c in tl.split('\t')]
            else:
                cols = [c.strip() for c in tl.split('|') if c.strip()]
            if cols:
                rows_data.append(cols)

        if rows_data:
            num_cols = max(len(r) for r in rows_data)
            norm_rows = [r + [''] * (num_cols - len(r)) for r in rows_data]
            table = doc.add_table(rows=len(norm_rows), cols=num_cols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER

            for r_idx, row in enumerate(norm_rows):
                for c_idx, val in enumerate(row):
                    cell = table.cell(r_idx, c_idx)
                    cell.text = val
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.line_spacing = 1.0

                    if r_idx == 0:
                        set_cell_background(cell, "2C3E50")
                        for run in p.runs:
                            run.font.bold = True
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                            run.font.size = Pt(9.5)
                    else:
                        if r_idx % 2 == 1:
                            set_cell_background(cell, "F8F9FA")
                        for run in p.runs:
                            run.font.size = Pt(9)

            doc.add_paragraph()

        table_lines = []
        in_table = False

    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\r\n')

        if '\t' in line:
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        stripped = line.strip()

        if i == 0 or stripped.startswith("Assignment 4"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run("Assignment #4: Experiment Execution, Results and Discussion\n")
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)

            p_sub = doc.add_paragraph()
            p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_sub = p_sub.add_run("The Limits of LLM Reliability: Evaluating Functional Correctness and Explanatory Accuracy in Algorithmic Problem-Solving\n")
            r_sub.font.size = Pt(13)
            r_sub.font.bold = True
            r_sub.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

            p_meta = doc.add_paragraph()
            p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_meta = p_meta.add_run("Authors: Ibragim Nurkassym, Orken Zhilkibek, Zhandos Tenglesbayev  |  Group: SE-2414  |  Date: November 8, 2026\n")
            r_meta.font.size = Pt(10)
            r_meta.font.italic = True
            r_meta.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
            i += 1
            continue

        if any(stripped.startswith(k) for k in ["Research Title:", "Team Members:", "Group:", "Date:"]):
            i += 1
            continue

        if re.match(r"^\d+\.\s+[A-Za-z]", stripped) or stripped.startswith("Appendix"):
            h = doc.add_heading(level=1)
            run = h.add_run(stripped)
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
            i += 1
            continue

        if re.match(r"^\d+\.\d+\s+[A-Za-z]", stripped):
            h = doc.add_heading(level=2)
            run = h.add_run(stripped)
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
            i += 1
            continue

        if stripped.endswith(":") and len(stripped) < 60 and not stripped.startswith("●") and not stripped.startswith("○"):
            p = doc.add_paragraph()
            run = p.add_run(stripped)
            run.font.bold = True
            run.font.size = Pt(11)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            i += 1
            continue

        if stripped.startswith("●") or stripped.startswith("•") or stripped.startswith("○") or stripped.startswith("* "):
            clean_text = re.sub(r"^[●•○\*\s]+", "", stripped)
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            if ":" in clean_text and len(clean_text.split(":", 1)[0]) < 35:
                label, rest = clean_text.split(":", 1)
                r_lbl = p.add_run(label + ":")
                r_lbl.font.bold = True
                p.add_run(rest)
            else:
                p.add_run(clean_text)
            i += 1
            continue

        if stripped:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            p.add_run(stripped)

            if "Figure 1 (fig1_model_comparison.png" in stripped:
                fig1_path = "results/figures/fig1_model_comparison.png"
                if os.path.exists(fig1_path):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(8)
                    p_img.paragraph_format.space_after = Pt(4)
                    doc.add_picture(fig1_path, width=Inches(6.2))

            elif "Figure 2 (fig2_latency_vs_correctness.png" in stripped:
                fig2_path = "results/figures/fig2_latency_vs_correctness.png"
                if os.path.exists(fig2_path):
                    p_img = doc.add_paragraph()
                    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_img.paragraph_format.space_before = Pt(8)
                    p_img.paragraph_format.space_after = Pt(4)
                    doc.add_picture(fig2_path, width=Inches(5.8))

        i += 1

    if in_table:
        flush_table()

    doc.save(output_docx_path)
    print(f"Successfully exported submission document: {output_docx_path}")


if __name__ == "__main__":
    md_in = "result.md"
    docx_out = "Assignment4_Nurkassym_Zhilkibek_Tenglesbayev.docx"
    build_docx(md_in, docx_out)
