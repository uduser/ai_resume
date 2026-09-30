# -*- coding: utf-8 -*-
"""Extract plain text from every source file under an input folder.

Supported: .pptx (slides + notes + tables), .docx (paragraphs + tables), .pdf (PyMuPDF),
.html, .md, .txt, .csv. Output: one UTF-8 .txt per source under the output folder,
named by the relative path with "/" replaced by "__", plus an index.md listing sizes.

Usage:
    python extract.py <input_dir> <output_dir> [--png]

--png also renders each PDF page to PNG (110 dpi) so a vision-capable agent can read
layout-heavy documents such as an old resume.

Dependencies: python-docx is NOT required (docx/pptx are parsed as raw XML);
PyMuPDF (pip install pymupdf) is needed only for .pdf.
"""
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def pptx_text(path):
    z = zipfile.ZipFile(path)
    slides = [n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
    slides.sort(key=lambda n: int(re.search(r'slide(\d+)', n).group(1)))
    out = []
    for n in slides:
        root = ET.fromstring(z.read(n))
        out.append(f"\n===== {os.path.basename(n)} =====")
        for tbl in root.iter('{%s}tbl' % NS['a']):
            for tr in tbl.findall('a:tr', NS):
                cells = []
                for tc in tr.findall('a:tc', NS):
                    cells.append(' '.join(''.join(t.text or '' for t in p.findall('.//a:t', NS))
                                          for p in tc.findall('.//a:p', NS)).strip())
                out.append(' | '.join(cells))
        for sp in root.iter('{%s}sp' % NS['p']):
            for p in sp.findall('.//a:p', NS):
                txt = ''.join(t.text or '' for t in p.findall('.//a:t', NS)).strip()
                if txt:
                    out.append(txt)
        notes = n.replace('slides/slide', 'notesSlides/notesSlide')
        if notes in z.namelist():
            nr = ET.fromstring(z.read(notes))
            ntxt = [''.join(t.text or '' for t in p.findall('.//a:t', NS)).strip() for p in nr.findall('.//a:p', NS)]
            ntxt = [t for t in ntxt if t and not t.isdigit()]
            if ntxt:
                out.append('[NOTES] ' + ' / '.join(ntxt))
    return '\n'.join(out)


def docx_text(path):
    z = zipfile.ZipFile(path)
    root = ET.fromstring(z.read('word/document.xml'))
    body = root.find('w:body', NS)
    out = []

    def ptext(p):
        return ''.join(t.text or '' for t in p.iter('{%s}t' % NS['w'])).strip()

    for child in body:
        tag = child.tag.split('}')[1]
        if tag == 'p':
            t = ptext(child)
            if t:
                out.append(t)
        elif tag == 'tbl':
            for tr in child.iter('{%s}tr' % NS['w']):
                cells = [' / '.join(ptext(p) for p in tc.findall('.//w:p', NS) if ptext(p))
                         for tc in tr.findall('w:tc', NS)]
                out.append(' | '.join(cells))
            out.append('')
    return '\n'.join(out)


def pdf_text(path, png_dir=None, stem=''):
    import fitz  # PyMuPDF
    doc = fitz.open(path)
    out = []
    for i, page in enumerate(doc):
        out.append(f"\n===== page {i + 1} =====")
        out.append(page.get_text())
        if png_dir:
            page.get_pixmap(dpi=110).save(os.path.join(png_dir, f'{stem}_p{i + 1}.png'))
    if not ''.join(out).strip().replace('=', '').replace('page', ''):
        out.append('[WARN] no extractable text; PDF may be scanned or DRM-protected')
    return '\n'.join(out)


def html_text(path):
    raw = open(path, encoding='utf-8', errors='ignore').read()
    raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', raw, flags=re.S | re.I)
    txt = re.sub(r'<[^>]+>', '\n', raw)
    return re.sub(r'\n\s*\n+', '\n', txt)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    png = '--png' in sys.argv
    os.makedirs(dst, exist_ok=True)
    rows = []
    for dirpath, _, files in os.walk(src):
        for f in sorted(files):
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, src)
            ext = f.lower().rsplit('.', 1)[-1] if '.' in f else ''
            stem = rel.replace(os.sep, '__').replace('/', '__')
            try:
                if ext == 'pptx':
                    txt = pptx_text(full)
                elif ext == 'docx':
                    txt = docx_text(full)
                elif ext == 'pdf':
                    txt = pdf_text(full, dst if png else None, stem)
                elif ext in ('html', 'htm'):
                    txt = html_text(full)
                elif ext in ('md', 'txt', 'csv'):
                    txt = open(full, encoding='utf-8', errors='ignore').read()
                else:
                    rows.append((rel, 'SKIPPED', 0))
                    continue
            except Exception as e:  # DRM, corrupt file, missing dependency
                txt = f'ERROR {type(e).__name__}: {e}'
            outp = os.path.join(dst, stem + '.txt')
            open(outp, 'w', encoding='utf-8').write(txt)
            status = 'ERROR' if txt.startswith('ERROR') else ('WARN' if '[WARN]' in txt else 'OK')
            rows.append((rel, status, len(txt)))
            print(f'{status:7} {len(txt):>7} chars  {rel}')
    with open(os.path.join(dst, 'index.md'), 'w', encoding='utf-8') as idx:
        idx.write('| source | status | chars |\n|---|---|---|\n')
        for rel, st, n in rows:
            idx.write(f'| {rel} | {st} | {n} |\n')
    print(f'\n{len(rows)} files -> {dst}/index.md')


if __name__ == '__main__':
    main()
