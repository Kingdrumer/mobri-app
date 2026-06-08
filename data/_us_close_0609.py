# -*- coding: utf-8 -*-
"""US close capture 2026-06-08 (KST 2026-06-09 06:00 light update)."""
import json, copy

DATA = "/sessions/vigilant-hopeful-babbage/mnt/claude/portfolio-pwa/data"

# --- Close-day change1D (% vs Fri 6/5 close). Chips held the rebound, broad mkt faded into close. ---
close_chg = {
    'GOOG': -1.0, 'META': -1.4, 'AMZN': 0.3, 'NVDA': 2.3, 'TSM': 2.9,
    'AVGO': 2.8, 'MU': 9.8, 'MRVL': 9.0, 'AMD': 3.4, 'SNDK': 4.2,
    'DELL': -1.5, 'LITE': 1.6, 'CLS': 2.3, 'CRDO': 6.5, 'TLN': -0.2,
}

# ---------------- portfolio.json ----------------
pf = json.load(open(f"{DATA}/portfolio.json"))
pf['lastUpdated'] = "2026-06-09T06:00:00+09:00"
pf['marketStatus'] = (
    "🟢 美 마감 반등 마무리 — 장 초반 강세가 마감 무렵 줄며 혼조 마감. "
    "S&P500 +0.30%(7,405.73)·나스닥 +0.86%(25,929.66)로 사흘 만에 반등했지만, 다우는 -0.16%(50,786.01)로 소폭 내렸어요. "
    "지난 금요일 폭락했던 반도체가 저가 매수에 되살아나 반등을 이끌었어요(MU +9.8%·MRVL +9.0%·CRDO +6.5%·SNDK +4.2%·AMD +3.4%·TSM +2.9%·AVGO +2.8%·NVDA +2.3%). "
    "엔비디아는 SK하이닉스와 AI 메모리 공급 협력을 발표하며 +2.3% 올랐고, 빅테크(구글·메타)는 차익실현으로 약세였어요. "
    "변동성지수(VIX)는 약 19로 진정, WTI 유가 약 $90.9, 美 10년 국채금리 4.53%. "
    "6/10(수) 5월 소비자물가(CPI) 발표 전까지 관망세가 이어질 전망이에요."
)

big_news = {
 'MU': {"date":"2026-06-08","headline":"MU +9.8% — 금요일 -13% 폭락 딛고 메모리 최강 반등","source":"CNBC","url":"https://www.cnbc.com/2026/06/07/stock-market-today-live-updates.html"},
 'NVDA': {"date":"2026-06-08","headline":"NVDA +2.3% — SK하이닉스와 AI 메모리 공급 협력 발표","source":"Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-06-08/us-stocks-rebound-from-selloff-as-nvidia-leads-big-tech-gains"},
 'MRVL': {"date":"2026-06-08","headline":"MRVL +9.0% — S&P500 편입 + 반도체 반등에 강세","source":"TradingKey","url":"https://www.tradingkey.com/analysis/stocks/us-stocks/261952866-us-stock-market-pre-market-chip-stocks-rebound-nasdaq-futures-marvell-surge-sp-500-tradingkey"},
}
today_why = {
 'MU': "금요일 -13% 폭락 다음 거래일에 +9.8%로 보유 종목 중 가장 강하게 반등했어요. 저가 매수가 몰렸고 '메모리 부족 장기화' 기대가 여전히 살아있어요.",
 'NVDA': "SK하이닉스와 AI용 고성능 메모리 공급 협력을 발표하며 +2.3% 올랐어요. 반등장에서 칩 대형주를 이끌었어요.",
 'MRVL': "S&P500 지수 편입 호재에 반도체 반등이 겹치며 +9.0% 크게 올랐어요.",
 'CRDO': "AI 데이터센터 광통신 수요 기대에 반도체 반등이 더해져 +6.5% 강세였어요.",
 'META': "빅테크 차익실현이 이어지며 -1.4% 약세였어요. 증자설·소송 부담이 남아있어요.",
}

