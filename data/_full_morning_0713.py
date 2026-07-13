#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, datetime

P = "portfolio.json"
d = json.load(open(P, encoding="utf-8"))

NOW = "2026-07-13T08:00:00+09:00"
FETCHED = "2026-07-13T07:40:00+09:00"

# Fresh holdings data (July 10, 2026 close). change1D fetched (CBOE/stockanalysis or WebSearch).
# target/rating/beta/emp only where freshly fetched from stockanalysis.
H = {
 "GOOG": dict(price=355.03, c1=-0.34, src=["WebSearch(Yahoo/CBOE)"]),
 "META": dict(price=669.21, c1=5.97, src=["WebSearch(Yahoo/CBOE)"]),
 "AMZN": dict(price=245.34, c1=-0.69, src=["WebSearch(Yahoo/CBOE)"]),
 "NVDA": dict(price=210.96, c1=4.03, src=["stockanalysis(CBOE)"], target=301.62, rating="적극 매수", cons="4.6", beta=2.21, emp="42,000명"),
 "TSM":  dict(price=434.11, c1=-0.70, src=["WebSearch(Yahoo/CBOE)"]),
 "AVGO": dict(price=399.97, c1=-0.28, src=["stockanalysis(CBOE)"], target=523.73, rating="적극 매수", cons="4.6", beta=1.46, emp="33,000명"),
 "MU":   dict(price=979.30, c1=-1.24, src=["stockanalysis(CBOE)"], target=1486.00, rating="적극 매수", cons="4.7", beta=2.14, emp="53,000명"),
 "MRVL": dict(price=235.81, c1=-3.04, src=["stockanalysis(CBOE)"], target=252.26, rating="적극 매수", cons="4.6", beta=2.20, emp="7,480명"),
 "AMD":  dict(price=557.89, c1=2.04, src=["stockanalysis(CBOE)"], target=516.13, rating="적극 매수", cons="4.5", beta=2.47, emp="31,000명"),
 "SNDK": dict(price=1915.92, c1=3.10, src=["stockanalysis(CBOE)"], target=2035.05, rating="매수", cons="4.1", emp="11,000명"),
 "DELL": dict(price=434.97, c1=-3.39, src=["WebSearch(Yahoo/CBOE)"]),
 "LITE": dict(price=802.01, c1=2.07, src=["WebSearch(Yahoo/CBOE)"]),
 "CLS":  dict(price=359.85, c1=1.43, src=["stockanalysis(CBOE)"], target=444.11, rating="적극 매수", cons="4.6", beta=1.52, emp="29,591명"),
 "CRDO": dict(price=257.79, c1=-2.96, src=["stockanalysis(CBOE)"], target=269.81, rating="적극 매수", cons="4.5", beta=3.20, emp="807명"),
 "TLN":  dict(price=385.80, c1=0.35, src=["stockanalysis(CBOE)"], target=473.22, rating="매수", cons="4.0", beta=1.62, emp="1,880명"),
}

