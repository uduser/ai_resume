# -*- coding: utf-8 -*-
"""Minimal Markdown -> DOCX converter tuned for a resume.
Supports: # / ## / ###, bullets (- or *), bold **x**, tables (| a | b |), --- rules, plain paragraphs.
Usage: python md2docx.py input.md output.docx
"""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT_ZH = 'Microsoft JhengHei'
FONT_EN = 'Calibri'

def set_font(run, size=None, bold=None, color=None, font_zh=FONT_ZH, font_en=FONT_EN):
    run.font.name = font_en
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = OxmlElement('w:rFonts'); rpr.append(rfonts)
    rfonts.set(qn('w:eastAsia'), font_zh)
    rfonts.set(qn('w:ascii'), font_en)
    rfonts.set(qn('w:hAnsi'), font_en)
    if size: run.font.size = Pt(size)
    if bold is not None: run.font.bold = bold
    if color: run.font.color.rgb = RGBColor.from_string(color)

def add_runs(p, text, size=9.5, color=None):
    # split by **bold**
    parts = re.split(r'(\*\*[^*]+\*\*)', text)
    for part in parts:
        if not part: continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2]); set_font(r, size=size, bold=True, color=color)
        else:
            r = p.add_run(part); set_font(r, size=size, color=color)

def para_spacing(p, before=0, after=2, line=1.03):
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line

def add_bottom_border(p, color='888888', sz='6'):
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), sz)
    bottom.set(qn('w:space'), '1'); bottom.set(qn('w:color'), color)
    pbdr.append(bottom); pPr.append(pbdr)

def convert(md_path, out_path):
    lines = open(md_path, encoding='utf-8').read().splitlines()
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(1.3); sec.bottom_margin = Cm(1.2)
    sec.left_margin = Cm(1.5); sec.right_margin = Cm(1.5)
    style = doc.styles['Normal']
    style.font.name = FONT_EN; style.font.size = Pt(9.5)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), FONT_ZH)

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        if line.startswith('<!--'):
            i += 1; continue
        if re.match(r'^-{3,}$', line.strip()):
            p = doc.add_paragraph(); para_spacing(p, 0, 2); add_bottom_border(p, 'BBBBBB', '4')
            i += 1; continue
        m = re.match(r'^(#{1,3})\s+(.*)$', line)
        if m:
            level = len(m.group(1)); text = m.group(2).strip()
            p = doc.add_paragraph()
            if level == 1:
                add_runs(p, text, size=19, color='1F3864'); para_spacing(p, 0, 1)
                for r in p.runs: r.font.bold = True
            elif level == 2:
                add_runs(p, text, size=12, color='1F3864'); para_spacing(p, 5, 2)
                for r in p.runs: r.font.bold = True
                add_bottom_border(p, '1F3864', '6')
            else:
                add_runs(p, text, size=10.5); para_spacing(p, 4, 1)
                for r in p.runs: r.font.bold = True
            i += 1; continue
        if line.strip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = lines[i].strip().strip('|')
                cells = [c.strip() for c in row.split('|')]
                if not all(re.match(r'^:?-{2,}:?$', c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                ncol = max(len(r) for r in rows)
                t = doc.add_table(rows=len(rows), cols=ncol)
                t.style = 'Table Grid'
                for ri, row in enumerate(rows):
                    for ci in range(ncol):
                        cell = t.cell(ri, ci)
                        cell.text = ''
                        p = cell.paragraphs[0]
                        add_runs(p, row[ci] if ci < len(row) else '', size=9.5)
                        para_spacing(p, 1, 1, 1.0)
                        if ri == 0:
                            for r in p.runs: r.font.bold = True
                doc.add_paragraph().paragraph_format.space_after = Pt(2)
            continue
        m = re.match(r'^(\s*)[-*]\s+(.*)$', line)
        if m:
            indent = len(m.group(1)) // 2
            p = doc.add_paragraph(style='List Bullet' if indent == 0 else 'List Bullet 2')
            add_runs(p, m.group(2)); para_spacing(p, 0, 1)
            i += 1; continue
        m = re.match(r'^\d+\.\s+(.*)$', line)
        if m:
            p = doc.add_paragraph(style='List Number')
            add_runs(p, m.group(1)); para_spacing(p, 0, 2)
            i += 1; continue
        # paragraph: merge consecutive lines
        buf = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3}\s|[-*]\s|\d+\.\s|\||-{3,}|<!--)', lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        p = doc.add_paragraph()
        add_runs(p, ' '.join(buf)); para_spacing(p, 0, 4)
    doc.save(out_path)
    print('saved', out_path)

if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
