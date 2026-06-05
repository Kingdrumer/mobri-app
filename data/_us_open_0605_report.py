#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
TS = "2026-06-05T22:46:00+09:00"
BASE = os.path.dirname(os.path.abspath(__file__))
def p(f): return os.path.join(BASE, f)

# reuse open data from portfolio (already updated)
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
byT = {s["ticker"]: s for s in pf["us"]}

rep = json.load(open(p("reports/2026-06-05.json"), encoding="utf-8"))
rep["lastUpdated"] = TS

# sync stockSnapshot to open prices
for snap in rep.get("stockSnapshot", []):
    t = snap["ticker"]
    if t in byT:
        s = byT[t]
        snap["price"] = s["price"]
        snap["change1D"] = s["change1D"]
        snap["change1W"] = s["change1W"]
        snap["change1M"] = s["change1M"]
        snap["changeYTD"] = s["changeYTD"]
        snap["signal"] = s["signal"]
        snap["priceSourcedFrom"] = s["priceSourcedFrom"]
        snap["dataQualityNote"] = s["dataQualityNote"]

# update marketStatus
rep["marketStatus"] = pf["marketStatus"]

# prepend open-session news (categorized, 3-field required)
open_news = [
 {"category":"미국 증시",
  "headline":"S&P·나스닥 개장 하락 — 고용 강세에 '금리 인상' 베팅 반전",
  "oneLineSummary":"미국 증시가 개장에서 하락 출발했어요. 5월 일자리가 예상의 2배 가까이 늘면서 '금리를 내릴 거란 기대'가 '오히려 올릴 수도 있다'로 바뀌었고, 금리에 민감한 기술주가 눌렸어요. S&P500은 -0.7%, 나스닥은 -1.3%로 시작했어요.",
  "summary":"6/5 개장 S&P500 7,528.27(-0.74%), 나스닥 26,494.53(-1.25%), 다우 51,487.32(-0.14% 보합). 5월 고용 깜짝 강세로 10년물 국채금리가 +5.5bp 뛰며 위험자산, 특히 고밸류 기술·반도체가 약세. S&P500은 1985년 이후 최장 '10주 연속 상승' 기록이 위협받는 중.",
  "ourImpact":"보유 종목 다수가 금리에 민감한 AI 성장주라 개장 분위기는 무거웠어요. 반도체(NVDA -2.4%·MU -3.6%)가 약했고, 빅테크(GOOG·META·AMZN)는 약보합 수준으로 상대적으로 버텼어요.",
  "impact":"negative",
  "sources":[{"name":"Yahoo Finance (6/5 개장 라이브)","url":"https://finance.yahoo.com/markets/live/stock-market-today-sp-500-nasdaq-slide-as-jobs-report-fuels-fed-hike-bets-230134469.html"}]},
 {"category":"미국 증시",
  "headline":"러셀2000 +1.5% 나홀로 강세 — 반도체서 중소형주로 이동",
  "oneLineSummary":"대형 기술주가 빠지는 동안 중소형주 지수인 러셀2000은 +1.5% 올라 나홀로 강세였어요. 경기가 탄탄하다는 고용 지표가 경기 민감한 중소형주엔 오히려 호재로 작용하면서, 돈이 반도체에서 다른 업종으로 옮겨가는 흐름이 이어졌어요.",
  "summary":"6/5 개장 러셀2000 2,935.33(+1.45%)로 3대 지수와 차별화. 강한 고용→경기 자신감이 경기민감·내수 중소형주에 우호적으로 작용. 반도체·고밸류 성장주에서 가치·중소형주로의 로테이션이 이틀째 진행. VIX는 15.95(+3.6%)로 소폭 상승.",
  "ourImpact":"우리 포트폴리오는 대형 AI주 중심이라 러셀 강세의 직접 수혜는 적어요. 다만 '돈이 한 업종에서 다른 업종으로 옮겨다니는' 로테이션 국면이라, 반도체가 쉬어갈 때 빅테크·전력주(TLN)가 받쳐주는 구조를 참고하면 좋아요.",
  "impact":"neutral",
  "sources":[{"name":"Yahoo Finance (6/5 개장)","url":"https://finance.yahoo.com/markets/live/stock-market-today-sp-500-nasdaq-slide-as-jobs-report-fuels-fed-hike-bets-230134469.html"}]},
 {"category":"개별 종목",
  "headline":"보유 반도체 이틀째 약세 — 엔비디아 -2.4%, 마이크론 -3.6%",
  "oneLineSummary":"보유 종목인 엔비디아가 개장에서 -2.4%, 마이크론이 -3.6% 내렸어요. 브로드컴의 다음 분기 AI 칩 전망 실망이 이틀째 반도체 전반으로 번졌고, 강한 고용에 금리까지 오르자 변동이 큰 AI 성장주가 더 눌렸어요.",
  "summary":"6/5 개장 NVDA $213.43(-2.39%), MU $960.24(-3.6%, 프리마켓), AVGO 약 $410(-2%대) 등 보유 반도체 동반 약세. 인텔 -5.7% 등 업종 전반 2일째 하락. 브로드컴 실적 실망 + 고용 강세발 금리 상승이 겹친 영향.",
  "ourImpact":"반도체 비중이 큰 우리 포트폴리오엔 단기 부담이에요. 다만 이들 대부분은 올해 큰 폭으로 오른 종목이라 변동이 큰 편이니, 하루하루 등락보다 흐름을 가볍게 지켜보면 좋아요. (NVDA·AVGO·MU는 실시간 확인, 나머지는 개장가 추정치예요.)",
  "impact":"negative",
  "sources":[{"name":"Yahoo Finance NVDA 실시간","url":"https://finance.yahoo.com/quote/NVDA/"},
             {"name":"Investing.com (AVGO/MU)","url":"https://www.investing.com/news/stock-market-news/why-is-micron-technology-stock-down-today-93CH-4728413"}]},
 {"category":"글로벌·지정학",
  "headline":"유가 하락 — 미·이란 협상 진전 기대, WTI $92.6",
  "oneLineSummary":"국제 유가가 소폭 내렸어요. 미국과 이란의 협상이 '마지막 단계'라는 트럼프 대통령 발언에 긴장이 다소 풀리면서, 미국 대표 원유(WTI)가 배럴당 92.6달러로 내렸어요. 유가가 진정되면 물가 부담도 조금 줄어요.",
  "summary":"6/5 WTI $92.63(-0.44%), 브렌트 $94.71(-0.34%). 미·이란 협상 진전 기대가 이스라엘-레바논 휴전 불확실성과 상쇄. 유가는 이번 주 누적 +6%대였으나 금요일 하락 전환. 유가 안정은 헤드라인 물가(전체 물가) 압력을 일부 완화.",
  "ourImpact":"유가가 진정되면 물가 부담이 줄어 금리 인상 압력도 다소 완화돼, 보유 AI 성장주엔 우호적 방향이에요. 반대로 보유 전력주 탈렌(TLN)은 에너지 강세가 식어도 전력 수요 테마로 별개 흐름을 보이는 편이에요.",
  "impact":"positive",
  "sources":[{"name":"TheStreet (6/5 유가)","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-05-2026"}]},
]
rep["news"] = open_news + rep.get("news", [])

# update report title to reflect open
rep["title"] = ("6/5(금) 22:30 美 개장 — 5월 고용 +17.2만 예상 2배 깜짝, 금리 '인하'→'인상' 베팅 반전. "
                "S&P -0.7%·나스닥 -1.3% 하락, 반도체 2일째 약세(NVDA -2.4%·MU -3.6%), 러셀 +1.5% 나홀로 강세")
rep["session"] = "fri-usopen"
rep["generatedAt"] = TS

json.dump(rep, open(p("reports/2026-06-05.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("report updated. news items:", len(rep["news"]), "| snapshot:", len(rep["stockSnapshot"]))
