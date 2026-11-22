"""Build textbook PDFs for one edition, with footer: chapter label, page within chapter, page within book.

usage: python3 build_all.py <edition> <src_dir> <css> <out_dir> [--book "書名.pdf"]
- strips a leading '# 華語領隊人員評量：新手教材' line
- fixes table widths, checks for overflowing cells, flags pages with large blank bottoms
"""
import sys, os, re, subprocess, glob, shutil, json
from pypdf import PdfReader, PdfWriter
sys.path.insert(0, os.path.dirname(__file__))
import fixtables
from bs4 import BeautifulSoup

ed, src, css, out = sys.argv[1:5]
book = sys.argv[sys.argv.index('--book') + 1] if '--book' in sys.argv else None
os.makedirs(out, exist_ok=True)
work = f'/tmp/build_{ed}'
shutil.rmtree(work, ignore_errors=True); os.makedirs(work)
shutil.copy(css, f'{work}/style.css')

CN = '零一二三四五六七八九十'
def cnum(n):
    return CN[n] if n <= 10 else '十' + CN[n - 10]

def label(stem):
    n = int(stem[:2]); name = stem[3:].split('：')[0]
    return name if n == 0 else f'第{cnum(n)}章　{name}'

CHECK_JS = r"""
<style>@media screen { body { width: 180mm; margin: 0; } }</style>
<script>
window.addEventListener('load', () => {
  const bad = [];
  document.querySelectorAll('td,th').forEach(c => {
    if (c.scrollWidth > c.clientWidth + 2) bad.push('CELL ' + c.textContent.trim().slice(0, 30));
  });
  document.querySelectorAll('table,pre,img').forEach(t => {
    if (t.getBoundingClientRect().width > document.body.clientWidth + 2) bad.push('WIDE ' + t.tagName + ' ' + t.textContent.trim().slice(0, 30));
  });
  const p = document.createElement('pre'); p.id = 'chk'; p.textContent = JSON.stringify(bad);
  document.body.appendChild(p);
});
</script>
"""

def chrome(args):
    return subprocess.run(['google-chrome', '--headless=new', '--no-sandbox', '--disable-gpu',
                           '--no-pdf-header-footer'] + args, capture_output=True, text=True).stdout

CALLOUT = {'info', 'plain', 'example', 'exam', 'trap', 'tip', 'answer'}

def is_block(t):
    return getattr(t, 'name', None) in ('p', 'ul', 'ol', 'table', 'div', 'blockquote')

def pairs_of(soup):
    out = []
    for t in soup.find_all(['table', 'div', 'p', 'ul', 'ol', 'blockquote']):
        if t.find_parent(['td', 'li']) or (t.name == 'div' and 'hk' in t.get('class', [])):
            continue
        nxt = t.find_next_sibling()
        if not is_block(nxt) or (nxt.name == 'div' and 'hk' in nxt.get('class', [])):
            continue
        callout = nxt.name == 'div' and set(nxt.get('class', [])) & CALLOUT
        prev_callout = t.name == 'div' and set(t.get('class', [])) & CALLOUT
        if (callout and not prev_callout) or t.name == 'table':
            out.append((t, nxt))
    return out

def apply_level(a, b, lv):
    if not lv: return
    for el in (a, b): el['class'] = el.get('class', []) + [f'tight{min(lv, 3)}']
    if lv >= 4:
        if 'break-inside:avoid' in a.get('style', '') or a.name in ('p', 'blockquote'):
            # short block: move it together with its note rather than split it
            w = BeautifulSoup('<div class="keep" style="break-inside:avoid"></div>', 'html.parser').div
            a.insert_before(w); w.append(a.extract()); w.append(b.extract())
        else:
            b['style'] = b.get('style', '') + ';break-before:avoid'
    if lv >= 3:
        # still slipping: tighten the blocks above it on the same page as well
        n = 0
        for p in a.find_previous_siblings():
            if n >= 8 or p.name == 'hr': break
            if is_block(p) and 'hk' not in p.get('class', []):
                p['class'] = p.get('class', []) + [f'tight{min(lv - 1, 3)}']
                n += 1

