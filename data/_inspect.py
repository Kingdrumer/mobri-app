import json
d=json.load(open('calendar-events.json'))
st=d['stock']
print('stock type:',type(st))
if isinstance(st,dict):
    print('stock keys sample:',list(st.keys())[:8])
    if '2026-06-01' in st:
        print('JUN1:',json.dumps(st['2026-06-01'],ensure_ascii=False)[:1200])
    if '2026-05-29' in st:
        print('MAY29:',json.dumps(st['2026-05-29'],ensure_ascii=False)[:1200])
elif isinstance(st,list):
    print('count:',len(st))
    for e in st:
        if isinstance(e,dict) and str(e.get('date','')).startswith('2026-06-01'):
            print('JUN1:',json.dumps(e,ensure_ascii=False)[:1200])
    print('--- recent ---')
    for e in st[-2:]:
        print(json.dumps(e,ensure_ascii=False)[:600])
