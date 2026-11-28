"""Build textbook PDFs (v3 layout): uniform type, no shrinking.

usage: python3 build_v3.py <edition> <src_dir> <css> <out_dir> [--book "書名.pdf"] [--only 00,03]

Layout rules
- Same font size everywhere. Nothing is scaled down to make it fit.
- Headings stay with what follows (break-after: avoid).
- Tables may continue on the next page (header row repeats, rows never split);
  only small tables (about 6 lines or less) are kept whole.
- Callout boxes are kept whole when short; long ones may continue on the next page.
- A callout that explains the block above it (.note) starts on the same page as that block ends.
- Fitting loop: a page whose bottom is left more than MAXBLANK empty because an unbreakable block
  moved to the next page gets that block made breakable, then the chapter is laid out again.
"""
import sys, os, re, subprocess, glob, shutil, json
from pypdf import PdfReader, PdfWriter
from PIL import Image
from bs4 import BeautifulSoup as BS
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtables

ed, src, css, out = sys.argv[1:5]
book = sys.argv[sys.argv.index('--book') + 1] if '--book' in sys.argv else None
only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
MAXBLANK = 0.12
os.makedirs(out, exist_ok=True)
work = f'/tmp/b3_{ed}'
shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
shutil.copy(css, f'{work}/style.css')

CN = '零一二三四五六七八九十'
def cnum(n): return CN[n] if n <= 10 else '十' + CN[n - 10]
def label(stem):
    n = int(stem[:2]); name = stem[3:].split('：')[0]
    return name if n == 0 else f'第{cnum(n)}章　{name}'

def chrome(args):
    return subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu',
                           '--no-pdf-header-footer'] + args, capture_output=True, text=True).stdout

CALLOUT = {'info', 'plain', 'example', 'exam', 'trap', 'tip', 'answer'}
def is_callout(el): return getattr(el, 'name', None) == 'div' and bool(set(el.get('class', [])) & CALLOUT)
def add_cls(el, c): el['class'] = list(dict.fromkeys(el.get('class', []) + [c]))
def del_cls(el, c): el['class'] = [x for x in el.get('class', []) if x != c]

CHECK_JS = r"""
<style>@media screen { body { width: 180mm; margin: 0; } }</style>
<script>
window.addEventListener('load', () => {
  const bad = [];
  document.querySelectorAll('td,th').forEach(c => { if (c.scrollWidth > c.clientWidth + 2) bad.push('CELL ' + c.textContent.trim().slice(0, 30)); });
  document.querySelectorAll('table').forEach(t => { if (t.getBoundingClientRect().width > document.body.clientWidth + 2) bad.push('WIDE ' + t.textContent.trim().slice(0, 30)); });
  const p = document.createElement('pre'); p.id = 'chk'; p.textContent = JSON.stringify(bad); document.body.appendChild(p);
});
</script>
"""

