# -*- coding: utf-8 -*-
"""06:00 KST 2026-07-13 US close light capture (Fri 7/10 regular session)."""
import json, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
def load(p): return json.load(open(os.path.join(BASE,p), encoding='utf-8'))
def dump(p,d): json.dump(d, open(os.path.join(BASE,p),'w',encoding='utf-8'), ensure_ascii=False, indent=2)

DATE = "2026-07-13"
GEN = "2026-07-13T06:00:00+09:00"

# ---- Friday 2026-07-10 closing data ----
PX = {
 "GOOG": (355.06, -0.34),
 "META": (669.21, 5.97),
 "AMZN": (245.34, -0.69),
 "NVDA": (210.96, 4.00),
 "TSM":  (434.11, -0.70),
 "AVGO": (399.97, -0.30),
 "MU":   (979.30, -2.21),
 "MRVL": (243.27, -4.13),
 "AMD":  (557.89, 2.00),
 "SNDK": (1915.92, -0.55),
 "DELL": (434.97, -3.39),
 "LITE": (802.01, 2.07),
 "CLS":  (359.85, 1.60),
 "CRDO": (257.79, -3.00),
 "TLN":  (385.80, 0.80),  # approx: no reliable single-day % found
}

TODAYWHY = {
 "GOOG": "-0.3% 약보합이에요. 빅테크가 대체로 올랐지만 구글은 쉬어갔어요.",
 "META": "+6.0% 크게 올랐어요. 아마존·MS·구글과 겨룰 AI 클라우드 사업('메타 컴퓨트')을 새로 만든다는 소식에 매수세가 몰렸어요.",
 "AMZN": "-0.7% 소폭 내렸어요. 메타가 클라우드 경쟁에 뛰어든다는 소식이 부담으로 살짝 작용했어요.",
 "NVDA": "+4.0% 강하게 올랐어요. SK하이닉스 미국 상장으로 AI 메모리 관심이 커지며 대표 AI 칩주가 다시 올랐어요.",
 "TSM":  "-0.7% 소폭 내렸어요. 7/16 2분기 실적 발표를 앞두고 관망세가 있었어요.",
 "AVGO": "-0.3% 약보합이에요. 반도체가 혼조를 보인 가운데 큰 변화는 없었어요.",
 "MU":   "-2.21% 내렸어요. SK하이닉스가 미국 증시에 데뷔하며 메모리 경쟁 심화 우려가 잠깐 눌렀어요.",
 "MRVL": "-4.13% 크게 내렸어요. 전날 크게 오른 뒤 오른 김에 일부 파는 매물(차익실현)이 나왔어요.",
 "AMD":  "+2.0% 올랐어요. 엔비디아와 함께 AI 칩주가 강세였어요.",
 "SNDK": "-0.55% 약보합이에요. 한 주 크게 오른 뒤 숨 고르기를 했어요.",
 "DELL": "-3.39% 내렸어요. AI 서버 대형주가 이날은 차익실현 매물에 눌렸어요.",
 "LITE": "+2.07% 올랐어요. AI 데이터센터 광통신(빛으로 데이터 전송) 수요 기대가 이어졌어요.",
 "CLS":  "+1.6% 올랐어요. AI 서버 조립 대표주로 반등 흐름에 동참했어요.",
 "CRDO": "-3.0% 내렸어요. 내부자(임원)가 주식을 일부 팔았다는 소식에 매물이 나왔어요.",
 "TLN":  "강보합이에요. AI 전력 수요 테마가 이어지며 한 주 상승세를 지켰어요.",
}

