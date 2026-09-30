# -*- coding: utf-8 -*-
"""One-shot setup: install dependencies, create folders. Safe to re-run.
Usage: python setup.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEPS = ['python-docx', 'pymupdf']

for d in ['input', 'work', 'work/extract', 'work/drafts', 'work/reviews', 'output']:
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

missing = []
for mod, pkg in [('docx', 'python-docx'), ('fitz', 'pymupdf')]:
    try:
        __import__(mod)
    except ImportError:
        missing.append(pkg)

if missing:
    print('installing:', ' '.join(missing))
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', *missing])
    if r.returncode != 0:
        print('pip failed. Run manually:  pip install ' + ' '.join(missing))
        sys.exit(1)

n = sum(len(f) for _, _, f in os.walk(os.path.join(ROOT, 'input')))
prof = os.path.exists(os.path.join(ROOT, 'profile.md'))
print(f'ok | input files: {n} | profile.md: {"yes" if prof else "not yet (will be created by /resume)"}')
if sys.platform != 'win32':
    print('note: PDF export uses Microsoft Word on Windows; on other systems install LibreOffice (soffice).')