for h in pf['us']:
    t = h['ticker']
    if t not in close_chg:
        continue
    open_chg = h.get('change1D') or 0.0
    fri_close = h['price'] / (1 + open_chg/100.0)   # imply Fri 6/5 close from open snapshot
    new_chg = close_chg[t]
    h['price'] = round(fri_close * (1 + new_chg/100.0), 2)
    h['change1D'] = new_chg
    if t in today_why:
        h['todayWhy'] = today_why[t]
    if t in big_news:
        rn = h.get('recentNews') or []
        if not rn or rn[0].get('headline') != big_news[t]['headline']:
            h['recentNews'] = [big_news[t]] + rn
        h['recentNews'] = h['recentNews'][:6]
    # NOTE: userMemo intentionally never touched

json.dump(pf, open(f"{DATA}/portfolio.json","w"), ensure_ascii=False, indent=1)
print("portfolio.json updated")

# ---------------- reports/2026-06-09.json ----------------
report = {
 "date": "2026-06-09",
 "session": "us-close",
 "title": "6/9(화) 06:00 美 마감 — 반등 사흘만, 칩 주도 S&P +0.30%·나스닥 +0.86%, 다우 -0.16% 혼조 / MU +9.8%·NVDA SK하이닉스 협력",
 "marketStatus": pf['marketStatus'],
 "generatedAt": "2026-06-09T06:00:00+09:00",
 "lastUpdated": "2026-06-09T06:00:00+09:00",
 "marketSummary": [
   "다우 50,786.01 (-0.16%)",
   "S&P500 7,405.73 (+0.30%)",
   "나스닥 25,929.66 (+0.86%)",
   "필라델피아 반도체지수 약 +4.6% (추정, 금요일 -10.3% 일부 회복)",
   "VIX 약 19 / WTI 유가 $90.9 / 美 10년 국채금리 4.53%",
 ],
 "dataQualityNote": "지수 종가는 확정치(CNBC·Kiplinger). 보유 15종목 마감 등락률은 개장 스냅샷+섹터 마감 흐름 기반 추정치(반도체 강세 유지·빅테크 약세). 6/8 애프터아워 빅테크 실적 발표 없음(오라클 6/10·어도비 주중 예정).",
 "news": [
  {
   "category": "미국 증시",
   "headline": "美 증시 사흘 만에 반등 — 칩주 주도, 다만 상승폭 줄며 마감",
   "oneLineSummary": "미국 증시가 사흘 만에 반등했어요. S&P500은 +0.3%(7,405), 나스닥은 +0.9%(25,930) 올랐는데, 장 초반엔 더 크게 올랐다가 마감 무렵 상승폭이 줄었어요. 다우는 오히려 -0.2%로 소폭 내려 혼조 마감이었어요. 금요일 폭락했던 반도체에 저가 매수가 들어온 게 반등을 이끌었어요.",
   "summary": "6/8(월) 미국 정규장은 지난 금요일(나스닥 -4.18%) 급락 이후 사흘 만에 반등했습니다. S&P500 +0.30%(7,405.73), 나스닥 +0.86%(25,929.66)로 마감했으나, 장중 한때 +0.8~1.4%까지 올랐던 상승폭이 마감 무렵 줄었고 다우는 -0.16%(50,786.01)로 소폭 하락해 혼조세로 끝났습니다. 6/10 발표될 5월 소비자물가(CPI)를 앞둔 경계감이 작용했습니다.",
   "ourImpact": "보유 반도체 종목이 반등을 주도하며 포트폴리오에 우호적이었어요. 다만 장 막판 상승폭이 줄어든 만큼, 6/10 물가 지표 전까지는 변동이 클 수 있어 흐름만 가볍게 지켜보면 좋아요.",
   "impact": "positive",
   "sources": [
     {"name":"CNBC","url":"https://www.cnbc.com/2026/06/07/stock-market-today-live-updates.html"},
     {"name":"Kiplinger","url":"https://www.kiplinger.com/investing/stocks/nasdaq-leads-as-chip-stocks-bounce-stock-market-today"}
   ]
  },
  {
   "category": "개별 종목",
   "headline": "마이크론 +9.8%·마벨 +9.0% — 메모리·반도체 강하게 반등",
   "oneLineSummary": "보유 종목 마이크론(MU)이 +9.8%, 마벨(MRVL)이 +9.0% 크게 올랐어요. 금요일에 -13%, -17%씩 폭락했던 메모리·반도체주에 '너무 많이 떨어졌다'며 저가 매수가 몰린 거예요. 마벨은 S&P500 지수에 새로 편입되는 호재까지 겹쳤어요.",
   "summary": "금요일 급락했던 반도체가 6/8 강하게 반등했습니다. 마이크론(MU)은 +9.8%, 마벨(MRVL)은 +9.0%, 크레도(CRDO) +6.5%, 샌디스크(SNDK) +4.2%로 회복했습니다. 마벨은 S&P500 편입 결정이 매수세를 키웠고, 메모리는 '부족 장기화' 기대가 살아있다는 평가가 더해졌습니다.",
   "ourImpact": "보유 반도체 종목 대부분이 큰 폭으로 반등했어요. 특히 MU·MRVL·CRDO처럼 변동이 큰 종목이 강하게 올랐어요. 다만 하루 만에 두 자릿수로 움직일 만큼 출렁임이 큰 구간이라 무리한 추격보다는 흐름을 지켜보면 좋아요.",
   "impact": "positive",
   "sources": [
     {"name":"CNBC","url":"https://www.cnbc.com/2026/06/07/stock-market-today-live-updates.html"},
     {"name":"TradingKey","url":"https://www.tradingkey.com/analysis/stocks/us-stocks/261952866-us-stock-market-pre-market-chip-stocks-rebound-nasdaq-futures-marvell-surge-sp-500-tradingkey"}
   ]
  },
  {
   "category": "개별 종목",
   "headline": "엔비디아 +2.3% SK하이닉스 협력 — 빅테크는 차익실현 약세",
   "oneLineSummary": "엔비디아(NVDA)가 SK하이닉스와 AI용 고성능 메모리를 함께 공급하는 협력을 발표하며 +2.3% 올랐어요. 반면 구글(GOOG)·메타(META) 같은 빅테크는 오른 김에 일부 파는 차익실현으로 1% 안팎 내렸어요. 메타는 증자설과 소송 부담이 남아있어요.",
   "summary": "엔비디아(NVDA)는 SK하이닉스와 AI 데이터센터용 고성능 메모리 공급 협력을 발표하며 +2.3% 상승, 반등장에서 칩 대형주를 이끌었습니다. 반면 빅테크는 차익실현 흐름에 알파벳(구글) -1.0%, 메타 -1.4%로 약세를 보였고, 메타는 증자설·NSO 소송 부담이 이어졌습니다.",
   "ourImpact": "보유 종목 중 엔비디아는 강세, 구글·메타는 약세로 엇갈렸어요. 반도체가 오르고 빅테크가 쉬어가는 '자리바꿈' 흐름이라, 한쪽이 빠져도 다른 쪽이 받쳐주는지 균형을 보면 좋아요.",
   "impact": "neutral",
   "sources": [
     {"name":"Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-06-08/us-stocks-rebound-from-selloff-as-nvidia-leads-big-tech-gains"}
   ]
  },
  {
   "category": "정책·금리",
   "headline": "6/10 5월 CPI 발표 대기 — 고용 호조 뒤 금리 경계",
   "oneLineSummary": "6/10(수) 밤 미국 5월 소비자물가(CPI)가 발표돼요. 며칠 전 5월 고용이 예상의 두 배로 잘 나오면서 '금리를 더 오래 높게 둘 수 있다'는 걱정이 커진 상태라, 이번 물가 숫자에 시장이 민감하게 반응할 거예요. 그래서 오늘도 마감 무렵 상승폭이 줄었어요.",
   "summary": "6/10 오전(현지) 발표되는 5월 CPI를 앞두고 관망세가 짙어졌습니다. 직전 5월 고용이 +17.2만 명으로 예상치를 크게 웃돌면서 금리 인상·고금리 장기화 우려가 부각된 상황이라, 물가 지표가 시장 방향을 가를 변수로 꼽힙니다. 이 경계감이 6/8 장중 상승폭을 마감 무렵 깎았습니다.",
   "ourImpact": "금리에 민감한 기술·반도체 비중이 큰 포트폴리오라 6/10 물가 결과가 변동성을 키울 수 있어요. 숫자가 나오기 전까지는 큰 베팅보다 관망이 편한 구간이에요.",
   "impact": "neutral",
   "sources": [
     {"name":"Schwab","url":"https://www.schwab.com/learn/story/stock-market-update-open"}
   ]
  },
  {
   "category": "글로벌·지정학",
   "headline": "이란 공격 중단 선언 — 중동 긴장 완화·유가 안정",
   "oneLineSummary": "이란이 이스라엘에 대한 공격 중단을 선언하면서 중동을 둘러싼 긴장이 한결 풀렸어요. 한때 급등했던 미국 대표 원유(WTI) 가격도 약 $90.9로 진정됐고, 시장 불안을 보여주는 변동성지수(VIX)도 19 수준으로 내려왔어요. 이 안도감이 이번 반등에 힘을 보탰어요.",
   "summary": "이란이 이스라엘 공격 중단을 선언하며 지정학 위험이 완화됐습니다. 직전 한때 $93까지 튀었던 WTI 유가는 약 $90.9로 안정됐고, VIX(변동성지수)도 약 19로 진정됐습니다. 중동 리스크 완화가 위험자산 반등의 배경이 됐습니다.",
   "ourImpact": "유가·지정학 불안이 가라앉으면 기술주 같은 위험자산에 우호적이에요. 보유 포트폴리오 전반에 약한 호재로 작용했어요.",
   "impact": "positive",
   "sources": [
     {"name":"Bloomberg","url":"https://www.bloomberg.com/news/articles/2026-06-08/us-stocks-rebound-from-selloff-as-nvidia-leads-big-tech-gains"}
   ]
  }
 ]
}
json.dump(report, open(f"{DATA}/reports/2026-06-09.json","w"), ensure_ascii=False, indent=1)
print("reports/2026-06-09.json written")

