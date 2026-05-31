import json
d=json.load(open('calendar-events.json'))
st=d['stock']
for e in st:
    if str(e.get('date',''))=='2026-05-29':
        print('MAY29 (enriched sample):')
        print(json.dumps(e,ensure_ascii=False,indent=1)[:1500])
        break
