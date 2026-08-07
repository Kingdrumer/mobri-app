#!/usr/bin/env python3
import json, os, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOW="2026-08-08T08:30:00+09:00"

# 1) index.json — update 08-08 to full-morning
idx=json.load(open("reports/index.json"))
shutil.copy("reports/index.json","reports/index.json.bak-0808")
entry={
 "date":"2026-08-08",
 "title":"8월 8일 (토) 풀 모닝 — S&P 사상 최고, 광통신·팰런티어 급등 · 국내 반도체는 HBM 우려로 약세",
 "summary":"[풀 모닝 08:00 KST] 보유 15종목 8/7 금 확정 종가 정산. S&P500 7,757.64(+0.62%, 사상 최고)·나스닥 +1.30%. 광통신주 LITE +6.2%·CRDO +8.5% 급등, 델 +3.7%, 샌디스크 -3.7% 조정. 시그널: 한화에어로(방산·외인 5일 순매수)·SK하이닉스·한미반도체(루빈 HBM 축소 우려 약세)·팰런티어(2Q +93%)·AAOI(광통신). 다음 이벤트 8/12 CPI.",
 "session":"full-morning",
 "generatedAt":NOW,
}
idx["reports"]=[e for e in idx["reports"] if e["date"]!="2026-08-08"]+[entry]
idx["lastUpdated"]=NOW
json.dump(idx, open("reports/index.json","w"), ensure_ascii=False, indent=2)

# 2) calendar-events.json — add full-morning dot for 08-08
cal=json.load(open("calendar-events.json"))
shutil.copy("calendar-events.json","calendar-events.json.before-full-morning-0808.bak")
fm={
 "type":"morning-brief","label":"8/8 풀 모닝 브리핑","color":"green","mood":"🟢","time":"08:00 KST",
 "title":"🟢 8/8(토) 풀 모닝 — S&P 사상 최고·광통신 급등, 보유 15종목 8/7 금 종가 정산",
 "description":"8/7(금) 뉴욕 강세 마감(S&P500 +0.62% 사상 최고)을 기준으로 보유 15종목을 정산했어요. 광통신주 LITE(루멘텀) +6.2%·CRDO(크레도) +8.5%가 급등했고 델 +3.7%, 반면 샌디스크는 차익실현(오른 김에 파는 것)으로 -3.7% 내렸어요. 국내는 '루빈 GPU HBM(고대역폭 메모리) 축소' 우려로 SK하이닉스·한미반도체가 약세였어요.",
 "impact":"positive",
 "ourImpact":"보유 광통신·반도체주 전반이 8/7 우호적으로 마감했어요(NVDA +2.3%·MRVL +3.9%). 국내 HBM 우려는 보유 마이크론(MU)·샌디스크와 테마가 연결되니 8/12 미국 물가(CPI) 전까지 흐름을 지켜보면 좋아요.",
 "stockImpacts":[
   {"ticker":"LITE","name":"루멘텀","change":"+6.2%","note":"AI 데이터센터 광통신(빛으로 데이터 전송) 수요 기대 급등"},
   {"ticker":"CRDO","name":"크레도","change":"+8.5%","note":"광통신 칩 수요+실적 기대 급등"},
   {"ticker":"SNDK","name":"샌디스크","change":"-3.7%","note":"YTD +340% 뒤 차익실현 조정"},
 ],
}
cal["stock"]["2026-08-08"]=[e for e in cal["stock"].get("2026-08-08",[]) if e.get("type")!="morning-brief"]+[fm]
cal["lastUpdated"]=NOW
json.dump(cal, open("calendar-events.json","w"), ensure_ascii=False, indent=2)
print("index + calendar updated. index entries:",len(idx["reports"]),"| 08-08 cal events:",len(cal["stock"]["2026-08-08"]))
