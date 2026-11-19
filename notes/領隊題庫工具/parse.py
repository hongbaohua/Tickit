import re,subprocess,json,glob,os,sys
D='/home/claude/raw/all'
MK={'':'A','':'B','':'C','':'D'}
SUBJ={'1':'領隊執業實務','2':'領隊執業法規','3':'觀光資源概要'}
def txt(f,layout=True):
    a=['pdftotext']+(['-layout'] if layout else [])+[f,'-']
    return subprocess.run(a,capture_output=True).stdout.decode('utf-8','ignore')
SKIP=re.compile(r'^\s*(代號|頁次|類\s*科|科\s*目|評量時間|考試時間|※注意|本科目共|禁止使用|本試題|座號|等\s*別|\d{3}\s*年|\d{3}年)')
def clean_join(parts):
    s=''
    for p in parts:
        p=p.strip()
        if not p: continue
        if s and re.search(r'[A-Za-z0-9,.)]$',s) and re.match(r'[A-Za-z0-9(]',p): s+=' '+p
        else: s+=p
    s=re.sub(r'[ 　]{2,}',' ',s)
    return s.strip()
def parse_q(f,n_expected):
    t=txt(f)
    lines=[l for l in t.split('\n')]
    out=[];cur=None;exp=1
    for l in lines:
        if SKIP.match(l) or re.match(r'^\s*\f',l) and SKIP.match(l.strip('\f')): continue
        l=l.replace('\f','')
        if re.match(r'^\s*(代號|頁次)',l): continue
        m=re.match(r'^\s{0,5}(\d{1,2})\s+(\S.*)$',l)
        if m and int(m.group(1))==exp and not any(k in l[:8] for k in MK):
            cur={'n':exp,'raw':[m.group(2)]};out.append(cur);exp+=1;continue
        m2=re.match(r'^\s{0,5}(\d{1,2})\s*$',l)
        if m2 and int(m2.group(1))==exp:
            cur={'n':exp,'raw':[]};out.append(cur);exp+=1;continue
        if cur is not None: cur['raw'].append(l)
    qs=[]
    for q in out:
        body='\n'.join(q['raw'])
        # split by markers
        idx=[(m.start(),MK[m.group()]) for m in re.finditer('[-]',body)]
        if len(idx)!=4 or [x[1] for x in idx]!=list('ABCD'):
            qs.append({'n':q['n'],'err':'markers','body':body});continue
        stem=clean_join(body[:idx[0][0]].split('\n'))
        opts={}
        for i,(p,L) in enumerate(idx):
            e=idx[i+1][0] if i<3 else len(body)
            opts[L]=clean_join(body[p+1:e].split('\n'))
        qs.append({'n':q['n'],'stem':stem,'opts':opts})
    return qs
def parse_key(f):
    t=txt(f)
    ans=[]
    for l in t.split('\n'):
        m=re.match(r'^\s*答\s*案\s+(.*)$',l)
        if m: ans+=re.findall(r'[A-D#]',m.group(1).replace('Ａ','A').replace('Ｂ','B').replace('Ｃ','C').replace('Ｄ','D'))
    note=''
    i=t.find('備')
    if i>=0: note=re.sub(r'\s+','',t[i:])
    return ans,note
def notes_map(note):
    note=note.translate(str.maketrans('ＡＢＣＤ０１２３４５６７８９','ABCD0123456789'))
    res={}
    for m in re.finditer(r'第(\d+)題([^，,。；;]*)',note):
        n=int(m.group(1));s=m.group(2)
        if '一律給分' in s: res[n]=('void',None)
        else:
            letters=re.findall(r'答([A-D]+)',s)
            singles=[x for x in letters if len(x)==1]
            if len(singles)==1: res[n]=('single',singles[0])
            else: res[n]=('multi',''.join(sorted(set(''.join(singles)))))
    return res
allq=[];report=[]
for f in sorted(glob.glob(D+'/*Q.pdf')):
    b=os.path.basename(f);y,s=b[:3],b[4]
    sfile=f.replace('Q.pdf','S.pdf');mfile=f.replace('Q.pdf','M.pdf')
    key,_=parse_key(sfile)
    notes={}
    if os.path.exists(mfile):
        mk,mnote=parse_key(mfile);notes=notes_map(mnote)
    qs=parse_q(f,len(key))
    ok=sum(1 for q in qs if 'stem' in q)
    report.append((b,len(key),len(qs),ok))
    for q in qs:
        if 'stem' not in q: continue
        n=q['n'];a=key[n-1] if n-1<len(key) else '?'
        st='ok';alt=None
        if n in notes:
            kind,v=notes[n]
            if kind=='single': a=v;st='corrected'
            elif kind=='void': st='void'
            else: st='multi';alt=v
        allq.append({'id':f'{y}-{s}-{n:02d}','year':int(y),'subj':SUBJ[s],'n':n,'stem':q['stem'],'opts':q['opts'],'ans':a,'status':st,'alt':alt})
json.dump(allq,open('/home/claude/work/bank_raw.json','w'),ensure_ascii=False,indent=0)
for r in report: print(r)
print(len(allq))