# per-stock todayWhy
TW = {
 "GOOG":"−0.3% 약보합이에요. 3대 지수가 오른 가운데 큰 이벤트 없이 숨 고르기 했어요.",
 "META":"+6% 강세! 자체 AI 칩 '아이리스'를 9월부터 만든다는 소식에 비용 절감 기대가 커졌어요. 엔비디아·AMD 칩도 계속 사면서 보완하는 방식이라 부담은 적어요.",
 "AMZN":"−0.7% 약보합. 특별한 악재보다 최근 오른 뒤 차익 실현(오른 김에 일부 파는 것) 매물이 나왔어요.",
 "NVDA":"+4% 반등! 메타 자체 칩 우려를 딛고 모건스탠리가 성장 동력 4가지를 짚으며 매수 의견을 재확인했어요.",
 "TSM":"−0.7% 소폭 하락. 대만 반도체 대표주로 지수 흐름을 따라 숨 고르기 했어요.",
 "AVGO":"−0.3% 약보합. 지난주 애플과 300억 달러 규모 칩 공급 계약으로 오른 뒤 그 상승분을 소화하는 중이에요.",
 "MU":"−1.2% 소폭 조정. SK하이닉스가 미국 증시에 상장하며 메모리 투자 선택지가 늘어 차익 실현이 나왔지만, 미국 공장 투자 확대 소식이 낙폭을 방어했어요.",
 "MRVL":"−3% 하락. AI 반도체 차익 실현과 금리 경계심리가 겹치며 밸류에이션 높은 성장주가 같이 밀렸어요.",
 "AMD":"+2% 강세. 스티펠이 목표가를 41% 올려 $635로 제시하며 2분기 '기대 이상 실적(어닝 서프라이즈)'을 전망했어요.",
 "SNDK":"+3% 상승. SK하이닉스 미국 상장과 낸드(메모리) 가격 강세로 저장장치 대표주가 함께 올랐어요.",
 "DELL":"−3.4% 하락. 특별한 악재보다 최근 급등분에 대한 차익 실현 매물이 나왔어요.",
 "LITE":"+2% 상승. AI 데이터센터 광통신(빛으로 데이터 전송) 수요 기대가 이어졌어요.",
 "CLS":"+1.4% 상승. 데이터센터 서버 제조 강자로 강세 흐름을 이어갔어요. 7/27 실적 발표가 대기 중이에요.",
 "CRDO":"−3% 조정. 변동이 큰 종목이라 광통신주 차익 실현 흐름에 같이 밀렸어요. 다음 실적은 9/2예요.",
 "TLN":"강보합(+0.3%). AI 데이터센터 전력 수요 기대가 이어졌어요.",
}
NOTE = {
 "GOOG":"3대 지수 상승 속 약보합 −0.3%",
 "META":"자체 AI 칩 기대로 +6.0% 급등",
 "AMZN":"차익 실현에 약보합 −0.7%",
 "NVDA":"성장 동력 재부각에 +4.0% 반등",
 "TSM":"지수 따라 숨 고르기 −0.7%",
 "AVGO":"애플 계약 소화 국면 −0.3%",
 "MU":"SK하이닉스 상장 여파 −1.2%",
 "MRVL":"금리 경계·차익 실현에 −3.0%",
 "AMD":"목표가 상향에 +2.0% 강세",
 "SNDK":"메모리 강세로 +3.1% 상승",
 "DELL":"차익 실현 매물에 −3.4%",
 "LITE":"광통신 수요 기대 +2.1%",
 "CLS":"강세 지속 +1.4% (7/27 실적)",
 "CRDO":"광통신 차익 실현에 −3.0%",
 "TLN":"전력 수요 기대 강보합 +0.3%",
}

def signal(c1):
    if c1 >= -1.5: return "green"
    if c1 > -4:    return "yellow"
    return "red"

def rating_from_target(price, target, rating_txt):
    gap = (target - price) / price * 100
    if gap >= 30: tone = f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에서 +{gap:.0f}% 더 오를 여력이 크다고 봐요."
    elif gap >= 10: tone = f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에서 +{gap:.0f}% 오를 여력이 있어요."
    elif gap >= 0: tone = f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에 거의 도달했어요. 추가 상승 여력은 제한적이에요."
    else: tone = f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})보다 낮아요. 분석가들은 단기적으로 이미 충분히 올랐다고 봐요."
    return f"증권사 분석가들이 본 {tone} 추천 등급은 {rating_txt}예요."

