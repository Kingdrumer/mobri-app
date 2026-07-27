#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, shutil, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
shutil.copy('reports/2026-07-27.json', 'reports/2026-07-27.json.bak-open0727')
shutil.copy('calendar-events.json', 'calendar-events.json.before-open-0727.bak')

NOW = "2026-07-27T22:45:00+09:00"

# ---------- report ----------
r = json.load(open('reports/2026-07-27.json', encoding='utf-8'))

open_news = [
 {
  "category": "미국 증시",
  "headline": "美 증시 상승 출발 — S&P +0.6%·나스닥 약 +1%·다우 +0.8%, 유가 급락에 위험자산 반등",
  "oneLineSummary": "미국 3대 지수가 모두 올라 출발했어요. 주말에 미국과 이란이 서로 공격을 멈추면서 국제 유가가 5% 가까이 급락했고(WTI 배럴당 $84.9), 물가 걱정이 줄어든 덕분에 기술주 중심으로 반등했어요. 공포지수(VIX)도 17.8로 떨어져 시장이 한결 안정된 모습이에요.",
  "summary": "7/27 미국 정규장(22:30 KST) 개장 직후 S&P500은 약 7,455(+0.6%), 나스닥 종합 약 +1%, 다우 +0.8%로 3대 지수가 동반 상승 출발했습니다. 주말 미국·이란의 상호 공격 중단으로 브렌트유가 한때 -7%, WTI가 $84.9(-5% 안팎)까지 급락하며 인플레이션·금리 부담 완화 기대가 위험자산 반등을 견인했고, VIX는 17.8(-4%대)로 하락했습니다.",
  "ourImpact": "유가 하락과 위험자산 선호로 보유 15개 종목 대부분이 상승 출발했어요. 특히 지난주 크게 밀렸던 반도체·메모리주(MU·SNDK·LITE)가 저가 매수로 +3% 안팎 반등했어요. 다만 이번 주 빅테크 실적과 FOMC가 몰려 있어 변동은 커질 수 있어요.",
  "impact": "positive",
  "sources": [
   {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/markets/live/stock-market-today-monday-july-27-dow-sp-500-nasdaq-080412540.html"},
   {"name": "Schwab", "url": "https://www.schwab.com/learn/story/stock-market-update-open"}
  ]
 },
 {
  "category": "정책·금리",
  "headline": "6월 내구재 주문 +1.6%, 예상 부합 — 기업 투자 견조",
  "oneLineSummary": "미국의 6월 내구재(오래 쓰는 비싼 물건, 예: 기계·비행기) 주문이 한 달 전보다 1.6% 늘었어요. 시장이 예상한 것과 딱 맞았고, 5월에 크게 줄었던(-4.5%) 걸 되돌린 결과예요. 기업들이 미래를 보고 투자를 이어간다는 신호라 경기가 아직 튼튼하다는 뜻이에요.",
  "summary": "미국 상무부가 7/27 21:30 KST(8:30 ET) 발표한 6월 내구재 주문이 전월 대비 +1.6%로 시장 컨센서스(시장 평균 예상치)에 부합했습니다. 운송 제외 +0.9%(예상 +0.8% 상회), 기업 투자 대리지표인 비국방 자본재(항공 제외) 주문은 +1.4%로 견조했습니다. 5월 -4.5% 급감을 상당 부분 되돌렸습니다.",
  "ourImpact": "경기가 튼튼하다는 신호는 실적을 앞둔 기술·AI 인프라 종목에 나쁘지 않아요. 다만 경기가 너무 좋으면 미국 중앙은행(Fed)이 금리 인하를 미룰 수 있어, 금리에 민감한 성장주(NVDA·AMD)엔 양날의 검이에요. 전력주 TLN(탈렌에너지)은 금리 영향을 덜 받는 편이에요.",
  "impact": "neutral",
  "sources": [
   {"name": "Investing.com", "url": "https://m.investing.com/news/stock-market-news/durable-goods-orders-headline-economic-data-due-monday-93CH-4812368"},
   {"name": "US Census Bureau", "url": "https://www.census.gov/manufacturing/m3/adv/pdf/durgd.pdf"}
  ]
 },
 {
  "category": "개별 종목",
  "headline": "반도체 저가매수 반등 — MU·SNDK·LITE +3% 안팎, NVDA는 차익실현에 -0.5%",
  "oneLineSummary": "지난주 크게 밀렸던 반도체·메모리 종목에 '싸졌으니 사자'는 저가 매수가 몰리며 마이크론(MU)·샌디스크(SNDK)·루멘텀(LITE)이 3% 안팎 올라 출발했어요. 반대로 엔비디아(NVDA)는 최근 많이 오른 만큼 차익 실현이 나와 -0.5%로 홀로 약보합이었어요. 브로드컴(AVGO)은 삼성과 대형 AI칩 협력 소식에 +2%대 반등했어요.",
  "summary": "개장 직후 보유 반도체주가 반등했습니다. MU +2.1%·SNDK +3.0%·LITE +3.1%·CRDO +2.7%·TSM +1.2%·AVGO +2.1%(삼성전자와 5년·2000억 달러 AI칩 협력 호재). 반면 NVDA는 SK하이닉스·OpenAI 협력 소식에도 차익 실현으로 -0.5%, AMD는 +0.7%로 차분했습니다. 오늘 밤 마감 후 CLS(셀레스티카) 2분기 실적이 예정돼 있습니다.",
  "ourImpact": "보유 반도체·메모리 종목 대부분이 저가 매수로 반등해 앱 신호가 초록(green)으로 바뀐 곳이 많아요. 다만 월간 기준으로는 여전히 많이 빠져 있는 종목(MRVL·SNDK·CLS)도 있어 흐름을 이어갈지 지켜보면 좋아요. 오늘 밤 CLS 실적이 첫 관문이에요.",
  "impact": "positive",
  "sources": [
   {"name": "StockAnalysis", "url": "https://stockanalysis.com/stocks/mu/"},
   {"name": "Barron's", "url": "https://www.barrons.com/articles/stock-movers-ed57540c"}
  ]
 }
]

r['news'] = open_news + r['news']
r['lastUpdated'] = NOW
r['marketStatus'] = "미국 정규장 개장 (22:30 KST)"
r['marketSummary'] = ("미국 증시가 상승 출발했어요. 개장 직후 S&P500 약 7,455(+0.6%)·나스닥 종합 약 +1%·다우 +0.8%로 "
 "3대 지수가 모두 올랐고, 공포지수 VIX는 17.8로 4%대 떨어졌어요. 주말 사이 미국과 이란이 상호 공격을 멈추면서 국제 유가가 "
 "급락한 게(WTI 배럴당 $84.9, -5% 안팎; 브렌트 한때 -7%) 위험자산 반등을 이끌었어요. 지난 금요일(7/24) 종가는 다우 51,947·"
 "S&P 7,412·나스닥 24,976이었어요. 오늘 21:30 발표된 6월 내구재 주문은 +1.6%로 예상에 부합했어요. 이번 주는 오늘 밤 "
 "셀레스티카(CLS)를 시작으로 빅테크 실적이 줄줄이 나오고, 수요일(7/29) FOMC(미국 금리 결정)까지 겹친 여름 최대 이벤트 주간이에요.")

if isinstance(r.get('indices'), dict):
    r['indices'] = {
      "dow":    {"value": "약 52,360", "change": "+0.8%", "note": "7/27 개장 직후 근사치 (금 종가 51,947.25)"},
      "sp500":  {"value": "약 7,455",  "change": "+0.6%", "note": "7/27 개장 직후 (금 종가 7,411.98)"},
      "nasdaq": {"value": "약 25,230", "change": "+1.0%", "note": "7/27 개장 직후 근사치 (금 종가 24,975.82)"},
      "vix":    {"value": "17.8", "change": "-4%대", "note": "공포지수 하락 = 불안 완화"},
      "wti":    {"value": "$84.9", "change": "-5% 안팎", "note": "중동 완화로 급락 (브렌트 한때 -7%)"},
      "us10y":  {"value": "약 4.66%", "change": "소폭 하락", "note": "금 4.68% → 유가 하락에 소폭 진정"},
      "note": "미국 정규장 개장 직후(월 22:30~ KST). 지수 레벨은 개장 초 근사치, 개별 15종목 가격은 StockAnalysis 실시간/프리마켓으로 검증했어요."
    }

json.dump(r, open('reports/2026-07-27.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("report news now:", len(r['news']))

# ---------- calendar ----------
c = json.load(open('calendar-events.json', encoding='utf-8'))
day = c['stock'].setdefault('2026-07-27', [])

indicator = {
 "type": "indicator",
 "label": "6월 내구재 주문 +1.6% (예상 부합)",
 "color": "green",
 "mood": "🟢",
 "time": "21:30 KST",
 "title": "🟢 6월 내구재 주문 +1.6% — 시장 예상치에 부합, 기업 투자 견조",
 "description": "미국 6월 내구재(오래 쓰는 비싼 물건: 기계·항공기 등) 주문이 전월 대비 +1.6%로 예상과 일치했어요. 5월 -4.5% 급감을 상당 부분 되돌렸고, 기업 투자 대리지표(비국방 자본재, 항공 제외)도 +1.4%로 견조했어요.",
 "impact": "내구재 주문(기업·소비자가 오래 쓰는 고가 제품 신규 주문)이 예상에 부합하며 미국 제조·투자 경기가 견조함을 시사했어요. 경기 견조는 위험자산에 우호적이지만, 너무 강하면 Fed(미국 중앙은행)의 금리 인하 시점이 늦춰질 수 있어 성장주엔 양날의 검이에요.",
 "ourImpact": "경기 견조 신호로 실적을 앞둔 보유 기술·AI 인프라 종목엔 배경이 나쁘지 않아요. 금리 민감한 NVDA·AMD는 인하 지연 우려가 있고, 전력주 TLN은 상대적으로 금리 영향이 덜해요.",
 "stockImpacts": [
   {"ticker": "DELL", "tone": "positive", "magnitude": "+1~2%", "text": "기업 IT·서버 투자 견조 신호 — 개장 프리마켓 +1.6%"},
   {"ticker": "NVDA", "tone": "neutral", "magnitude": "-0.5%", "text": "금리 인하 지연 우려로 성장주 부담 — 개장 -0.5% 약보합"},
   {"ticker": "TLN",  "tone": "neutral", "magnitude": "+0.9%", "text": "전력주로 금리 영향 상대적으로 덜함"}
 ]
}

open_event = {
 "type": "market",
 "label": "월 22:30 KST 미국 정규장 개장 — 🟢 3대 지수 상승 출발, 반도체 저가매수 반등",
 "color": "green",
 "mood": "🟢",
 "time": "22:45 KST 개장 캡처",
 "title": "🟢 미국 개장(7/27) — S&P +0.6%·나스닥 약 +1%·다우 +0.8%, 유가 급락에 위험자산 반등",
 "description": "미국 3대 지수가 모두 올라 출발했어요. 주말 미국·이란 공격 중단으로 국제 유가가 급락(WTI $84.9, -5% 안팎)하고 물가 걱정이 줄면서 기술주 중심 반등이 나왔어요. 공포지수 VIX는 17.8로 떨어졌어요. 보유 15개 종목 가격을 실시간 시세로 정정·최신화했어요(직전 값은 목요일 급락 이전 시세가 남아 있었음).",
 "impact": "유가 급락 → 인플레이션·금리 부담 완화 → 성장주(기술주) 우호적. 다만 수요일 FOMC(7/29)와 빅테크 실적(META·MSFT 7/29, AMZN·AAPL 7/30)을 앞둔 경계감이 공존해요.",
 "ourImpact": "보유 종목 대부분 상승 출발 — 특히 지난주 급락했던 MU·SNDK·LITE·CRDO가 +3% 안팎 반등했고 AVGO는 삼성 협력 호재로 +2%대. NVDA만 차익 실현으로 -0.5% 약보합이에요. 오늘 밤 마감 후 CLS 실적이 이번 주 실적 릴레이의 첫 관문이에요.",
 "stockImpacts": [
   {"ticker": "SNDK", "tone": "positive", "magnitude": "+3.0%", "text": "낸드 메모리 저가매수 반등(프리마켓)"},
   {"ticker": "LITE", "tone": "positive", "magnitude": "+3.1%", "text": "광통신 부품 저가매수 반등(프리마켓)"},
   {"ticker": "MU",   "tone": "positive", "magnitude": "+2.1%", "text": "메모리 저가매수 반등(프리마켓)"},
   {"ticker": "AVGO", "tone": "positive", "magnitude": "+2.1%", "text": "삼성전자 5년 AI칩 협력 호재(프리마켓)"},
   {"ticker": "GOOG", "tone": "positive", "magnitude": "+2.3%", "text": "낙폭 회복하며 반등 개장"},
   {"ticker": "NVDA", "tone": "negative", "magnitude": "-0.5%", "text": "차익 실현에 홀로 약보합 개장"},
   {"ticker": "CLS",  "tone": "neutral", "magnitude": "+0.9%", "text": "오늘 밤 2분기 실적 발표 대기"}
 ]
}

day.append(indicator)
day.append(open_event)
c['lastUpdated'] = NOW
json.dump(c, open('calendar-events.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("calendar 2026-07-27 events now:", len(c['stock']['2026-07-27']))
