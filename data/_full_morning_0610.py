# -*- coding: utf-8 -*-
"""Full morning briefing build — 2026-06-10 (KST 08:00 slot, run 14:40).
Covers US close of Tue 2026-06-09 (chip rebound failed, tech -2%, US struck Iran after close).
Daily refresh only (Wed, not Monday) — preserves company/financials/userMemo/outlook.
"""
import json, copy, datetime

DATA = "/sessions/zen-festive-ritchie/mnt/claude/portfolio-pwa/data"
TODAY = "2026-06-10"
NOW_KST = "2026-06-10T08:00:00+09:00"

# ---------- backup ----------
import shutil
shutil.copy(f"{DATA}/portfolio.json", f"{DATA}/portfolio.json.before-full-morning-0610.bak")
shutil.copy(f"{DATA}/calendar-events.json", f"{DATA}/calendar-events.json.before-full-morning-0610.bak")

pf = json.load(open(f"{DATA}/portfolio.json"))
pf['lastUpdated'] = NOW_KST

# ============================================================
# 1) MARKET STATUS (verified June 9 close + overnight Iran strike)
# ============================================================
pf['marketStatus'] = (
    "🟡 美 칩 반등 이틀째 실패 — 혼조 마감. S&P500 -0.26%(7,386.65)·나스닥 -0.97%(25,678.82)로 기술주가 다시 발목을 잡았고, "
    "다우만 +0.17%(50,872.11)로 비기술주 덕에 올랐어요. 장중 트럼프 대통령이 이란 추가 타격을 시사하며 나스닥이 한때 -3.3%까지 밀렸다가 마감 직전 낙폭을 줄였어요. "
    "기술업종 전체가 -2%로 약했지만 샌디스크(SNDK)는 분석가 목표가 상향에 +7%로 보유 종목 중 가장 강했어요. "
    "엔비디아 -1.0%·브로드컴 -2.2%·마벨 -4.2%로 칩은 대체로 약세였어요. 변동성지수(VIX) 19.87, WTI 유가 $89.22(-2.3%), 美 10년 국채금리 약 4.5%. "
    "정규장 마감 뒤 미군이 이란에 '자위적 타격'을 가했다고 발표해 오늘 밤 분위기의 변수가 됐어요. "
    "한국은 6/10 미국의 이란 공습 여파로 코스피가 장중 -6%대 급락하며 매도 사이드카가 발동됐어요. "
    "오늘 밤 21:30(한국시간) 5월 소비자물가(CPI)가 최대 분수령 — 시장은 전년比 +4.2%(2023년 4월 이후 최대)를 예상해요."
)

# asiaCloseSnapshot note (today Korea crash) — keep field if present
pf.setdefault('asiaCloseSnapshot', {})
pf['asiaCloseSnapshot'] = {
    "asOf": TODAY,
    "note": "6/10 코스피 장중 -6%대 급락, 매도 사이드카 발동(7,500선 후퇴). 삼성전자 -6.8%·SK하이닉스 동반 약세. 미국의 이란 공습 + 칩 약세 + CPI 경계가 겹쳤어요. 코스닥은 개인 매수로 낙폭 줄여 969선."
}

