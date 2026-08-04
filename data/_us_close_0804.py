# -*- coding: utf-8 -*-
import json, datetime

NOW = "2026-08-04T06:10:00+09:00"
p = json.load(open('portfolio.json'))

# ticker -> (change1D pct, price, confirmed?)
MOVES = {
 'GOOG': (4.98, 374.40, True),
 'META': (6.55, 593.15, True),
 'AMZN': (4.53, 283.89, True),
 'NVDA': (3.20, 207.17, True),
 'AMD':  (0.80, 479.96, True),
 'AVGO': (0.30, 390.45, False),
 'TSM':  (2.00, 412.34, False),
 'MU':   (1.50, 835.38, False),
 'MRVL': (3.00, 193.19, False),
 'SNDK': (1.00, 1226.98, False),
 'DELL': (2.00, 413.48, False),
 'LITE': (4.00, 742.50, False),
 'CLS':  (3.50, 343.04, False),
 'CRDO': (4.00, 215.27, False),
 'TLN':  (1.50, 339.11, False),
}
SRC_CONF = ["247WallSt/CNBC(8/3 미국 종가)", "WebSearch 교차확인"]
SRC_EST  = ["지수·섹터 기반 추정(정확한 종가 미확정)", "WebSearch(8/3)"]

# todayWhy for confirmed big movers
TODAYWHY = {
 'GOOG': "구글 클라우드 82% 성장·연 CapEx 가이던스 상향($205B) 소식에 아마존발 AI 훈풍까지 겹치며 8/3 +5.0% 상승했어요.",
 'META': "메타가 8/3 +6.6% 급등하며 실적 발표 뒤 빠졌던 9% 하락분을 되돌렸어요. 광고 매출이 27% 늘어난 게 재평가됐어요.",
 'AMZN': "아마존이 8/3 +4.5% 올라 시가총액 3조 달러를 넘었어요. AWS(클라우드) 매출 +37% 서프라이즈가 계속 힘을 냈어요.",
 'NVDA': "엔비디아가 8/3 빅테크 랠리 속 +3.2% 상승했어요. AI 반도체 수요 기대가 이어졌어요.",
}
# recentNews prepend for these
NEWNEWS = {
 'GOOG': {"date":"2026-08-03","headline":"GOOG +5.0% $374.40 — 클라우드 82% 성장·CapEx 상향","easySummary":"구글(GOOG)이 8/3 +5.0% 올랐어요. 구글 클라우드 매출이 82% 늘고 올해 투자 계획을 $205B로 올린 게 호재였어요.","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/08/03/amazon-tops-3t-meta-rallies-7-as-ai-hyperscalers-ride-earnings-momentum/"},
 'META': {"date":"2026-08-03","headline":"META +6.6% $593.15 — 광고 27% 성장에 실적 하락분 회복","easySummary":"메타(META)가 8/3 +6.6% 급등했어요. 광고 매출이 27% 늘어난 게 부각되며 실적 발표 후 빠졌던 9%를 되돌렸어요.","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/08/03/amazon-tops-3t-meta-rallies-7-as-ai-hyperscalers-ride-earnings-momentum/"},
 'AMZN': {"date":"2026-08-03","headline":"AMZN +4.5% $283.89 — 시총 3조 달러 돌파","easySummary":"아마존(AMZN)이 8/3 +4.5% 올라 시가총액 3조 달러를 넘었어요. AWS(클라우드) +37% 성장이 계속 주가를 밀어올렸어요.","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/08/03/amazon-tops-3t-meta-rallies-7-as-ai-hyperscalers-ride-earnings-momentum/"},
 'NVDA': {"date":"2026-08-03","headline":"NVDA +3.2% $207.17 — 빅테크 랠리 동반 상승","easySummary":"엔비디아(NVDA)가 8/3 +3.2% 올랐어요. AI 반도체 수요 기대와 위험자산 선호 회복에 반도체가 함께 강했어요.","source":"CNBC/WebSearch","url":"https://www.cnbc.com/2026/08/02/stock-market-today-live-updates.html"},
}

for s in p['us']:
    t = s.get('ticker')
    if t in MOVES:
        chg, price, conf = MOVES[t]
        s['change1D'] = chg
        s['price'] = price
        s['priceSourcedFrom'] = SRC_CONF if conf else SRC_EST
        if not conf:
            s['dataQualityNote'] = "8/3 종가는 지수·섹터 흐름 기반 추정치예요(정확한 개별 종가 미확정). 다음 정산 브리핑에서 교차검증해요."
        else:
            s['dataQualityNote'] = ""
        if t in TODAYWHY:
            s['todayWhy'] = TODAYWHY[t]
        if t in NEWNEWS:
            rn = s.get('recentNews') or []
            if not (rn and rn[0].get('date')=='2026-08-03'):
                s['recentNews'] = [NEWNEWS[t]] + rn
        # clear stale after-hours (no holding reported AH on 8/3)
        s['afterHoursPrice'] = None
        s['afterHoursChange1D'] = None

# ---- market status / session strings ----
p['lastUpdated'] = NOW
p['marketStatus'] = ("🟢 8/4(화) 새벽이에요. 방금 끝난 8/3(월) 미국 정규장은 이란 긴장 완화로 유가가 6% 급락하고 빅테크가 크게 오르며 3대 지수가 나란히 상승 마감했어요"
 "(다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%). 아마존이 시총 3조 달러를 넘었고(+4.5%), 메타(+6.6%)·구글(+5.0%)·엔비디아(+3.2%)가 상승을 이끌었어요. "
 "장 마감 뒤엔 팰런티어가 실적 서프라이즈로 시간외 +13% 급등했어요. 오늘 밤엔 보유 종목 AMD 실적(8/4)이 대기예요.")
p['marketSession'] = ("8/4(화) 06시 KST — 8/3(월) 미국 정규장 '종가' 기준으로 정산했어요. 지수: 다우 53,178.41(+1.32%)·S&P500 7,600.50(+1.48%)·나스닥 25,913.90(+2.1%). "
 "유가(WTI)는 이란 협상 재개에 약 $79로 6% 급락, VIX(변동성 지수)는 약 15.7로 진정.")
p['holidayNote'] = ("🟢 8/4(화)예요. 8/3(월) 미국장이 큰 폭 상승 마감해 보유 빅테크 가격을 8/3 종가로 갱신했어요. 오늘 밤(미 동부 장 마감 후) 보유 종목 AMD가 2분기 실적을 발표해요.")
p['dataNote'] = ("8/4(화) 06시 미국 마감 캡처(라이트). 빅테크 5종(GOOG·META·AMZN·NVDA·AMD)은 8/3 종가를 24/7 Wall St.·CNBC·WebSearch로 교차확인했어요. "
 "그 외 종목(AVGO·TSM·MU·MRVL·SNDK·DELL·LITE·CLS·CRDO·TLN)은 8/3 지수(+2.1%)·섹터 흐름 기반 추정치로, priceSourcedFrom에 '추정'으로 표시했어요. "
 "지수·유가·VIX는 실시간 검색으로 확인한 8/3 미국 마감 기준.")

json.dump(p, open('portfolio.json','w'), ensure_ascii=False, indent=1)
print("portfolio.json updated OK")
for s in p['us']:
    print(f"  {s['ticker']:5} {s['price']:>9}  {s['change1D']:+.2f}%  {'CONF' if s['priceSourcedFrom']==SRC_CONF else 'est'}")
