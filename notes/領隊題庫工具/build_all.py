"""Build textbook PDFs for one edition, with footer: chapter label, page within chapter, page within book.

usage: python3 build_all.py <edition> <src_dir> <css> <out_dir> [--book "書名.pdf"]
- strips a leading '# 華語領隊人員評量：新手教材' line
- fixes table widths, checks for overflowing cells, flags pages with large blank bottoms
"""
import sys, os, re, subprocess, glob, shutil, json
from pypdf import PdfReader, PdfWriter
sys.path.insert(0, os.path.dirname(__file__))
import fixtables

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
    # overflow check on a copy
    chk = f'{work}/{stem}.chk.html'
    open(chk, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read().replace('</head>', CHECK_JS + '</head>'))
    dom = chrome(['--virtual-time-budget=3000', '--dump-dom', 'file://' + chk])
    m = re.search(r'<pre id="chk">(.*?)</pre>', dom, re.S)
    bad = json.loads(m.group(1).replace('&quot;', '"')) if m else ['CHECK FAILED']
    for b in bad: problems.append(f'{stem}: {b}')
    pdf = f'{work}/{stem}.raw.pdf'
    chrome(['--print-to-pdf=' + pdf, 'file://' + html])
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

print('total pages', total)
print('\n'.join(problems) or 'no problems')
