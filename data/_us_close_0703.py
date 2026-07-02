# -*- coding: utf-8 -*-
"""Mobri 06:00 KST 7/3 라이트 — 미국 7/2 정규장 마감 캡처."""
import json, shutil, datetime

BASE = "/sessions/funny-hopeful-gates/mnt/claude/portfolio-pwa/data"
NOW = "2026-07-03T06:00:00+09:00"

# ---- backups ----
shutil.copy(f"{BASE}/portfolio.json", f"{BASE}/portfolio.json.before-us-close-0703.bak")
shutil.copy(f"{BASE}/calendar-events.json", f"{BASE}/calendar-events.json.before-us-close-0703.bak")

# ticker -> (close_price, change1D_pct)
CLOSE = {
    'GOOG': (354.30, -1.00),
    'META': (582.90, -4.90),
    'AMZN': (242.67, 0.40),
    'NVDA': (194.83, -1.39),
    'TSM':  (434.16, -2.27),
    'AVGO': (360.45, -2.41),
    'MU':   (975.56, -5.49),
    'MRVL': (245.29, -9.84),
    'AMD':  (517.82, -4.26),
    'SNDK': (1808.68, -11.00),
    'DELL': (391.50, -7.94),
    'LITE': (714.38, -10.83),
    'CLS':  (329.28, -9.04),
    'CRDO': (245.80, -5.13),
    'TLN':  (373.40, 3.50),
}

# beginner-friendly today reasons
WHY = {
 'GOOG': "7/2 유럽 최고법원이 41억 유로(약 6조원) 과징금을 확정하면서 살짝 눌렸어요. 다만 낙폭은 -1% 안팎으로 크지 않았어요.",
 'META': "전날 '클라우드 사업 진출' 기대로 +9% 급등했던 게 하루 만에 되돌려지며 -4.9% 내렸어요. 저커버그가 사내 회의에서 'AI 개발이 기대만큼 빠르지 않다'고 말한 점도 부담이 됐어요.",
 'AMZN': "위성인터넷(Leo) 연내 상용화 소식에 +0.4%로 소폭 올랐어요. 이날 보유 빅테크 중 몇 안 되는 상승 종목이었어요.",
 'NVDA': "반도체가 이틀째 차익실현(오른 김에 일부 파는 것)에 눌렸지만 -1.4%로 상대적으로 선방했어요.",
 'TSM':  "반도체 약세에 -2.3% 내렸어요. 7/16 2분기 실적 발표가 다음 분기점이에요.",
 'AVGO': "AI 반도체 차익실현 흐름에 -2.4% 하락했어요.",
 'MU':   "메모리 대장주로서 이틀째 차익실현에 -5.5% 내렸어요. 다만 올해 상승폭이 워낙 커서 조정 성격이에요.",
 'MRVL': "AI 광통신·맞춤형 칩 대표주로 변동이 큰 종목인데, 이날 -9.8%로 보유 종목 중 낙폭이 가장 컸어요.",
 'AMD':  "AI 반도체 차익실현에 -4.3% 내렸어요. 정규장 이후 시간외에선 소폭(+0.2%) 반등했어요.",
 'SNDK': "메모리 열풍을 주도했던 종목이라, 이틀 합쳐 약 -20%(당일 -11%) 급락했어요. 그동안 많이 오른 데 따른 차익실현이에요.",
 'DELL': "AI 서버 대표주인데 -7.9% 급락했어요. 유통 파트너(Arrow)와의 계약 종료 소식과 반도체 약세가 겹쳤어요.",
 'LITE': "AI 데이터센터용 광통신 부품주로 변동이 큰데 -10.8% 급락했어요. 그동안 급등한 데 따른 차익실현이에요.",
 'CLS':  "AI 서버 조립 대표주로 -9.0% 급락했어요. AI 하드웨어 전반의 차익실현 흐름에 함께 휩쓸렸어요.",
 'CRDO': "AI 연결(광·구리) 칩 대표주로 변동이 큰데 -5.1% 내렸어요.",
 'TLN':  "원자력·전력주라, 기술주에서 빠져나온 돈이 들어오며 +3%대 강세를 보였어요. 방어적 성격이 부각됐어요.",
}

