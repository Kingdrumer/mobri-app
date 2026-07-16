# -*- coding: utf-8 -*-
import json
d=json.load(open('calendar-events.json'))
st=d["stock"]
DATE="2026-07-16"
ev={"type":"negative","label":"메모리 급락·한은 금리인상","color":"red","time":"장중",
 "title":"메모리 차익 실현 급락 + 한국은행 금리 인상 쇼크",
 "description":"어젯밤(7/15) 미국 메모리·AI 하드웨어가 차익 실현에 급락(MU·SNDK −8%, DELL −9.8%)했고, 오늘 아침 한국은행이 3년 반 만에 기준금리를 올려(2.50%→2.75%) 코스피가 7%대 급락하며 매도 사이드카(급락 시 프로그램 매도를 잠깐 멈추는 장치)가 발동됐어요.",
 "impact":"미국 대형 기술주는 6월 물가 둔화(CPI 3.5%)에 강세였지만, 그동안 폭등한 메모리는 차익 실현(오른 김에 파는 것)에 밀렸어요. 한국 금리 인상은 아시아 투자심리에 부담이에요.",
 "ourImpact":"보유 종목 DELL(−9.8%)·SNDK(−8.1%)·MU(−8.0%)·LITE(−7.7%)·MRVL(−7.3%)가 크게 밀렸고, 대형기술주 GOOG·META·AMZN(+3%대)과 NVDA·TLN은 강세로 방어했어요.",
 "stockImpacts":[
  {"ticker":"DELL","tone":"negative","magnitude":"−9.8%","text":"AI 서버·메모리 노출에 최대 낙폭"},
  {"ticker":"SNDK","tone":"negative","magnitude":"−8.1%","text":"메모리 차익 실현 급락"},
  {"ticker":"MU","tone":"negative","magnitude":"−8.0%","text":"중국 경쟁 우려·차익 실현"},
  {"ticker":"GOOG","tone":"positive","magnitude":"+3.6%","text":"물가 둔화에 대형기술주 랠리 주도"},
 ]}
if DATE not in st: st[DATE]=[]
# avoid duplicate of this market event
st[DATE]=[e for e in st[DATE] if e.get("label")!="메모리 급락·한은 금리인상"]
st[DATE].append(ev)
d["lastUpdated"]="2026-07-16T08:20:00+09:00"
json.dump(d,open('calendar-events.json','w'),ensure_ascii=False,indent=1)
print("CALENDAR UPDATED. 7/16 events:", len(st[DATE]))
