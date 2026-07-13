#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

PF = json.load(open("portfolio.json", encoding="utf-8"))
sig = PF["signals"]

NOW = "2026-07-13T08:00:00+09:00"

def src(name,url): return {"name":name,"url":url}

news = [
 # 1. 미국 증시
 {"category":"미국 증시","impact":"positive",
  "headline":"미 3대 지수 모두 상승 — 변동성 컸던 한 주 플러스로 마감",
  "oneLineSummary":"금요일(7/10) 다우·S&P500·나스닥 3대 지수가 모두 올라 흔들렸던 한 주를 플러스로 끝냈어요. 반도체가 주중 크게 출렁였지만 마지막 날 AI·메모리주가 반등하며 지수를 끌어올렸어요. 다음 주 물가 지표와 은행 실적을 앞두고 관망 속 소폭 상승이었어요.",
  "summary":"7/10 다우 52,637.01(+0.29%), S&P500 7,575.39(+0.42%), 나스닥 26,281.61(+0.29%)로 3대 지수가 모두 상승 마감했습니다. 주중 삼성전자 실적 실망·중국 딥시크 자체 칩 보도로 반도체가 급락했으나, 후반 메모리·AI주 반등으로 주간 상승 전환했습니다.",
  "ourImpact":"보유 종목 대부분이 반등에 동참했어요. META(+6.0%)·NVDA(+4.0%)·SNDK(+3.1%)가 강했고, 일부 종목은 차익 실현에 밀렸지만 전반 흐름은 우호적이에요.",
  "sources":[src("CNBC","https://www.cnbc.com/2026/07/09/stock-market-today-live-updates.html"),src("Yahoo Finance","https://finance.yahoo.com/news/live/stock-market-today-friday-july-10-dow-sp-nasdaq-113921604.html")]},
 {"category":"미국 증시","impact":"positive",
  "headline":"공포지수(VIX) 15로 하락 — 시장 심리 안정",
  "oneLineSummary":"시장의 불안 정도를 보여주는 공포지수(VIX·낮을수록 안정)가 15.03으로 5% 넘게 내렸어요. 한 주 내내 반도체가 크게 출렁였지만 금요일 반등으로 투자 심리가 다시 차분해졌어요. 다음 주 물가 발표 전까지는 안정된 분위기예요.",
  "summary":"7/10 VIX가 15.03으로 -5.11% 하락했습니다. 주중 반도체 급락으로 잠시 튀었던 변동성이 금요일 AI·메모리주 반등과 함께 진정됐습니다. 15선은 역사적으로 낮은(안정적인) 수준입니다.",
  "ourImpact":"변동이 큰 반도체 보유 종목(MRVL·CRDO·SNDK 등)에는 우호적 환경이에요. 다만 7/14 물가 발표 결과에 따라 다시 흔들릴 수 있어 흐름을 가볍게 지켜보면 좋아요.",
  "sources":[src("CNN Markets","https://www.cnn.com/markets")]},
 # 2. 아시아 증시
 {"category":"아시아 증시","impact":"positive",
  "headline":"코스피 +2.5%·니케이 +1.2%·항셍 +0.6% 동반 상승",
  "oneLineSummary":"금요일 아시아 주요 지수가 모두 올랐어요. 코스피가 +2.5%로 가장 크게 뛰었는데, SK하이닉스의 미국 상장 기대가 반도체주 전반을 밀어올렸어요. 일본 니케이와 홍콩 항셍도 위험 자산 선호가 살아나며 동반 상승했어요.",
  "summary":"7/10 코스피 7,475.94(+2.5%), 니케이225 68,558(+1.2%), 항셍 24,175.12(+0.60%)로 아시아 3대 지수가 동반 상승했습니다. SK하이닉스 나스닥 상장 기대가 한국 반도체주를 견인했습니다.",
  "ourImpact":"한국 반도체 강세는 미국 상장 메모리주(MU·SNDK)와 대만 TSM에도 우호적 신호예요. 글로벌 메모리 사이클이 함께 움직이는 흐름이에요.",
  "sources":[src("CNBC Asia","https://www.cnbc.com/2026/07/03/stock-market-today-live-updates.html")]},
 # 3. 개별 종목
 {"category":"개별 종목","impact":"positive",
  "headline":"SK하이닉스 나스닥 데뷔 +14% — 외국기업 사상 최대 IPO",
  "oneLineSummary":"SK하이닉스가 미국 나스닥에 상장하며 첫날 약 +14% 급등했어요($168.01, 공모가 $149). 외국 기업이 미국에서 판 규모로는 사상 최대인 265억 달러를 조달했는데, 2014년 알리바바 기록을 넘어섰어요. AI 서버에 필수인 고대역폭메모리(HBM) 세계 1위라는 점이 부각됐어요.",
  "summary":"7/10 SK하이닉스가 ADR(미국주식예탁증서) 형태로 나스닥에 상장, 공모가 $149에서 종가 $168.01(+13%)로 마감했습니다. 조달액 265억$는 외국 기업 미국 상장 사상 최대이며, 금요일 잠정 티커 SKHYV, 월요일부터 SKHY로 거래됩니다. HBM 시장 약 57% 점유가 강점입니다.",
  "ourImpact":"메모리 열기가 다시 살아나 보유 종목 MU·SNDK, 시그널 종목 WDC에 우호적이에요. 다만 메모리 투자 선택지가 늘어난 만큼 자금이 분산될 수 있어 개별 흐름은 갈릴 수 있어요.",
  "sources":[src("CNBC","https://www.cnbc.com/2026/07/10/sk-hynix-skhy-stock-nasdaq.html"),src("Bloomberg","https://www.bloomberg.com/news/articles/2026-07-10/sk-hynix-indicated-to-climb-17-after-26-5-billion-adr-offering")]},
 {"category":"개별 종목","impact":"positive",
  "headline":"메타 자체 AI 칩 '아이리스' 9월 생산 — 보유 META +6%",
  "oneLineSummary":"메타(META)가 자체 개발한 첫 AI 칩 '아이리스'를 9월부터 생산한다는 소식에 주가가 +6% 급등했어요. 브로드컴과 함께 설계하고 대만 TSMC가 만드는데, 엔비디아·AMD 의존도를 낮추려는 시도예요. 다만 기존 칩도 계속 사면서 '보완'하는 방식이라 엔비디아(+4%)도 함께 올랐어요.",
  "summary":"메타가 자체 AI 칩 'Iris'(MTIA 4세대)를 9월 양산 개시한다고 밝혔습니다. 브로드컴 협력·TSMC 생산 구조로, 6주 만에 테스트를 통과했습니다. 엔비디아·AMD를 '대체'가 아닌 '보완'하는 전략으로 해석되며 NVDA는 오히려 +4% 반등했습니다.",
  "ourImpact":"보유 META(+6.0%)·NVDA(+4.0%)·AVGO·TSM 모두 수혜·연관 종목이에요. 칩 자체 설계 흐름은 브로드컴(AVGO)·TSMC(TSM)에 장기 호재로 작용해요.",
  "sources":[src("Yahoo Finance","https://finance.yahoo.com/technology/ai/articles/mark-zuckerberg-turning-meta-bigger-030100431.html"),src("Blockonomi","https://blockonomi.com/nvidia-nvda-stock-slides-as-meta-prepares-in-house-ai-chip-launch-this-fall/")]},
 # 4. 정책·금리
 {"category":"정책·금리","impact":"neutral",
  "headline":"7/14 6월 소비자물가(CPI) + 대형은행 실적 동시 발표",
  "oneLineSummary":"이번 주 최대 분수령은 화요일(7/14)이에요. 밤 21:30 6월 소비자물가(CPI·물가 상승률)가 나오는데, 전체 물가는 진정되겠지만 근원물가(식품·에너지 뺀 물가)는 2.9%로 예상돼요. 같은 날 JP모건·골드만삭스 등 대형 은행 5곳이 2분기 실적을 발표하며 어닝 시즌이 시작돼요.",
  "summary":"6월 CPI가 7/14(화) 미 동부시간 08:30(한국 21:30) 발표됩니다. 헤드라인 CPI는 휘발유 하락으로 둔화 기대, 근원 CPI는 2.9% 전망입니다. 같은 날 JPMorgan·Goldman Sachs·BofA·Citi·Wells Fargo가 Q2 실적을 발표하며 어닝 시즌이 개막합니다.",
  "ourImpact":"물가가 예상보다 높게 나오면 금리 인하 기대가 후퇴해 밸류에이션 높은 성장주(보유 반도체·AI주)가 흔들릴 수 있어요. 결과 확인 전까지 변동에 대비하면 좋아요.",
  "sources":[src("Finance Calendar","https://www.financecalendar.com/event/us-cpi-report-july-2026/"),src("Benzinga","https://www.benzinga.com/markets/equities/26/07/60405656/bank-earnings-week")]},
 {"category":"정책·금리","impact":"positive",
  "headline":"애플-브로드컴 300억 달러 미국산 칩 계약",
  "oneLineSummary":"애플이 브로드컴(AVGO)과 300억 달러가 넘는 다년 계약을 맺고 미국에서 만든 맞춤형 무선 칩 150억 개 이상을 공급받기로 했어요. 애플의 역대 최대 미국 제조 약속인데, 브로드컴 콜로라도 공장도 15억 달러 들여 확장해요. 지난주 발표 당시 브로드컴이 크게 올랐어요.",
  "summary":"애플이 브로드컴(AVGO)과 $30B+ 다년 계약을 체결, 미국산 맞춤형 무선 연결 칩 150억 개 이상을 공급받기로 했습니다. 콜로라도 공장 $1.5B 확장 포함, 애플의 최대 미국 제조 투자입니다.",
  "ourImpact":"보유 AVGO(브로드컴)의 장기 매출 가시성을 높이는 호재예요. 대만 TSM에도 파운드리 물량 측면에서 우호적이에요.",
  "sources":[src("Reuters","https://stockanalysis.com/stocks/avgo/"),src("CNBC","https://stockanalysis.com/stocks/avgo/")]},
 # 5. 글로벌·지정학
 {"category":"글로벌·지정학","impact":"neutral",
  "headline":"WTI 유가 $71대 — 중동 긴장에 주간 +3.5%",
  "oneLineSummary":"미국 대표 원유(WTI) 가격이 금요일 $71.2 부근으로 소폭 내렸지만, 한 주로는 약 +3.5% 올랐어요. 미국과 이란의 긴장이 다시 불거지며 공급 우려가 커졌기 때문이에요. 유가가 오르면 물가를 자극해 금리 인하를 늦출 수 있어 시장이 예민하게 보고 있어요.",
  "summary":"7/10 WTI 유가가 약 $71.2/배럴로 마감(주간 +3.5%)했습니다. 미·이란 긴장 재점화로 공급 우려가 커졌고, 미 10년물 국채금리도 4.5%대로 상승했습니다. 유가 상승은 인플레이션 재자극 요인으로 주시되고 있습니다.",
  "ourImpact":"유가·금리 상승은 성장주 전반에 부담이지만, 보유 종목 중 전력회사 TLN(탈렌에너지)에는 에너지 가격 강세가 우호적으로 작용할 수 있어요.",
  "sources":[src("Fortune","https://fortune.com/article/price-of-oil-07-10-2026/"),src("CNBC US10Y","https://www.cnbc.com/quotes/US10Y")]},
]

