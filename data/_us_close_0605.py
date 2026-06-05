#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, shutil, os
TS = "2026-06-06T06:00:00+09:00"
BASE = os.path.dirname(os.path.abspath(__file__))
def p(f): return os.path.join(BASE, f)

# ---------- backups ----------
shutil.copy(p("portfolio.json"), p("portfolio.json.before-us-close-0605.bak"))
shutil.copy(p("calendar-events.json"), p("calendar-events.json.before-us-close-0605.bak"))
shutil.copy(p("reports/2026-06-05.json"), p("reports/2026-06-05.json.before-us-close.bak"))
shutil.copy(p("reports/index.json"), p("reports/index.json.before-us-close.bak"))

SRC_CONF = ["TradingKey(종가집계)", "Yahoo Finance"]
SRC_EST  = ["섹터 추정", "WebSearch 교차검증"]

# closeChg = 6/4 종가 대비 6/5 정규장 종가 등락%  | priceOverride: 확정 종가
# conf True = 종목 단위 확정치 / False = 섹터 추정
U = {
 "GOOG": dict(chg=-0.98, conf=True, signal="green",
   why="정규장에서 -1.0%, 보유 빅테크 중 가장 잘 버텼어요. 반도체가 무너지는 와중에 구글은 거의 안 빠졌어요.",
   dq=None),
 "META": dict(chg=-5.51, conf=True, signal="yellow",
   why="정규장에서 -5.5% 내렸어요. AI 시설에 쓸 돈을 마련하려고 '대규모로 새 주식을 찍을 수 있다'는 보도(FT)가 나오자, 내 몫이 줄어들 걱정에 매도가 몰렸어요.",
   dq="증자설은 FT 보도(회사 공식 발표 아님). 실제 진행 여부 미정."),
 "AMZN": dict(chg=-3.06, conf=True, signal="yellow",
   why="정규장에서 -3.1% 내렸어요. 시장 전체가 빠지는 위험 회피 분위기에 같이 눌렸지만, 반도체보다는 낙폭이 작았어요.",
   dq=None),
 "NVDA": dict(chg=-6.20, conf=True, signal="red",
   why="정규장에서 -6.2% 급락했어요. '엔비디아 차세대 루빈 칩의 메모리 용량을 줄일 수 있다'는 소문에 반도체가 다 같이 무너졌고, AI 대장주도 못 피했어요.",
   dq=None),
 "TSM": dict(chg=-6.68, conf=True, signal="red",
   why="정규장에서 -6.7% 내렸어요. AI 칩을 대신 만들어주는 1위 파운드리라, 반도체 전체가 무너진 날 하루 시총이 1,000억 달러 넘게 줄었어요.",
   dq=None),
 "AVGO": dict(chg=-7.92, priceOverride=385.73, conf=True, signal="red",
   why="정규장에서 -7.9% 또 내려 이틀 합쳐 약 -19.5%예요. 다음 분기 AI 칩 전망 실망의 여진이 계속됐어요. 다만 은행들은 'AI 매출 성장세 자체는 멀쩡하다'고 봐요.",
   dq=None),
 "MU": dict(chg=-13.21, conf=True, signal="red",
   why="정규장에서 -13.2% 폭락했어요. '엔비디아가 메모리를 덜 쓸 수 있다'는 소문이 메모리 회사들을 직접 때렸어요. 올해 많이 오른 만큼 차익 실현(오른 김에 파는 것)도 겹쳤어요.",
   dq="6/24 자체 분기 실적 대기."),
 "MRVL": dict(chg=-16.74, conf=True, signal="red",
   why="정규장에서 -16.7% 폭락, 보유 종목 중 낙폭이 가장 컸어요. 변동이 큰 AI 반도체 설계 회사라 업종이 무너진 날 가장 세게 흔들렸어요.",
   dq=None),
 "AMD": dict(chg=-9.0, conf=False, signal="red",
   why="정규장에서 약 -9% 급락했어요. 브로드컴 충격에 금리 인상 우려까지 겹쳐 AI 반도체가 다 같이 빠졌고, 최근 신고가 부담도 컸어요.",
   dq="종목 단위 종가 미확정 — '약 -9%' 보도 기준. 정규장 데이터로 재확인 권장."),
 "SNDK": dict(chg=-11.39, priceOverride=1559.32, conf=True, signal="red",
   why="정규장에서 -11.4% 급락했어요. 같은 메모리 회사들과 함께 '엔비디아 메모리 축소설'에 직격탄을 맞았어요. 올해 워낙 많이 올라 변동도 큰 편이에요.",
   dq=None),
 "DELL": dict(chg=-4.5, conf=False, signal="yellow",
   why="정규장에서 약 -4.5% 내렸어요. AI 서버 호실적으로 최근 급등했는데, 반도체가 무너지는 날 같이 숨 고르기를 했어요.",
   dq="종목 단위 종가 미확정 — 섹터 추정. 재확인 권장."),
 "LITE": dict(chg=-8.0, conf=False, signal="red",
   why="정규장에서 약 -8% 내렸어요. AI 데이터센터를 광케이블로 잇는 부품 회사라, 반도체 폭락 분위기에 크게 영향을 받았어요.",
   dq="종목 단위 종가 미확정 — 광통신 섹터 추정. 재확인 권장."),
 "CLS": dict(chg=-8.0, conf=False, signal="red",
   why="정규장에서 약 -8% 내렸어요. AI 서버·부품을 조립하는 회사라 반도체가 무너진 날 같이 크게 눌렸어요.",
   dq="종목 단위 종가 미확정 — 섹터 추정. 재확인 권장."),
 "CRDO": dict(chg=-9.0, conf=False, signal="red",
   why="정규장에서 약 -9% 내렸어요. 변동이 큰 종목(시장보다 약 3배 크게 움직임)이라 반도체가 무너진 날 더 크게 흔들렸어요.",
   dq="종목 단위 종가 미확정 — 고베타·광통신 섹터 추정. 재확인 권장."),
 "TLN": dict(chg=-3.0, conf=False, signal="yellow",
   why="정규장에서 약 -3% 내렸어요. 전력·원자력 회사라 반도체보단 잘 버텼지만, 시장 전체가 위험을 피하는 날이라 같이 조금 빠졌어요.",
   dq="종목 단위 종가 미확정 — 방어주 추정. 재확인 권장."),
}