def prepare(html):
    s = BS(open(html, encoding='utf-8').read(), 'html.parser')
    body = s.body
    for h in s.find_all(['h2', 'h3', 'h4']):
        w = s.new_tag('div', attrs={'class': 'hk'}); h.wrap(w)
    # small tables stay whole (fixtables marks estimated <= 12 lines; we use a stricter estimate here)
    for t in s.find_all('table'):
        st = t.get('style', '').replace(';break-inside:avoid', '')
        t['style'] = st
        rows = t.find_all('tr')
        lines = sum(max(1, len(r.get_text()) // 40) for r in rows)
        if lines <= 7: add_cls(t, 'nb')
    for d in s.find_all('div'):
        if is_callout(d):
            if len(d.get_text()) < 420: add_cls(d, 'nb')
            else: d['style'] = 'break-inside:auto'
    for l in s.find_all(['ul', 'ol']):
        if not l.find_parent(['li', 'td']) and len(l.find_all('li')) <= 4 and len(l.get_text()) < 260:
            add_cls(l, 'nb')
    top = [c for c in body.children if getattr(c, 'name', None)]
    for a, b in zip(top, top[1:]):
        # a callout right after a table explains it: start it on the page where the table ends
        if is_callout(b) and a.name == 'table':
            add_cls(b, 'note')
        # a short lead-in sentence stays with the table/list it introduces
        if a.name == 'p' and len(a.get_text()) < 120 and b.name in ('table', 'ul', 'ol'):
            add_cls(a, 'lead')
    # a section start (heading + what it introduces + its first block) is one unit:
    # if it does not fit at the bottom of a page, the whole section starts on the next page
    top = [c for c in body.children if getattr(c, 'name', None)]
    i = 0; n = 0
    while i < len(top):
        if 'hk' not in top[i].get('class', []): i += 1; continue
        chain = [top[i]]; j = i + 1
        while j < len(top) and ('hk' in top[j].get('class', []) or (top[j].name == 'p' and len(top[j].get_text()) < 150)):
            chain.append(top[j]); j += 1
        if j < len(top):
            chain.append(top[j]); j += 1
            if chain[-1].name == 'table' and j < len(top) and 'note' in top[j].get('class', []):
                chain.append(top[j]); j += 1
        w = s.new_tag('div', attrs={'class': 'sec', 'data-sec': str(n)}); n += 1
        chain[0].insert_before(w)
        for el in chain: w.append(el.extract())
        i = j
    open(html, 'w', encoding='utf-8').write(str(s))

SEC_JS = r"""
<style>@media screen { body { width: 180mm; margin: 0; } }</style>
<script>
window.addEventListener('load', () => {
  const r = {};
  document.querySelectorAll('div.sec').forEach(d => { r[d.dataset.sec] = d.getBoundingClientRect().height; });
  const p = document.createElement('pre'); p.id = 'sec'; p.textContent = JSON.stringify(r); document.body.appendChild(p);
});
</script>
"""

def limit_sections(html):
    # a section unit taller than ~55% of a page would leave too much blank: let it split,
    # but still require room for the heading plus a good start of its content
    dom = chrome(['--virtual-time-budget=3000', '--dump-dom', 'file://' + html + '.sec.html']) if False else None
    t = html + '.sec.html'
    open(t, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read().replace('</head>', SEC_JS + '</head>'))
    m = re.search(r'<pre id="sec">(.*?)</pre>', chrome(['--virtual-time-budget=3000', '--dump-dom', 'file://' + t]), re.S)
    hts = json.loads(m.group(1).replace('&quot;', '"')) if m else {}
    page_px = (297 - 31) / 25.4 * 96
    s = BS(open(html, encoding='utf-8').read(), 'html.parser')
    for d in s.find_all('div', class_='sec'):
        if hts.get(d['data-sec'], 0) > 0.55 * page_px:
            hk = d.find('div', class_='hk')
            if hk: add_cls(hk, 'secr')
            d.unwrap()
    open(html, 'w', encoding='utf-8').write(str(s))

def top_blocks(s):
    return [c for c in s.body.children if getattr(c, 'name', None)]

def render(html, pdf, marks):
    s = BS(open(html, encoding='utf-8').read(), 'html.parser')
    if marks:
        for k, b in enumerate(top_blocks(s)):
            tgt = b.find(['h2', 'h3', 'h4', 'p', 'li', 'td', 'th']) or b
            m = s.new_tag('span', attrs={'class': 'mk'}); m.string = f'QB{k}Q'; tgt.insert(0, m)
    t = html + '.r.html'; open(t, 'w', encoding='utf-8').write(str(s))
    chrome(['--print-to-pdf=' + pdf, 'file://' + t])

def blanks(pdf):
    d = f'{work}/img'; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run(['pdftoppm', '-r', '24', '-gray', pdf, f'{d}/b'], check=True)
    res = []
    for im in sorted(glob.glob(f'{d}/b-*.pgm')):
        a = Image.open(im); W, H = a.size; px = a.load()
        top, bottom = int(H * 15 / 297), int(H * (297 - 16) / 297)
        last = top
        for y in range(top, bottom):
            if any(px[x, y] < 225 for x in range(int(W * .05), int(W * .95))): last = y
        res.append((bottom - last) / (bottom - top))
    return res

def marker_pos(pdf):
    """block index -> (page, y in pt)"""
    x = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    pos = {}; page = -1
    for line in x.split('\n'):
        if '<page ' in line: page += 1
        m = re.search(r'yMin="([\d.]+)".*>QB(\d+)Q<', line)
        if m: pos.setdefault(int(m.group(2)), (page, float(m.group(1))))
    return pos

problems = []

def relax(el):
    """make an element (and a keep chain it heads) allowed to split; return True if anything changed"""
    ch = False
    if 'nb' in el.get('class', []): del_cls(el, 'nb'); ch = True
    if is_callout(el) and el.get('style') != 'break-inside:auto': el['style'] = 'break-inside:auto'; ch = True
    return ch

def fit_loop(html, pdf):
    for it in range(8):
        render(html, pdf, True)
        bl = blanks(pdf); pos = marker_pos(pdf)
        s = BS(open(html, encoding='utf-8').read(), 'html.parser'); tb = top_blocks(s)
        changed = False; left = []
        for i in range(len(bl) - 1):
            if bl[i] <= MAXBLANK: continue
            # first block starting on page i+1
            starts = sorted((y, k) for k, (p, y) in pos.items() if p == i + 1)
            if not starts: left.append((i, '')); continue
            y, k = starts[0]
            if y > 115:  # page i+1 begins with the continuation of a block: nothing moved whole
                left.append((i, 'cont')); continue
            # walk the chain that moved together: headings / lead-ins + the block they hold on to
            cand = []; j = k
            while j < len(tb):
                cand.append(tb[j])
                if 'hk' in tb[j].get('class', []) or 'lead' in tb[j].get('class', []): j += 1; continue
                break
            # a note pulled its predecessor along: allow the predecessor to split instead
            if k > 0 and 'note' in tb[k].get('class', []): cand.append(tb[k - 1])
            if j + 1 < len(tb) and 'note' in tb[j + 1].get('class', []): cand.append(tb[j + 1])
            if any(relax(c) for c in cand): changed = True
            else: left.append((i, tb[k].get_text()[:12]))
        if not changed: break
        open(html, 'w', encoding='utf-8').write(str(s))
    render(html, pdf, False)

def fit(html, pdf, stem):
    fit_loop(html, pdf)
    # a last page holding only a few lines: set the whole chapter slightly tighter (same font size)
    for cls in ('compact1', 'compact2'):
        pg = [x for x in subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f') if x.strip()]
        if len(pg) < 2 or len([l for l in pg[-1].split('\n') if l.strip()]) > 10: break
        shutil.copy(html, html + '.bak')
        s = BS(open(html, encoding='utf-8').read(), 'html.parser'); s.body['class'] = [cls]
        open(html, 'w', encoding='utf-8').write(str(s))
        fit_loop(html, pdf + '.c.pdf')
        if len(PdfReader(pdf + '.c.pdf').pages) < len(pg):
            os.replace(pdf + '.c.pdf', pdf); break
        os.replace(html + '.bak', html)
    bl = blanks(pdf)
    for i in range(len(bl) - 1):
        if bl[i] > MAXBLANK: problems.append(f'{stem}: page {i+1} blank {bl[i]:.0%}')

files = sorted(glob.glob(f'{src}/*.md'))
chapters = []
for f in files:
    stem = os.path.basename(f)[:-3]
    md = re.sub(r'\A# 華語領隊人員評量：新手教材\s*\n', '', open(f, encoding='utf-8').read())
    tmp = f'{work}/{stem}.md'; open(tmp, 'w', encoding='utf-8').write(md)
    html = f'{work}/{stem}.html'; pdf = f'{work}/{stem}.raw.pdf'
    fmt = 'gfm' if ed == '精簡版' else 'markdown+hard_line_breaks-tex_math_dollars-auto_identifiers'
    subprocess.run(['pandoc', tmp, '-f', fmt, '-t', 'html5', '-s', '--metadata', f'pagetitle={stem}',
                    '-c', 'style.css', '-o', html], check=True)
    fixtables.fix(html)
    prepare(html)
    limit_sections(html)
    chk = f'{work}/{stem}.chk.html'
    open(chk, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read().replace('</head>', CHECK_JS + '</head>'))
    m = re.search(r'<pre id="chk">(.*?)</pre>', chrome(['--virtual-time-budget=3000', '--dump-dom', 'file://' + chk]), re.S)
    for b in (json.loads(m.group(1).replace('&quot;', '"')) if m else ['CHECK FAILED']): problems.append(f'{stem}: {b}')
    if only and stem[:2] not in only:
        render(html, pdf, False)
    else:
        fit(html, pdf, stem)
    chapters.append((stem, pdf, len(PdfReader(pdf).pages)))
    print(stem, chapters[-1][2], flush=True)

total = sum(c[2] for c in chapters)
pages = []; start = 0
for stem, pdf, n in chapters:
    for i in range(n):
        pages.append((label(stem), f'本章 {i+1} / {n}' + (f'　｜　全書 {start+i+1} / {total}' if book else '')))
    start += n
ov = ['<html><head><meta charset="utf-8"><style>@page{size:A4;margin:0}body{margin:0;font-family:"Noto Sans CJK TC";}',
      '.pg{height:297mm;position:relative;break-after:page;overflow:hidden}',
      '.ft{position:absolute;left:15mm;right:15mm;bottom:7mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#7a8a90;border-top:0.5px solid #c8d4d8;padding-top:2mm}',
      '</style></head><body>']
ov += [f'<div class="pg"><div class="ft"><span>{l}</span><span>{r}</span></div></div>' for l, r in pages]
ov.append('</body></html>')
open(f'{work}/overlay.html', 'w', encoding='utf-8').write(''.join(ov))
chrome(['--print-to-pdf=' + f'{work}/overlay.pdf', 'file://' + f'{work}/overlay.html'])
over = PdfReader(f'{work}/overlay.pdf').pages
bookw = PdfWriter(); k = 0
for stem, pdf, n in chapters:
    w = PdfWriter()
    for p in PdfReader(pdf).pages:
        p.merge_page(over[k]); k += 1; w.add_page(p); bookw.add_page(p)
    w.write(f'{out}/{stem}.pdf')
if book:
    bookw.write(f'{work}/book.pdf')
    subprocess.run(['qpdf', '--object-streams=generate', '--compression-level=9', '--recompress-flate',
                    f'{work}/book.pdf', f'{out}/{book}'], check=True)

# heading stranded at the bottom of a page
for stem, pdf, n in chapters:
    heads = {re.sub(r'\s+', '', h.get_text()) for h in BS(open(f'{work}/{stem}.html', encoding='utf-8').read(), 'html.parser').find_all(['h2', 'h3', 'h4'])}
    txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    for i, pg in enumerate(txt.split('\f')[:-1]):
        lines = [re.sub(r'\s+', '', l) for l in pg.split('\n') if l.strip()]
        if lines and lines[-1] in heads: problems.append(f'{stem}: page {i+1} ends with heading {lines[-1]}')
print('total pages', total)
print('\n'.join(problems) or 'no problems')