marketSummary = {
 "dow":{"close":52637.01,"change":0.29,"note":"52,637(+0.29%). 한 주를 플러스로 마감했어요.","approx":False},
 "sp500":{"close":7575.39,"change":0.42,"note":"7,575(+0.42%). AI·메모리주 반등이 지수를 끌어올렸어요.","approx":False},
 "nasdaq":{"close":26281.61,"change":0.29,"note":"26,282(+0.29%). 기술주 반등으로 상승 마감했어요.","approx":False},
 "vix":{"close":15.03,"change":-5.11,"note":"공포지수(낮을수록 안정) 15.03으로 5% 넘게 내려 시장이 차분해졌어요.","approx":False},
 "wti":{"close":71.2,"change":None,"note":"미국 대표 원유(WTI) $71.2 부근. 주간으로는 +3.5% 올랐어요.","approx":True},
 "us10y":{"close":4.55,"change":None,"note":"미 10년물 국채금리 4.5%대. 중동 긴장·유가 상승에 올랐어요.","approx":True},
 "fearGreed":{"value":49,"label":"중립(Neutral)","note":"공포·탐욕 지수 49로 중립 구간이에요."},
 "kospi":{"close":7475.94,"change":2.5,"note":"코스피 +2.5%. SK하이닉스 상장 기대로 반도체가 강했어요.","approx":False},
 "nikkei":{"close":68558.0,"change":1.2,"note":"니케이 +1.2%.","approx":False},
 "hangseng":{"close":24175.12,"change":0.60,"note":"항셍 +0.6%.","approx":False},
}

