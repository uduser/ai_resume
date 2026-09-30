# -*- coding: utf-8 -*-
"""Style gate for a Traditional-Chinese resume in Markdown.

Usage: python check_style.py <resume.md> [--max-cjk 1450] [--max-lead 4]

Reports (exit code 1 if any HARD failure):
  HARD  half-width punctuation glued to CJK text
  HARD  HTML comments left in the file (internal notes must not ship)
  HARD  CJK character count above --max-cjk
  SOFT  banned / mainland-China / AI-flavoured words
  SOFT  "主導" used more than --max-lead times
  SOFT  bullets that do not start with a verb-ish token (heuristic)
"""
import re
import sys

BANNED = [
    '優化', '落地', '痛點', '打造', '賦能', '深耕', '致力', '聚焦', '凸顯', '彰顯', '體現',
    '里程碑', '此外', '值得注意', '顯著', '全面', '綜上', '不可或缺', '蓬勃', '日新月異',
    '占比', '校驗', '彈窗', '佈署', '用戶', '數據驅動', '視頻', '服務器', '軟件', '硬件',
    '信息', '質量', '默認', '網絡', '數據庫', '調試', '運行', '高效', '閉環', '抓手', '賽道',
    '不只是', '不僅僅', '而是一種', '——', '—',
]
NON_VERB_START = ('負責', '協助', '參與', '相關', '具備', '擁有', '關於')


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    max_cjk = int(sys.argv[sys.argv.index('--max-cjk') + 1]) if '--max-cjk' in sys.argv else 1450
    max_lead = int(sys.argv[sys.argv.index('--max-lead') + 1]) if '--max-lead' in sys.argv else 4
    s = open(path, encoding='utf-8').read()
    hard = 0

    cjk = len(re.findall(r'[一-鿿]', s))
    en = len(re.findall(r'[A-Za-z0-9][A-Za-z0-9.\-/:%+]*', s))
    print(f'CJK chars: {cjk}   EN/num tokens: {en}   total chars: {len(s)}')
    if cjk > max_cjk:
        print(f'HARD  CJK count {cjk} > {max_cjk}')
        hard += 1

    n = s.count('<!--')
    if n:
        print(f'HARD  {n} HTML comment block(s) present')
        hard += 1

    for m in re.finditer(r'[一-鿿][,.;:!?()"]|[,.;:!?()"][一-鿿]', s):
        print('HARD  half-width punctuation near CJK:', repr(s[max(0, m.start() - 10):m.end() + 10]))
        hard += 1

    for w in BANNED:
        c = s.count(w)
        if c:
            print(f'SOFT  banned word "{w}" x{c}')

    lead = s.count('主導')
    if lead > max_lead:
        print(f'SOFT  「主導」 x{lead} (> {max_lead})')

    for line in s.splitlines():
        if line.lstrip().startswith(('- ', '* ')):
            body = re.sub(r'^\s*[-*]\s+(\*\*[^*]+\*\*[：:]?\s*)?', '', line)
            if body.startswith(NON_VERB_START):
                print('SOFT  bullet starts with a duty word:', body[:30])

    print('RESULT:', 'FAIL' if hard else 'PASS')
    sys.exit(1 if hard else 0)


if __name__ == '__main__':
    main()
