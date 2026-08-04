# -*- coding: utf-8 -*-
import json

# ---- index.json ----
idx = json.load(open('reports/index.json'))
entry = {
 "date":"2026-08-04",
 "title":"8월 4일 (화) 06:00 미국 마감 캡처 — 🟢 3대 지수 급등 (다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%) / 이란 완화·유가 -6% / 아마존 시총 3조달러·메타 +7%·구글 +5% / 팰런티어 시간외 +13% 실적 서프라이즈 / 오늘 밤 AMD(보유) 실적",
 "summary":"미국 마감 캡처(라이트). 8/3(월) 뉴욕은 이란 협상 재개·유가 6% 급락에 빅테크 강세로 3대 지수 급등(다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%). 아마존 시총 3조달러 돌파(+4.5%)·메타 +6.6%·구글 +5.0%·엔비디아 +3.2%. 장 마감 후 팰런티어 2분기 실적 서프라이즈(매출 +93%, 가이던스 상향)로 시간외 +약 13.6%. 보유 빅테크 5종 종가 교차확인, 그 외 종목 지수·섹터 기반 추정. 오늘 밤 AMD(8/4)·수요일 SNDK·TLN(8/5) 실적, 8/7 고용보고서 대기."
}
if not (idx['reports'] and idx['reports'][0].get('date')=='2026-08-04'):
    idx['reports'].insert(0, entry)
idx['lastUpdated'] = "2026-08-04T06:10:00+09:00"
json.dump(idx, open('reports/index.json','w'), ensure_ascii=False, indent=1)
print("index.json reports now:", len(idx['reports']), "| first:", idx['reports'][0]['date'])

# ---- calendar-events.json ----
cal = json.load(open('calendar-events.json'))
st = cal['stock']
cap = {"type":"info","label":"미국 마감 캡처 (화)","color":"blue","mood":"🟢","time":"06:00 KST 라이트",
 "title":"🟢 미국 마감 캡처(8/4 화 06:00) — 8/3 뉴욕 급등 반영 (나스닥 +2.1%) / 아마존 시총 3조달러·팰런티어 시간외 +13%",
 "description":"8/3(월) 미국 정규장이 이란 긴장 완화와 유가 6% 급락, 빅테크 강세로 3대 지수 급등 마감했어요(다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%). 아마존이 +4.5%로 시가총액 3조 달러를 넘었고 메타(+6.6%)·구글(+5.0%)·엔비디아(+3.2%)가 함께 강했어요. 장 마감 후 팰런티어가 2분기 실적 서프라이즈(매출 +93%, 연 가이던스 상향)로 시간외 +약 13% 급등했어요. 앱의 보유 빅테크 가격을 8/3 종가로 갱신했어요.",
 "impact":"positive",
 "ourImpact":"보유 빅테크 GOOG·AMZN·META·NVDA 동반 강세로 우호적. 오늘 밤 보유 종목 AMD 실적(장 마감 후)이 다음 변수예요.",
 "stockImpacts":"AMZN +4.5%(시총 3조달러) / META +6.6% / GOOG +5.0% / NVDA +3.2% / AMD +0.8%(오늘 밤 실적) / 그 외 보유 종목은 지수·섹터 기반 추정 반영"}
existing = st.get('2026-08-04', [])
# prepend capture if not present
if not any(e.get('label')=='미국 마감 캡처 (화)' for e in existing):
    st['2026-08-04'] = [cap] + existing
cal['lastUpdated'] = "2026-08-04T06:10:00+09:00"
json.dump(cal, open('calendar-events.json','w'), ensure_ascii=False, indent=1)
print("calendar 2026-08-04 events:", len(st['2026-08-04']))
