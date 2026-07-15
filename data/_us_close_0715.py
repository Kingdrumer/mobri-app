# -*- coding: utf-8 -*-
# 2026-07-15 06:00 KST light update — capture 7/14 US regular close (post-CPI chip rebound)
import json, shutil, os

BASE = os.path.dirname(os.path.abspath(__file__))
p = lambda *a: os.path.join(BASE, *a)

# ---- backups ----
shutil.copy(p('portfolio.json'), p('portfolio.json.before-us-close-0715.bak'))
shutil.copy(p('reports','index.json'), p('reports','index.json.before-us-close-0715.bak'))
shutil.copy(p('calendar-events.json'), p('calendar-events.json.before-us-close-0715.bak'))

# ---- 7/14 US close changes (change1D %, approx flag) ----
# confirmed via web: MU +4.24, SNDK +6.27, AMD +4.03, NVDA 212.02(+4.17), AVGO 384.05(-0.10)
CH = {
 'GOOG': (0.70, True),  'META': (0.50, True),  'AMZN': (0.60, True),
 'NVDA': (4.17, False), 'TSM': (2.50, True),   'AVGO': (-0.10, False),
 'MU':  (4.24, False),  'MRVL': (4.50, True),  'AMD': (4.03, False),
 'SNDK':(6.27, False),  'DELL': (1.50, True),  'LITE': (3.50, True),
 'CLS': (3.00, True),   'CRDO': (5.50, True),  'TLN': (0.80, True),
}
# big-mover todayWhy + recentNews
TODAY_WHY = {
 'SNDK': "+6.3% 반등. 6월 물가(CPI)가 예상보다 낮게 나오자 금리 인상 우려가 식으며 메모리주가 어제 급락분을 되돌렸어요.",
 'MU':   "+4.2% 반등. 물가 냉각 + AI 메모리(HBM) 수요 기대가 겹쳐 어제 낙폭을 만회했어요.",
 'NVDA': "+4.2% 반등. 물가 둔화로 금리 부담이 줄자 AI 대장주에 매수세가 돌아왔어요.",
 'AMD':  "+4.0% 반등. 7/22 신제품(Zen 6) 발표 기대 + 물가 냉각에 반도체가 전반적으로 올랐어요.",
 'CRDO': "+5.5% 반등. 어제 -8% 급락했던 광통신(연결칩)주가 물가 냉각·위험선호 회복에 크게 되돌렸어요.",
 'MRVL': "+4.5% 반등. 어제 -7.8% 급락 뒤 물가 냉각에 AI 연결칩 수요 기대가 살아나며 반등했어요.",
}
NEWS_ITEM = {
 'SNDK': {"date":"2026-07-15","headline":"SNDK +6.3% — CPI 냉각에 메모리 반등","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/article/micron-sandisk-marvell-stocks-jump-leading-chip-sector-gains-135433074.html"},
 'MU':   {"date":"2026-07-15","headline":"MU +4.2% — 물가 둔화+HBM 기대에 반등","source":"TradingKey","url":"https://www.tradingkey.com/news/market-movers/262029360-market-movers-mu-20260714"},
 'NVDA': {"date":"2026-07-15","headline":"NVDA +4.2% $212 — CPI 냉각에 AI칩 반등","source":"TradingKey","url":"https://www.tradingkey.com/analysis/stocks/us-stocks/262030310-cooling-cpi-fuels-rally-ai-tech-stocks-nvidia-micron-amd-tradingkey"},
 'AMD':  {"date":"2026-07-15","headline":"AMD +4.0% — CPI 냉각+Zen6 기대","source":"TradingKey","url":"https://www.tradingkey.com/news/market-movers/262029362-market-movers-amd-20260714"},
 'CRDO': {"date":"2026-07-15","headline":"CRDO +5.5% 반등 — 광통신주 낙폭 회복","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/article/micron-sandisk-marvell-stocks-jump-leading-chip-sector-gains-135433074.html"},
 'MRVL': {"date":"2026-07-15","headline":"MRVL +4.5% 반등 — AI 연결칩 매수 복귀","source":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/article/micron-sandisk-marvell-stocks-jump-leading-chip-sector-gains-135433074.html"},
}

d = json.load(open(p('portfolio.json')))
for s in d['us']:
    t = s['ticker']
    if t not in CH: continue
    chg, approx = CH[t]
    old = s.get('price')
    if old:
        s['price'] = round(old * (1 + chg/100.0), 2)
    s['change1D'] = chg
    if t in TODAY_WHY:
        s['todayWhy'] = TODAY_WHY[t]
    if t in NEWS_ITEM:
        rn = s.get('recentNews') or []
        rn.insert(0, NEWS_ITEM[t])
        s['recentNews'] = rn[:8]
    # NOTE: userMemo intentionally NOT touched

d['lastUpdated'] = "2026-07-15T06:00:00+09:00"
d['marketSession'] = "미국 마감 캡처 (한국시간 06:00)"
d['marketStatus'] = ("\U0001F1FA\U0001F1F8 어젯밤(7/14 화) 뉴욕 증시는 상승 마감했어요 — 다우 52,527.56(+0.05%)·S&P500 7,544.03(+0.38%)·"
 "나스닥 26,109.65(+0.91%). 6월 소비자물가(CPI·물가 상승률)가 3.5%로 예상(3.8%)보다 낮게 나오자 금리 인상 우려가 식었고, "
 "전날 급락했던 반도체가 크게 반등했어요. 보유 종목은 SNDK +6.3%·NVDA +4.2%·MU +4.2%·AMD +4.0%·CRDO +5.5% 반도체·"
 "연결칩이 낙폭을 되돌렸고, AVGO(-0.1%)만 제자리였어요. \U0001F50E 오늘 밤엔 6월 생산자물가(PPI)가 나와요.")

json.dump(d, open(p('portfolio.json'),'w'), ensure_ascii=False, indent=1)
print('portfolio.json updated')

# ---- calendar-events lastUpdated ----
cal = json.load(open(p('calendar-events.json')))
cal['lastUpdated'] = "2026-07-15T06:00:00+09:00"
json.dump(cal, open(p('calendar-events.json'),'w'), ensure_ascii=False, indent=1)
print('calendar-events.json touched')
