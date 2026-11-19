import json,sys
b=json.load(open('bank_cls.json'))
subj,topics,ymin=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3])
qs=[q for q in b if q['subj']==subj and q['topic'] in topics and q['year']>=ymin and q['status']!='void']
qs.sort(key=lambda q:(-q['year'],q['n']))
for q in qs:
    print(f"{q['year']}|{' '.join(q['stem'].split())[:110]}→{q['opts'].get(q['ans'],'')[:60]}")
print(len(qs))