def keep_with_previous(html, pdf, stem):
    # a note right after a table (or a callout box after anything) must start on the page where its
    # predecessor ends. When it slips to the next page, tighten both blocks and render again.
    from bs4 import BeautifulSoup as BS
    base = open(html, encoding='utf-8').read()
    level = {}
    for it in range(7):
        soup = BS(base, 'html.parser')
        prs = pairs_of(soup)
        for k, (a, b) in enumerate(prs):
            apply_level(a, b, level.get(k, 0))
            mk = lambda tag: BS(f'<span class="mk">{tag}</span>', 'html.parser').span
            last = a.find_all('tr')[-1].find(['td', 'th']) if a.name == 'table' else (a.find_all('li')[-1] if a.name in ('ul', 'ol') and a.find_all('li') else a)
            last.append(mk(f'QE{k}Q'))
            (b.find(['p', 'li', 'td', 'th']) or b).insert(0, mk(f'QS{k}Q'))
        test = html[:-5] + '.fit.html'
        open(test, 'w', encoding='utf-8').write(str(soup))
        chrome(['--print-to-pdf=' + pdf, 'file://' + test])
        txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
        page = {}
        for i, pg in enumerate(txt):
            for m in re.finditer(r'Q([ES]\d+)Q', pg): page.setdefault(m.group(1), i)
        bad = [k for k in range(len(prs)) if page.get(f'S{k}', 0) > page.get(f'E{k}', 0)]
        if not bad:
            break
        if it == 6:
            for k in bad:
                a, b = prs[k]
                problems.append(f'{stem}: p{page.get(f"E{k}",0)+1} [{a.name} {a.get_text()[:15]!r}] -> [{b.get_text()[:15]!r}]')
            break
        for k in bad: level[k] = level.get(k, 0) + 1
        # level 4+: let the predecessor split so its tail travels with the note
    # final render without markers but with the same tightening
    soup = BS(base, 'html.parser')
    for k, (a, b) in enumerate(pairs_of(soup)):
        apply_level(a, b, level.get(k, 0))
    open(html, 'w', encoding='utf-8').write(str(soup))
    chrome(['--print-to-pdf=' + pdf, 'file://' + html])
    # a last page holding only a few lines: tighten the whole chapter slightly to pull them back
    for cls in ('compact1', 'compact2'):
        pages_txt = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
        pages_txt = [p for p in pages_txt if p.strip()]
        if len(pages_txt) < 2 or len([l for l in pages_txt[-1].split('\n') if l.strip()]) > 6:
            break
        n0 = len(pages_txt)
        body = soup.find('body'); body['class'] = [cls]
        open(html + '.c.html', 'w', encoding='utf-8').write(str(soup))
        chrome(['--print-to-pdf=' + pdf + '.c.pdf', 'file://' + html + '.c.html'])
        if len(PdfReader(pdf + '.c.pdf').pages) < n0:
            os.replace(html + '.c.html', html); os.replace(pdf + '.c.pdf', pdf)
            break
    # final verification of note-with-predecessor on the layout actually shipped
    from bs4 import BeautifulSoup as BS2
    v = BS2(open(html, encoding='utf-8').read(), 'html.parser')
    prs = pairs_of(v)
    for k, (a, b) in enumerate(prs):
        last = a.find_all('tr')[-1].find(['td', 'th']) if a.name == 'table' else (a.find_all('li')[-1] if a.name in ('ul', 'ol') and a.find_all('li') else a)
        last.append(BS2(f'<span class="mk">QE{k}Q</span>', 'html.parser').span)
        (b.find(['p', 'li', 'td', 'th']) or b).insert(0, BS2(f'<span class="mk">QS{k}Q</span>', 'html.parser').span)
    open(html + '.v.html', 'w', encoding='utf-8').write(str(v))
    chrome(['--print-to-pdf=' + pdf + '.v.pdf', 'file://' + html + '.v.html'])
    page = {}
    for i, pg in enumerate(subprocess.run(['pdftotext', pdf + '.v.pdf', '-'], capture_output=True, text=True).stdout.split('\f')):
        for m in re.finditer(r'Q([ES]\d+)Q', pg): page.setdefault(m.group(1), i)
    for k, (a, b) in enumerate(prs):
        if page.get(f'S{k}', 0) > page.get(f'E{k}', 0):
            problems.append(f'{stem}: VERIFY p{page.get(f"E{k}",0)+1} note separated from {a.name} {a.get_text()[:15]!r}')