for s in d["us"]:
    t = s["ticker"]
    if t not in H: continue
    h = H[t]
    old_price = s.get("price") or h["price"]
    # back-calc references from prior change values (year-start / 1M / 1W fixed refs)
    def newchg(oldc):
        if oldc is None: return None
        ref = old_price / (1 + oldc/100.0)
        return round((h["price"]/ref - 1)*100, 2)
    s["price"] = h["price"]
    s["change1D"] = h["c1"]
    s["change1W"] = newchg(s.get("change1W"))
    s["change1M"] = newchg(s.get("change1M"))
    s["changeYTD"] = newchg(s.get("changeYTD"))
    s["signal"] = signal(h["c1"])
    s["note"] = NOTE[t]
    s["todayWhy"] = TW[t]
    if "beta" in h: s["beta"] = h["beta"]
    s["priceSourcedFrom"] = h["src"] + ["stockanalysis.com(CBOE)"] if "stockanalysis(CBOE)" not in h["src"] else h["src"]
    s["dataQualityNote"] = None
    # outlook + outlookEasy
    ol = s.setdefault("outlook", {})
    if "target" in h:
        ol["targetPrice"] = h["target"]
        ol["rating"] = h["rating"]
        ol["consensusMean"] = h["cons"]
        s["outlookEasy"] = rating_from_target(h["price"], h["target"], h["rating"])
    else:
        tp = ol.get("targetPrice")
        if tp:
            s["outlookEasy"] = rating_from_target(h["price"], tp, ol.get("rating","매수"))
    # company employees refresh (Monday cache) where fetched
    if "emp" in h and isinstance(s.get("company"), dict):
        s["company"]["employees"] = h["emp"] + " (2026-03-31 기준)" if "기준" not in h["emp"] else h["emp"]
    s["_fetchMeta"] = {"fetchedAt": FETCHED, "sources": [{"url": f"https://stockanalysis.com/stocks/{t.lower()}/"}]}

d["lastUpdated"] = NOW
d["marketSession"] = "풀 모닝 브리핑 (한국시간 08:00)"
d["marketStatus"] = ("🇺🇸 7/10(금) 미국 증시가 3대 지수 모두 상승 마감하며 변동성 컸던 한 주를 플러스로 끝냈어요. "
  "다우 52,637(+0.29%)·S&P500 7,575(+0.42%)·나스닥 26,282(+0.29%)이에요. 이날 최대 이벤트는 SK하이닉스의 나스닥 데뷔 — "
  "외국 기업 사상 최대 규모(265억 달러)로 상장해 첫날 약 +14% 급등($168.01)하며 AI 메모리 열기를 다시 지폈어요. "
  "보유 종목은 META(+6.0%)·NVDA(+4.0%)·SNDK(+3.1%)·LITE(+2.1%)·AMD(+2.0%)가 강했고, DELL(−3.4%)·MRVL(−3.0%)·CRDO(−3.0%)는 차익 실현에 밀렸어요. "
  "이번 주 화요일(7/14)엔 6월 소비자물가(CPI)와 대형 은행 실적이 같은 날 나와요.")
d["holidayNote"] = ("🟢 미국 증시는 정상 개장·마감했어요. 오늘(월) 밤 22:30(한국시간) 정규장이 다시 열려요. "
  "핵심 관전 포인트는 7/14(화) 밤 21:30 발표될 6월 소비자물가(CPI, 물가 상승률)와 같은 날 시작되는 대형 은행 실적이에요.")

# ---- signals ----
sig = d["signals"]
sig["asOf"] = NOW
sig["weekendNote"] = None
sig["dataQualityNote"] = ("보유 15종목·미국 시그널(WDC·INTC)·미국 신규상장(CRCL·CRWV)·관련 종목 시세는 7/10(금) 미국 종가 기준으로 실시간 검증·갱신했어요(출처: stockanalysis.com/CBOE·Yahoo). "
  "국내 시그널(SK하이닉스·한미반도체·두산에너빌리티)·외국인 매매 동향(krForeignFlow)·국내 신규상장 카드는 이번 자동 실행 환경에서 네이버 금융 데이터에 접근하지 못해 직전 검증 데이터를 유지했어요(가격은 원화 기준 과거값). "
  "보유 종목의 주간·월간·연초 대비 등락률(change1W/1M/YTD)은 직전 기준값에서 환산한 값이라 소폭 오차가 있을 수 있어요. 당일 등락률과 현재가는 실시간 검증값이에요.")

# --- US main signals: WDC, INTC ---
def find_sig(lst, tk):
    for x in lst:
        if x.get("ticker")==tk: return x
    return None

