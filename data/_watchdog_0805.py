#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mobri 워치독 자가복구 — 2026-08-05 풀 브리핑 (8/4 화 미국 종가 정산)"""
import json, os, shutil, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(BASE, *a)

TODAY = "2026-08-05"
NOW_KST = "2026-08-05T09:55:00+09:00"

# ---- 8/4(화) 미국 종가 검증 데이터 ----
# prev = 8/3 종가(기존 portfolio), new = 8/4 종가, verified 여부
PRICES = {
    # ticker: (new_price, sources, note, verified)
    "GOOG": (375.35, ["Motley Fool 실시간 티커", "CNN Business"], None, True),
    "META": (587.94, ["Motley Fool 실시간 티커", "CNN Business"], None, True),
    "AMZN": (277.42, ["Motley Fool 실시간 티커", "CNN Business"], None, True),
    "NVDA": (211.94, ["Motley Fool 실시간 티커", "TradingKey"], None, True),
    "AMD":  (518.58, ["Yahoo Finance", "TradingKey"], "정규장 +7.0% 마감 후 실적 발표 → 시간외 약 -8%", True),
    "AVGO": (409.29, ["TradingKey(8/4 마감)", "WebSearch"], None, True),
    "MU":   (878.86, ["TradingKey(8/4)", "WebSearch"], None, True),
    "MRVL": (219.83, ["TradingKey(8/4 마감)", "WebSearch"], None, True),
    "SNDK": (1433.45, ["TradingKey(+11.51%)", "WebSearch($1,430.59)"], "두 출처 평균(<0.5% 차이)", True),
    "DELL": (452.72, ["TradingKey(8/4 마감)", "WebSearch"], None, True),
    "LITE": (849.47, ["WebSearch(종가 $849.47)", "Benzinga"], None, True),
    # 미검증 — 8/4 종가 신뢰성 확보 실패 → 8/3 종가 유지, 추측 안 함
    "TSM":  (None, ["WebSearch"], "8/4 미국 종가 미확인 — 직전(8/3) 종가 유지", False),
    "CLS":  (None, ["WebSearch"], "8/4 미국 종가 미확인 — 직전(8/3) 종가 유지", False),
    "CRDO": (None, ["WebSearch"], "8/4 미국 종가 미확인 — 직전(8/3) 종가 유지", False),
    "TLN":  (None, ["WebSearch"], "8/4 미국 종가 미확인 — 직전(8/3) 종가 유지", False),
}

# 8/4 종목별 상승 이유 (검증된 종목만 갱신)
TODAY_WHY = {
    "GOOG": "빅테크 랠리에 소폭 동참하며 +0.8% 올랐어요. TPU(구글 자체 AI 칩) 물량 확대 기대가 이어졌어요.",
    "META": "빅테크가 대체로 강했지만 메타는 차익실현에 -0.4% 소폭 조정됐어요. 급등 뒤 숨 고르기예요.",
    "AMZN": "시총 3조 달러 돌파 직후 차익실현 매물에 -2.3% 되밀렸어요. 급등 뒤 단기 출렁임이에요.",
    "NVDA": "AI 반도체 대표주로 +2.6% 오르며 지수 신고가 랠리에 힘을 보탰어요.",
    "AMD":  "정규장에서 +7.0% 급등해 마감했지만, 장 마감 후 2분기 실적(매출 +50% 신기록)이 '기대만큼 폭발적이진 않다'는 평가에 시간외에서 약 -8% 되밀렸어요.",
    "AVGO": "AI 네트워킹·맞춤형 칩(ASIC) 수요 기대에 +4.4% 올랐어요.",
    "MU":   "메모리 업황 반등 기대와 FMS 2026(메모리·스토리지 연례 행사)을 앞두고 +6.0% 올랐어요.",
    "MRVL": "차세대 AI 메모리·스토리지 솔루션 공개 소식에 +13.4% 급등하며 주가가 $200을 넘었어요.",
    "SNDK": "낸드 메모리 강세와 8/5 실적 기대가 겹치며 +11.5% 급등했어요. 오늘(8/5) 밤 실적을 발표해요.",
    "DELL": "기업용 AI 서버 수요와 하드웨어 교체 사이클 회복 기대에 +8.6% 급등했어요.",
    "LITE": "미국이 중국산 광통신 모듈 수입 규제를 추진한다는 소식에 광통신 수혜주로 부각되며 종가 $849.47로 크게 올랐어요.",
}