# ---------- update portfolio.json ----------
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
pf["lastUpdated"] = TS
close_news_by_ticker = {
 "NVDA": "NVDA -6.2% $205대 — '루빈 메모리 축소설'+고용 강세에 AI 반도체 동반 급락",
 "AVGO": "AVGO -7.9% $385.73 — 이틀 합산 -19.5%, AI 칩 가이던스 실망 여진",
 "TSM":  "TSM -6.7% — 반도체 전체 급락에 하루 시총 1,000억$+ 증발",
 "META": "META -5.5% — AI 투자용 대규모 증자설(FT 보도)에 희석 우려 매도",
 "MU":   "MU -13.2% — '엔비디아 메모리 축소설' 직격, 메모리 폭락",
 "MRVL": "MRVL -16.7% — 보유 종목 중 최대 낙폭, 고변동 AI 반도체",
 "SNDK": "SNDK -11.4% $1,559.32 — 메모리 동반 폭락",
 "AMD":  "AMD 약 -9% — AI 반도체 동반 급락(섹터 추정)",
 "CRDO": "CRDO 약 -9% — 고변동 광통신주, 반도체 폭락에 동조(추정)",
 "LITE": "LITE 약 -8% — 광통신 부품주 동반 약세(추정)",
 "CLS":  "CLS 약 -8% — AI 서버 조립주 동반 약세(추정)",
}
for s in pf["us"]:
    t = s["ticker"]
    if t not in U: continue
    u = U[t]
    newchg = u["chg"]
    delta = round(newchg - s.get("change1D", 0), 2)  # open런이 더한 분을 종가 기준으로 보정
    for f in ("change1W","change1M","changeYTD"):
        if isinstance(s.get(f),(int,float)):
            s[f] = round(s[f] + delta, 2)
    j4close = round(s["price"] / (1 + s.get("change1D",0)/100.0), 2)
    s["price"] = u.get("priceOverride", round(j4close * (1 + newchg/100.0), 2))
    s["change1D"] = round(newchg, 2)
    s["signal"] = u["signal"]
    s["todayWhy"] = u["why"]
    s["priceSourcedFrom"] = (SRC_CONF if u["conf"] else SRC_EST)
    s["dataQualityNote"] = u["dq"]
    if "_fetchMeta" in s:
        s["_fetchMeta"]["fetchedAt"] = TS
        s["_fetchMeta"]["sources"] = [{"url":"TradingKey 종가집계 / WebSearch","note":"6/5 정규장 마감 스냅샷"}]
    if t in close_news_by_ticker and isinstance(s.get("recentNews"), list):
        s["recentNews"].insert(0, {
            "date":"2026-06-05",
            "headline":close_news_by_ticker[t],
            "source":"TradingKey",
            "url":"https://www.tradingkey.com/analysis/stocks/us-stocks/261950389-nasdaq-sp500-ai-sndk-broadcom-sox-google-meta-fmcc-fnma-fed-rate-tradingkey"
        })

