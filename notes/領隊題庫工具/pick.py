import json,sys
b=json.load(open('bank_cls.json'))
subj,topics,ymin,ymax=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3]),int(sys.argv[4])
qs=[q for q in b if q['subj']==subj and q['topic'] in topics and ymin<=q['year']<=ymax and q['status'] in('ok','corrected') and not q['excluded']]
qs.sort(key=lambda q:(-q['year'],q['n']))
for q in qs:
    o=' / '.join(f"{k}{' '.join(v.split())[:22]}" for k,v in q['opts'].items())
    print(f"{q['id']}({q['ans']}) {' '.join(q['stem'].split())[:95]} ‖ {o}")
print(len(qs))
