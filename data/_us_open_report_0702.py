import json

NOW = "2026-07-02T22:45:00+09:00"

# ---------- REPORT ----------
r = json.load(open("reports/2026-07-02.json"))
r["lastUpdated"] = NOW
r["session"] = "US_OPEN"

# marketSummary -> open prices
ms = r["marketSummary"]
ms["dow"] = {"close": 52612.86, "change": 0.6, "note": "22:30 개장가 — 약한 고용에 강보합 출발"}
ms["sp500"] = {"close": 7519.62, "change": 0.49, "note": "22:30 개장가"}
ms["nasdaq"] = {"close": 26121.10, "change": 0.31, "note": "22:30 개장가 — 반도체 반등에 상승 전환"}
ms["vix"] = {"close": 16.07, "change": -3.1, "note": "공포지수 — 낮을수록 안정. 16선 초반 안정권"}
ms["wti"] = {"price": 67.72, "change": -1.25, "note": "WTI(미국 대표 원유). 수요 둔화 우려로 소폭 하락"}
ms["ust10y"] = {"yield": 4.49, "change": 0.27, "note": "미 10년 국채 금리. 약한 고용에도 소폭 상승"}

# open-capture news (prepend, category order)
open_news = [
 {
  "category": "정책·금리",
  "headline": "6월 미국 일자리 5.7만 명 증가, 예상 11.3만 명 크게 밑돌아",
  "oneLineSummary": "미국에서 6월 한 달간 늘어난 일자리가 5만7천 개로, 시장이 예상한 11만3천 개의 절반 수준밖에 안 됐어요. 실업률은 4.2%로 예상(4.3%)보다 살짝 낮았고요. 최근 3개월간 탄탄하던 고용이 한풀 꺾인 신호라, 미국 중앙은행(Fed)이 금리를 더 올릴 필요가 줄었다는 해석에 시장은 오히려 안도하는 분위기예요.",
  "summary": "미 노동부가 7/2 21:30 KST(현지 8:30) 발표한 6월 비농업 신규 고용(NFP, 한 달간 늘어난 일자리 수)이 5.7만 명으로 시장 평균 예상치(컨센서스) 11.3만 명을 크게 하회했습니다. 실업률은 4.2%로 예상(4.3%)을 소폭 밑돌았습니다. 3개월 연속 강했던 고용이 둔화하며, Fed가 금리를 서둘러 올릴 명분이 약해졌다는 해석에 지수 선물이 개장 전 반등했습니다. 다만 케빈 워시 Fed 의장이 '연내 금리 인상 가능성'을 열어둔 상태라 시장은 데이터를 계속 주시하는 분위기입니다.",
  "ourImpact": "금리 부담이 줄면 변동이 큰 성장주에 우호적이라, 전날 급락했던 반도체 보유주(MU·TSM·NVDA)의 반등에 힘을 실었어요. 반면 금리 영향을 덜 받는 전력주 TLN(탈렌에너지)도 저가 매수에 +3% 반등하며 상대적으로 안정적인 흐름을 보이고 있어요.",
  "impact": "positive",
  "sources": [
   {"name": "CNBC", "url": "https://www.cnbc.com/2026/07/01/stock-market-today-live-updates.html"},
   {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/markets/live/stock-market-today-thursday-july-2-223136955.html"}
  ]
 },
 {
  "category": "미국 증시",
  "headline": "미 정규장 강보합 출발 — 반도체 반등·메타 차익실현 '순환매 되돌림'",
  "oneLineSummary": "미국 증시가 22:30 개장 직후 S&P500 +0.5%, 다우 +0.6%, 나스닥 +0.3%로 강보합 출발했어요. 어제 크게 빠졌던 반도체가 저가 매수로 반등하고, 반대로 어제 +8.8% 급등했던 메타는 오른 김에 파는 차익실현에 -2%대로 숨을 고르는 '순환매 되돌림' 흐름이에요. 7/3 독립기념일 휴장을 앞둔 단축 주간이라 거래량은 적은 편이에요.",
  "summary": "7/2 22:30 KST 미 정규장이 강보합으로 출발했습니다. 약한 6월 고용지표로 금리 부담이 완화되며 위험자산 선호가 살아났고, 전날 필라델피아 반도체지수를 -6%대 끌어내렸던 메모리·반도체가 저가 매수로 반등했습니다(MU +1.1%·TSM +1.1%). 반대로 전날 +8.8% 급등한 메타는 차익실현에 -2%대 조정을 받으며 어제와 정반대의 순환매가 나타났습니다. VIX는 16.1로 안정권입니다.",
  "ourImpact": "보유 종목이 순환매 양쪽에 걸쳐 있어요. 반도체(MU·TSM·NVDA)는 반등하고, 어제 급등했던 메타(META)는 -2%대 되돌림 중이에요. 전체적으로는 어제 급락분을 일부 만회하는 안정적 출발이라 흐름을 가볍게 지켜보면 좋아요.",
  "impact": "positive",
  "sources": [
   {"name": "CNBC", "url": "https://www.cnbc.com/2026/07/01/stock-market-today-live-updates.html"}
  ]
 },
 {
  "category": "개별 종목",
  "headline": "델(DELL) -4%대 — 메모리 값 상승에 '서버 원가 부담' 우려로 등급 하향",
  "oneLineSummary": "보유 종목 델(DELL)이 개장 직후 -4%대로 가장 크게 밀렸어요. 최근 메모리 반도체 값이 오르면서 델이 만드는 AI 서버의 부품 원가가 올라 이익이 눌릴 수 있다는 걱정에, 모건스탠리가 투자 매력 등급을 낮췄기(다운그레이드) 때문이에요. 올해 200% 넘게 오른 만큼 차익실현도 겹쳤어요.",
  "summary": "델 테크놀로지스(DELL)가 7/2 개장 직후 -4%대로 하락했습니다. 메모리 반도체 가격 상승이 AI 서버 원가 부담으로 이어질 수 있다는 모건스탠리의 투자의견 하향(다운그레이드)이 배경입니다. 델은 지난 분기 AI 서버 매출이 급증했지만, 2월 이후 200% 넘게 오른 뒤라 밸류에이션 부담과 차익실현 매물이 겹쳤습니다.",
  "ourImpact": "델(DELL)은 보유 종목 중 오늘 낙폭이 가장 커요. 메모리 값 상승이 서버·부품 제조사엔 원가 부담이 될 수 있다는 점에서, 같은 하드웨어 조립주인 CLS(셀레스티카)에도 비슷한 심리가 번질 수 있어 함께 지켜보면 좋아요.",
  "impact": "negative",
  "sources": [
   {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/quote/DELL/"},
   {"name": "Stocktwits", "url": "https://stocktwits.com/news-articles/markets/equity/why-did-dell-technologies-tumble-5-percent-pre-market-today/cLPkvbDREIw"}
  ]
 },
]

r["news"] = open_news + r.get("news", [])
json.dump(r, open("reports/2026-07-02.json", "w"), ensure_ascii=False, indent=2)
print("report updated, news count:", len(r["news"]))

# ---------- CALENDAR ----------
c = json.load(open("calendar-events.json"))
c["lastUpdated"] = NOW
nfp_event = {
 "type": "indicator",
 "label": "6월 고용보고서 — 예상 하회",
 "color": "green",
 "time": "21:30 KST",
 "title": "6월 비농업 신규 고용(NFP) 5.7만 명 — 예상 11.3만 명 크게 하회",
 "description": "6월 미국 일자리 5.7만 명 증가로 예상(11.3만)의 절반 수준. 실업률 4.2%(예상 4.3%).",
 "impact": "고용이 예상보다 크게 약하게 나오면서 Fed(미국 중앙은행) 금리 인상 부담이 완화됐어요. 금리 인하 기대가 살아나면 변동이 큰 성장주에 우호적이에요. 다만 워시 의장이 연내 인상 가능성을 열어둬 시장은 데이터를 계속 주시해요.",
 "ourImpact": "금리 부담 완화로 전날 급락한 반도체(MU·TSM·NVDA) 반등에 우호적. 금리 영향 덜 받는 전력주 TLN도 반등.",
 "stockImpacts": [
  {"ticker": "MU", "tone": "positive", "magnitude": "+1%대", "text": "금리 부담 완화 + 저가 매수로 반등"},
  {"ticker": "TSM", "tone": "positive", "magnitude": "+1%대", "text": "반도체 낙폭 과대 반등"},
  {"ticker": "NVDA", "tone": "neutral", "magnitude": "보합", "text": "급락 뒤 안정 시도"},
  {"ticker": "TLN", "tone": "positive", "magnitude": "+3%", "text": "금리 영향 적은 전력주 반등"},
  {"ticker": "DELL", "tone": "negative", "magnitude": "-4%대", "text": "등급 하향 별도 악재(고용과 무관)"},
 ],
}
day = c["stock"].get("2026-07-02", [])
day.append(nfp_event)
c["stock"]["2026-07-02"] = day
json.dump(c, open("calendar-events.json", "w"), ensure_ascii=False, indent=2)
print("calendar updated, 7/2 events:", len(c["stock"]["2026-07-02"]))