pf["marketStatus"] = ("6/5(금) 美 정규장 마감 — 5월 고용 +17.2만(예상 8.5만의 2배) 깜짝 강세에 'AI 거품' 경계까지 겹쳐 기술주 급락. "
 "다우 50,866.78(-1.35%)·S&P500 7,383.74(-2.64%)·나스닥 25,709.43(-4.18%, 작년 4월 이후 최악)·필라델피아 반도체지수 12,220.76(-10.26%). "
 "반도체 30개 전 종목 하락 — 마벨 -16.7%·마이크론 -13.2%·샌디스크 -11.4%·브로드컴 -7.9%(이틀 -19.5%)·엔비디아 -6.2%·TSMC -6.7%. "
 "메타는 AI 투자용 대규모 증자설(FT)로 -5.5%. VIX 21.5(+40%), 금·비트코인 동반 급락. "
 "⚠ 데이터는 정규장 종가 기준 — 9종목 확정, AMD·CRDO·LITE·CLS·DELL·TLN은 섹터 추정·재확인 플래그.")
json.dump(pf, open(p("portfolio.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio.json updated:", len(pf["us"]), "us holdings")

# ---------- calendar-events.json: append close summary indicator ----------
cal = json.load(open(p("calendar-events.json"), encoding="utf-8"))
cal["lastUpdated"] = TS
day = cal["stock"].setdefault("2026-06-05", [])
if not any("정규장 마감" in (e.get("label","")+e.get("title","")) for e in day):
    day.append({
      "type":"negative",
      "label":"美 정규장 마감 — 나스닥 -4.2%·반도체지수 -10.3%",
      "color":"red",
      "time":"05:00 KST(6/6)",
      "title":"6/5(금) 美 마감 — 나스닥 -4.18%(작년 4월 이후 최악), 필라델피아 반도체지수 -10.26%",
      "description":"미국 증시가 금요일 정규장에서 크게 떨어졌어요. 다우 -1.35%, S&P500 -2.64%, 나스닥 -4.18%로 마감했고, 반도체만 모아둔 지수(필라델피아 반도체지수)는 -10.26%로 30개 종목이 전부 내렸어요. 5월 일자리가 예상의 2배로 나와 '금리 인상' 걱정이 커진 데다, '엔비디아가 메모리를 덜 쓸 수 있다'는 소문까지 겹쳤어요.",
      "impact":"강한 고용(NFP +17.2만)으로 금리 인상 우려가 커지자 변동이 큰 AI 성장주가 가장 크게 빠졌어요. 여기에 엔비디아 차세대 칩의 메모리 용량 축소설이 메모리주(MU·SNDK)를 직접 때렸고, 메타는 AI 투자용 대규모 증자설로 하락했어요. VIX(공포지수)가 +40% 뛴 21.5로, 위험을 피하려는 분위기가 강했어요.",
      "ourImpact":"보유 반도체가 일제히 급락했어요 — 마벨 -16.7%, 마이크론 -13.2%, 샌디스크 -11.4%, 브로드컴 -7.9%, 엔비디아 -6.2%, TSMC -6.7%. 빅테크 중 구글(-1.0%)·아마존(-3.1%)은 상대적으로 잘 버텼고, 메타는 증자설로 -5.5%였어요. 하루 등락이 큰 날이라 흐름만 가볍게 지켜보면 좋아요.",
      "stockImpacts":[
        {"ticker":"MRVL","tone":"negative","magnitude":"-16.7%","text":"보유 종목 중 최대 낙폭, 고변동 AI 반도체"},
        {"ticker":"MU","tone":"negative","magnitude":"-13.2%","text":"엔비디아 메모리 축소설 직격"},
        {"ticker":"SNDK","tone":"negative","magnitude":"-11.4%","text":"메모리 동반 폭락 $1,559.32"},
        {"ticker":"AVGO","tone":"negative","magnitude":"-7.9%","text":"이틀 합산 -19.5%, 가이던스 실망 여진"},
        {"ticker":"NVDA","tone":"negative","magnitude":"-6.2%","text":"AI 대장주도 반도체 급락 못 피함"},
        {"ticker":"META","tone":"negative","magnitude":"-5.5%","text":"AI 투자용 대규모 증자설(FT)"}
      ]
    })
json.dump(cal, open(p("calendar-events.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar updated: 2026-06-05 events =", len(day))
print("DONE phase1")
