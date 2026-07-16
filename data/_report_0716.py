# -*- coding: utf-8 -*-
import json
d=json.load(open('portfolio.json'))
DATE="2026-07-16"
def S(name,url): return {"name":name,"url":url}
news=[
 {"category":"미국 증시","impact":"positive",
  "headline":"뉴욕증시 3대 지수 상승 마감…물가 둔화에 대형기술주 랠리",
  "oneLineSummary":"어젯밤(7/15) 미국 증시는 다우·S&P500·나스닥이 모두 올랐어요. 6월 물가(CPI)가 예상보다 크게 식자 구글(+3.6%)·메타(+3.1%)·아마존(+3.0%) 같은 대형 기술주로 돈이 몰렸어요. 공포지수(VIX, 시장 불안 정도)는 15.67로 −5% 내려 시장은 차분했어요.",
  "summary":"7월 15일(현지) 뉴욕증시는 다우 52,658.64(+0.29%)·S&P500 7,572.40(+0.38%)·나스닥 26,269.23(+0.62%)로 마감했습니다. 6월 CPI 둔화로 금리 인상 경계가 완화되며 대형 기술주가 상승을 이끌었고, VIX는 15.67로 하락했습니다.",
  "ourImpact":"보유 대형기술주 GOOG·META·AMZN이 나란히 +3%대로 강했어요. 지수는 올랐지만 보유 반도체·메모리 종목은 반대로 크게 밀려 종목별 온도차가 컸어요.",
  "sources":[S("CNBC (7/15 마감)","https://www.cnbc.com/2026/07/14/stock-market-today-live-updates.html")]},

 {"category":"미국 증시","impact":"negative",
  "headline":"메모리·AI 하드웨어 급락…MU −8%·SNDK −8%·WDC −9%",
  "oneLineSummary":"그동안 폭등했던 메모리·AI 하드웨어 종목이 어젯밤 크게 밀렸어요. 마이크론(MU) −8%, 샌디스크(SNDK) −8%, 웨스턴디지털(WDC) −9%가 대표적이에요. 특별한 악재보다는 '오른 김에 팔자(차익 실현)'와 SK하이닉스의 약한 전망, 중국 경쟁 우려가 겹친 결과예요.",
  "summary":"메모리 반도체가 일제히 급락했습니다. 마이크론은 연초 대비 +244%, 샌디스크는 +640% 폭등한 뒤라 차익 실현 매물이 집중됐고, SK하이닉스의 약한 실적 전망과 중국 업체 경쟁 우려가 하락을 키웠습니다. 확인된 개별 악재는 없었습니다.",
  "ourImpact":"보유 종목 DELL(−9.8%)·SNDK(−8.1%)·MU(−8.0%)·LITE(−7.7%)·MRVL(−7.3%)가 크게 밀렸어요. 다만 엔비디아(+0.3%)·TLN(+0.8%)은 버텨 낙폭을 일부 방어했어요.",
  "sources":[S("24/7 Wall St. (7/15 Micron China fears)","https://247wallst.com/investing/2026/07/15/micron-drops-8-on-china-competition-fears-dragging-intel-amd-and-marvell/"),
             S("Yahoo Finance (memory selloff)","https://finance.yahoo.com/markets/stocks/articles/micron-shares-slide-semiconductor-selloff-122643510.html")]},

 {"category":"아시아 증시","impact":"negative",
  "headline":"코스피 금리 인상發 7%대 급락…매도 사이드카 발동",
  "oneLineSummary":"오늘 아침 한국은행이 3년 반 만에 기준금리를 올리자(2.50%→2.75%) 코스피가 장중 7% 넘게 급락하고 매도 사이드카(급락 시 프로그램 매도를 잠깐 멈추는 장치)가 발동됐어요. 어젯밤 미국 반도체 약세까지 겹쳐 삼성전자(−8%대)·SK하이닉스(−10%대)가 급락을 이끌었어요.",
  "summary":"7월 16일 코스피는 한국은행의 기준금리 0.25%p 인상과 미국 반도체 약세가 겹치며 장중 7% 넘게 급락, 오전 9시 10분 매도 사이드카가 발동됐습니다. 외국인·기관이 각각 1조 원 넘게 순매도했고 반도체 대형주 낙폭이 두드러졌습니다.",
  "ourImpact":"보유 종목은 미국주라 직접 영향은 없지만, 한국 반도체 급락은 오늘 밤 미국 반도체 투자심리에 부담이 될 수 있어요. 특히 SK하이닉스와 같은 메모리 흐름인 MU·SNDK·WDC를 지켜보면 좋아요.",
  "sources":[S("문화일보 (7/16 기준금리 0.25%p 인상)","https://n.news.naver.com/mnews/article/021/0002805153"),
             S("파이낸셜뉴스 (7/16 매도 사이드카)","https://n.news.naver.com/mnews/article/014/0005549031")]},

 {"category":"개별 종목","impact":"negative",
  "headline":"DELL −9.8%…보유 종목 중 최대 낙폭",
  "oneLineSummary":"보유 종목 델(DELL)이 어젯밤 −9.8%로 가장 크게 밀렸어요. AI 서버와 메모리에 많이 노출된 회사라, 이날 메모리 급락의 직격탄을 맞았어요. 최근 많이 오른 데 따른 차익 실현도 겹쳤어요.",
  "summary":"델은 AI 서버·스토리지 사업에서 메모리 가격에 민감한 구조라 메모리 급락일에 낙폭이 컸습니다. 전날까지의 강세에 따른 차익 실현 매물도 더해졌습니다. 컨센서스 목표가는 $482.08(등급 3.93)입니다.",
  "ourImpact":"델은 보유 종목 중 오늘 낙폭이 가장 컸어요. 다만 연초 대비로는 여전히 +258% 수준이라 큰 그림은 유지되고 있어요. 실적 발표 전까지 변동을 가볍게 지켜보면 좋아요.",
  "sources":[S("Benzinga (7/15 memory-chip rout)","https://www.benzinga.com/markets/market-summary/26/07/60478486/memory-chip-selloff-wednesday-nasdaq-100-sandisk-plunges-wednesday-market-news")]},

 {"category":"개별 종목","impact":"positive",
  "headline":"엔비디아 +0.3%…반도체 약세 속 선방",
  "oneLineSummary":"보유 종목 엔비디아(NVDA)가 메모리·반도체가 대부분 급락한 날에도 +0.3%로 잘 버텼어요. AI 대장주라 매도세가 상대적으로 덜했고, 물가 둔화로 대형주 선호가 살아난 것도 도움이 됐어요.",
  "summary":"엔비디아는 메모리 급락과 별개로 AI 가속기 수요 기대가 유지되며 강보합 마감했습니다. 컨센서스 목표가 $296.80(등급 4.27)로 상승 여력이 크다는 평가가 이어지고 있습니다.",
  "ourImpact":"엔비디아의 선방이 보유 반도체 종목의 낙폭을 일부 방어했어요. AI 대장주가 흔들리지 않는 한 반도체 조정은 순환매(돈이 종목을 옮겨 다니는 흐름) 성격일 수 있어요.",
  "sources":[S("네이버 금융 NVDA","https://m.stock.naver.com/worldstock/stock/NVDA.O/total")]},

 {"category":"정책·금리","impact":"positive",
  "headline":"美 6월 CPI 3.5%로 예상 하회…물가 둔화 뚜렷",
  "oneLineSummary":"미국 6월 소비자물가(CPI, 물가 상승률)가 전년 대비 +3.5%로 시장 예상(3.8%)을 밑돌았어요. 식품·에너지를 뺀 근원물가도 2.6%로 예상(2.9%)보다 낮았어요. 물가가 식으면 금리를 더 올릴 이유가 줄어 증시엔 호재예요.",
  "summary":"6월 CPI는 전년 대비 +3.5%, 전월 대비 −0.4%로 모두 예상을 밑돌았습니다. 근원 CPI는 2.6%로 둔화했고, 미 10년물 국채금리는 4.58%로 하락했습니다. 에너지 가격 하락이 물가를 끌어내렸습니다.",
  "ourImpact":"물가 둔화는 보유 대형기술주(GOOG·META·AMZN) 랠리의 직접 배경이 됐어요. 금리 부담이 줄면 성장주 전반에 우호적이라 보유 종목 대부분에 긍정적이에요.",
  "sources":[S("CNBC (6월 CPI)","https://www.cnbc.com/2026/07/14/consumer-price-index-inflation-report-june-2026.html"),
             S("CNBC (국채금리 하락)","https://www.cnbc.com/2026/07/14/treasury-yields-rise-as-fed-rate-hike-expectations-grow.html")]},

 {"category":"정책·금리","impact":"negative",
  "headline":"한국은행 3년 반 만에 금리 인상…2.50%→2.75%",
  "oneLineSummary":"한국은행 금융통화위원회가 오늘 기준금리를 연 2.50%에서 2.75%로 0.25%p 올렸어요. 2023년 1월 이후 3년 반 만의 인상으로, 긴축(돈을 조이는) 통화 정책으로 방향을 튼 거예요. 이 소식에 코스피가 급락했어요.",
  "summary":"한국은행은 7월 16일 기준금리를 0.25%p 인상해 연 2.75%로 결정했습니다. 3년 6개월 만의 인상으로 긴축 전환 신호로 해석됐고, 가계대출·주식시장이 동시에 고금리 충격에 노출되며 증시가 급락했습니다.",
  "ourImpact":"한국 금리 인상은 보유 미국주에 직접 영향은 작지만, 아시아 투자심리 위축이 오늘 밤 미국장 개장 분위기에 부담이 될 수 있어요. 환율·글로벌 위험선호를 함께 지켜보면 좋아요.",
  "sources":[S("문화일보 (7/16 기준금리 인상)","https://n.news.naver.com/mnews/article/021/0002805153")]},

 {"category":"글로벌·지정학","impact":"negative",
  "headline":"이란-미국 긴장 재점화…국제유가 $80 돌파",
  "oneLineSummary":"이란과 미국의 군사적 긴장이 다시 불거지면서 국제유가(WTI, 미국 대표 원유 가격)가 배럴당 $80을 넘어섰어요. 6월엔 잠시 진정돼 유가가 내렸는데, 휴전이 흔들리며 다시 올랐어요. 유가가 오르면 물가 둔화 흐름에 걸림돌이 될 수 있어요.",
  "summary":"이란과 미국의 적대 재점화로 WTI 유가가 $80을 돌파했습니다. 6월 에너지 지수는 −5.7%로 큰 폭 하락했으나 지정학 리스크로 다시 반등했습니다. 유가 상승은 하반기 물가 경로의 변수로 지목됩니다.",
  "ourImpact":"유가 상승은 전력 수요주 TLN에는 상대적 우호적일 수 있지만, 물가 둔화 흐름을 흔들면 금리 기대에 부담이 돼요. 보유 종목 전반의 배경 변수로 가볍게 지켜보면 좋아요.",
  "sources":[S("CNBC (에너지·유가)","https://www.cnbc.com/2026/07/14/consumer-price-index-inflation-report-june-2026.html")]},
]

