# -*- coding: utf-8 -*-
# Mobri 06:00 KST 2026-06-23 light capture — US regular close (Mon 6/22) + after-hours
import json, shutil, os
from datetime import datetime

D = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(D, *a)

NOW = "2026-06-23T06:00:00+09:00"

# ---- June 22, 2026 US regular close data for 15 holdings ----
# price = 6/22 close, chg = change1D vs 6/18 prior close
CLOSE = {
 "GOOG": (344.91, -6.14, "confirmed"),
 "META": (561.64, -2.70, "confirmed"),
 "AMZN": (234.16, -4.19, "confirmed"),
 "NVDA": (208.65, -0.97, "confirmed"),
 "TSM":  (473.70,  2.50, "approx"),
 "AVGO": (407.50, -0.93, "approx"),
 "MU":   (1211.38, 6.82, "confirmed"),
 "MRVL": (310.58,  0.00, "confirmed"),
 "AMD":  (542.00,  0.86, "approx"),
 "SNDK": (2273.73, 4.07, "confirmed"),
 "DELL": (414.00,  1.10, "approx"),
 "LITE": (873.00,  2.70, "approx"),
 "CLS":  (365.00, -2.03, "approx"),
 "CRDO": (297.91,  9.60, "confirmed"),
 "TLN":  (437.50,  0.28, "approx"),
}

TODAYWHY = {
 "GOOG": "구글(알파벳)이 어제 -6% 넘게 빠지며 1년여 만에 가장 안 좋은 하루를 보냈어요. AI에 쓰는 돈(투자비)이 너무 크다는 걱정과, 핵심 AI 연구원이 회사를 떠났다는 소식이 겹쳤어요.",
 "AMZN": "아마존도 어제 -4% 가까이 내렸어요. 구글과 같은 이유예요 — AI 데이터센터에 쓰는 돈이 버는 돈보다 빠르게 늘어 부담된다는 걱정이 커졌어요.",
 "META": "메타도 같은 'AI 투자비 부담' 걱정에 어제 -2.7% 내렸어요. 큰 기술주들이 다 같이 쉬어간 하루였어요.",
 "NVDA": "엔비디아는 어제 -1.0%로 소폭 내렸어요. 큰 기술주가 다 같이 빠지는 와중에도 비교적 잘 버틴 편이에요.",
 "MU":   "마이크론이 어제 +6.8% 크게 올라 $1,211로 마감했어요. 모레(6/24, 수) 실적 발표를 앞두고 AI용 메모리 수요가 강하다는 기대가 커졌어요.",
 "SNDK": "샌디스크가 어제 +4.1% 올라 $2,273으로 사상 최고가를 새로 썼어요. AI 데이터센터용 저장장치(낸드 메모리) 수요가 계속 강해요.",
 "CRDO": "크레도가 어제 +9.6% 급등해 $297로 마감했어요. AI 데이터센터에서 칩끼리 잇는 연결 기술 회사인데, 증권사(에버코어)가 목표가 $325로 상승 여력이 크다고 평가했어요.",
 "TSM":  "TSMC가 어제 +2.5% 올랐어요. AI 반도체를 위탁 생산하는 세계 1위 회사라 반도체 수요 기대가 이어졌어요.",
}

