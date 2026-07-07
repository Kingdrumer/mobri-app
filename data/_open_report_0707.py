# -*- coding: utf-8 -*-
import json, io, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOW = "2026-07-07T22:45:00+09:00"

r = json.load(io.open("reports/2026-07-07.json", encoding="utf-8"))

# --- marketSummary -> open snapshot ---
ms = r.get("marketSummary", {})
ms["dow"] = {"close": 53137.58, "change": 0.15, "note": "개장 직후 53,138(+0.15%)로 또 사상 최고를 갈아치웠어요. 반도체를 피한 돈이 산업재·금융 같은 다른 대형주로 몰린 순환매 덕이에요.", "approx": False}
ms["sp500"] = {"close": 7521.63, "change": -0.21, "note": "약 7,522(-0.2%). 반도체 약세가 지수를 눌렀지만 비반도체 강세가 낙폭을 방어했어요.", "approx": False}
ms["nasdaq"] = {"close": 25915.31, "change": -0.79, "note": "약 25,915(-0.8%). 기술주·반도체 비중이 커서 딥시크발 반도체 투매에 가장 크게 밀렸어요.", "approx": False}
ms["sox"] = {"close": 12359.73, "change": -4.19, "note": "필라델피아 반도체지수(반도체주 묶음)가 -4.2% 급락. 딥시크 자체 칩 개발 보도가 직격탄이었어요.", "approx": False}
ms["vix"] = {"close": 15.92, "change": 2.25, "note": "공포지수(낮을수록 안정)가 15.9로 소폭 올랐지만 여전히 차분한 편이에요.", "approx": False}
ms["wti"] = {"price": 69.67, "change": 1.63, "note": "WTI(미국 대표 원유)가 69.7달러로 +1.6% 올랐어요. 중동 긴장이 다시 부각됐어요.", "approx": False}
ms["gold"] = {"price": 4180.70, "change": 0.32, "note": "금값 4,181달러(+0.3%). 안전자산 수요가 조금 붙었어요.", "approx": False}
r["marketSummary"] = ms