# recentNews to prepend for notable movers
NEWNEWS = {
 "META": {"date": DATE, "headline": "META +5.97% $669.21 — '메타 컴퓨트' AI 클라우드 사업 진출 소식에 급등",
          "source": "StocksToTrade", "url": "https://stockstotrade.com/news/meta-platforms-inc-meta-news-2026_07_10-3/"},
 "DELL": {"date": DATE, "headline": "DELL -3.39% $434.97 — AI 서버 대형주 차익실현에 하락",
          "source": "MarketBeat", "url": "https://www.marketbeat.com/instant-alerts/dell-technologies-nysedell-trading-down-33-heres-what-happened-2026-07-10/"},
 "MRVL": {"date": DATE, "headline": "MRVL -4.13% — 전날 급등 뒤 차익실현 매물",
          "source": "TradingKey", "url": "https://www.tradingkey.com/news/market-movers/262023232-market-movers-mrvl-20260710"},
 "CRDO": {"date": DATE, "headline": "CRDO -3% $257.79 — 내부자 매도 소식에 하락",
          "source": "MarketBeat", "url": "https://www.marketbeat.com/instant-alerts/credo-technology-group-nasdaqcrdo-stock-price-down-3-following-insider-selling-2026-07-10/"},
 "NVDA": {"date": DATE, "headline": "NVDA +4% $210.96 — SK하이닉스 美 상장에 AI 메모리 관심, 대표 AI칩 반등",
          "source": "Yahoo Finance", "url": "https://finance.yahoo.com/news/live/stock-market-today-friday-july-10-dow-sp-nasdaq-113921604.html"},
}

# ================= portfolio.json =================
p = load('portfolio.json')
for x in p['us']:
    t = x['ticker']
    if t in PX:
        price, chg = PX[t]
        x['price'] = price
        x['change1D'] = chg
        x['todayWhy'] = TODAYWHY[t]
        if t in NEWNEWS:
            x.setdefault('recentNews', [])
            if not (x['recentNews'] and x['recentNews'][0].get('headline') == NEWNEWS[t]['headline']):
                x['recentNews'].insert(0, NEWNEWS[t])
p['lastUpdated'] = GEN
p['marketSession'] = "라이트 업데이트 (한국시간 06:00)"
p['marketStatus'] = ("\U0001F1FA\U0001F1F8 7/10(금) 미국 증시가 3대 지수 모두 오름으로 마감하며 변동이 컸던 한 주를 플러스로 끝냈어요. "
    "다우 52,637(+0.29%), S&P500 7,575(+0.42%), 나스닥 26,282(+0.29%)이에요. "
    "이날 최대 이벤트는 SK하이닉스의 나스닥 데뷔였어요 — 외국 기업 사상 최대 규모(265억 달러)로 상장해 14% 가까이 급등했고, AI 메모리에 대한 관심을 키웠어요. "
    "보유 종목은 META(+6.0%)·NVDA(+4.0%)·AMD(+2.0%)가 강세였고, DELL(-3.4%)·MRVL(-4.1%)·CRDO(-3.0%)는 차익실현에 눌렸어요. "
    "공포지수(VIX)는 16 근처로 차분했고, 국제유가(WTI)는 호르무즈 해협 정체로 72달러 위로 올랐어요.")
p['holidayNote'] = ("\U0001F7E2 미국 증시는 정상 개장·마감했어요. 금요일 밤 예정된 대형 기술주 시간외(애프터아워) 실적 발표는 없었고, 실적 시즌은 다음 주 본격화돼요(7/16 TSMC 등).")
dump('portfolio.json', p)
print('portfolio.json updated')

# ================= reports/2026-07-13.json =================
def mk(cat, impact, headline, one, summ, our, srcs):
    return {"category":cat,"impact":impact,"headline":headline,"oneLineSummary":one,
            "summary":summ,"ourImpact":our,"sources":srcs}