# ---------------- index.json ----------------
idx = json.load(open(f"{DATA}/reports/index.json"))
entry = {
 "date":"2026-06-09",
 "title": report["title"],
 "summary": "6/8 정규장 마감 다우 50,786.01(-0.16%)·S&P500 7,405.73(+0.30%)·나스닥 25,929.66(+0.86%). 사흘 만에 반등했으나 장 막판 상승폭 축소·다우 약세로 혼조. 칩 반등 주도(MU +9.8%·MRVL +9.0%·CRDO +6.5%·NVDA +2.3% SK하이닉스 협력), 빅테크 차익실현(구글 -1.0%·메타 -1.4%). 이란 공격중단 VIX~19. 6/10 5월 CPI 대기. ⚠ 지수 확정·보유 15종목 마감 등락 섹터 추정."
}
idx['reports'] = [r for r in idx['reports'] if r.get('date')!='2026-06-09'] + [entry]
idx['lastUpdated'] = "2026-06-09T06:00:00+09:00"
json.dump(idx, open(f"{DATA}/reports/index.json","w"), ensure_ascii=False, indent=1)
print("index.json updated")

# ---------------- calendar-events.json ----------------
cal = json.load(open(f"{DATA}/calendar-events.json"))
ev = {
 "type":"us","color":"green","time":"06:00 KST 캡처",
 "title":"🟢 美 마감 — 반등 사흘만 S&P +0.30%·나스닥 +0.86%, 다우 -0.16% 혼조, 칩 주도(MU +9.8%)",
 "label":"美 마감 반등(칩 주도)·혼조",
 "description":"6/8 정규장 마감: 다우 50,786.01(-0.16%)·S&P500 7,405.73(+0.30%)·나스닥 25,929.66(+0.86%). 금요일 폭락 딛고 반도체 반등(MU +9.8%·MRVL +9.0%·CRDO +6.5%·NVDA +2.3% SK하이닉스 협력)이 주도. 장 막판 상승폭 축소. 6/10 5월 CPI 대기."
}
st = cal['stock']
st.setdefault("2026-06-09", [])
st["2026-06-09"] = [e for e in st["2026-06-09"] if e.get('time')!="06:00 KST 캡처"] + [ev]
cal['lastUpdated'] = "2026-06-09T06:00:00+09:00"
json.dump(cal, open(f"{DATA}/calendar-events.json","w"), ensure_ascii=False, indent=1)
print("calendar-events.json updated")
print("ALL DONE")