# --- news to prepend (US open) ---
new_news = [
 {
  "category": "미국 증시",
  "headline": "개장 다우 53,138 또 사상 최고(+0.15%)·나스닥 -0.8% — '반도체 팔고 딴 데 사는' 순환매",
  "oneLineSummary": "미국 증시가 열리자마자 반도체가 크게 흔들렸어요. 나스닥은 -0.8% 밀렸지만, 반도체를 판 돈이 다른 대형주로 옮겨가면서 다우는 53,138(+0.15%)로 또 한 번 사상 최고를 갈아치웠어요. 같은 시장 안에서 반도체만 빠지고 나머지는 버티는 '순환매' 장세예요.",
  "summary": "7/7 개장 직후 다우는 53,137.58(+0.15%)로 사상 최고를 재차 경신했고, S&P500 -0.21%(7,521.63), 나스닥 -0.79%(25,915.31)로 엇갈렸다. 필라델피아 반도체지수(SOX)는 -4.19% 급락. 딥시크 자체 칩 개발 보도로 반도체가 투매되는 가운데 산업재·커뮤니케이션 등 비반도체 대형주로 자금이 이동하는 순환매가 뚜렷했다. VIX는 15.9로 안정권.",
  "ourImpact": "보유 종목이 반도체(NVDA·MU·AMD·SNDK 등)와 비반도체(GOOG·META·AMZN)로 나뉘어 오늘은 희비가 갈렸어요. 지수 전체보다 종목별 흐름을 보는 게 좋은 날이에요.",
  "impact": "neutral",
  "sources": [{"name": "CNBC", "url": "https://www.cnbc.com/2026/07/06/stock-market-today-live-updates.html"}]
 },
 {
  "category": "개별 종목",
  "headline": "'중국 딥시크, 자체 AI 칩 개발' 로이터 보도 — 반도체 투매, SNDK·AMD·MU 급락",
  "oneLineSummary": "중국 AI 회사 딥시크가 엔비디아 칩 대신 쓸 자기네 AI 칩을 만들고 있다는 로이터 보도가 나왔어요. 'AI 칩을 사줄 손님이 줄어드는 것 아니냐'는 걱정에 개장하자마자 반도체주가 우르르 빠졌어요. 엔비디아 -1.7%, 그리고 보유 종목인 낸드·메모리·맞춤형 칩 회사들이 더 크게 밀렸어요.",
  "summary": "로이터는 7/7 중국 딥시크가 추론(inference)용 자체 AI 칩을 개발 중이라고 보도했다. 엔비디아·삼성 등에 대한 의존도를 낮추려는 시도로, AI 칩 수요 둔화 우려가 반도체 전반으로 확산됐다. 개장가 기준 SNDK -7.8%, AMD -6.7%, MU -6.1%, MRVL -5.9%, CRDO -5.5%, TSM -3.3%, AVGO -1.6%, NVDA -1.7%. 다만 경쟁력 있는 AI 칩 양산에는 수년과 대규모 투자가 필요하고 미국의 대중 수출규제가 걸림돌이라는 신중론도 나온다.",
  "ourImpact": "보유 15종목 중 반도체 비중이 커서 오늘 낙폭이 컸어요. 특히 변동이 큰 SNDK·AMD·MU·MRVL·CRDO가 민감하게 반응했어요. 딥시크 칩이 실제 양산까지 시간이 걸린다는 점도 함께 지켜보면 좋아요.",
  "impact": "negative",
  "sources": [{"name": "Investing.com", "url": "https://in.investing.com/news/stock-market-news/nvidia-stock-slips-after-report-says-deepseek-is-designing-its-own-ai-chip-5484926"}]
 },
 {
  "category": "개별 종목",
  "headline": "반도체 피한 돈은 빅테크로 — META +1.8%·GOOG +0.7%·AMZN +0.4% 강세",
  "oneLineSummary": "반도체에서 빠져나온 돈이 검색·광고·쇼핑으로 돈 버는 대형 기술주로 옮겨갔어요. 메타가 +1.8%로 보유 종목 중 가장 강했고, 구글(+0.7%)·아마존(+0.4%)도 올랐어요. 반도체가 흔들릴 때 이런 비(非)반도체 대형주가 방어 역할을 해준 하루예요.",
  "summary": "딥시크발 반도체 투매 속에서 비반도체 빅테크는 상대적 강세를 보였다. 개장가 기준 META +1.8%(610.98), GOOG +0.65%(367.28), AMZN +0.40%(245.14). 서버 수요 기대가 있는 DELL도 +0.1%로 버텼고, 전력·원자력주 TLN은 보합으로 반도체 이슈와 무관하게 안정적이었다.",
  "ourImpact": "포트폴리오가 반도체 한쪽으로만 쏠려 있지 않아, 오늘처럼 반도체가 빠지는 날 META·GOOG·AMZN·TLN이 완충 역할을 해줬어요. 분산이 힘을 발휘한 하루예요.",
  "impact": "positive",
  "sources": [{"name": "CNBC", "url": "https://www.cnbc.com/quotes/META"}]
 }
]

r["news"] = new_news + r.get("news", [])
r["lastUpdated"] = NOW
r["session"] = "US_OPEN"
r["title"] = ("7월 7일 (화) 개장 — 미국 정규장 열리자 '딥시크 자체 AI 칩' 보도로 반도체 투매(SOX -4.2%)·나스닥 -0.8%, "
  "그래도 순환매로 다우 53,138 또 사상 최고 / 보유 종목 SNDK -7.8%·AMD -6.7%·MU -6.1% 약세, META +1.8%·GOOG +0.7%는 강세")

json.dump(r, io.open("reports/2026-07-07.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("report updated. news count:", len(r["news"]))