# recentNews prepend for the biggest movers
NEWS_PREPEND = {
 'META': {"date":"2026-07-02","headline":"META -4.9% $582.90 — 전날 +9% 급등분 하루 만에 되돌림","source":"CNBC","url":"https://www.cnbc.com/2026/07/02/metas-push-into-cloud-computing-means-wall-street-has-to-prepare-for-lower-margins.html"},
 'MU':   {"date":"2026-07-02","headline":"MU -5.5% $975.56 — 메모리 이틀째 차익실현","source":"TipRanks","url":"https://www.tipranks.com/news/why-mu-sndk-nvda-and-amd-stocks-are-falling-today"},
 'MRVL': {"date":"2026-07-02","headline":"MRVL -9.8% $245.29 — 보유 종목 중 최대 낙폭","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/articles/stock-market-news-july-2-132600808.html"},
 'AMD':  {"date":"2026-07-02","headline":"AMD -4.3% $517.82 — AI 반도체 차익실현(시간외 +0.2%)","source":"TipRanks","url":"https://www.tipranks.com/news/why-mu-sndk-nvda-and-amd-stocks-are-falling-today"},
 'SNDK': {"date":"2026-07-02","headline":"SNDK -11% — 이틀 합쳐 약 -20% 급락","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/articles/stock-market-news-july-2-132600808.html"},
 'DELL': {"date":"2026-07-02","headline":"DELL -7.9% $391.50 — Arrow 유통계약 종료 + 반도체 약세","source":"TheFly","url":"https://www.tipranks.com/news/the-fly/dell-ends-enterprise-computing-distribution-deal-with-arrow-crn-reports-thefly-news"},
 'LITE': {"date":"2026-07-02","headline":"LITE -10.8% $714.38 — 광통신 부품주 차익실현","source":"StockAnalysis","url":"https://stockanalysis.com/stocks/lite/"},
 'CLS':  {"date":"2026-07-02","headline":"CLS -9.0% $329.28 — AI 서버 조립주 급락","source":"CNBC","url":"https://www.cnbc.com/2026/07/01/chip-stocks-notched-record-rallies-in-second-quarter-start-q3-with-dud.html"},
 'CRDO': {"date":"2026-07-02","headline":"CRDO -5.1% $245.80 — AI 연결칩 차익실현","source":"CNBC","url":"https://www.cnbc.com/2026/07/01/chip-stocks-notched-record-rallies-in-second-quarter-start-q3-with-dud.html"},
}

# tickers whose close is an approximate/intraday-last capture
APPROX = {'GOOG','SNDK','DELL','LITE','CRDO','TLN'}

pf = json.load(open(f"{BASE}/portfolio.json", encoding="utf-8"))
for x in pf['us']:
    t = x['ticker']
    if t in CLOSE:
        price, chg = CLOSE[t]
        x['price'] = price
        x['change1D'] = chg
        x['todayWhy'] = WHY[t]
        if t in NEWS_PREPEND:
            rn = x.get('recentNews') or []
            # avoid dup if rerun
            if not rn or rn[0].get('headline') != NEWS_PREPEND[t]['headline']:
                rn.insert(0, NEWS_PREPEND[t])
            x['recentNews'] = rn
        if t in APPROX:
            x['dataQualityNote'] = "7/2 마감 직전~마감 시점의 최신 체결가 기준이라 공식 종가와 소폭 차이가 있을 수 있어요."
        else:
            x['dataQualityNote'] = None

pf['marketSession'] = "US_CLOSE"
pf['lastUpdated'] = NOW
pf['marketStatus'] = ("🔴 7/2(목) 미국 정규장 마감 — 다우 52,900.07(+1.14%) 사상 최고 마감. "
    "약한 6월 고용(NFP 5.7만)에 금리 부담이 줄자 은행·통신 등 비(非)기술주로 돈이 돌았어요. "
    "반면 반도체·AI 하드웨어는 이틀째 차익실현으로 나스닥 25,832.67(-0.80%), S&P 7,483.24(보합). "
    "보유주 중 MRVL -9.8%·SNDK -11%·LITE -10.8%·CLS -9%·DELL -7.9%·MU -5.5%가 크게 빠졌고, META는 전날 +9% 급등분을 되돌려 -4.9%. "
    "7/3(금)은 미국 독립기념일 휴장이에요.")
pf['holidayNote'] = ("🔴 7/2(목) 미국 정규장이 마감됐어요(종가 기준). 다우는 사상 최고지만, 그동안 많이 오른 반도체·AI 하드웨어는 이틀째 차익실현으로 하락했어요. "
    "7/3(금)은 미국 독립기념일 휴장이라 다음 미국 장은 7/6(월)에 열려요.")

json.dump(pf, open(f"{BASE}/portfolio.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("portfolio.json updated. tickers:", [(x['ticker'],x['price'],x['change1D']) for x in pf['us']])