report={
 "date":DATE,
 "session":"풀 모닝 브리핑 (한국시간 08:00)",
 "title":"7월 16일 (목) 풀 모닝 — 물가 둔화 대형주 랠리 vs 메모리 급락, 한은 금리 인상 쇼크",
 "marketStatus":d["marketStatus"],
 "generatedAt":"2026-07-16T08:20:00+09:00",
 "lastUpdated":"2026-07-16T08:20:00+09:00",
 "marketSummary":("어젯밤(7/15) 미국은 6월 물가 둔화에 대형 기술주가 랠리했지만(구글·메타·아마존 +3%대), 그동안 폭등했던 메모리·AI 하드웨어는 차익 실현에 급락했어요(MU·SNDK −8%, DELL −9.8%). "
  "3대 지수는 소폭 상승, VIX는 15.67로 하락. 오늘 아침 한국은 한국은행이 3년 반 만에 금리를 올려(2.75%) 코스피가 7% 넘게 급락하고 매도 사이드카가 발동됐어요."),
 "dataQualityNote":d["signals"]["dataQualityNote"],
 "news":news,
 "afterHoursNote":"오늘 밤 22:30(한국시간) 미국 정규장이 다시 열려요. 메모리 차익 실현이 이어질지, 한은 금리 인상 충격이 미국·아시아 심리에 번질지가 관전 포인트예요.",
 "weekAhead":[
  {"date":"2026-07-16","event":"넷플릭스(NFLX) 2분기 실적 발표 예정"},
  {"date":"2026-07-17","event":"미국 6월 소매판매·주간 실업수당청구"},
  {"date":"2026-07-27","event":"보유 종목 CLS(셀레스티카) 실적 발표 예정"},
 ],
 "scheduleNote":"이번 주 대형 기술·반도체 실적 시즌이 본격화돼요. 보유 종목은 CLS(7/27)가 가장 임박해요.",
 "holidayNote":d["holidayNote"],
 "signals":d["signals"],
 "indices":{
  "dow":{"value":"52,658.64","change":"+0.29%"},
  "sp500":{"value":"7,572.40","change":"+0.38%"},
  "nasdaq":{"value":"26,269.23","change":"+0.62%"},
  "vix":{"value":"15.67","change":"-5.03%"},
  "us10y":{"value":"4.58%"},
  "wti":{"value":"$80+","note":"이란-미국 긴장 재점화"},
 },
}
json.dump(report,open(f'reports/{DATE}.json','w'),ensure_ascii=False,indent=1)
print("REPORT WRITTEN:", f'reports/{DATE}.json', '| news:', len(news))

# ---- index.json ----
idx=json.load(open('reports/index.json'))
idx["reports"]=[r for r in idx["reports"] if r.get("date")!=DATE]
idx["reports"].append({"date":DATE,"title":"7월 16일 (목) 풀 모닝","summary":"물가 둔화 대형주 랠리·메모리 급락, 한은 금리 인상에 코스피 7%↓ 사이드카"})
idx["reports"].sort(key=lambda x:x["date"])
idx["lastUpdated"]="2026-07-16T08:20:00+09:00"
json.dump(idx,open('reports/index.json','w'),ensure_ascii=False,indent=1)
print("INDEX UPDATED, total reports:", len(idx["reports"]))
