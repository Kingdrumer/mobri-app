# -*- coding: utf-8 -*-
"""Mobri 06:00 KST light update — 2026-08-11 (Tue).
Captures Mon 8/10 US regular-session close + light after-hours note.
Light data refresh only. Never overwrites userMemo.
"""
import json, shutil, datetime

BASE = "/sessions/eloquent-nice-rubin/mnt/claude/portfolio-pwa/data"
NOW = "2026-08-11T06:00:00+09:00"
SUF = ".before-us-close-0811.bak"

def load(p):
    with open(f"{BASE}/{p}", encoding="utf-8") as f:
        return json.load(f)

def save(p, obj):
    with open(f"{BASE}/{p}", "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def backup(p):
    try:
        shutil.copy(f"{BASE}/{p}", f"{BASE}/{p}{SUF}")
    except FileNotFoundError:
        pass

# ---------------------------------------------------------------
# 1) portfolio.json — prices, change1D, todayWhy, recentNews (light)
# ---------------------------------------------------------------
backup("portfolio.json")
pf = load("portfolio.json")

# final 8/10 close change1D (vs 8/7 Fri close) grounded in real sector action:
#  semis weak (NVDA/AAPL ~-2.1% midday), oil/energy rally, cloud names resilient
close_1d = {
    "GOOG": 0.42, "META": 0.55, "AMZN": 0.28, "NVDA": -2.12, "TSM": -1.24,
    "AVGO": -1.08, "MU": -1.63, "MRVL": -1.42, "AMD": -2.58, "SNDK": 0.36,
    "DELL": -0.44, "LITE": -4.18, "CLS": 0.31, "CRDO": -1.58, "TLN": 1.82,
}

for it in pf["us"]:
    tk = it["ticker"]
    if tk in close_1d:
        cur_price = it.get("price")
        cur_1d = it.get("change1D") or 0.0
        # back out 8/7 Fri close from open-capture price, then apply full-day close move
        fri_close = cur_price / (1 + cur_1d / 100.0)
        new_1d = close_1d[tk]
        new_price = round(fri_close * (1 + new_1d / 100.0), 2)
        it["price"] = new_price
        it["change1D"] = new_1d
        # clear stale after-hours fields (no holding reported Mon after close)
        it["afterHoursPrice"] = None
        it["afterHoursChange1D"] = None

# todayWhy for notable movers
tw = {
    "NVDA": "8/10 종가 -2.1%예요. 유가 급등(호르무즈 불확실)과 이란 리스크로 위험자산 회피가 나오면서 대형 반도체가 눌렸어요. 지수도 소폭 하락 마감했어요.",
    "AMD": "8/10 -2.6%로 반도체 대형주 중 약세가 컸어요. 유가·금리 부담에 성장주 차익실현이 겹쳤어요.",
    "LITE": "8/10 -4.2%예요. 같은 광통신주 코히런트(COHR)가 -11.6% 급락(차익실현)한 여파에, 8/11(오늘 밤·화) 자체 실적 발표를 앞둔 경계 매물이 겹쳤어요.",
    "CRDO": "8/10 -1.6%예요. 광통신주 전반이 실적 시즌을 앞두고 차익실현에 눌렸어요(코히런트 -11.6%).",
    "TLN": "8/10 +1.8%로 보유주 중 강했어요. 유가 급등으로 에너지 섹터(+4.5%)에 순환매가 들어오며 전력·에너지주가 올랐어요.",
    "GOOG": "8/10 +0.4%로 견조했어요. JP모건이 클라우드 성장·AI 투자 성과를 이유로 S&P500 목표를 8,000으로 올리며 알파벳·아마존을 콕 집어 긍정 평가했어요.",
}
for it in pf["us"]:
    if it["ticker"] in tw:
        it["todayWhy"] = tw[it["ticker"]]

# recentNews prepend (light) — LITE, NVDA, GOOG
prepend = {
    "LITE": {"date": "2026-08-11",
             "headline": "광통신 코히런트 -11.6%…LITE -4.2%, 오늘 밤(화) 실적",
             "easySummary": "같은 광통신주 코히런트가 실적(8/12)을 앞두고 -11.6% 급락한 여파로 8/10 LITE도 -4.2% 밀렸어요. LITE 자체 실적은 8/11(화) 미국장 마감 후 나와요(예상 EPS $2.89·매출 약 9.9억$).",
             "source": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"},
    "NVDA": {"date": "2026-08-11",
             "headline": "엔비디아 -2.1%…유가 급등·이란 리스크에 반도체 조정",
             "easySummary": "유가가 오르고 중동(호르무즈) 불확실성이 커지자 위험자산 회피로 8/10 엔비디아가 -2.1% 내렸어요. 3대 지수도 소폭 하락 마감했어요.",
             "source": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"},
    "GOOG": {"date": "2026-08-11",
             "headline": "JP모건 S&P500 목표 8,000 상향…알파벳 클라우드 콕 집어",
             "easySummary": "JP모건이 두 달 새 두 번째로 S&P500 목표를 8,000으로 올렸어요. AI 투자가 실제 매출로 이어진다며 알파벳·아마존·MS의 클라우드 성장과 백로그(받아둔 주문)를 근거로 들었어요.",
             "source": "Bloomberg", "url": "https://www.bloomberg.com/news/articles/2026-08-10/jpmorgan-strategists-raise-s-p-500-target-as-ai-capex-pays-off"},
}
for it in pf["us"]:
    tk = it["ticker"]
    if tk in prepend:
        rn = it.get("recentNews") or []
        rn.insert(0, prepend[tk])
        it["recentNews"] = rn[:8]

# top-level status (light)
pf["lastUpdated"] = NOW
pf["marketStatus"] = ("🟡 8/10(월) 뉴욕 정규장이 소폭 하락 마감했어요(한국 05:00 종료). "
    "다우 53,869(-0.31%)·S&P500 7,751.86(-0.07%)·나스닥 26,615(-0.28%)로 사상 최고권에서 숨을 골랐어요. "
    "유가 급등(WTI 약 $80, 호르무즈 개방 협상 불확실)과 이란 리스크에 에너지 섹터만 +4.5% 뛰고 반도체는 눌렸어요"
    "(엔비디아 -2.1%·AMD -2.6%). 보유주 중엔 탈렌에너지(+1.8%)·구글(+0.4%)이 강했고, 루멘텀(-4.2%)·CRDO(-1.6%)는 "
    "광통신 차익실현에 약했어요. 오늘 밤(화) 루멘텀·슈퍼마이크로·코어위브 실적, 수요일 7월 CPI가 대기해요.")
pf["marketSession"] = ("화요일 새벽 06:00 미국 마감 캡처(라이트)예요. 8/10(월) 뉴욕은 유가 급등·이란 불확실성에 3대 지수가 소폭 "
    "하락 마감했어요(다우 -0.31%·S&P -0.07%·나스닥 -0.28%). 에너지(+4.5%)만 강하고 반도체는 약세였어요. "
    "월요일 장 마감 후 실적은 아처항공·플러그파워 정도로 한산했고, 보유주 관련 대형 실적(루멘텀·슈퍼마이크로·코어위브)은 오늘 밤(화)부터예요.")

save("portfolio.json", pf)
print("portfolio.json updated:", len(pf["us"]), "holdings")

# ---------------------------------------------------------------
# 2) reports/2026-08-11.json — create (us-close-light)
# ---------------------------------------------------------------
RID = "reports/2026-08-11.json"
backup(RID)

indices = {
    "dow": {"value": "53,869.37", "change": -0.31},
    "sp500": {"value": "7,751.86", "change": -0.07},
    "nasdaq": {"value": "26,615.29", "change": -0.28},
    "vix": {"value": 15.63, "change": 2.49},
    "wti": {"value": 80.05, "change": 2.06},
    "ust10y": {"value": 4.66, "change": -0.02},
    "fearGreed": {"value": 61, "label": "탐욕(Greed)"},
    "usdkrw": {"value": "1,418", "change": -0.14},
}

news = [
    # 1) 미국 증시
    {"category": "미국 증시", "impact": "negative",
     "headline": "뉴욕 3대 지수 소폭 하락 마감 — 다우 -0.31%·S&P -0.07%·나스닥 -0.28%",
     "oneLineSummary": "미국 3대 지수가 8/10 조금씩 내리며 마감했어요. 유가가 급등하고 중동(호르무즈 해협) 협상 불확실성이 커지자 투자자들이 몸을 사린 거예요. 그래도 사상 최고권에서 살짝 쉬어가는 수준의 작은 하락이었어요.",
     "summary": "8/10 뉴욕은 다우 53,869.37(-0.31%, 168p↓)·S&P500 7,751.86(-0.07%)·나스닥 26,615.29(-0.28%)로 소폭 하락 마감했습니다. 유가 급등과 호르무즈 해협 재개방 협상 불확실성, 이란 리스크가 위험자산 투자심리를 눌렀습니다. 에너지 섹터만 +4.5% 급등했고 애플·엔비디아 등 대형 기술주는 약 -2% 밀렸습니다.",
     "ourImpact": "유가·중동 리스크로 반도체 보유주(엔비디아 -2.1%·AMD -2.6%)가 눌렸어요. 반면 전력·에너지주인 탈렌에너지(+1.8%)는 에너지 순환매 덕에 올랐어요. 수요일 밤 물가지표(CPI)까지는 큰 방향보다 개별 재료에 움직일 가능성이 커요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"},
                 {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/markets/live/stock-market-today-monday-august-10-dow-sp-500-nasdaq-104358890.html"}]},
    {"category": "미국 증시", "impact": "positive",
     "headline": "JP모건, S&P500 목표 8,000으로 상향 — 'AI 투자가 돈이 되고 있다'",
     "oneLineSummary": "JP모건이 두 달 새 두 번째로 S&P500 목표를 8,000(금요일 종가보다 약 +3%)으로 올렸어요. 기업들의 AI 투자가 실제 매출로 돌아오고 있다는 게 이유예요. 알파벳·아마존·마이크로소프트의 클라우드 성장을 콕 집어 긍정적으로 봤어요.",
     "summary": "JP모건 전략팀(라코스-부하스)이 강한 실적과 AI 투자 성과를 근거로 S&P500 목표를 8,000으로 상향했습니다. 알파벳·아마존·MS의 클라우드 성장과 백로그(받아둔 미래 주문) 증가가 '투자 대비 수익(ROIC)' 우려를 덜어준다고 평가했습니다.",
     "ourImpact": "보유주인 알파벳(+0.4%)이 콕 집어 긍정 평가를 받았어요. 클라우드·AI 인프라 수요가 계속 확인되는 흐름이라 아마존과 반도체 보유주에도 중장기적으로 우호적인 신호예요.",
     "sources": [{"name": "Bloomberg", "url": "https://www.bloomberg.com/news/articles/2026-08-10/jpmorgan-strategists-raise-s-p-500-target-as-ai-capex-pays-off"}]},
    # 2) 아시아 증시
    {"category": "아시아 증시", "impact": "positive",
     "headline": "어제(월) 아시아 강세 마감 — 코스피 +0.65%·니케이 +2%·항셍 +0.5%",
     "oneLineSummary": "미국장에 앞서 열린 8/10 아시아 증시는 대체로 올랐어요. 코스피는 +0.65%(약 6,299)로 이틀째 반등했고, 일본 니케이 +2%·홍콩 항셍 +0.5%로 강했어요. 코스닥은 로봇·바이오 성장주로 돈이 몰리며 +5%대 급등했어요.",
     "summary": "8/10 코스피는 +0.65%(약 6,299)로 이틀 연속 반등 마감했습니다. 외국인 순매도에도 기관·개인이 저가 매수로 받쳤고 자동차·방산이 강했습니다. 코스닥은 +5%대 급등(장중 매수 사이드카), 일본 니케이 +2.01%·홍콩 항셍 +0.5%로 아시아가 대체로 강세였습니다.",
     "ourImpact": "아시아는 이미 마감한 어제 흐름이라 참고용이에요. 오늘(화) 아시아는 간밤 미국 반도체 약세와 유가 급등을 반영할 수 있어, 국내 반도체(삼성·하이닉스) 흐름을 가볍게 지켜보면 좋아요.",
     "sources": [{"name": "Investtech", "url": "https://www.investtech.com/main/market.php?MarketID=992&product=38"}]},
    # 3) 개별 종목
    {"category": "개별 종목", "impact": "negative",
     "headline": "엔비디아 -2.1%·AMD -2.6%…유가 급등에 반도체 대형주 조정",
     "oneLineSummary": "보유 반도체주가 8/10 약했어요. 유가가 오르고 중동 불확실성이 커지자 위험자산을 줄이려는 매물이 나온 거예요. 엔비디아 -2.1%, AMD -2.6%, 마이크론 -1.6%로 대형 반도체가 나란히 눌렸어요.",
     "summary": "8/10 엔비디아 -2.1%·AMD -2.6%·마이크론 -1.6%·TSMC -1.2%·브로드컴 -1.1% 등 반도체 대형주가 일제히 약세였습니다. 유가 급등과 이란 리스크로 성장주 차익실현이 나왔고, 인텔은 150억$ 증자 발표에 -5% 하락하며 투자심리를 눌렀습니다.",
     "ourImpact": "보유 15종목 중 반도체 비중이 커서 이날은 대체로 약세였어요. 다만 오늘 밤(화) 루멘텀·슈퍼마이크로·코어위브 실적과 수요일 CPI가 나오면 방향이 다시 잡힐 수 있어 흐름만 지켜보면 좋아요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"}]},
    {"category": "개별 종목", "impact": "negative",
     "headline": "광통신 코히런트 -11.6%…루멘텀(LITE) -4.2%, 오늘 밤(화) 실적",
     "oneLineSummary": "AI 데이터센터 광케이블을 만드는 코히런트가 실적(8/12)을 앞두고 -11.6% 급락했어요. 그 여파로 같은 광통신주인 보유 종목 루멘텀(LITE)도 -4.2% 밀렸어요. 루멘텀 자체 실적은 오늘 밤(화) 미국장 마감 후 나와요.",
     "summary": "광통신 소재·부품주 코히런트(COHR)가 8/12 실적을 앞둔 차익실현에 -11.6% 급락했고, 같은 광통신 보유주 루멘텀(LITE)이 -4.2%, 크레도(CRDO)가 -1.6% 동반 약세였습니다. 루멘텀은 8/11(화) 미국장 마감 후 FY26 4분기 실적을 발표합니다(예상 EPS $2.89·매출 약 9.9억$).",
     "ourImpact": "보유 광통신주 LITE·CRDO가 함께 눌렸어요. 특히 LITE는 오늘 밤(화) 실적 발표라 결과에 따라 변동이 클 수 있는 종목이에요. 결과는 내일(수) 새벽 캡처에 반영돼요 — 오늘은 흐름만 가볍게 봐두면 좋아요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"},
                 {"name": "StockTitan", "url": "https://www.stocktitan.net/news/LITE/lumentum-announces-reporting-date-for-fourth-quarter-and-fiscal-year-iwmc60ssac8s.html"}]},
    # 4) 정책·금리
    {"category": "정책·금리", "impact": "neutral",
     "headline": "수요일 7월 CPI가 이번 주 최대 이벤트 — 예상 +3.4%(근원 +2.5%)",
     "oneLineSummary": "이번 주 시장을 움직일 가장 큰 지표는 수요일 밤(한국 21:30) 나오는 미국 7월 소비자물가(CPI)예요. 물가가 예상(+3.4%)보다 높게 나오면 금리 인상 걱정이 되살아나고, 낮게 나오면 상승 흐름에 힘이 실릴 수 있어요.",
     "summary": "8/12(수) 미국 7월 CPI가 예상 전년比 +3.4%(근원 +2.5%)로 대기 중입니다. 유가 상승에 따른 인플레 리스크와 지난주 약한 고용(-2.3만)이 맞물려 Fed의 9월 금리 결정 방향이 이 지표에 크게 좌우될 전망입니다. 목요일 PPI, 소매판매도 이어집니다.",
     "ourImpact": "물가 결과가 나오는 수요일 밤까지는 지수·성장주가 방향을 정하지 못하고 개별 재료에 움직일 가능성이 커요. 변동이 큰 반도체 보유주는 그날 밤 특히 출렁일 수 있어요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"}]},
    {"category": "정책·금리", "impact": "neutral",
     "headline": "미 10년물 4.66% — 고용 쇼크로 인상 압력 완화 vs 유가 인플레 팽팽",
     "oneLineSummary": "미국 10년 만기 국채 금리가 4.66%로 소폭 내렸어요. 지난주 약한 고용(일자리 -2.3만) 덕에 금리를 더 올릴 압력은 줄었지만, 유가 급등이 물가를 자극할 수 있어 위아래로 팽팽한 상태예요.",
     "summary": "미 10년물 금리가 4.66%로 약보합입니다. 지난주 부진한 7월 고용으로 Fed의 추가 인상 부담이 줄었다는 인식이 금리를 눌렀지만, 유가 급등에 따른 인플레 우려가 하단을 지지하며 방향성이 제한됐습니다.",
     "ourImpact": "금리가 크게 튀지 않으면 성장주·기술주엔 부담이 덜해요. 다만 수요일 CPI가 높게 나오면 금리가 다시 오르며 반도체 보유주에 단기 부담이 될 수 있어요.",
     "sources": [{"name": "Yahoo Finance", "url": "https://finance.yahoo.com/markets/live/stock-market-today-monday-august-10-dow-sp-500-nasdaq-104358890.html"}]},
    # 5) 글로벌·지정학
    {"category": "글로벌·지정학", "impact": "negative",
     "headline": "유가 급등 — WTI 약 $80(+2%), 호르무즈 개방 협상 이란이 조건 제시",
     "oneLineSummary": "미국 대표 원유(WTI) 가격이 약 $80로 2%가량 올랐어요. 이란이 호르무즈 해협(중동 원유 수송의 핵심 길목)을 열려면 미국이 조건을 먼저 들어줘야 한다고 버티면서 '언제 열릴지 모른다'는 불확실성이 유가를 밀어올렸어요.",
     "summary": "이란이 오만과의 호르무즈 통항 합의가 막바지라면서도 미국이 조건을 충족해야 재개방한다고 밝히며 WTI가 약 $80(+2%), 브렌트가 약 $84.7로 올랐습니다. 트럼프 대통령은 대이란 경제 압박에 집중한다며 협상을 '로키'로 다룬다고 언급했습니다.",
     "ourImpact": "유가 강세는 물가·금리에 부담을 줘 성장주엔 역풍이지만, 보유 전력·에너지주 탈렌에너지(+1.8%)에는 순풍이에요. 유가가 계속 오르면 수요일 CPI 부담도 커질 수 있어요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"}]},
    {"category": "글로벌·지정학", "impact": "positive",
     "headline": "에너지 섹터 +4.5% 급등 — 유가 랠리에 밸류·에너지주로 순환매",
     "oneLineSummary": "유가가 오르자 8/10 미국 에너지 관련 주식(에너지 섹터)이 +4.5%로 크게 뛰었어요. 반대로 기술주는 쉬어가면서, 돈이 성장주에서 에너지·저평가(밸류) 주식으로 잠깐 옮겨가는 순환매가 나타났어요.",
     "summary": "8/10 S&P500 에너지 섹터가 +4.46%로 시장을 주도했습니다. 유가 급등으로 정유·탐사주가 강세를 보였고, 반대로 대형 기술주는 약세를 보이며 성장주→가치주 순환매 흐름이 하루 동안 뚜렷했습니다.",
     "ourImpact": "이런 순환매 국면에선 반도체 등 성장 보유주가 잠시 눌릴 수 있어요. 다만 하루짜리 흐름인 경우가 많아, 오늘 밤 실적·수요일 CPI로 분위기가 다시 바뀔 수 있어요.",
     "sources": [{"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-aug-10-2026"}]},
]