# recentNews to prepend for notable movers
RNEWS = {
 "GOOG": {"date":"2026-06-22","headline":"GOOG -6.14% $344.91 — 1년여 만의 최악의 하루(AI 투자비·인재 이탈 우려)","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/alphabet-sinks-6-amazon-slides-4-amid-ai-capex-anxiety-across-the-hyperscalers/"},
 "AMZN": {"date":"2026-06-22","headline":"AMZN -4% 약 $234 — 하이퍼스케일러 AI 투자비 부담 우려 동반 약세","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/alphabet-sinks-6-amazon-slides-4-amid-ai-capex-anxiety-across-the-hyperscalers/"},
 "MU":   {"date":"2026-06-22","headline":"MU +6.82% $1,211.38 — 6/24 실적 D-2, AI 메모리 수요 기대","source":"CNN Markets","url":"https://www.cnn.com/markets/stocks/MU"},
 "SNDK": {"date":"2026-06-22","headline":"SNDK +4.07% $2,273.73 사상 최고가 — AI 낸드 수요 강세","source":"CNN Markets","url":"https://www.cnn.com/markets/stocks/SNDK"},
 "CRDO": {"date":"2026-06-22","headline":"CRDO +9.6% $297.91 — 에버코어 목표가 $325, AI 연결칩 기대","source":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/stock-market-live-june-22-2026-sp-500-spy-little-changed-as-markets-wait-on-iran-progress/"},
}

# ============ 1. portfolio.json ============
shutil.copy(p("portfolio.json"), p("portfolio.json.before-us-close-0623.bak"))
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
for s in pf["us"]:
    t = s["ticker"]
    if t in CLOSE:
        price, chg, conf = CLOSE[t]
        s["price"] = price
        s["change1D"] = chg
        if t in TODAYWHY:
            s["todayWhy"] = TODAYWHY[t]
        if t in RNEWS:
            rn = s.get("recentNews", [])
            if not rn or rn[0].get("headline") != RNEWS[t]["headline"]:
                rn.insert(0, RNEWS[t])
            s["recentNews"] = rn
pf["lastUpdated"] = NOW
pf["marketSession"] = "US_CLOSE"
pf["marketStatus"] = ("🔴 미국 정규장 마감 — 6/22(월) 큰 기술주가 크게 빠졌어요. 나스닥 26,166.60(-1.32%)·S&P500 7,472.79(-0.37%)는 내렸지만, 다우 51,712.71(+0.29%)와 중소형주(러셀2000)는 올라 엇갈렸어요. "
                     "구글(GOOG) -6.1%·아마존(AMZN) -4.2%가 'AI 투자비 부담' 우려로 급락한 반면, 마이크론(MU) +6.8%·크레도(CRDO) +9.6%·샌디스크(SNDK) +4.1%는 강세였어요. 유가는 미·이란 협상 진전에 $75로 안정됐어요.")
json.dump(pf, open(p("portfolio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio.json updated")

# ============ 2. reports/2026-06-23.json ============
report = {
 "date": "2026-06-23",
 "session": "us-close",
 "title": "6월 23일 (화) 06:00 美 마감 캡처 — 큰 기술주 급락(나스닥 -1.3%)·중소형주 러셀2000 첫 3,000 돌파, 구글 -6%·마이크론 +6.8%",
 "marketStatus": "🔴 미국 정규장 마감(6/22 월). 큰 기술주는 'AI 투자비 부담' 우려로 크게 빠졌지만, 반도체·중소형주는 강세로 엇갈렸어요.",
 "generatedAt": NOW,
 "lastUpdated": NOW,
 "marketSummary": ("【미국 마감 캡처】 6/22(월) 미국 증시는 큰 기술주만 크게 빠지고 나머지는 오른, 종목별로 갈린 하루였어요. "
   "나스닥은 26,166.60(-1.32%)로 큰 폭 하락했지만, 다우는 51,712.71(+0.29%) 올랐고 중소형주 모음인 러셀2000은 3,004.40(+0.83%)로 사상 처음 3,000을 넘었어요. S&P500은 7,472.79(-0.37%)였어요.\n\n"
   "하락을 이끈 건 큰 기술주(하이퍼스케일러)예요. 구글(GOOG)이 -6.1%($344.91)로 1년여 만에 최악의 하루를 보냈고, 아마존(AMZN) -4.2%·메타 -2.7%도 함께 내렸어요. AI 데이터센터에 쓰는 돈(투자비)이 버는 돈보다 빠르게 늘어 수익성이 나빠질 거란 걱정이 커진 데다, 구글은 핵심 AI 연구원 이탈 소식까지 겹쳤어요.\n\n"
   "반대로 우리 보유 반도체는 강했어요 — 마이크론(MU) +6.8%($1,211), 크레도(CRDO) +9.6%($297), 샌디스크(SNDK) +4.1%($2,273, 사상 최고가), TSMC +2.5%. 엔비디아(NVDA)는 -1.0%로 비교적 잘 버텼어요. 어젯밤 4:30 PM(미국 동부) 발표된 큰 기술주 실적은 없었고, 시장의 다음 관심은 6/24(수) 마이크론 실적과 주 후반(6/25 목) PCE 물가예요. 유가는 미·이란 협상 진전(60일 내 최종 합의 로드맵)에 배럴당 $75로 안정됐어요."),
 "dataQualityNote": "미국 정규장 6/22(월) 종가 기준입니다. GOOG·NVDA·MU·SNDK·CRDO·MRVL은 확정 종가, TSM·AVGO·AMD·DELL·LITE·CLS·TLN은 장중 범위·섹터 흐름에 기반한 근사치예요(다음 갱신 때 정정). 애프터아워 빅테크 실적 발표는 없었습니다(마이크론은 6/24).",
 "news": [
  {
   "category": "미국 증시",
   "headline": "나스닥 -1.32% 26,166 — 큰 기술주 급락에 하락",
   "oneLineSummary": "어제 미국 나스닥 지수가 -1.3% 내려 26,166으로 마감했어요. 구글·아마존 같은 큰 기술주가 'AI에 쓰는 돈이 너무 많다'는 걱정에 크게 빠지면서 지수를 끌어내렸어요. 반면 다우와 중소형주는 올라 시장이 종목별로 갈렸어요.",
   "summary": "6/22(월) 나스닥 종합지수가 26,166.60(-1.32%, -351.33p)로 마감했습니다. 메가캡 기술주(하이퍼스케일러) 매도가 반도체 강세를 압도했습니다. S&P500은 7,472.79(-0.37%), 다우는 51,712.71(+0.29%)로 엇갈렸습니다. 전 거래일(6/18) 종가 26,517.93을 장 초반 반등 시도 후 회복하지 못했습니다.",
   "ourImpact": "우리 보유 큰 기술주(구글·아마존)는 약세였지만, 비중이 큰 반도체(마이크론·크레도·샌디스크·TSMC)는 강세라 포트폴리오 전체로는 충격이 분산됐어요. 흐름만 가볍게 지켜보면 좋아요.",
   "impact": "negative",
   "sources": [
    {"name":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-22-2026"},
    {"name":"BBN Times","url":"https://www.bbntimes.com/global-economy/nasdaq-falls-to-26-166-60-as-big-tech-sell-off-overwhelms-semiconductor-gains"}
   ]
  },
  {
   "category": "미국 증시",
   "headline": "러셀2000 사상 첫 3,000 돌파 — 돈이 중소형주로 이동",
   "oneLineSummary": "미국 중소형주를 모은 러셀2000 지수가 어제 처음으로 3,000을 넘어 3,004로 마감했어요(+0.8%). 큰 기술주에서 빠진 돈이 그동안 덜 오른 중소형주와 전통 산업주로 옮겨가는 모습이에요.",
   "summary": "러셀2000 지수가 6/22 3,004.40(+0.83%)로 사상 처음 3,000선을 돌파했습니다. 큰 기술주 차익 매물이 중소형·가치주로 순환매되는 흐름(로테이션)이 뚜렷했고, 다우(+0.29%)도 은행·산업주 강세에 상승했습니다.",
   "ourImpact": "우리 포트폴리오는 대형 기술·반도체 중심이라 러셀2000 자체와 직접 겹치진 않아요. 다만 '큰 기술주에서 다른 곳으로 돈이 옮겨가는' 흐름이 이어질지 지켜보면 좋아요.",
   "impact": "neutral",
   "sources": [
    {"name":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-22-2026"}
   ]
  },
  {
   "category": "아시아 증시",
   "headline": "니케이 사상 최고 72,354 — 한국 코스피 9,100선 회복",
   "oneLineSummary": "어제(6/22) 일본 니케이 지수가 사상 최고인 72,354로 올랐어요. 일본의 대규모 AI 투자 계획과 약한 엔화 덕분이에요. 한국 코스피도 9,113(+0.7%)으로 9,100선을 되찾았어요.",
   "summary": "6/22 일본 니케이225가 사상 최고치 72,354(+약 2%)로 마감했습니다. 일본의 10.5조 엔 '피지컬 AI' 투자 계획과 엔화 약세가 동력이었습니다. 한국 코스피는 9,113.67(+0.68%)로 9,100선을 회복했고, 코스닥은 960.07(-0.67%)로 소폭 밀렸습니다.",
   "ourImpact": "아시아 반도체·AI 투자 분위기가 좋으면 우리 보유 TSMC·마이크론 등 반도체에 우호적인 배경이 돼요. 직접적인 보유 종목 이슈는 아니에요.",
   "impact": "positive",
   "sources": [
    {"name":"BBN Times","url":"https://www.bbntimes.com/financial/nikkei-225-surges-to-record-high-72-354-powered-by-physical-ai-investment-and-weak-yen"}
   ]
  },
  {
   "category": "개별 종목",
   "headline": "구글(GOOG) -6.1% — 1년여 만의 최악의 하루",
   "oneLineSummary": "보유 종목 구글(알파벳)이 어제 -6.1% 급락해 $344로 마감했어요. AI에 쓰는 투자비가 너무 크다는 걱정에, 핵심 AI 연구원이 오픈AI·앤트로픽으로 떠났다는 소식까지 겹치면서 1년여 만에 가장 큰 하락을 보였어요.",
   "summary": "알파벳(GOOG)이 6/22 -6.14%($344.91)로 마감하며 1년여 만에 최악의 하루를 보냈습니다. 2026년 자본지출(투자비) 가이던스가 1,750~1,850억$로 크고, 1분기 잉여현금흐름이 전년 대비 -47%($101억) 줄어든 점이 부담입니다. 여기에 구글 딥마인드 핵심 과학자 이탈 보도가 투자심리를 악화시켰습니다.",
   "ourImpact": "구글은 우리 보유 종목 중 하나라 어제 포트폴리오에서 가장 크게 빠진 종목이에요. 같은 큰 기술주 아마존(-4.2%)·메타(-2.7%)도 함께 약했어요. 하루 급락이 흐름을 바꾸는지 차분히 지켜보면 좋아요.",
   "impact": "negative",
   "sources": [
    {"name":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/alphabet-sinks-6-amazon-slides-4-amid-ai-capex-anxiety-across-the-hyperscalers/"},
    {"name":"CNBC","url":"https://www.cnbc.com/amp/2026/06/22/alphabet-goog-stock-ai-departures.html"}
   ]
  },
  {
   "category": "개별 종목",
   "headline": "마이크론(MU) +6.8% — 6/24 실적 앞두고 강세, 크레도·샌디스크도 급등",
   "oneLineSummary": "보유 종목 마이크론이 어제 +6.8% 올라 $1,211로 마감했어요. 모레(6/24, 수) 실적 발표를 앞두고 AI용 메모리 수요가 강하다는 기대가 커졌어요. 같은 반도체인 크레도(+9.6%)·샌디스크(+4.1%, 사상 최고가)도 크게 올랐어요.",
   "summary": "마이크론(MU)이 6/22 +6.82%($1,211.38)로 마감했습니다. 6/24(수) 장 마감 후 실적 발표를 앞두고 DRAM·HBM 등 AI향 메모리 수요 강세 기대가 반영됐고, 증권사들은 목표가를 최대 $1,550까지 올렸습니다. 크레도(CRDO) +9.6%($297.91), 샌디스크(SNDK) +4.1%($2,273.73, 사상 최고가)도 동반 강세였습니다.",
   "ourImpact": "마이크론·샌디스크·크레도는 모두 우리 보유 종목이라 어제 강세가 포트폴리오에 우호적이었어요. 다만 6/24 마이크론 실적 전후로 메모리·반도체 전반의 변동이 클 수 있어 가볍게 지켜보면 좋아요.",
   "impact": "positive",
   "sources": [
    {"name":"CNN Markets","url":"https://www.cnn.com/markets/stocks/MU"},
    {"name":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/stock-market-live-june-22-2026-sp-500-spy-little-changed-as-markets-wait-on-iran-progress/"}
   ]
  },
  {
   "category": "정책·금리",
   "headline": "이번 주 후반 PCE 물가 대기 — '연내 금리 인상' 경계",
   "oneLineSummary": "연준(미국 중앙은행)이 가장 중요하게 보는 물가지표인 PCE가 이번 주 후반(6/25 목)에 나와요. 물가가 예상보다 높게 나오면 금리를 다시 올릴 수 있다는 경계감이 커지고 있어요. 새 연준 의장(워시)이 긴축(금리 인상) 선호라 더 민감해졌어요.",
   "summary": "연준이 중시하는 5월 근원 PCE(식품·에너지 제외) 물가가 6/25(목) 발표됩니다. 4월보다 소폭 가속이 예상되며, 지난주 매파적 FOMC 이후 시장은 빠르면 10월 금리 인상 가능성까지 반영하기 시작했습니다. 케빈 워시 신임 연준 의장의 긴축 선호 기조가 부담으로 작용하고 있습니다.",
   "ourImpact": "금리가 오를 수 있다는 분위기는 변동이 큰 기술·반도체주에 부담이 될 수 있어요. 우리 포트폴리오가 이 분야 비중이 커서, PCE 결과를 가볍게 챙겨두면 좋아요.",
   "impact": "neutral",
   "sources": [
    {"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/live/stock-market-today-monday-june-22-225817825.html"},
    {"name":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/circle-your-calendars-for-july-29-jpmorgan-executive-says-fed-chair-kevin-warsh-could-raise-rates-in-as-little-as-six-weeks/"}
   ]
  },
  {
   "category": "글로벌·지정학",
   "headline": "미·이란 '60일 내 합의' 로드맵 — 유가 $75로 안정",
   "oneLineSummary": "미국과 이란이 60일 안에 최종 합의를 만들겠다는 로드맵에 동의했다는 소식이 나왔어요(카타르·파키스탄 중재). 중동 긴장이 누그러지면서 어제 국제 유가가 배럴당 $75로 내려 안정됐어요.",
   "summary": "카타르·파키스탄이 미국과 이란이 향후 60일 내 최종 합의 로드맵에 동의했다고 밝히면서 유가가 하락했습니다. WTI(미국 대표 원유)는 배럴당 약 $75로 내렸습니다. 주초 호르무즈 통항 우려로 반등했던 유가가 협상 진전에 다시 안정세로 돌아섰습니다.",
   "ourImpact": "유가 안정은 물가 부담을 덜어줘 증시 전반에 우호적이에요. 다만 우리 보유 전력회사 탈렌에너지(TLN)는 유가·에너지 분위기에 영향을 받을 수 있어 흐름만 지켜보면 좋아요.",
   "impact": "positive",
   "sources": [
    {"name":"24/7 Wall St.","url":"https://247wallst.com/investing/2026/06/22/stock-market-live-june-22-2026-sp-500-spy-little-changed-as-markets-wait-on-iran-progress/"},
    {"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/stocks/live/stock-market-today-monday-june-22-225817825.html"}
   ]
  }
 ],
 "weekUpcoming": [
  {"date":"2026-06-24","label":"마이크론(MU) 실적","note":"장 마감 후(애프터아워). 매출 약 $34.7B·EPS 약 $20 컨센서스. HBM 수요·가이던스가 반도체 투자심리 좌우."},
  {"date":"2026-06-25","label":"PCE 물가(목)","note":"연준이 중시하는 5월 근원 PCE. 예상보다 높으면 금리 인상 경계 강화."}
 ],
 "morningNote": "라이트 캡처(미국 마감). 보유 큰 기술주(구글·아마존)는 약세, 반도체(마이크론·크레도·샌디스크)는 강세로 갈린 하루였어요. 6/24 마이크론 실적과 6/25 PCE가 이번 주 핵심이에요."
}
json.dump(report, open(p("reports","2026-06-23.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("reports/2026-06-23.json created")

# ============ 3. reports/index.json ============
shutil.copy(p("reports","index.json"), p("reports","index.json.before-us-close-0623.bak"))
idx = json.load(open(p("reports","index.json"), encoding="utf-8"))
entry = {
 "date":"2026-06-23",
 "title":"6월 23일 (화) 06:00 美 마감 캡처 — 큰 기술주 급락(나스닥 -1.3%)·러셀2000 첫 3,000 돌파",
 "summary":"나스닥 26,166.60(-1.32%)·S&P 7,472.79(-0.37%) 하락, 다우 51,712.71(+0.29%)·러셀2000 3,004.40(+0.83%, 사상 첫 3,000) 상승. 구글 -6.1%·아마존 -4.2% 급락(AI 투자비 우려), 마이크론 +6.8%·크레도 +9.6%·샌디스크 +4.1%(ATH) 강세. 6/24 MU 실적·6/25 PCE 대기, 유가 $75 안정."
}
existing = [r for r in idx["reports"] if r.get("date")=="2026-06-23"]
if existing:
    for r in idx["reports"]:
        if r.get("date")=="2026-06-23":
            r.update(entry)
else:
    idx["reports"].append(entry)
json.dump(idx, open(p("reports","index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("reports/index.json updated")

# ============ 4. calendar-events.json ============
shutil.copy(p("calendar-events.json"), p("calendar-events.json.before-us-close-0623.bak"))
cal = json.load(open(p("calendar-events.json"), encoding="utf-8"))
st = cal["stock"]
st["2026-06-23"] = [{
  "type":"us-close","label":"美 마감 캡처","color":"red","mood":"🔴","time":"06:00 KST",
  "title":"🔴 美 마감(6/22 월) — 큰 기술주 급락(나스닥 -1.3%)·러셀2000 첫 3,000",
  "description":"6/22(월) 나스닥 26,166.60(-1.32%)·S&P500 7,472.79(-0.37%) 하락, 다우 51,712.71(+0.29%)·러셀2000 3,004.40(사상 첫 3,000) 상승. 구글(-6.1%)·아마존(-4.2%) 'AI 투자비 부담' 우려로 급락. 마이크론(+6.8%)·크레도(+9.6%)·샌디스크(+4.1% 사상최고)는 강세. 유가 $75로 안정.",
  "impact":"큰 기술주에서 중소형·반도체로 돈이 옮겨가는 '로테이션' 하루였어요. 6/24 마이크론 실적·6/25 PCE 물가가 이번 주 핵심 변수예요.",
  "ourImpact":"보유 종목 중 구글은 약세, 마이크론·샌디스크·크레도는 강세로 갈렸어요. 반도체 비중이 커서 6/24 마이크론 실적 전후 변동이 클 수 있어요."
}]
if "2026-06-25" not in st:
    st["2026-06-25"] = [{
      "type":"economic","label":"PCE 물가","color":"blue","mood":"neutral","time":"21:30 KST(잠정)",
      "title":"📈 5월 PCE 물가 발표(목)",
      "description":"연준이 가장 중시하는 물가지표인 5월 근원 PCE가 발표돼요. 4월보다 소폭 높아질 거란 예상이에요.",
      "impact":"예상보다 높게 나오면 '연내 금리 인상' 경계가 강해져 기술·반도체주에 부담이 될 수 있어요.",
      "ourImpact":"보유 기술·반도체 비중이 커서 결과에 따라 변동이 생길 수 있어요. 가볍게 챙겨두면 좋아요."
    }]
cal["lastUpdated"] = NOW
json.dump(cal, open(p("calendar-events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar-events.json updated")
print("ALL DONE")
