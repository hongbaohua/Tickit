import json,shutil,glob,os
R='/home/claude/Tickit'; T=R+'/docs/questions/華語領隊人員評量'; W='/home/claude/work'; P='/home/claude/pdf2'
for f in glob.glob(W+'/out_v2/華語領隊人員評量/*.md'): shutil.copy(f,T)
for f in glob.glob(W+'/textbook/*.md'): shutil.copy(f,T+'/教材')
for f in glob.glob(P+'/out_old/*.pdf'): shutil.copy(f,T+'/教材/PDF')
os.makedirs(T+'/教材/詳細版',exist_ok=True)
for f in glob.glob(W+'/textbook_v2/*.md')+glob.glob(P+'/out_new/*.pdf'): shutil.copy(f,T+'/教材/詳細版')
N=R+'/notes/領隊題庫工具'
for f in ['build_v2.py','test_parser.js','t2.js','deploy.py']: shutil.copy(W+'/'+f,N)
for f in ['build_v3.py','fixtables.py','style3.css','old3.css']: shutil.copy(P+'/'+f,N)
for f in glob.glob(W+'/v2/*.json'): shutil.copy(f,N+'/v2')
m=json.load(open(R+'/docs/questions/manifest.json'))
u=json.load(open(W+'/units_v2.json'))
for t in m['topics']:
    if t['name']=='華語領隊人員評量': t['units']=[{'unit':x['unit'],'file':x['file']} for x in u]
json.dump(m,open(R+'/docs/questions/manifest.json','w'),ensure_ascii=False,indent=2)
print('ok',len(u))