weekAhead = [
 {"date":"2026-07-14","event":"6월 소비자물가(CPI) 발표 (韓 21:30) + 대형은행 실적(JPM·GS·BofA·씨티·웰스파고)","impact":"이번 주 최대 분수령 — 물가·금리 방향 + 어닝 시즌 개막"},
 {"date":"2026-07-15","event":"6월 생산자물가(PPI) 발표 예정","impact":"기업이 파는 물건값 흐름 — 물가 추세 확인"},
 {"date":"2026-07-16","event":"6월 소매판매 + 넷플릭스 등 실적(예정)","impact":"소비 경기 체크 + 빅테크 실적 시즌 본격화"},
 {"date":"2026-07-23","event":"인텔(INTC) 2분기 실적 (시그널 종목)","impact":"파운드리 적자 개선 여부가 관건"},
 {"date":"2026-07-27","event":"셀레스티카(CLS) 2분기 실적 (보유)","impact":"데이터센터 서버 수요 확인 — 보유 종목 이벤트"},
 {"date":"2026-07-29","event":"웨스턴디지털(WDC)·알파벳(GOOG) 실적(예정)","impact":"저장장치·클라우드 수요 확인 — 보유·시그널 이벤트"},
]

report = {
 "date":"2026-07-13",
 "session":"full-morning",
 "title":"7월 13일 (월) 08:00 풀 모닝 — 미 3대 지수 상승 마감(다우 +0.29·S&P +0.42·나스닥 +0.29%), SK하이닉스 나스닥 데뷔 +14%(외국기업 사상 최대 IPO) / 보유 META +6.0%·NVDA +4.0%·SNDK +3.1% 강세, DELL −3.4%·MRVL −3.0% 약세",
 "marketStatus":PF["marketStatus"],
 "generatedAt":NOW,
 "lastUpdated":NOW,
 "marketSummary":marketSummary,
 "dataQualityNote":sig["dataQualityNote"],
 "news":news,
 "afterHoursNote":"미국 증시는 7/13(월) 밤 22:30(한국시간) 정규장이 다시 열려요. 7/14(화) 밤 CPI·은행 실적을 앞두고 관망세가 예상돼요.",
 "weekAhead":weekAhead,
 "scheduleNote":"이번 주는 화요일(7/14) 6월 CPI와 대형 은행 실적이 같은 날 나오며 어닝 시즌이 시작돼요. 보유 종목은 7/27 CLS, 7/29 WDC·GOOG 실적이 대기 중이에요.",
 "holidayNote":None,
 "signals":sig,
}

json.dump(report, open("reports/2026-07-13.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("report written. news count:", len(news))

# update index.json
idx = json.load(open("reports/index.json", encoding="utf-8"))
entry = {"date":"2026-07-13","title":"7월 13일 (월) 풀 모닝 브리핑","summary":"미 3대 지수 상승 마감·SK하이닉스 나스닥 +14% 데뷔 / META +6%·NVDA +4% / 7/14 CPI·은행 실적 대기"}
reports = idx.get("reports", [])
reports = [r for r in reports if r.get("date")!="2026-07-13"]
reports.append(entry)
reports.sort(key=lambda r: r.get("date",""))
idx["reports"] = reports
idx["lastUpdated"] = NOW
json.dump(idx, open("reports/index.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("index updated. total reports:", len(reports))