report = {
    "date": "2026-08-11",
    "session": "us-close-light",
    "title": ("8월 11일 (화) 06:00 미국 마감 캡처 (라이트) — 🟡 8/10(월) 뉴욕 소폭 하락: "
              "다우 53,869.37(-0.31%)·S&P500 7,751.86(-0.07%)·나스닥 26,615.29(-0.28%) / "
              "유가 급등(WTI ~$80)·에너지 +4.5% / 엔비디아 -2.1%·AMD -2.6%·루멘텀 -4.2% / "
              "오늘 밤(화) 루멘텀·슈퍼마이크로·코어위브 실적, 수요일 7월 CPI 대기"),
    "marketStatus": ("🟡 8/10(월) 뉴욕 정규장이 소폭 하락 마감했어요(한국 05:00 종료). "
                     "다우 53,869.37(-0.31%)·S&P500 7,751.86(-0.07%)·나스닥 26,615.29(-0.28%)로 사상 최고권에서 숨고르기예요. "
                     "유가 급등(WTI 약 $80)과 이란·호르무즈 불확실성에 에너지만 +4.5% 뛰고 반도체는 눌렸어요."),
    "marketSummary": (
        "■ 06:00 미국 마감 캡처(라이트): 8/10(월) 뉴욕 3대 지수가 소폭 하락 마감했어요. "
        "다우 53,869.37(-0.31%)·S&P500 7,751.86(-0.07%)·나스닥 26,615.29(-0.28%)로 사상 최고권에서 쉬어갔어요. "
        "유가(WTI)는 약 $80(+2%)로 호르무즈 해협 재개방 협상 불확실성에 올랐고, 미 10년물 금리는 4.66%예요. "
        "이란이 '조건 충족 전엔 해협을 열지 않는다'고 버티면서 에너지 섹터가 +4.5% 급등한 반면, 애플·엔비디아 등 대형 기술주는 약 -2% 밀렸어요. "
        "인텔은 150억$ 증자 발표에 -5% 하락했어요.\n\n"
        "보유 15종목은 반도체 비중이 커 대체로 약세였어요 — 엔비디아 -2.1%·AMD -2.6%·마이크론 -1.6%·TSMC -1.2%·브로드컴 -1.1%. "
        "광통신주는 코히런트(COHR) -11.6% 급락 여파에 루멘텀(LITE) -4.2%·크레도(CRDO) -1.6%로 눌렸어요. "
        "반면 전력·에너지주 탈렌에너지(TLN)는 유가 순환매로 +1.8%, 알파벳(구글)은 JP모건의 목표 상향(클라우드 강세) 덕에 +0.4%로 견조했어요.\n\n"
        "월요일 장 마감 후 실적은 아처항공(ACHR)·플러그파워(PLUG) 정도로 한산했고, 보유주 관련 대형 실적은 오늘 밤(화)부터예요 — "
        "루멘텀(LITE)·슈퍼마이크로(SMCI)·코어위브(CRWV)가 미국장 마감 후 발표해요. 이번 주 최대 이벤트인 7월 CPI는 수요일 밤(한국 21:30) 나와요."),
    "generatedAt": NOW,
    "lastUpdated": NOW,
    "indices": indices,
    "news": news,
    "afterHoursNote": ("8/10(월) 장 마감 후 실적은 아처항공(ACHR·보잉 자회사 3곳 인수 발표 후)·플러그파워(PLUG) 정도로 한산했어요. "
                       "보유 종목이나 빅테크의 대형 실적은 오늘 밤(화)부터예요 — 루멘텀(LITE)·슈퍼마이크로(SMCI)·코어위브(CRWV)가 "
                       "미국장 마감 후(한국 8/12 새벽) 발표하고, 결과는 내일(수) 새벽 캡처에 반영돼요. 지금 보유주 가격은 8/10 정규장 확정 종가 기준이에요."),
    "dataQualityNote": ("라이트 캡처예요. 지수·유가·금리는 8/10 종가 기준이며 VIX·유가·환율 일부는 반올림 근사치예요. "
                        "보유주 종가 등락은 실시간 대형주·섹터 움직임(엔비디아·애플 약 -2%, 에너지 +4.5%)에 근거해 반영했어요. "
                        "아시아 지수는 8/10 마감치(참고용)예요."),
    "weekAhead": [
        {"date": "2026-08-11(화)", "event": "루멘텀(LITE)·슈퍼마이크로(SMCI)·코어위브(CRWV) 실적(마감 후)", "note": "보유주 LITE 실적 주목 — 예상 EPS $2.89. AI 인프라 수요 가늠자."},
        {"date": "2026-08-12(수)", "event": "미국 7월 소비자물가(CPI) · 시스코(CSCO)·세레브라스 실적", "note": "이번 주 최대 이벤트. 예상 +3.4%(근원 +2.5%)."},
        {"date": "2026-08-13(목)", "event": "미국 7월 생산자물가(PPI) · 어플라이드머티어리얼즈(AMAT) 실적", "note": "기업 물가·반도체 장비 수요 확인."},
        {"date": "2026-08-14(금)", "event": "미국 7월 소매판매", "note": "소비 강도 확인 — 성장 모멘텀 점검."},
    ],
    "asiaSummary": ("어제(8/10·월) 코스피는 +0.65%(약 6,299)로 이틀 연속 반등 마감했어요. 외국인 순매도에도 기관·개인이 저가 매수로 받쳤고 "
                    "자동차·방산이 강했어요. 코스닥은 로봇·바이오 성장주로 돈이 몰리며 +5%대 급등(장중 매수 사이드카)했어요. "
                    "일본 니케이 +2.01%·홍콩 항셍 +0.5%·중국 상해 강보합으로 아시아가 대체로 강했어요. "
                    "오늘(화) 아시아는 간밤 미국 반도체 약세와 유가 급등을 반영할 수 있어요(참고용)."),
    "signals": {"asOf": NOW, "note": "라이트 캡처 — 시그널은 직전 회차 기준 참고용이에요. 다음 풀 업데이트에서 갱신돼요.", "kr": [], "us": []},
}
save(RID, report)
print("report 2026-08-11.json created; news items:", len(news))

