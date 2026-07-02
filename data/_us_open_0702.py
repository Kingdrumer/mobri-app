import json, datetime

NOW = "2026-07-02T22:45:00+09:00"

# averaged CNBC + Yahoo open prices, and true prev close (both sources agree)
# ticker: (cnbc, yahoo, prevClose_true)
Q = {
 "GOOG": (358.85, 358.71, 357.89),
 "META": (599.27, 599.84, 612.91),
 "AMZN": (243.52, 243.605, 241.70),
 "NVDA": (197.89, 197.61, 197.58),
 "TSM":  (449.48, 448.964, 444.29),
 "AVGO": (369.01, 369.46, 369.34),
 "MU":   (1044.18, 1041.99, 1032.28),
 "MRVL": (266.73, 265.79, 272.05),
 "AMD":  (531.85, 530.925, 540.88),
 "SNDK": (1996.10, 1992.405, 2032.22),
 "DELL": (407.21, 406.02, 425.48),
 "LITE": (782.00, 784.995, 801.16),
 "CLS":  (352.79, 353.26, 361.62),
 "CRDO": (253.13, 253.37, 259.09),
 "TLN":  (370.81, 371.75, 360.79),
}

# per-stock signal + friendly todayWhy (market OPEN, 22:30 KST)
INFO = {
 "GOOG": ("green", "6월 고용이 예상보다 약하게 나오자 금리 부담이 줄면서, 어제에 이어 소프트웨어 빅테크로 돈이 도는 순환매 흐름에 개장 직후 +0.3% 안팎 올랐어요."),
 "META": ("yellow", "전날 'AI 계산능력 판매' 소식에 +8.8% 급등했던 만큼, 오늘은 오른 김에 일부 파는 차익실현이 나오며 개장 직후 -2%대로 숨 고르기 중이에요."),
 "AMZN": ("green", "약한 고용지표로 금리 인하 기대가 살아나며 빅테크 훈풍을 받아 개장 직후 +0.8% 안팎 강세로 출발했어요."),
 "NVDA": ("green", "어제 반도체 급락의 진앙이었지만 오늘은 낙폭 과대 인식에 개장 직후 보합권(±0%)에서 안정을 찾는 모습이에요."),
 "TSM": ("green", "전날 -6.8% 급락했던 반동으로 저가 매수가 들어오며 개장 직후 +1%대 반등으로 출발했어요."),
 "AVGO": ("yellow", "반도체 전반이 진정되며 개장 직후 보합권에서 방향을 탐색 중이에요. 최근 낙폭이 컸던 만큼 변동은 이어질 수 있어요."),
 "MU": ("green", "어제 -6.9% 크게 빠졌던 마이크론이 오늘은 저가 매수에 개장 직후 +1%대 반등하며 메모리주 반등을 이끌고 있어요."),
 "MRVL": ("yellow", "전날 -8.7% 급락 뒤에도 매물이 이어지며 개장 직후 -2%대 약세가 계속되고 있어요. 변동이 큰 종목이라 흐름을 가볍게 지켜보면 좋아요."),
 "AMD": ("yellow", "반도체 차익실현 여파가 남아 개장 직후 -1.8% 안팎 약세로 출발했어요. 변동이 큰 성장주라 등락 폭이 클 수 있어요."),
 "SNDK": ("yellow", "올해 크게 오른 만큼 차익실현 매물이 이어져 개장 직후 -1.9% 안팎 약세예요. 최근 변동이 매우 큰 종목이에요."),
 "DELL": ("red", "메모리 값 상승이 서버 원가 부담으로 번질 수 있다는 모건스탠리의 등급 하향(분석가가 투자 매력 등급을 낮춘 것) 여파로 개장 직후 -4%대로 가장 크게 밀렸어요."),
 "LITE": ("yellow", "광통신 부품주로, 반도체 조정 분위기에 함께 눌리며 개장 직후 -2%대 약세로 출발했어요."),
 "CLS": ("yellow", "AI 서버 조립주로 반도체 조정과 함께 개장 직후 -2%대로 밀렸어요. 최근 흐름 대비 변동이 커진 구간이에요."),
 "CRDO": ("yellow", "AI 데이터센터 연결 부품주로, 반도체 차익실현 흐름에 동조하며 개장 직후 -2%대 약세예요."),
 "TLN": ("green", "지난주 -17.8% 크게 빠졌던 전력주가 오늘은 저가 매수와 데이터센터 전력 수요 기대가 살아나며 개장 직후 +3% 안팎 반등으로 출발했어요."),
}

d = json.load(open("portfolio.json"))

for s in d["us"]:
    t = s["ticker"]
    if t not in Q:
        continue
    cnbc, yh, prev = Q[t]
    price = round((cnbc + yh) / 2, 2)
    chg1d = round((price / prev - 1) * 100, 2)
    # recompute 1W/1M/YTD keeping historical anchor from prior stored values
    op = s["price"]
    for fld in ["change1W", "change1M", "changeYTD"]:
        old = s.get(fld)
        if old is None:
            continue
        anchor = op / (1 + old / 100.0)
        s[fld] = round((price / anchor - 1) * 100, 2)
    s["price"] = price
    s["change1D"] = chg1d
    sig, why = INFO[t]
    s["signal"] = sig
    s["todayWhy"] = why
    s["priceSourcedFrom"] = ["CNBC", "Yahoo"]
    s["dataQualityNote"] = None

# top-level session fields
d["lastUpdated"] = NOW
d["marketSession"] = "US_OPEN"
d["marketStatus"] = ("\U0001F7E2 7/2(목) 미국 정규장 개장(22:30 KST) — 6월 고용 약하게(NFP 5.7만 명, 예상 11.3만 명) 나오며 금리 부담 완화 → S&P500 +0.5%·나스닥 +0.3%·다우 +0.6% 강보로 출발. 전날 급락했던 반도체(MU·TSM)는 저가 매수로 반등, 메타는 차익실현으로 -2%대 숨 고르기. VIX 16.1로 안정. 7/3(금) 독립기념일 휴장이라 이번 주 미 정규장은 오늘이 마지막.")
d["holidayNote"] = ("\U0001F7E2 오늘(7/2) 미국 정규장이 22:30 KST 개장했어요. 가격은 개장 직후 값 기준이에요. 7/3(금)은 미국 독립기념일 휴장이라 이번 주 미 정규장은 오늘 밤이 마지막이에요.")

json.dump(d, open("portfolio.json", "w"), ensure_ascii=False, indent=2)
print("portfolio.json updated")
for s in d["us"]:
    print(f"{s['ticker']:5} {s['price']:>9} 1D={s['change1D']:>6} 1W={s['change1W']:>6} 1M={s['change1M']:>6} YTD={s['changeYTD']:>7} {s['signal']}")