files = sorted(glob.glob(f'{src}/*.md'))
chapters = []
problems = []
for f in files:
    stem = os.path.basename(f)[:-3]
    md = open(f, encoding='utf-8').read()
    md = re.sub(r'\A# 華語領隊人員評量：新手教材\s*\n', '', md)
    tmp = f'{work}/{stem}.md'; open(tmp, 'w', encoding='utf-8').write(md)
    html = f'{work}/{stem}.html'
    fmt = 'gfm' if ed == '精簡版' else 'markdown+hard_line_breaks-tex_math_dollars-auto_identifiers'
    subprocess.run(['pandoc', tmp, '-f', fmt, '-t', 'html5', '-s', '--metadata', f'pagetitle={stem}',
                    '-c', 'style.css', '-o', html], check=True)
    fixtables.fix(html)
    from bs4 import BeautifulSoup as _BS
    _s = _BS(open(html, encoding='utf-8').read(), 'html.parser')
    for _h in _s.find_all(['h2', 'h3', 'h4']):
        _w = _s.new_tag('div', attrs={'class': 'hk'}); _h.wrap(_w)
    for _l in _s.find_all(['ul', 'ol']):
        if len(_l.find_all('li')) <= 6 and len(_l.get_text()) < 400:
            _l['style'] = (_l.get('style', '') + ';break-inside:avoid').lstrip(';')
    for _p in _s.find_all('p'):
        _n = _p.find_next_sibling()
        if _n is not None and _n.name == 'table' and len(_p.get_text()) < 120 and not _p.find_parent(['td', 'li']):
            if 'break-inside:avoid' in _n.get('style', ''):
                _w = _s.new_tag('div', attrs={'class': 'keep', 'style': 'break-inside:avoid'})
                _p.insert_before(_w); _w.append(_p.extract()); _w.append(_n.extract())
            else:
                _w = _s.new_tag('div', attrs={'class': 'hk'}); _p.wrap(_w)
    # heading chains: heading (+ short intro) (+ sub-heading) + a block that must not split -> one unit
    def _avoid(el):
        return el is not None and getattr(el, 'name', None) in ('table', 'div', 'ul', 'ol') and (
            'break-inside:avoid' in el.get('style', '') or (el.name == 'div' and set(el.get('class', [])) & CALLOUT))
    for _h in list(_s.find_all('div', class_='hk')):
        if _h.parent is None or _h.find_parent('div', class_='keep') or _h.find('h2'):
            continue
        chain = [_h]; nx = _h.find_next_sibling()
        while nx is not None and len(chain) < 5:
            if nx.name == 'div' and 'hk' in nx.get('class', []) and not nx.find('h2'):
                chain.append(nx)
            elif nx.name == 'p' and len(nx.get_text()) < 150:
                chain.append(nx)
            else:
                break
            nx = nx.find_next_sibling()
        if _avoid(nx) and len(nx.get_text()) < 900:
            chain.append(nx)
            _w = _s.new_tag('div', attrs={'class': 'keep', 'style': 'break-inside:avoid'})
            chain[0].insert_before(_w)
            for el in chain: _w.append(el.extract())
    open(html, 'w', encoding='utf-8').write(str(_s))
    # overflow check on a copy
    chk = f'{work}/{stem}.chk.html'
    open(chk, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read().replace('</head>', CHECK_JS + '</head>'))
    dom = chrome(['--virtual-time-budget=3000', '--dump-dom', 'file://' + chk])
    m = re.search(r'<pre id="chk">(.*?)</pre>', dom, re.S)
    bad = json.loads(m.group(1).replace('&quot;', '"')) if m else ['CHECK FAILED']
    for b in bad: problems.append(f'{stem}: {b}')
    pdf = f'{work}/{stem}.raw.pdf'
    keep_with_previous(html, pdf, stem)
    chapters.append((stem, pdf, len(PdfReader(pdf).pages)))