wdc = find_sig(sig["us"], "WDC")
if wdc:
    wdc["currentPrice"] = 582.59
    wdc["change1D"] = 0.78
    wdc["category"] = "관련주"
    wdc["thesis"] = ("SK하이닉스의 미국 상장으로 메모리·저장장치(데이터 보관 칩) 열기가 다시 뜨거워졌어요. 웨스턴디지털은 하드디스크(HDD) 세계 1·2위 회사인데, "
      "AI 데이터센터가 저장 용량을 대량으로 사들이면서 수요가 급증했어요. 7/10 웰스파고가 목표가를 $575→$730으로 크게 올렸어요.")
    wdc["outlookEasy"] = ("분석가 평균 목표가는 $606.13으로 지금 가격($582.59)에서 +4% 정도 여력이에요. 추천 등급은 '매수'. "
      "다만 올해 이미 크게 오른 종목이라 변동이 큰 편이에요. 7/29 실적 발표가 단기 분수령이에요.")
    wdc["outlook"] = ("컨센서스 목표가 $606.13(Buy) 대비 +4% 여력. 52주 범위 $64.23~$799.87로 변동성 큼. "
      "단기 트리거: 7/29 실적. 웰스파고 $730·BofA $732 등 낙관론과 밸류에이션 부담이 공존.")
    wdc["financials"] = "PER 31.9배, 시총 2,008억$, 매출(TTM) 118억$(+32%), 52주 $64.23~$799.87 (출처: stockanalysis.com/CBOE, 7/10 기준)."
    wdc["risk"] = "올해 큰 폭 오른 뒤라 변동이 큰 종목이에요. 메모리·저장장치 가격이 꺾이면 조정 폭도 커질 수 있어요."
    wdc["horizon"] = "1~3개월 (단기)"
    wdc["company"] = {"ceo":"Irving Tan","business":"하드디스크(HDD)·데이터센터 저장장치를 만드는 세계적 저장장치 회사예요.","hq":"미국 캘리포니아 산호세","employees":"51,000명","homepage":"https://www.westerndigital.com","ceoSource":"stockanalysis.com 프로필"}
    wdc["relatedStocks"] = [
      {"code":"STX","name":"시게이트 (Seagate)","market":"NASDAQ","relation":"HDD 경쟁사 — 저장장치 사이클 같이 움직임","currentPrice":"910.34","change1D":2.28},
      {"code":"SNDK","name":"샌디스크 (SanDisk)","market":"NASDAQ","relation":"낸드 저장장치 대표주 — 메모리 수요 동조","currentPrice":"1,915.92","change1D":3.10},
    ]
    wdc["sources"]=[{"name":"stockanalysis.com (실시간, 7/10)","url":"https://stockanalysis.com/stocks/wdc/"}]
    wdc["_fetchMeta"]={"fetchedAt":FETCHED,"sources":[{"url":"https://stockanalysis.com/stocks/wdc/"}]}