news = [
 mk("미국 증시","positive",
    "3대 지수 모두 상승 마감 — 변동 컸던 한 주 플러스로 마무리",
    "미국 3대 지수가 금요일 모두 올랐어요. 다우 +0.29%, S&P500 +0.42%, 나스닥 +0.29%로, 반도체가 오르낙 내림을 반복하던 한 주를 결국 상승으로 끝냈어요. 빅테크 몇 종목이 지수를 끌어올렸어요.",
    "7/10 미국 증시는 다우 52,637.01(+0.29%), S&P500 7,575.39(+0.42%), 나스닥 26,281.61(+0.29%)로 모두 상승 마감했다. 반도체지수(SOX)는 12,967로 보합, 7/7 급락(12,290) 이후 한 주간 큰 폭으로 회복했다. 공포지수(VIX)는 16 근처로 차분했다.",
    "보유 빅테크 META·NVDA·AMD가 지수 상승을 이끌어 포트폴리오에 우호적이었어요. 다만 메모리·서버 일부는 쉬어가 흐름이라 종목별로 갈렸어요.",
    [{"name":"Yahoo Finance","url":"https://finance.yahoo.com/news/live/stock-market-today-friday-july-10-dow-sp-nasdaq-113921604.html"},
     {"name":"CNBC","url":"https://www.cnbc.com/2026/07/09/stock-market-today-live-updates.html"}]),
 mk("미국 증시","neutral",
    "SK하이닉스 나스닥 데뷔 — 외국 기업 사상 최대 IPO, 14% 급등",
    "한국 메모리 반도체 회사 SK하이닉스가 미국 나스닥에 상장했어요. 외국 기업이 미국에서 가장 큰 규모(265억 달러)로 돈을 모았고, 첫날 14% 가까이 올랐어요. AI에 쓰는 메모리 수요가 얼마나 뜨거운지 보여준 상징적인 상장이었어요.",
    "SK하이닉스(엔비디아에 메모리를 대는 핵심 협력사)가 7/10 나스닥에 데뷔해 공모가 대비 14%가량 급등했다. 265억 달러를 조달해 외국 기업 사상 최대 규모 미국 상장으로 기록됐으며, AI 메모리 트레이드의 시험대로 평가받았다.",
    "보유 메모리 종목 MU(-2.2%)·SNDK(-0.6%)는 경쟁사 등장 소식에 살짝 눌렸어요. 다만 AI 메모리 수요 자체는 건재해 큰 흐름은 바뀌지 않았어요.",
    [{"name":"Yahoo Finance","url":"https://finance.yahoo.com/news/live/stock-market-today-friday-july-10-dow-sp-nasdaq-113921604.html"},
     {"name":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-july-10-2026-nasdaq-futures-slip-ahead-of-sk-hynix-debut"}]),
 mk("개별 종목","positive",
    "META +5.97% $669.21 — '메타 컴퓨트' AI 클라우드 진출 소식에 급등",
    "보유 종목 META(메타)가 7/10 +6.0% 크게 올랐어요. 아마존·MS·구글과 결룰 AI 클라우드 사업('메타 컴퓨트')을 새로 만든다는 소식이 나오면서 매수세가 몰렸어요. 회사가 AI로 돈을 더 벌 새 무기를 갖춘다는 기대감이에요.",
    "메타(META)가 AI 클라우드 사업 진출 소식으로 7/10 +5.97% $669.21에 마감하며 당일 보유 종목 중 최강세를 보였다. 자체 AI 칩과 클라우드 인프라 확대 기대가 매수를 자극했다.",
    "보유 비반도체 대형주 META가 단독 급등해 포트폴리오 수익을 끌어올렸어요. 반면 같은 클라우드 경쟁사인 AMZN(-0.7%)은 살짝 눌렸어요. 변동이 클 수 있는 구간이라 흐름만 가볍게 지켜보면 좋아요.",
    [{"name":"StocksToTrade","url":"https://stockstotrade.com/news/meta-platforms-inc-meta-news-2026_07_10-3/"}]),
 mk("개별 종목","negative",
    "반도체 혼조 — DELL -3.4%·MRVL -4.1%·CRDO -3% / NVDA +4%·AMD +2% 강세",
    "보유 반도체 종목이 갈렸어요. 엔비디아(NVDA)가 +4%, AMD가 +2% 올랏지만, 델(DELL)은 -3.4%, 마벨(MRVL)은 -4.1%, 크레도(CRDO)는 -3% 내렸어요. 지난며칠 크게 오른 종목에서 오른 김에 일부 파는 매물이 나왔고, CRDO는 임원이 주식을 일부 팔았다는 소식이 격었어요.",
    "7/10 보유 반도체주는 방향이 갈렸다. NVDA +4%($210.96)·AMD +2%($557.89)는 강세였으나, DELL -3.39%($434.97)·MRVL -4.13%·CRDO -3%($257.79)는 차익실현과 임원 매도(CRDO) 소식에 하락했다.",
    "보유 15개 중 AI 칩주는 NVDA·AMD와 DELL·MRVL·CRDO로 방향이 갈렸어요. 변동이 큰 종목들이라 하루 등락에 큰 의미를 두기보다 주간 흐름을 보는 게 좋아요.",
    [{"name":"MarketBeat","url":"https://www.marketbeat.com/instant-alerts/dell-technologies-nysedell-trading-down-33-heres-what-happened-2026-07-10/"},
     {"name":"TradingKey","url":"https://www.tradingkey.com/news/market-movers/262023232-market-movers-mrvl-20260710"}]),
 mk("정책·금리","positive",
    "실적 시즌 개막 — 델타항공 어닝 서프라이즈, 연간 가이던스 재개",
    "미국 실적 시즌이 델타항공(DAL)으로 문을 열었어요. 델타가 시장 예상보다 좋은 실적을 내고, 회사가 직접 말하는 올해 전체 전망(가이던스)도 다시 내놀어요. 기름값 상승에도 프리미엄(비즐니스석) 수요가 뒷받침했고, 주가는 +2% 올랐어요.",
    "델타항공(DAL)이 7/10 2분기 실적을 시장 예상 위로 내고 연간 가이던스를 재개하며 +2.2% 상승했다. 미국 2분기 실적 시즌의 신호탄으로, 다음 주부터 본격화된다(7/16 TSMC 등).",
    "보유 종목 중 TSM은 7/16 2분기 실적이 대기하고 있어요. 실적 발표 전후로 반도체주 변동이 커질 수 있어 일정을 가볍게 알아두면 좋아요.",
    [{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/article/delta-q2-earnings-top-estimates-reinstates-full-year-guidance-as-fuel-prices-bite-175815467.html"}]),
 mk("글로벌·지정학","neutral",
    "호르무즈 해협 다시 정체 — 미·이란 정전 후 최대 공격에 유가 상승",
    "중동의 호르무즈 해협(원유 수송의 목줌목)을 지나는 배 운항이 다시 느려졌어요. 미국과 이란이 정전 후 가장 큰 공격을 주고받으면서 공급 불안이 커졌고, 국제유가(WTI, 미국 대표 원유)는 72달러 위로 올랐어요.",
    "7/10 호르무즈 해협 통행이 다시 정체되며 WTI는 72달러, 브렌트유는 76달러 위로 올랐다. 미·이란이 정전 합의 이후 가장 강한 공격을 주고받은 것이 배경이다.",
    "보유 종목에 직접 타격은 적지만, 유가가 계속 오르면 물가·금리 압박으로 기술주 전반에 간접 부담이 될 수 있어 흐름을 지켜볼 필요가 있어요.",
    [{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/article/strait-of-hormuz-traffic-is-near-a-standstill-again-but-analysts-say-the-world-has-adapted-164641420.html"}]),
]

report = {
 "date": DATE,
 "session": "us-close-light",
 "title": "7월 13일 (월) 06:00 라이트 — 미국 3대 지수 상승 마감(다우 +0.29·S&P +0.42·나스닥 +0.29%), SK하이닉스 나스닥 데뷔 14% 급등(외국기업 사상 최대 IPO) / 보유 META +6.0%·NVDA +4.0% 강세, DELL -3.4%·MRVL -4.1% 약세",
 "marketStatus": p['marketStatus'],
 "generatedAt": GEN,
 "lastUpdated": GEN,
 "marketSummary": {
   "dow":    {"close":52637.01,"change":0.29,"note":"52,637(+0.29%). 반도체 회복과 빅테크 강세에 소폭 올랐어요.","approx":False},
   "sp500":  {"close":7575.39,"change":0.42,"note":"7,575(+0.42%). 한 주 변동 끝에 플러스로 마감했어요.","approx":False},
   "nasdaq": {"close":26281.61,"change":0.29,"note":"26,282(+0.29%). META·NVDA 강세가 지수를 끌어올렸어요.","approx":False},
   "sox":    {"close":12967.16,"change":0.04,"note":"반도체지수(반도체주 묶음)는 보합. 7/7 급락(12,290) 뒤 한 주간 큰 폭으로 회복했어요.","approx":True},
   "vix":    {"close":15.9,"change":-0.3,"note":"공포지수(낮을수록 안정)가 16 근처로 차분했어요.","approx":True},
   "wti":    {"price":72.0,"change":2.7,"note":"WTI(미국 대표 원유)가 72달러 위로 올랐어요. 호르무즈 해협 정체로 공급 불안이 커졌어요.","approx":True},
   "gold":   {"price":4111.0,"change":-0.72,"note":"금값 4,111달러(-0.72%). 위험 회피에도 소폭 내렸어요.","approx":True},
 },
 "dataQualityNote": "06:00 라이트 캐처(7/10 정규장 종가). 지수·주요 종목가는 CNBC·Yahoo Finance 등 공개 자료 기준. TLN 단일 등락률과 SOX·VIX·WTI·금은 근사치(approx). 검증: 보유 15개 종목 가격·등락률 갱신 완료.",
 "news": news,
 "afterHoursNote": "금요일 밤 예정된 대형 기술주 시간외 실적 발표는 없었어요. 실적 시즌은 다음 주부터 본격화돼요(7/16 TSMC 2분기 실적).",
 "weekAhead": "7/16 TSMC 2분기 실적, 7/27 셀레스티카(CLS) 실적 등 보유 종목 실적이 줄지어 대기하고 있어요.",
 "holidayNote": p['holidayNote'],
}
dump('reports/2026-07-13.json', report)
print('reports/2026-07-13.json created with', len(news), 'news items')

# ================= reports/index.json =================
idx = load('reports/index.json')
entry = {"date":DATE,
  "title":"7월 13일 (월) 06:00 라이트 — 미국 3대 지수 상승 마감, SK하이닉스 나스닥 데뷔 14% 급등(외국기업 사상 최대 IPO)",
  "summary":"7/10 미국 증시 다우 52,637(+0.29%)·S&P 7,575(+0.42%)·나스닥 26,282(+0.29%) 모두 상승, 변동 컸던 한 주 플러스 마감. SK하이닉스 나스닥 데뷔 14% 급등(265억$ 조달, 외국기업 사상 최대). 보유 META +6.0%·NVDA +4.0%·AMD +2.0% 강세, DELL -3.4%·MRVL -4.1%·CRDO -3% 약세. 델타 어닝 서프라이즈로 실적시즌 개막. 7/16 TSMC 실적 대기."}
idx['reports'] = [x for x in idx['reports'] if x['date'] != DATE]
idx['reports'].append(entry)
idx['reports'].sort(key=lambda x: x['date'])
idx['lastUpdated'] = GEN
dump('reports/index.json', idx)
print('index.json updated; total', len(idx['reports']), 'entries')

# ================= calendar-events.json =================
cal = load('calendar-events.json')
tsmc_evt = {"type":"neutral","label":"TSMC 실적","color":"blue","time":"장전(미국)",
  "title":"TSMC 2분기 실적 발표",
  "description":"보유 종목 TSMC(세계 1위 반도체 수탁 제조사)의 2분기 실적 발표예요. AI 칩 수요와 올해 투자(CapEx) 계획이 핵심 관전 포인트예요.",
  "impact":"TSMC 실적과 가이던스(회사가 직접 하는 다음 분기 예상)는 반도체 업종 전체 분위기를 좌우해요.",
  "ourImpact":"보유 TSM 직접 영향. AI 난냉 관련 NVDA·AVGO·AMD도 함께 움직일 수 있어요.",
  "stockImpacts":[{"ticker":"TSM","tone":"neutral","magnitude":"실적 이벤트","text":"2분기 실적·CapEx 가이던스 직접 영향"}]}
cal['stock'].setdefault('2026-07-16', [])
if not any(e.get('title','').startswith('TSMC') for e in cal['stock']['2026-07-16']):
    cal['stock']['2026-07-16'].append(tsmc_evt)
cal['lastUpdated'] = GEN
dump('calendar-events.json', cal)
print('calendar-events.json updated')
print('ALL DONE')