total = sum(c[2] for c in chapters)

# footer overlay: one long HTML, one div per page of the whole book
pages = []
start = 0
for stem, pdf, n in chapters:
    for i in range(n):
        right = f'本章 {i+1} / {n}' + (f'　｜　全書 {start+i+1} / {total}' if book else '')
        pages.append((label(stem), right))
    start += n
ov = ['<html><head><meta charset="utf-8"><style>@page{size:A4;margin:0}body{margin:0;font-family:"Noto Sans CJK TC";}',
      '.pg{height:297mm;position:relative;break-after:page;overflow:hidden}',
      '.ft{position:absolute;left:15mm;right:15mm;bottom:7mm;display:flex;justify-content:space-between;font-size:8.5pt;color:#7a8a90;border-top:0.5px solid #c8d4d8;padding-top:2mm}',
      '</style></head><body>']
for l, r in pages:
    ov.append(f'<div class="pg"><div class="ft"><span>{l}</span><span>{r}</span></div></div>')
ov.append('</body></html>')
open(f'{work}/overlay.html', 'w', encoding='utf-8').write(''.join(ov))
chrome(['--print-to-pdf=' + f'{work}/overlay.pdf', 'file://' + f'{work}/overlay.html'])
over = PdfReader(f'{work}/overlay.pdf').pages
assert len(over) >= total, (len(over), total)

bookw = PdfWriter()
k = 0
for stem, pdf, n in chapters:
    w = PdfWriter()
    for p in PdfReader(pdf).pages:
        p.merge_page(over[k]); k += 1
        w.add_page(p); bookw.add_page(p)
    w.write(f'{out}/{stem}.pdf')
if book:
    bookw.write(f'{out}/{book}')

# blank-bottom check: render small, measure empty rows above the footer
for stem, pdf, n in chapters:
    subprocess.run(['pdftoppm', '-r', '20', '-gray', f'{out}/{stem}.pdf', f'{work}/b'], check=True)
    imgs = sorted(glob.glob(f'{work}/b-*.pgm'))
    from PIL import Image
    for i, im in enumerate(imgs):
        a = Image.open(im); W, H = a.size; px = a.load()
        bottom = int(H * 0.93)  # above footer
        last = 0
        for y in range(int(H * 0.04), bottom):
            if any(px[x, y] < 200 for x in range(int(W * .06), int(W * .94), 2)): last = y
        blank = (bottom - last) / H
        if blank > 0.30 and i < len(imgs) - 1:
            problems.append(f'{stem}: page {i+1} blank bottom {blank:.0%}')
        os.remove(im)

# heading stranded at page bottom: last text line on a page equals a heading
from bs4 import BeautifulSoup
for stem, pdf, n in chapters:
    heads = set()
    for h in BeautifulSoup(open(f'{work}/{stem}.html', encoding='utf-8').read(), 'html.parser').find_all(['h1','h2','h3','h4']):
        heads.add(re.sub(r'\s+', '', h.get_text()))
    txt = subprocess.run(['pdftotext', '-layout', f'{out}/{stem}.pdf', '-'], capture_output=True, text=True).stdout
    for i, pg in enumerate(txt.split('\f')[:-1]):
        lines = [re.sub(r'\s+', '', l) for l in pg.split('\n') if l.strip()]
        body = [l for l in lines if not l.startswith(('第', '導讀')) or '本章' not in l]
        if body and body[-1] in heads:
            problems.append(f'{stem}: page {i+1} ends with heading {body[-1]}')
print('total pages', total)
print('\n'.join(problems) or 'no problems')
