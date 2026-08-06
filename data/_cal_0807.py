# -*- coding: utf-8 -*-
import json, datetime
KST = datetime.timezone(datetime.timedelta(hours=9))
gen = datetime.datetime.now(KST).replace(microsecond=0).isoformat()
d = json.load(open('calendar-events.json', encoding='utf-8'))
st = d['stock']
recap = {
 "type":"market-recap","label":"8/6 뉴욕 마감 정산","color":"amber","mood":"🟡","time":"06:00 KST",
 "title":"🟡 8/6(목) 뉴욕 혼조·약세 — 다우 53,885.00(-0.85%, 464p↓)·S&P500 7,709.96(-0.18%)·나스닥 26,348.35(-0.06%), 다우 사상 최고서 후퇴",
 "description":"전날 급등한 기술주에 차익실현(오른 김에 일부 파는 것) 매물이 나오고, 국제유가(WTI, 미국 대표 원유 가격)가 홍해 선박 공격에 $75.8로 반등, 미 10년물 국채금리도 4.6%대로 다시 오르며 지수가 무거웠어요. 안전자산 금은 $4,321(+0.4%)로 급등했어요. 소프트웨어주에 실적 실망 매물(데이터독·허브스팟)이 나온 반면, 장 마감 후 애프터아워 실적에서 에어비앤비(ABNB)가 +9.4% 급등했어요. 보유 종목은 엔비디아·크레도·탈렌이 오르고 메모리(마이크론·샌디스크)는 내려 차별화됐어요.",
 "impact":"미국 정규장 마감 정산(라이트 캡처)이에요. 지수·유가·애프터아워 실적은 확정치, 보유 종목 개별 종가는 섹터 흐름 반영 추정치로 다음 세션에 재정산해요. 오늘 밤 21:30 KST 7월 고용보고서가 최대 변수예요."
}
day = st.get('2026-08-07', [])
day = [e for e in day if e.get('type')!='market-recap']  # avoid dup
day.insert(0, recap)
st['2026-08-07'] = day
d['lastUpdated'] = gen
json.dump(d, open('calendar-events.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("calendar 2026-08-07 events:", len(st['2026-08-07']), "| types:", [e.get('type') for e in st['2026-08-07']])