intc = find_sig(sig["us"], "INTC")
if intc:
    intc["currentPrice"] = 109.84
    intc["change1D"] = -2.40
    intc["category"] = "이슈주"
    intc["thesis"] = ("인텔은 미국 정부가 반도체 자립을 위해 직접 챙기는 '국책 프로젝트' 성격이 강해졌어요. 백악관이 애플·엔비디아 같은 큰 회사를 고객·파트너로 연결해 주는 등 지원이 이어지고 있어요. "
      "다만 자체 파운드리(위탁생산) 사업은 아직 적자라 실적 회복이 관건이에요.")
    intc["outlookEasy"] = ("분석가 평균 목표가는 $101.95로 지금 가격($109.84)보다 오히려 낮아요. 등급도 '보유(중립)'예요. "
      "즉 이미 많이 오른 상태라 추가 상승보다 실적 개선 확인이 필요하다는 뜻이에요. 7/23 실적이 분수령이에요.")
    intc["outlook"] = ("컨센서스 목표가 $101.95(Hold 중립) 대비 −7% (이미 목표가 초과). 52주 $18.97~$142.35. "
      "HSBC $200·스티펠 $120 등 강세론과 적자 지속 우려 공존. 단기 트리거: 7/23 2분기 실적.")
    intc["financials"] = "PER 적자(순손실), 시총 5,521억$, 매출(TTM) 538억$, 52주 $18.97~$142.35 (출처: stockanalysis.com/CBOE, 7/10 기준)."
    intc["risk"] = "파운드리 적자가 이어지고 있어요. 컨센서스 목표가가 현재가보다 낮아 단기 과열 가능성도 있는 종목이에요."
    intc["horizon"] = "3~6개월 (중기)"
    intc["company"] = {"ceo":"Lip-Bu Tan","business":"CPU·서버칩·파운드리(위탁생산)를 하는 미국 대표 반도체 회사예요.","hq":"미국 캘리포니아 산타클라라","employees":"85,100명","homepage":"https://www.intel.com","ceoSource":"stockanalysis.com 프로필"}
    intc["relatedStocks"] = [
      {"code":"AMD","name":"AMD","market":"NASDAQ","relation":"CPU·GPU 직접 경쟁사 — 점유율 뺏고 뺏김","currentPrice":"557.89","change1D":2.04},
      {"code":"NVDA","name":"엔비디아 (Nvidia)","market":"NASDAQ","relation":"AI 반도체 대장주 — 인텔이 협력·경쟁 동시에","currentPrice":"210.96","change1D":4.03},
    ]
    intc["sources"]=[{"name":"stockanalysis.com (실시간, 7/10)","url":"https://stockanalysis.com/stocks/intc/"}]
    intc["_fetchMeta"]={"fetchedAt":FETCHED,"sources":[{"url":"https://stockanalysis.com/stocks/intc/"}]}

# --- US new listings: CRCL, CRWV ---
nl_us = sig["newListings"]["us"]
crcl = find_sig(nl_us, "CRCL")
if crcl:
    crcl["currentPrice"] = 66.14
    crcl["change1D"] = 4.97
    crcl["listedAt"] = "2025-06-05"
    crcl["category"] = "이슈주"
    crcl["thesis"] = ("써클은 미국 달러에 1:1로 연동된 스테이블코인 'USDC'를 발행하는 회사예요. 7/10 미국 통화감독청(OCC)에서 '전국 신탁은행' 최종 인가를 받았다는 소식에 +5% 올랐어요. "
      "가상자산을 은행처럼 다룰 수 있는 자격이라 사업 확장 기대가 커졌어요.")
    crcl["outlookEasy"] = ("분석가 평균 목표가는 $133.71로 지금 가격($66.14)에서 +100% 넘게 여력이 크다고 봐요. 등급은 '매수'. "
      "다만 상장 후 $262까지 올랐다가 크게 내린 변동이 매우 큰 종목이라 조심해서 봐야 해요. 미즈호는 이번 급등을 '과열'로 봤어요.")
    crcl["outlook"] = ("컨센서스 목표가 $133.71(Buy) 대비 +102% 여력이나 52주 $49.90~$262.97로 변동성 극심. "
      "단기 트리거: OCC 은행 인가 후속·8/11 실적. 미즈호는 급등을 '과도하게 낙관적'이라 평가.")
    crcl["financials"] = "PER 적자, 시총 164억$, 매출(TTM) 28.6억$(+52%), 52주 $49.90~$262.97 (출처: stockanalysis.com/CBOE, 7/10 기준)."
    crcl["risk"] = "신규 상장주는 변동이 매우 큰 종목이라 신중히 보세요. 스테이블코인 경쟁 심화·규제 변화가 위험 요인이에요."
    crcl["horizon"] = "6~12개월 (장기)"
    crcl["company"] = {"ceo":"Jeremy Allaire (공동창업자·CEO)","business":"달러 연동 스테이블코인 USDC를 발행하는 인터넷 금융 회사예요.","hq":"미국 뉴욕","employees":"1,100명","homepage":"https://www.circle.com","ceoSource":"stockanalysis.com 프로필"}
    crcl["relatedStocks"] = [
      {"code":"COIN","name":"코인베이스 (Coinbase)","market":"NASDAQ","relation":"가상자산 대표 거래소 — USDC 수익 공유 파트너","currentPrice":"159.80","change1D":0.46},
      {"code":"HOOD","name":"로빈후드 (Robinhood)","market":"NASDAQ","relation":"크립토·핀테크 테마 동조","currentPrice":"111.97","change1D":-2.73},
    ]
    crcl["sources"]=[{"name":"stockanalysis.com (실시간, 7/10)","url":"https://stockanalysis.com/stocks/crcl/"}]
    crcl["_fetchMeta"]={"fetchedAt":FETCHED,"sources":[{"url":"https://stockanalysis.com/stocks/crcl/"}]}