def approx(a, b):
    return round((a - b) / b * 100, 2)

# ---------- 1) portfolio.json 갱신 ----------
pf_path = p("portfolio.json")
shutil.copy(pf_path, p("portfolio.json.before-full-morning-0805.bak"))
pf = json.load(open(pf_path, encoding="utf-8"))

guard_ok, guard_warn = [], []
for h in pf["us"]:
    t = h["ticker"]
    if t not in PRICES:
        continue
    new_price, sources, note, verified = PRICES[t]
    if verified and new_price is not None:
        old = h["price"]
        d1 = approx(new_price, old)
        # 누적수익률 근사 롤포워드 (직전 값 + 당일 변동)
        for k in ("change1W", "change1M", "changeYTD"):
            if isinstance(h.get(k), (int, float)):
                h[k] = round(h[k] + d1, 2)
        h["price"] = new_price
        h["change1D"] = d1
        h["priceSourcedFrom"] = sources
        h["dataQualityNote"] = note
        if t in TODAY_WHY:
            h["todayWhy"] = TODAY_WHY[t]
        # 시간외: 이번 캡처는 정규장 종가 기준 → AMD만 실적 반영, 나머지 stale 제거
        if t == "AMD":
            h["afterHoursPrice"] = 477.1
            h["afterHoursChange1D"] = -8.0
        else:
            h["afterHoursPrice"] = None
            h["afterHoursChange1D"] = None
        guard_ok.append(f"{t} {old}→{new_price} ({d1:+}%)")
    else:
        # 미검증 — 가격 유지, 경고 노트
        h["dataQualityNote"] = note
        h["afterHoursPrice"] = None
        h["afterHoursChange1D"] = None
        guard_warn.append(f"{t} 8/4 미확인(8/3 {h['price']} 유지)")

pf["lastUpdated"] = NOW_KST
pf["marketSession"] = ("수요일 오전 8/5 (KST) 워치독 자가복구. 직전 미국 거래일 8/4(화) 마감을 정산했어요. "
    "3대 지수가 사상 최고를 새로 썼어요 — 다우 54,085.88(+1.71%, 5.4만 첫 돌파)·S&P500 7,736.52(+1.79%)·"
    "나스닥 26,584.99(+2.59%). 팰런티어가 실적 서프라이즈로 +29% 폭등하며 AI 소프트웨어 강세를 이끌었어요. "
    "장 마감 후 보유 종목 AMD는 실적을 냈지만 시간외 약 -8% 조정됐어요. 미국 정규장은 오늘 밤 22:30 KST 개장 예정이에요.")
pf["holidayNote"] = ("🟢 오늘은 평일(수)이라 미국장은 오늘 밤 22:30 KST 정상 개장해요. "
    "오늘 밤엔 보유 종목 샌디스크(SNDK)·탈렌에너지(TLN) 실적이 발표돼요.")
pf["dataNote"] = ("수요일 오전(8/5) 워치독 자가복구 풀 브리핑. 보유 15종목 중 11종목은 8/4(화) 미국 종가를 "
    "CNBC/Motley Fool·Yahoo Finance·TradingKey 교차검증으로 갱신했어요(빅테크 4종목은 실시간 티커로 이중 확인). "
    "TSM·CLS·CRDO·TLN 4종목은 8/4 종가를 신뢰성 있게 확인하지 못해 추측 없이 8/3 종가를 유지했고 각 종목에 표시했어요. "
    "국내 시그널 데이터는 직전 회차 기준을 유지했어요.")

json.dump(pf, open(pf_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("✓ portfolio.json 갱신")
print("  검증 OK:", len(guard_ok), "| 경고:", len(guard_warn))
for g in guard_warn: print("   ⚠", g)