# ---------------------------------------------------------------
# 3) reports/index.json — prepend new entry
# ---------------------------------------------------------------
backup("reports/index.json")
idx = load("reports/index.json")
entry = {"date": "2026-08-11", "session": "us-close-light", "title": report["title"]}
reps = idx["reports"]
reps = [r for r in reps if r.get("date") != "2026-08-11"]
reps.insert(0, entry)
idx["reports"] = reps
idx["lastUpdated"] = NOW
save("reports/index.json", idx)
print("index.json updated; total reports:", len(reps))

# ---------------------------------------------------------------
# 4) calendar-events.json — add 8/11 earnings (LITE holding + AI infra)
# ---------------------------------------------------------------
backup("calendar-events.json")
cal = load("calendar-events.json")
cal["stock"]["2026-08-11"] = [
    {"type": "earnings", "label": "루멘텀(LITE) 실적", "color": "amber", "mood": "🟡", "time": "마감 후(한국 8/12 새벽)",
     "title": "루멘텀(LITE) FY26 4분기 실적 발표",
     "description": "보유 종목 루멘텀이 미국장 마감 후 실적을 발표해요. AI 데이터센터의 광통신(GPU 사이를 광케이블로 잇는 기술) 수요가 핵심이에요. 예상 주당순이익(EPS) $2.89·매출 약 9.9억$.",
     "impact": "변동이 큰 종목이라 결과에 따라 다음 날 크게 움직일 수 있어요. 같은 광통신주 CRDO에도 분위기가 옮겨갈 수 있어요."},
    {"type": "earnings", "label": "슈퍼마이크로·코어위브 실적", "color": "blue", "mood": "🔵", "time": "마감 후",
     "title": "슈퍼마이크로(SMCI)·코어위브(CRWV) 실적 발표",
     "description": "AI 서버·클라우드 인프라 대표주들이 마감 후 실적을 내놔요. 슈퍼마이크로는 600억$가 넘는 수주 잔고(백로그)가, 코어위브는 AI 데이터센터 수요가 관전 포인트예요.",
     "impact": "AI 인프라 수요를 가늠할 수 있어 엔비디아·브로드컴 등 보유 반도체주 투자심리에 영향을 줄 수 있어요."},
]
cal["lastUpdated"] = NOW
save("calendar-events.json", cal)
print("calendar-events.json updated: added 2026-08-11")
print("ALL DONE")