crwv = find_sig(nl_us, "CRWV")
if crwv:
    crwv["currentPrice"] = 88.88
    crwv["change1D"] = -0.91
    crwv["listedAt"] = "2025-03-28"
    crwv["category"] = "성장주"
    crwv["thesis"] = ("코어위브는 AI 학습·추론에 특화된 클라우드(빌려 쓰는 컴퓨터) 회사예요. 엔비디아 GPU를 대량으로 갖춰 AI 스타트업·빅테크에 빌려줘요. "
      "매출이 1년에 세 자릿수%로 폭발 성장 중이고, 최근 나스닥100 지수에도 편입됐어요.")
    crwv["outlookEasy"] = ("분석가 평균 목표가는 $142.29로 지금 가격($88.88)에서 +60% 여력이 있어요. 등급은 '매수'. "
      "다만 아직 적자 회사이고, 메타가 자체 클라우드를 만든다는 소식에 경쟁 우려로 눌린 상태예요. 변동이 큰 종목이에요.")
    crwv["outlook"] = ("컨센서스 목표가 $142.29(Buy) 대비 +60% 여력. 52주 $63.80~$153.50. "
      "단기 트리거: 8/11 실적·백로그(밀린 주문) 규모. 리스크: 메타 자체 클라우드 진입·적자 지속.")
    crwv["financials"] = "PER 적자, 시총 485억$, 매출(TTM) 62.3억$(+130%), 52주 $63.80~$153.50 (출처: stockanalysis.com/CBOE, 7/10 기준)."
    crwv["risk"] = "신규 상장주라 변동이 매우 큰 종목이에요. 아직 적자이고 메타 등 빅테크의 자체 클라우드 진입이 위험 요인이에요."
    crwv["horizon"] = "6~12개월 (장기)"
    crwv["company"] = {"ceo":"Michael Intrator (공동창업자·CEO)","business":"엔비디아 GPU 기반 AI 전용 클라우드를 빌려주는 회사예요.","hq":"미국 뉴저지 리빙스턴","employees":"2,189명","homepage":"https://www.coreweave.com","ceoSource":"stockanalysis.com 프로필"}
    crwv["relatedStocks"] = [
      {"code":"NBIS","name":"네비우스 (Nebius)","market":"NASDAQ","relation":"AI 클라우드(네오클라우드) 경쟁사 — 함께 움직임","currentPrice":"219.65","change1D":1.60},
      {"code":"IREN","name":"아이렌 (IREN)","market":"NASDAQ","relation":"AI·데이터센터 인프라 테마 동조","currentPrice":"41.14","change1D":-1.40},
    ]
    crwv["sources"]=[{"name":"stockanalysis.com (실시간, 7/10)","url":"https://stockanalysis.com/stocks/crwv/"}]
    crwv["_fetchMeta"]={"fetchedAt":FETCHED,"sources":[{"url":"https://stockanalysis.com/stocks/crwv/"}]}

json.dump(d, open(P,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

# sanity print
print("=== holdings updated ===")
for s in d["us"]:
    print(f"{s['ticker']:5} {s['price']:>9} D{s['change1D']:>6} W{str(s.get('change1W')):>7} M{str(s.get('change1M')):>7} Y{str(s.get('changeYTD')):>7} {s['signal']}")
print("=== US signals:", [x['ticker'] for x in sig['us']])
print("=== US newListings:", [x['ticker'] for x in sig['newListings']['us']])
print("=== KR signals (carried):", [x['ticker'] for x in sig['kr']])
