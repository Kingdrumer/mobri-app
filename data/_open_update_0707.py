# -*- coding: utf-8 -*-
import json, io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

NOW = "2026-07-07T22:45:00+09:00"

# ticker: (last, chgpct, open, prev, todayWhy)
DATA = {
 "GOOG": (367.28, 0.65, 367.24, 364.90, "+0.7% 소폭 올랐어요. 반도체가 흔들리자 투자자들이 검색·광고로 안정적으로 돈 버는 구글 같은 비(非)반도체 대형주로 갈아탄 덕을 봤어요."),
 "META": (610.98, 1.78, 607.59, 600.29, "+1.8% 올랐어요. 반도체를 피한 돈이 SNS·광고 대장주로 몰리면서 오늘 보유 종목 중 가장 강했어요."),
 "AMZN": (245.14, 0.40, 246.98, 244.16, "+0.4% 강보합. 반도체가 약한 날에도 클라우드·쇼핑 대형주로서 방어적인 흐름을 보였어요."),
 "NVDA": (192.33, -1.65, 192.37, 195.55, "-1.7% 내렸어요. 중국 딥시크가 자체 AI 칩을 만든다는 로이터 보도에 'AI 칩 수요가 줄까' 하는 걱정이 커졌어요."),
 "TSM": (437.08, -3.26, 438.02, 451.79, "-3.3% 하락. 엔비디아 칩을 위탁생산하는 회사라 딥시크 자체 칩 소식에 같이 밀렸어요."),
 "AVGO": (367.99, -1.58, 366.56, 373.90, "-1.6% 하락. AI 네트워크·맞춤형 칩 대표주라 반도체 파는 분위기에 동참했어요."),
 "MU": (924.90, -6.08, 923.01, 984.75, "-6.1% 급락. AI 메모리(HBM) 대장주인데 딥시크 자체 칩 우려로 반도체 투매의 직격탄을 맞았어요."),
 "MRVL": (234.64, -5.87, 234.92, 249.27, "-5.9% 급락. 맞춤형 AI 칩을 만드는 회사라 반도체가 팔리는 날 변동이 큰 편이에요."),
 "AMD": (515.00, -6.71, 515.91, 552.05, "-6.7% 급락. 어제 +6.6% 급등했던 만큼 딥시크 소식에 차익 실현 매물까지 겹쳐 되돌림이 컸어요."),
 "SNDK": (1608.18, -7.81, 1619.28, 1744.43, "-7.8% 급락. 낸드 메모리주로 원래 변동이 큰 편인데 반도체 투매에 오늘 보유 종목 중 낙폭이 가장 컸어요."),
 "DELL": (412.19, 0.09, 397.75, 411.80, "강보합(+0.1%). AI 서버 수요 기대가 버팀목이 돼 반도체가 약한 날에도 잘 버텼어요."),
 "LITE": (726.24, -0.69, 699.42, 731.25, "-0.7% 약보합. 광통신 부품주라 반도체만큼은 아니지만 기술주 약세에 소폭 밀렸어요."),
 "CLS": (344.22, -1.71, 339.90, 350.20, "-1.7% 하락. AI 서버를 위탁생산하는 회사라 반도체 파는 분위기를 함께 탔어요."),
 "CRDO": (250.90, -5.52, 249.86, 265.55, "-5.5% 하락. 어제 +9.8% 급등했던 변동 큰 종목이라 반도체 되돌림에 낙폭이 컸어요."),
 "TLN": (377.63, -0.04, 369.02, 377.79, "보합(0.0%). 전력·원자력 회사라 반도체 이슈와 상관이 적어 오늘도 흔들림 없이 버텼어요."),
}
DQ = "미국 정규장 개장 약 10분 뒤(한국시각 22:42경) 실시간 체결가예요. 장중이라 종가와는 달라질 수 있어요."

p = json.load(io.open("portfolio.json", encoding="utf-8"))
updated = 0
for h in p["us"]:
    t = h["ticker"]
    if t not in DATA:
        continue
    last, chgpct, opn, prev, why = DATA[t]
    sp = h["price"]  # stored price == prev close
    # back out reference prices from stored change fields, recompute with new last
    def recompute(storedChg):
        if storedChg is None: return None
        ref = sp/(1+storedChg/100.0)
        return round((last/ref-1)*100.0, 2)
    h["price"] = last
    h["change1D"] = round((last/prev-1)*100.0, 2)
    h["change1W"] = recompute(h.get("change1W"))
    h["change1M"] = recompute(h.get("change1M"))
    h["changeYTD"] = recompute(h.get("changeYTD"))
    h["todayWhy"] = why
    h["priceSourcedFrom"] = ["CNBC", "Yahoo"]
    h["dataQualityNote"] = DQ
    updated += 1

# indices snapshot (us list is holdings only; store index snapshot in a side key)
p["lastUpdated"] = NOW
p["marketSession"] = "US_OPEN_TUESDAY"
p["marketStatus"] = ("\U0001F1FA\U0001F1F8 7/7(화) 미국 증시는 개장 직후 반도체가 크게 흔들렸어요. "
  "중국 딥시크가 자체 AI 칩을 만든다는 로이터 보도에 필라델피아 반도체지수(SOX)가 -4.2% 급락하고, "
  "나스닥은 -0.8%. 반면 반도체를 피한 돈이 다른 대형주로 몰리며 다우는 53,138(+0.15%)로 사상 최고를 또 갈아치웠어요(순환매). "
  "S&P는 -0.2%, 공포지수(VIX) 15.9로 대체로 차분했어요. 보유 종목 중 SNDK -7.8%·AMD -6.7%·MU -6.1%가 약했고, "
  "META(+1.8%)·GOOG(+0.7%)는 올랐어요.")
p["holidayNote"] = ("\U0001F7E2 미국 증시는 정상 개장했어요. 오늘의 핵심은 '중국 딥시크의 자체 AI 칩 개발' 보도로 촉발된 반도체 투매예요. "
  "반도체를 팔고 비(非)반도체 대형주로 갈아타는 순환매가 나오면서 다우만 사상 최고를 경신했어요.")

json.dump(p, io.open("portfolio.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("portfolio updated:", updated, "stocks")
for h in p["us"]:
    print(h["ticker"], h["price"], "1D", h["change1D"], "1W", h["change1W"], "1M", h["change1M"], "YTD", h["changeYTD"])
