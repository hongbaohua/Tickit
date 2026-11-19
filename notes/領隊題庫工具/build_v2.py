import json,os
b={q['id']:q for q in json.load(open('bank_cls.json'))}
SUBJ={'1':'領隊執業實務','2':'領隊執業法規','3':'觀光資源概要'}
OUT='out_v2/華語領隊人員評量'; os.makedirs(OUT,exist_ok=True)
UNITS=[
 ('01 法規 旅遊契約','01_法規_旅遊契約：民法旅遊專節與國外旅遊定型化契約.md','v2/u01.json'),
 ('02 法規 兩岸港澳','02_法規_兩岸條例、港澳條例與兩岸現況.md','v2/u02.json'),
 ('03 法規 旅行業','03_法規_旅行業管理規則、發展觀光條例與領隊規則.md','v2/u03.json'),
 ('06 實務 航空','06_實務_航空票務與機場作業.md','v2/u06.json'),
 ('07 實務 急救緊急','07_實務_急救保健、緊急事件與旅遊保險.md','v2/u07.json'),
 ('10 資源 中國歷史','10_資源_中國歷史與港澳.md','v2/u10.json'),
 ('11 資源 中國地理','11_資源_中國地理與世界遺產.md','v2/u11.json'),
]
def esc(s): return ' '.join(s.replace('ˉ','').split())
def write(name,items):
    Q=[];A=[]
    for i,it in enumerate(items,1):
        if 'id' in it:
            q=b[it['id']]; stem,opts,ans=q['stem'],q['opts'],q['ans']
            src=f"{q['year']}年{q['subj']}第{q['n']}題"
        else:
            stem,opts,ans=it['stem'],it['opts'],it['ans']; src='自編題（依現行條文出題）'
        Q.append(f"{i}. {esc(stem)}\n"+''.join(f"    ({k}) {esc(opts[k])}\n" for k in 'ABCD'))
        e=esc(it.get('exp',''));A.append(f"{i}. ({ans}) {esc(opts[ans])}｜{src}"+(f"。解析：{e}" if e else "")+"\n")
    open(f'{OUT}/{name}','w').write('\n'.join(Q)+'\n解答與詳細解析\n\n'+'\n'.join(A))
    return len(items)
units=[]
for d,name,f in UNITS:
    n=write(name,json.load(open(f))); units.append({'unit':d,'file':name,'n':n})
# mock exams: 115 原卷
for d,s in [('15 法規 模擬考','2'),('16 實務 模擬考','1'),('17 資源 模擬考','3')]:
    qs=[q for q in b.values() if q['year']==115 and q['id'].split('-')[1]==s and not q['excluded']]
    qs.sort(key=lambda q:q['n'])
    name=d.replace(" ","_",2)+f"：115年{SUBJ[s]}全真模擬（限時60分鐘）.md"
    n=write(name,[{'id':q['id'],'exp':''} for q in qs]); units.append({'unit':d,'file':name,'n':n})
json.dump(units,open('units_v2.json','w'),ensure_ascii=False,indent=1)
print(units)