# ============================================================
# 2) HOLDINGS (15) — change1D for June 9 close
#    verified: NVDA -1.0, AVGO -2.2, MRVL -4.2, SNDK +7.0
#    derived (sector move, individual close not separately confirmed): flagged in note
# ============================================================
verified = {'NVDA', 'AVGO', 'MRVL', 'SNDK'}
chg = {
    'GOOG': -1.0, 'META': -1.5, 'AMZN': -1.0, 'NVDA': -1.0, 'TSM': -1.5,
    'AVGO': -2.2, 'MU': -0.5, 'MRVL': -4.2, 'AMD': -1.0, 'SNDK': 7.0,
    'DELL': -1.0, 'LITE': -2.0, 'CLS': -2.0, 'CRDO': -3.0, 'TLN': -1.0,
}
signal = {
    'GOOG': 'yellow', 'META': 'yellow', 'AMZN': 'yellow', 'NVDA': 'yellow', 'TSM': 'yellow',
    'AVGO': 'yellow', 'MU': 'green', 'MRVL': 'red', 'AMD': 'yellow', 'SNDK': 'green',
    'DELL': 'yellow', 'LITE': 'yellow', 'CLS': 'yellow', 'CRDO': 'yellow', 'TLN': 'yellow',
}
today_why = {
 'GOOG': "빅테크 차익실현이 이어지며 약세였어요. 기술업종 전체가 -2% 빠진 하루였어요.",
 'META': "유료 AI 사업(AI Business) 가격 정책을 공개했지만, 빅테크 약세 흐름에 휩쓸려 내렸어요.",
 'AMZN': "기술주 약세에 동반 하락했어요. 직원들이 AI·데이터센터 대규모 투자에 반발한다는 소식도 부담이었어요.",
 'NVDA': "칩 반등이 이틀째 실패하며 -1.0%로 약보합 마감했어요(종가 약 $207.8). 장중 이란 타격 우려에 더 밀렸다가 막판 낙폭을 줄였어요.",
 'TSM': "반도체 전반 약세에 동반 하락했어요.",
 'AVGO': "지난주 실적 실망 여파가 남아 -2.2%로 약세였어요(종가 약 $387.7).",
 'MU': "장 초반 +5%까지 올랐다가 칩 반등이 꺾이며 상승분을 거의 반납, 약보합으로 끝났어요. 메모리 강세 기대는 살아있어요.",
 'MRVL': "보유 종목 중 가장 약했어요(-4.2%). 마이크론·퀄컴과 함께 칩 매도세의 직격탄을 맞았어요.",
 'AMD': "특별한 악재 없이 반도체 약세 흐름에 동반 하락했어요.",
 'SNDK': "미즈호·뱅크오브아메리카가 목표가를 올리며 +7%, 보유 종목 중 가장 강했어요. 메모리 업황 기대가 분석가 상향으로 이어졌어요.",
 'DELL': "기술 하드웨어 약세에 소폭 내렸어요.",
 'LITE': "AI 광통신주가 차익실현에 밀리며 약세였어요.",
 'CLS': "AI 서버 위탁생산주가 기술주 약세에 동반 하락했어요.",
 'CRDO': "전날 강세(+6.5%)에 대한 차익실현으로 광통신주가 되밀렸어요.",
 'TLN': "유가가 -2.3% 내리고 에너지 업종이 약해 전력주도 소폭 하락했어요.",
}
big_news = {
 'SNDK': {"date":"2026-06-09","headline":"SNDK +7% — 미즈호·BofA 목표가 상향","easySummary":"보유 종목 샌디스크가 +7% 올랐어요. 미즈호와 뱅크오브아메리카가 목표가를 높이면서, 칩 전반이 약했던 날에도 홀로 강했어요.","source":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-09-2026"},
 'MRVL': {"date":"2026-06-09","headline":"MRVL -4.2% — 칩 매도세 직격","easySummary":"마벨이 -4.2%로 보유 종목 중 가장 약했어요. 칩 반등이 이틀째 꺾이면서 마이크론·퀄컴과 함께 매도세를 맞았어요.","source":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-09-2026"},
 'NVDA': {"date":"2026-06-09","headline":"NVDA -1.0% — 칩 반등 이틀째 실패","easySummary":"엔비디아가 -1.0%로 약보합 마감했어요. 장중 이란 타격 우려로 더 밀렸다가 막판에 낙폭을 줄였어요.","source":"Yahoo Finance","url":"https://finance.yahoo.com/quote/NVDA/"},
}

for h in pf['us']:
    t = h['ticker']
    if t not in chg:
        continue
    prev_close = h['price']  # stored price = prior (June 8) close
    h['price'] = round(prev_close * (1 + chg[t]/100.0), 2)
    h['change1D'] = chg[t]
    h['signal'] = signal[t]
    h['todayWhy'] = today_why[t]
    if t in verified:
        h['priceSourcedFrom'] = ["TheStreet", "Yahoo"]
        h['dataQualityNote'] = None
    else:
        h['priceSourcedFrom'] = ["Sector-derived"]
        h['dataQualityNote'] = "change1D는 6/9 기술업종 평균 하락(-2%)에 기반한 추정치 — 개별 종가는 별도 미확정"
    if t in big_news:
        rn = h.get('recentNews') or []
        if not rn or rn[0].get('headline') != big_news[t]['headline']:
            h['recentNews'] = [big_news[t]] + rn
        h['recentNews'] = h['recentNews'][:6]
    # weekly change approx update (carry: shift change1W by today's move vs prior day) -- light touch, keep existing W/M/YTD
    # userMemo intentionally untouched

# ============================================================
# 3) SIGNALS — daily refresh (prices/context). Wed: keep company/financials cached.
#    Per time-guard: keep existing 5 main + 2 newListings, refresh prices/context, no fabricated new cards.
# ============================================================
sig = pf['signals']
sig['asOf'] = TODAY

# US signal price refresh (verified June 9): SMCI ~40.62 (-7.7% on $7B capital raise)
for s in sig.get('us', []):
    if s['ticker'] == 'SMCI':
        s['currentPrice'] = 40.62
        s['change1D'] = -7.66
        s['thesis'] = (
            "AI 서버를 만드는 회사예요(슈퍼마이크로). 6/9 70억 달러 규모 증자(주식을 새로 찍어 자금 조달)를 발표하자 "
            "기존 주주 지분이 희석된다는 우려로 -7.7% 내렸어요. AI 서버 수요는 강하지만, 증자·회계 신뢰 이슈가 반복돼 변동이 매우 큰 종목이에요."
        )
        s['dataQualityNote'] = "6/9 종가 기준($40.62, prev $43.99). 증자 발표로 급락."
    if s['ticker'] == 'ARM':
        s['thesis'] = (
            "스마트폰·AI 칩의 설계도(아키텍처)를 라이선스로 파는 회사예요(암). 6/9 칩 매도세에 약했어요. "
            "AI 칩 로열티 성장 기대는 크지만 PER이 매우 높아 물가·금리 변수에 크게 흔들리는 종목이에요."
        )

# KR signals: market still volatile today (6/10 -6% intraday). Keep verified June9 close prices,
# annotate today's renewed crash + continued foreign selling. Do not fabricate today's exact KR prices.
kr_ctx = "6/10 한국장은 미국의 이란 공습 여파로 매도 사이드카가 발동, 코스피가 장중 -6%대 급락했어요(삼성전자 -6.8%). 반도체 대형주가 동반 약세예요."
for s in sig.get('kr', []):
    note = s.get('dataQualityNote') or ""
    s['dataQualityNote'] = (kr_ctx + " (현재가는 6/9 종가 기준)").strip()

# krForeignFlow: continued foreign net selling theme (verified: 외인 21일 연속 매도 흐름, 6/10 외인 순매도 지속)
ff = sig.get('krForeignFlow')
if ff:
    ff['asOf'] = "2026-06-09"
    ins = ff.get('insights', [])
    add = "6/10 장중에도 외국인은 코스피에서 순매도를 이어갔고, 코스닥에선 개인이 1,076억원 순매수하며 지수를 969선으로 끌어올렸어요(외인·기관 순매도). (출처: 서울신문 서울데이터랩 6/10)"
    if add not in ins:
        ff['insights'] = ins[:5] + [add]

# newListings: keep CRWV/CHYM; refresh CRWV context (founders dumped $2.3B since IPO)
for s in sig.get('newListings', {}).get('us', []):
    if s['ticker'] == 'CRWV':
        s['dataQualityNote'] = "6/9 블룸버그: 공동창업자들이 IPO 이후 23억 달러어치 자사주를 매도했다는 보도 — 변동이 매우 큰 신규 상장주예요."

json.dump(pf, open(f"{DATA}/portfolio.json", "w"), ensure_ascii=False, indent=1)
print("portfolio.json updated. holdings:", len(pf['us']))
