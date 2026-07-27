#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""US open capture 2026-07-27 22:30 KST — verified via StockAnalysis(CBOE/S&P), Investing.com cross."""
import json, shutil, datetime, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
shutil.copy('portfolio.json', 'portfolio.json.bak-open0727')

NOW = "2026-07-27T22:45:00+09:00"

# ticker: (current_price, friday_close, session, source_time_ET, signal, todayWhy)
DATA = {
 "GOOG": (326.34, 319.09, "open", "9:31", "green",
   "중동 긴장 완화로 유가가 급락하면서 위험자산이 반등했고, 지난 목요일 실적 후 급락했던 낙폭을 되돌리며 +2%대로 올라 개장했어요."),
 "META": (605.05, 595.19, "open", "9:33", "green",
   "이번 주 수요일(7/29) 실적 발표를 앞두고 저가 매수가 들어오면서 +1.7%로 올라 출발했어요. 유가 하락도 투자심리에 힘을 보탰어요."),
 "AMZN": (234.69, 232.11, "open", "9:40", "green",
   "중동 완화·유가 급락에 위험자산이 반등하며 +1%대로 올라 개장했어요. 목요일(7/30) 실적 발표가 대기 중이에요."),
 "NVDA": (205.76, 206.84, "open", "9:35", "yellow",
   "SK하이닉스·OpenAI 관련 대형 협력 소식이 이어졌지만, 최근 많이 오른 만큼 차익 실현이 나오며 -0.5%로 약보합 출발했어요."),
 "TSM": (408.40, 403.41, "premarket", "9:18", "green",
   "반도체 저가 매수가 유입되며 프리마켓에서 +1%대로 올랐어요. 금요일 큰 하락(-2.9%)을 일부 되돌리는 흐름이에요."),
 "AVGO": (389.87, 381.92, "premarket", "9:11", "green",
   "삼성전자와 5년·2000억 달러 규모 AI칩 협력 소식이 호재로 작용해 프리마켓에서 +2%로 반등했어요."),
 "MU": (940.00, 920.95, "premarket", "9:18", "green",
   "메모리 반도체에 저가 매수가 몰리며 프리마켓에서 +2%대로 반등했어요. 금요일 -7% 급락분을 일부 회복하는 모습이에요."),
 "MRVL": (196.94, 194.23, "open", "9:33", "green",
   "AI 인프라 반도체 저가 매수세에 +1.4%로 올라 개장했어요. 금요일 큰 조정 뒤 반등 시도예요."),
 "AMD": (525.49, 521.95, "open", "9:36", "yellow",
   "지난주 AI 행사 이후 목표주가 상향이 이어졌지만, 반도체가 전반적으로 강한 가운데 AMD는 +0.7%로 상대적으로 차분하게 출발했어요."),
 "SNDK": (1480.00, 1436.56, "premarket", "9:18", "green",
   "금요일 -10.8% 급락했던 낸드 메모리주가 저가 매수에 프리마켓 +3%로 강하게 반등했어요."),
 "DELL": (444.40, 437.50, "premarket", "9:05", "green",
   "AI 서버 수요 기대에 프리마켓에서 +1.6%로 올랐어요. 최근 조정 뒤 반등 흐름이에요."),
 "LITE": (786.43, 762.99, "premarket", "5:30", "green",
   "광통신 부품주가 저가 매수에 프리마켓 +3%로 반등했어요. 금요일 큰 하락(-8.5%)을 일부 되돌렸어요."),
 "CLS": (308.00, 305.28, "open", "9:32", "yellow",
   "오늘 밤(미국 장 마감 후) 2분기 실적 발표를 앞두고 +0.9%로 소폭 올라 개장했어요. 결과에 따라 변동이 커질 수 있어요."),
 "CRDO": (218.96, 213.15, "premarket", "8:32", "green",
   "AI 연결(커넥티비티) 반도체가 저가 매수에 프리마켓 +2.7%로 반등했어요. 변동이 큰 종목이라 등락 폭이 커요."),
 "TLN": (363.22, 359.90, "premarket", "8:24", "yellow",
   "전력·원자력 발전주로, 유가 급락 속에서도 프리마켓 +0.9%로 소폭 올랐어요. 금리 영향을 덜 받아 상대적으로 차분해요."),
}

d = json.load(open('portfolio.json', encoding='utf-8'))

def rebase(old_price, old_pct, new_price):
    base = old_price / (1 + old_pct/100.0)
    return round((new_price/base - 1)*100, 2)

changed = 0
for s in d['us']:
    t = s['ticker']
    if t not in DATA: continue
    price, fri, sess, tm, sig, why = DATA[t]
    old_price = s['price']
    s['price'] = price
    s['change1D'] = round((price - fri)/fri*100, 2)
    # rebase weekly/monthly/YTD off preserved historical baselines
    s['change1W'] = rebase(old_price, s.get('change1W',0), price)
    s['change1M'] = rebase(old_price, s.get('change1M',0), price)
    s['changeYTD'] = rebase(old_price, s.get('changeYTD',0), price)
    s['signal'] = sig
    s['todayWhy'] = why
    s['priceSourcedFrom'] = ["StockAnalysis(CBOE·S&P)", "Investing.com교차"]
    if sess == "premarket":
        s['dataQualityNote'] = f"개장 직전 프리마켓 시세({tm} ET) 기준 · 전일(7/24) 종가 대비"
    else:
        s['dataQualityNote'] = None
    changed += 1

d['lastUpdated'] = NOW
d['marketSession'] = "미국 정규장 개장 (22:30 KST / 9:30 ET)"
d['holidayNote'] = None
# note top-level data-quality context (do not touch per-stock 'note','outlook','recentNews',etc.)
d['dataNote'] = ("가격·change1D는 StockAnalysis(CBOE·S&P Global) 실시간/프리마켓 시세로 재검증(Investing.com 교차). "
                 "직전 저장값이 목요일 AI-capex 급락 이전 시세로 남아 있어 실제 시장가로 정정함. "
                 "change1W/M/YTD는 보존된 과거 기준가로 재계산한 근사치.")

json.dump(d, open('portfolio.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"updated {changed} tickers")
for s in d['us']:
    print(f"  {s['ticker']:5} {s['price']:>9} 1D={s['change1D']:>6} W={s['change1W']:>7} M={s['change1M']:>7} YTD={s['changeYTD']:>7} {s['signal']}")
