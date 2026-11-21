"""Assign sensible column widths to every table in a pandoc HTML file.

Rules
- A column whose longest cell is short (<= SHORT chars) gets just enough width for that text.
- The remaining width is shared by the other columns:
  * equally, when their average text lengths are similar (parallel columns such as 包含 / 不包含)
  * otherwise in proportion to their average length, clamped so no column is starved or bloated.
- table-layout: fixed so the browser follows the widths exactly.
"""
import sys, re, math
from bs4 import BeautifulSoup

LINE = 46.0   # CJK chars that fit across the text width at table font size
SHORT = 9

def vlen(s):
    s = re.sub(r'\s+', '', s)
    n = 0.0
    for ch in s:
        n += 1.0 if ord(ch) > 0x2E80 else 0.55
    return n

def fix(path):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    for t in soup.find_all('table'):
        for cg in t.find_all('colgroup'):
            cg.decompose()
        rows = [r.find_all(['td', 'th']) for r in t.find_all('tr')]
        n = max(len(r) for r in rows)
        cols = [[] for _ in range(n)]
        for r in rows:
            for i, c in enumerate(r[:n]):
                # longest single line inside the cell (respect <br>)
                cc = BeautifulSoup(str(c), 'html.parser')
                for br in cc.find_all('br'): br.replace_with('\n')
                parts = [vlen(p) for p in cc.get_text('').split('\n')] or [0]
                cols[i].append((max(parts), vlen(c.get_text())))
        mx = [max(x[0] for x in c) for c in cols]
        avg = [sum(x[1] for x in c) / len(c) for c in cols]
        w = [0.0] * n
        short = [i for i in range(n) if mx[i] <= SHORT and n > 1]
        if len(short) == n:  # every column short: equal
            short = []
        for i in short:
            w[i] = (mx[i] + 1.6) / LINE
        rest = [i for i in range(n) if i not in short]
        left = max(1.0 - sum(w), 0.35)
        if rest:
            a = [max(avg[i], 3) for i in rest]
            if max(a) / min(a) < 1.8:
                for i in rest: w[i] = left / len(rest)
            else:
                s = [math.sqrt(x) for x in a]
                tot = sum(s)
                for i, x in zip(rest, s): w[i] = left * x / tot
        tot = sum(w)
        cg = soup.new_tag('colgroup')
        for x in w:
            cg.append(soup.new_tag('col', style=f'width:{100 * x / tot:.1f}%'))
        t.insert(0, cg)
        fr = [x / tot for x in w]
        est = 0
        for r in rows:
            est += max(math.ceil(max(vlen(c.get_text()), 1) / max(fr[i] * LINE - 1, 1)) for i, c in enumerate(r[:n])) + 0.4
        t['style'] = 'table-layout:fixed;width:100%' + (';break-inside:avoid' if est <= 26 else '')
    open(path, 'w', encoding='utf-8').write(str(soup))

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix(p)
