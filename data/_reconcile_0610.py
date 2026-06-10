# -*- coding: utf-8 -*-
"""Reconcile report/index/calendar to the (watchdog) authoritative portfolio.json.
A concurrent watchdog rewrote portfolio.json with richer multi-sourced data after my
full-morning run. Align my deliverables to it; keep 10-category news but fix per-stock
specifics; add verified 6/10 KST Korea crash (fresh today info)."""
import json
DATA = "/sessions/zen-festive-ritchie/mnt/claude/portfolio-pwa/data"
TODAY = "2026-06-10"
pf = json.load(open(f"{DATA}/portfolio.json"))
MS = pf['marketStatus']
hold = {h['ticker']: h for h in pf['us']}

S_TS = {"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-09-2026"}
S_CNBC = {"name": "CNBC", "url": "https://www.cnbc.com/2026/06/08/stock-market-today-live-updates.html"}
S_YF = {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/markets/live/stock-market-today-tuesday-june-9-dow-sp-500-nasdaq-rise-ai-225640870.html"}
S_SEOUL = {"name": "서울신문 서울데이터랩(6/10)", "url": "https://www.seoul.co.kr/news/economy/securities/2026/06/10/20260610500033"}
S_SEDAILY = {"name": "서울경제(6/10)", "url": "https://www.sedaily.com/article/20054045"}
S_REUTERS = {"name": "Reuters", "url": "https://www.reuters.com/world/us/us-small-business-sentiment-falls-may-inflation-worries-mount-2026-06-09/"}
S_INV = {"name": "Investing.com", "url": "https://www.investing.com/news/commodities-news/oil-rises-nearly-1-as-us-launches-new-strikes-against-iran-supply-tightens-4734262"}

news = [
 {"category":"미국 증시",
  "headline":"美 증시 혼조 마감 — 기술주 약세, 다우만 신고가권",
  "oneLineSummary":"미국 증시가 기술주 약세로 혼조 마감했어요. S&P500 -0.3%(7,386)·나스닥 -1.0%(25,679)는 내렸지만 다우는 +0.2%(50,872)로 비기술주 덕에 강보합이었어요. 전날 반등했던 반도체에 다시 차익실현(오른 김에 파는 것)이 들어오며 기술업종 전체가 약했어요.",
  "summary":"6/9(화) S&P500 -0.26%(7,386.65), 나스닥 -0.97%(25,678.82), 다우 +0.17%(50,872.11). 기술·에너지만 하락 업종이었고 나머지는 올라 지수 약세는 사실상 기술주 탓. 러셀2000(소형주)은 +0.25%. VIX 약 20.5로 상승.",
  "ourImpact":"보유 종목 대부분이 반도체라 차익실현 매물에 동반 약세였어요. 다만 크레도(CRDO)는 실적 호조로 +13%대 급등하며 홀로 강했어요. 오늘 밤 물가 지표 전까지 변동이 클 수 있어요.",
  "impact":"negative","sources":[S_TS,S_CNBC]},
 {"category":"미국 증시",
  "headline":"장중 트럼프 '이란 추가 타격' 시사에 나스닥 한때 -3.3% 급락",
  "oneLineSummary":"장중 트럼프 대통령이 이란 추가 타격을 시사하자 나스닥이 한때 -3.3%까지 밀렸어요. 동시에 '2~3일 안에 합의 가능' 발언도 나오며 마감 무렵 낙폭을 줄였어요. 정규장이 끝난 뒤 미군이 이란에 '자위적 타격'을 발표해 오늘 밤 변수가 됐어요.",
  "summary":"6/9 장중 트럼프 대통령의 이란 대응 발언에 나스닥 -3.3%·S&P500 -2.2%까지 급락 후 만회. 마감 후 미군이 이란에 자위적 타격을 발표했습니다. 금요일 스페이스X 대형 IPO 대비 자금 이동까지 겹쳐 위험 줄이기(de-risking) 흐름이 강했습니다.",
  "ourImpact":"지정학 헤드라인에 지수가 출렁이면 변동이 큰 보유 반도체주도 같이 흔들려요. 방향보다 변동성 자체가 커진 국면이라 단기 흐름만 가볍게 지켜보면 좋아요.",
  "impact":"negative","sources":[S_TS]},
 {"category":"아시아 증시",
  "headline":"코스피, 6/9 +8% 급반등했다가 6/10 -6%대 급락 — 매도 사이드카",
  "oneLineSummary":"한국 증시가 하루 단위로 크게 출렁였어요. 6/9 코스피는 +8.18%(8,097) 급반등하며 전날 '검은 월요일'을 하루 만에 되돌렸지만, 오늘(6/10)은 미군의 이란 공습 여파로 장중 -6%대 급락하며 매도 사이드카(급락 시 프로그램 매도를 잠시 멈추는 장치)가 발동됐어요.",
  "summary":"6/9 코스피 +8.18%(8,097) 급반등 → 6/10 장중 -6%대 급락, 매도 사이드카 발동(7,500선 후퇴). 삼성전자 -6.8%·SK하이닉스 동반 약세, 외국인 순매도 지속. 코스닥은 개인 순매수(1,076억원)로 낙폭 줄여 969선 회복.",
  "ourImpact":"한국 반도체(삼성·SK하이닉스)와 미국 보유 반도체는 같은 업황을 타서 흐름이 비슷해요. 한국장 급락은 오늘 밤 미국 반도체에도 부담 신호가 될 수 있어, CPI 결과까지 변동을 지켜보면 좋아요.",
  "impact":"negative","sources":[S_SEDAILY,S_SEOUL]},
 {"category":"아시아 증시",
  "headline":"중국 5월 수출 +19.4% 예상 상회 — 관세에도 신규시장 개척",
  "oneLineSummary":"중국의 5월 수출이 1년 전보다 +19.4%, 수입은 +27.4% 늘어 둘 다 예상을 웃돌았어요. 미국 관세 부담 속에서도 새 시장을 뚫어낸 결과예요. 다만 중국 내수는 여전히 부진해, 수출로 버티는 구조라는 평가가 나와요.",
  "summary":"6/9 발표된 중국 5월 무역지표는 수출 +19.4%·수입 +27.4%로 모두 시장 예상을 상회했습니다. 미국 관세·무역장벽에도 신규시장 개척에 성공했다는 신호지만 내수는 부진했습니다.",
  "ourImpact":"중국 교역 호조는 글로벌 IT·반도체 수요에 긍정적 신호예요. 보유 반도체주의 큰 그림(AI·메모리 수요)엔 우호적이지만, 단기 지수는 지정학·물가에 더 휘둘리고 있어요.",
  "impact":"neutral","sources":[S_YF]},
 {"category":"개별 종목",
  "headline":"보유 CRDO +13%대 급등 — 분기 실적 서프라이즈",
  "oneLineSummary":"보유 종목 크레도(CRDO)가 어제 +13%대 급등했어요. 분기 실적이 시장 예상을 크게 웃돌았고, 골드만삭스·미즈호·니덤 등 여러 증권사가 목표가를 올렸어요. AI 데이터센터에서 칩끼리 연결하는 광통신(빛으로 데이터를 보내는 기술) 수요가 강하다는 게 확인됐어요.",
  "summary":"6/9 크레도(CRDO)는 분기 실적이 컨센서스(시장 평균 예상치)를 크게 상회하며 +13%대 급등했습니다. 골드만($250)·미즈호($290)·니덤($275) 등 목표가 상향이 잇따랐습니다. 같은 광통신주 LITE는 -8.2%로 차익실현에 밀려 대조됐습니다.",
  "ourImpact":"보유 종목 중 CRDO가 단독 급등했어요. 같은 광통신 분야 LITE(루멘텀)는 오히려 -8.2%로 크게 빠져, 종목별로 희비가 갈렸어요. 변동이 큰 종목이라 흐름만 가볍게 지켜보면 좋아요.",
  "impact":"positive","sources":[S_TS,S_YF]},
 {"category":"개별 종목",
  "headline":"칩·광통신 차익실현 — MRVL -7.6%·LITE -8.2%·AMD -3.0%, MU는 골드만 목표가 2배 상향",
  "oneLineSummary":"전날 급등했던 반도체·광통신주가 하루 만에 크게 빠졌어요. 마벨(MRVL) -7.6%, 루멘텀(LITE) -8.2%, AMD -3.0%로 차익실현 매물이 쏟아졌어요. 반면 마이크론(MU)은 골드만삭스가 목표가를 $400→$900으로 두 배 넘게 올렸는데도, 전날 +10% 급등 뒤라 -1.4% 내렸어요.",
  "summary":"6/9 전날 반등했던 칩·광통신주에 차익실현이 집중돼 MRVL -7.6%(전날 +9%의 되돌림), LITE -8.2%, AMD -3.0%로 약세였습니다. 골드만삭스는 마이크론(MU) 목표가를 $400→$900으로 상향했으나 MU는 전날 급등 부담에 -1.4% 마감했습니다. 샌디스크(SNDK)는 장 초반 +6.9%까지 올랐다 +0.3%로 상승분을 반납했습니다.",
  "ourImpact":"보유 반도체가 차익실현 매물에 동반 약세였어요. 특히 MRVL·LITE는 변동이 큰 종목이라 지수보다 더 출렁였어요. MU·SNDK는 증권사 목표가 상향이 계속돼 업황 기대 자체는 살아있어요.",
  "impact":"negative","sources":[S_TS,S_YF]},
 {"category":"정책·금리",
  "headline":"오늘 밤 21:30 5월 CPI 발표 — 예상 +4.2%로 2023년 4월 이후 최대",
  "oneLineSummary":"오늘 밤 한국시간 21:30에 미국 5월 소비자물가(CPI)가 나와요. 시장은 1년 전보다 +4.2% 올랐을 거라 보는데, 맞으면 2023년 4월 이후 가장 큰 상승폭이에요(4월은 +3.8%). 물가가 예상보다 높으면 '연준이 금리를 올릴 수도 있다'는 걱정이 커질 수 있어요.",
  "summary":"로이터 집계 기준 5월 헤드라인 CPI(전체 물가)는 전년比 +4.2% 예상으로, 4월(+3.8%)보다 가속해 2023년 4월 이후 최대가 예상됩니다. 한국시간 6/10 21:30 발표. 호르무즈 봉쇄에 따른 에너지·물류비 상승이 물가를 밀어올리는 구조입니다.",
  "ourImpact":"물가가 높게 나오면 금리 인상 우려로 기술·성장주가 흔들리기 쉬워요. 보유 반도체주가 가장 민감한 구간이라, 발표 직후 변동이 클 수 있어요. 결과를 확인한 뒤 흐름을 보면 좋아요.",
  "impact":"negative","sources":[S_REUTERS]},
 {"category":"정책·금리",
  "headline":"美 2년물 국채금리 1년래 최고 — '금리 인상' 베팅 확산",
  "oneLineSummary":"미국 2년 만기 국채금리가 1년 만에 가장 높은 약 4.15%까지 올랐어요. 강한 고용지표 뒤로 '연준이 10월쯤 금리를 0.25%p 올릴 수도 있다'는 베팅이 커졌어요. 소기업 낙관지수는 떨어지고 가격 인상 계획은 4년 만에 최고로 늘어, 물가 압력이 계속될 거란 신호가 나왔어요.",
  "summary":"6/9 미국 2년물 국채금리가 약 4.15%로 1년래 최고. 빠르면 10월 0.25%p 인상을 일부 반영하기 시작했습니다. NFIB 소기업 낙관지수는 95.3(-0.6p), 향후 3개월 가격 인상 계획 비중은 약 4년 만에 최고로 인플레 고착 우려를 키웠습니다.",
  "ourImpact":"금리가 더 오를 수 있다는 신호는 비싼 성장주에 부담이에요. PER이 높은 AI·반도체주는 금리 뉴스에 민감하니, 오늘 밤 CPI와 함께 금리 흐름도 같이 보면 좋아요.",
  "impact":"negative","sources":[S_REUTERS,S_YF]},
 {"category":"글로벌·지정학",
  "headline":"미군, 장 마감 후 이란에 '자위적 타격' — 호르무즈 봉쇄 지속",
  "oneLineSummary":"미국 정규장이 끝난 뒤 미군이 이란에 '자위적 타격(자기 방어 차원의 공격)'을 가했다고 발표했어요. 트럼프 대통령이 낮에 추가 타격을 시사한 직후예요. 원유가 지나가는 호르무즈 해협 봉쇄가 계속되는 가운데, 유가는 이란 긴장에 다시 들썩이고 있어요.",
  "summary":"6/9 장 마감 후 미군이 이란에 자위적 타격을 발표했습니다. WTI 유가는 6/9 정규장에서 종가 기준 $89.22(-2.3%)로 내렸으나, 마감 후 미군 타격 소식에 유가 선물 곡선은 다시 위로 움직였습니다(약 $95 호가). 호르무즈 해협(세계 원유의 약 1/5 통과)은 여전히 봉쇄 상태입니다.",
  "ourImpact":"유가·지정학은 물가에 직접 영향을 줘서, 오늘 밤 CPI와 묶여 시장 분위기를 좌우해요. 전력주 TLN, 에너지 민감 종목엔 양방향 변수예요. 결과를 보고 판단하면 좋아요.",
  "impact":"negative","sources":[S_TS,S_INV]},
 {"category":"글로벌·지정학",
  "headline":"SpaceX 6/11 공모가·6/12 상장 — 역대 최대 75조원 규모 / OpenAI도 IPO 서류",
  "oneLineSummary":"일론 머스크의 스페이스X가 6/11 공모가를 정하고 6/12 상장해요. 주당 $135에 약 5.6억 주를 팔아 750억 달러(약 100조원 이상)를 조달, 기업가치 1.8조 달러로 역대 최대 상장이 될 전망이에요. 주문이 2배 넘게 몰렸어요. 챗GPT의 오픈AI도 상장 서류를 비공개로 제출했어요.",
  "summary":"스페이스X IPO는 6/11 가격 결정·6/12 거래 시작 예정으로, 555.6백만 주를 주당 $135에 공모해 약 750억 달러 조달, 기업가치 약 1.8조 달러가 거론됩니다(2배 초과 청약). 같은 주 오픈AI가 IPO 서류를 비공개 제출(앞서 앤트로픽도 제출)해 두 AI 대표주자의 올가을 데뷔 가능성이 열렸습니다.",
  "ourImpact":"대형 IPO에 자금이 쏠리면 기존 기술주에서 돈이 잠시 빠질 수 있어요. 다만 AI 투자 열기를 보여주는 신호이기도 해, 보유 AI 인프라(엔비디아·브로드컴 등)엔 중장기 우호적 분위기예요.",
  "impact":"neutral","sources":[S_YF]},
]

report = {
 "date": TODAY, "session":"full-morning",
 "title":"6/10(수) 08:00 풀 모닝 — 美 기술주 약세 혼조 S&P -0.26%·나스닥 -0.97% / CRDO +13% 실적 급등·MRVL -7.6% / 장 마감 후 미군 이란 공습 / 한국 6/10 -6% 매도 사이드카 / 오늘 밤 5월 CPI(예상 +4.2%)",
 "marketStatus": MS,
 "generatedAt":"2026-06-10T08:00:00+09:00","lastUpdated":pf['lastUpdated'],
 "marketSummary":"S&P500 7,386.65(-0.26%)·나스닥 25,678.82(-0.97%)·다우 50,872.11(+0.17%)·러셀2000 +0.25%. VIX 약 20.5. WTI 종가 $89.22(-2.3%, 마감 후 이란 타격에 $95 호가)·美 10년물 약 4.5%·2년물 약 4.15%(1년래 최고). 전날 반등 반도체 차익실현(MRVL -7.6%·LITE -8.2%·AMD -3.0%), CRDO +13% 실적 급등. 장 마감 후 미군 이란 공습. 한국 6/9 +8.18% 반등→6/10 -6% 매도 사이드카. 오늘 밤 21:30 5월 CPI(예상 +4.2%).",
 "dataQualityNote":"지수·VIX는 TheStreet/CNBC 검증. 보유 종목 가격은 portfolio.json(CNBC+Yahoo+stockanalysis 교차) 기준. WTI는 6/9 종가 $89.22 검증(마감 후 이란 타격으로 호가 상승).",
 "news": news,
}
json.dump(report, open(f"{DATA}/reports/{TODAY}.json","w"), ensure_ascii=False, indent=1)
print("report reconciled, news:", len(news))

idx = json.load(open(f"{DATA}/reports/index.json"))
idx['reports'] = [r for r in idx['reports'] if r['date']!=TODAY]
idx['reports'].append({"date":TODAY,"title":report['title'],
 "summary":"美 기술주 약세 혼조(S&P -0.26%·나스닥 -0.97%·다우 +0.17%). 전날 반등 칩 차익실현 — MRVL -7.6%·LITE -8.2%·AMD -3.0%, 반면 CRDO +13% 실적 급등·MU 골드만 목표가 $900 상향. 장 마감 후 미군 이란 공습. 한국 6/9 +8.18% 반등→6/10 -6% 매도 사이드카. 오늘 밤 21:30 5월 CPI 예상 +4.2%·SpaceX 6/12 상장."})
idx['reports'].sort(key=lambda r:r['date'])
json.dump(idx, open(f"{DATA}/reports/index.json","w"), ensure_ascii=False, indent=1)
print("index reconciled:", len(idx['reports']))

cal = json.load(open(f"{DATA}/calendar-events.json"))
cal['stock'][TODAY] = [{
 "type":"morning","label":"08:00 풀 모닝","color":"yellow","mood":"🟡","time":"08:00 KST",
 "title":"🟡 풀 모닝 — 美 기술주 약세 혼조·CRDO +13% 실적 급등, 장 마감 후 美 이란 공습, 한국 6/10 -6% 매도 사이드카, 오늘 밤 5월 CPI(예상 +4.2%)",
 "description":"6/9(화) 美 증시는 기술주 약세로 혼조 마감했어요(S&P500 -0.26%·나스닥 -0.97%·다우 +0.17%). 전날 반등했던 반도체에 차익실현(오른 김에 파는 것)이 재개되며 마벨(MRVL) -7.6%·루멘텀(LITE) -8.2%·AMD -3.0%로 약세였어요. 반면 보유 종목 크레도(CRDO)는 분기 실적이 예상을 크게 웃돌며 +13%대 급등했어요. 장중 트럼프의 이란 추가 타격 시사에 나스닥이 한때 -3.3%까지 밀렸다가 회복했고, 정규장 마감 후 미군이 이란에 '자위적 타격(자기 방어 차원의 공격)'을 발표했어요. 한국은 6/9 +8.18% 급반등했다가, 오늘(6/10) 미군의 이란 공습 여파로 코스피가 장중 -6%대 급락하며 매도 사이드카(급락 시 프로그램 매도를 잠시 멈추는 장치)가 발동됐어요. 오늘 밤 21:30(한국시간) 5월 소비자물가(CPI)가 최대 분수령 — 예상 +4.2%(2023년 4월 이후 최대).",
 "impact":"오늘 밤 CPI(소비자물가) 결과가 금리 방향을 좌우해요. 높게 나오면 금리 인상(돈을 빌리는 비용을 올리는 것) 우려로 기술·반도체주가 흔들릴 수 있어요.",
 "ourImpact":"보유 반도체 비중이 커서 CPI·지정학 변수에 변동이 클 수 있어요. CRDO는 실적 호조로 단독 급등(+13%)했고, MRVL·LITE는 변동이 큰 종목이라 차익실현에 크게 출렁였어요.",
 "stockImpacts":[]
}]
cal['lastUpdated'] = pf['lastUpdated']
json.dump(cal, open(f"{DATA}/calendar-events.json","w"), ensure_ascii=False, indent=1)
print("calendar reconciled")
