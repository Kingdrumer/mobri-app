#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, shutil, datetime, os
BASE="/sessions/inspiring-epic-pascal/mnt/claude/portfolio-pwa/data"
now_kst=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
iso=now_kst.strftime("%Y-%m-%dT%H:%M:%S+09:00")

# ---------- calendar-events.json ----------
CAL=os.path.join(BASE,"calendar-events.json")
shutil.copy(CAL, CAL+".before-us-open-0611.bak")
c=json.load(open(CAL,encoding="utf-8"))
day="2026-06-11"
ppi_event={
  "type":"indicator",
  "label":"5월 PPI 핫(+1.1%)","color":"red",
  "time":"21:30 KST",
  "title":"美 5월 PPI(생산자물가) 전월비 +1.1%·전년비 6.5% — 2022년 11월 이후 최고",
  "description":"미국 5월 생산자물가가 시장 예상(+0.7%)을 웃돈 전월비 +1.1%, 전년비 6.5%로 나오며 인플레 부담이 이어졌어요. 같은 시각 주간 신규 실업수당 청구는 예상(22만 건) 수준이었어요.",
  "impact":"PPI(생산자물가지수)는 공장·기업이 물건을 '팔 때' 받는 가격이에요. 소비자물가(CPI)보다 한 발 앞서 움직여서 '앞으로 물가가 더 오를까'를 가늠하는 선행 지표예요. 어제 CPI(+4.2%)에 이어 PPI까지 뜨겁게 나오면서, Fed(미국 중앙은행)가 금리 내리는 시점이 더 미뤄질 수 있다는 우려가 남았어요. 다만 이란 공습 종료에 따른 위험선호 회복이 더 강해 증시는 반등 출발했어요.",
  "ourImpact":"금리 인하가 늦춰지면 변동이 큰 성장주(NVDA·AMD·MU 등)에 단기 부담이 될 수 있어요. 하지만 오늘은 오라클발 AI 투자 기대가 더 커서 반도체가 오히려 반등 출발했어요.",
  "stockImpacts":[
    {"ticker":"MU","tone":"positive","magnitude":"+2.0%","text":"메모리 공급부족 기대가 물가 부담을 눌러 반등 출발"},
    {"ticker":"MRVL","tone":"positive","magnitude":"+5.0%","text":"S&P500 편입+AI 네트워크 기대로 강하게 반등"},
    {"ticker":"NVDA","tone":"neutral","magnitude":"+0.6%","text":"금리 우려와 AI 수요 기대가 맞물려 소폭 반등"},
    {"ticker":"TLN","tone":"negative","magnitude":"미확보","text":"유가 하락+금리 부담으로 전력주 약세 우려"}
  ]
}
lst=c["stock"].get(day,[])
# prepend so it shows near top; avoid duplicate
lst=[e for e in lst if not (e.get("type")=="indicator" and "PPI" in e.get("title",""))]
lst.insert(0, ppi_event)
c["stock"][day]=lst
c["lastUpdated"]=iso
json.dump(c, open(CAL,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("CALENDAR updated:", day, "events now", len(c['stock'][day]))

# ---------- reports/2026-06-11.json ----------
RP=os.path.join(BASE,"reports","2026-06-11.json")
shutil.copy(RP, RP+".before-us-open-0611.bak")
r=json.load(open(RP,encoding="utf-8"))

new_news=[
 {
  "category":"미국 증시",
  "headline":"美 증시 반등 출발 — 이란 공습 종료에 위험선호 회복",
  "oneLineSummary":"어제 물가 충격과 중동 긴장에 급락했던 미국 증시가 오늘은 반등하며 열었어요. 미군이 이란 공습을 '완료했다'고 밝히면서 전쟁이 곧 진정될 거란 기대가 돌았고, 공포지수(VIX)도 20.8로 6% 넘게 내려왔어요.",
  "summary":"개장 직후 S&P500은 약 7,306(+0.5%), 나스닥100 선물은 +1.2%로 반등했고 VIX(변동성·공포지수)는 20.8(-6%)로 진정됐습니다. 미군이 이란에 대한 추가 공습을 '완료'했다고 발표하면서 위험자산 선호가 회복됐고, 어제 CPI 쇼크로 4~5% 급락했던 반도체가 반등을 주도했습니다.",
  "ourImpact":"보유 반도체·AI 하드웨어가 일제히 반등 출발했어요(MRVL +5.0%·SNDK +3.6%·MU +2.0%·AMD +1.9%). 다만 메타는 -1.4%로 홀로 약했어요.",
  "impact":"positive",
  "sources":[{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/live/stock-market-today-thursday-june-11-dow-sp-500-nasdaq-222511784.html"},{"name":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-11-2026"}]
 },
 {
  "category":"개별 종목",
  "headline":"오라클 -10% 급락에도 반도체·AI 하드웨어는 반등",
  "oneLineSummary":"오라클이 클라우드 매출 부진과 빚 부담으로 -10% 급락했지만, 정작 'AI 데이터센터에 700억 달러를 더 쓰겠다'는 투자 계획이 칩·서버 회사엔 호재로 읽혔어요. 그래서 엔비디아·AMD·델·마이크론 같은 종목은 오히려 올랐어요.",
  "summary":"오라클은 4분기 클라우드 매출이 시장 기대(99.9억$)를 밑돈 99.1억$에 그쳤고, AI 투자비 마련을 위해 약 400억$를 차입·증자로 조달한다는 소식에 부채 우려로 약 10% 급락했습니다. 반대로 오라클의 대규모 데이터센터 투자(내년 약 700억$)는 GPU·서버 수요 지속 신호로 해석돼 AI 하드웨어주가 반등했습니다.",
  "ourImpact":"보유 종목 중 AMD(+1.9%)·MU(+2.0%)·NVDA(+0.6%)·SNDK(+3.6%)가 수혜를 봤어요. 델(DELL)도 프리마켓 강세 보도가 있었지만 개장가는 데이터 지연으로 확인 중이에요.",
  "impact":"positive",
  "sources":[{"name":"TipRanks","url":"https://www.tipranks.com/news/nvda-amd-dell-smci-why-ai-hardware-and-chip-stocks-are-rising-today-june-11-2026"},{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/live/stock-market-today-thursday-june-11-dow-sp-500-nasdaq-222511784.html"}]
 },
 {
  "category":"정책·금리",
  "headline":"5월 PPI 전월비 +1.1%·전년비 6.5% — 예상 상회",
  "oneLineSummary":"미국 5월 생산자물가(PPI)가 예상(+0.7%)보다 높은 전월비 +1.1%로 나왔어요. 전년비로는 6.5%로 2022년 11월 이후 가장 높아요. 어제 소비자물가(CPI)에 이어 물가가 계속 뜨겁다는 신호라, 금리 인하 시점이 더 미뤄질 수 있다는 우려가 남았어요.",
  "summary":"미 노동부가 21:30 KST 발표한 5월 PPI(생산자물가·기업이 팔 때 받는 가격)는 전월비 +1.1%로 시장 예상(+0.7%)을 웃돌았고, 전년비 6.5%로 2022년 11월 이후 최고치였습니다. CPI에 이은 인플레 서프라이즈로 Fed 금리 인하 지연 우려가 있으나, 이란 리스크 완화가 더 부각돼 증시는 반등 출발했습니다.",
  "ourImpact":"금리 인하가 늦어지면 변동이 큰 성장주(NVDA·AMD·MU)에 단기 부담이 될 수 있어요. 전력주 TLN은 금리 영향을 더 받는 편이라 흐름을 지켜보면 좋아요.",
  "impact":"negative",
  "sources":[{"name":"Investing.com","url":"https://www.investing.com/news/stock-market-news/ppi-and-jobless-claims-highlight-thursdays-economic-calendar-93CH-4735890"},{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/live/stock-market-today-thursday-june-11-dow-sp-500-nasdaq-222511784.html"}]
 },
 {
  "category":"글로벌·지정학",
  "headline":"美, 이란 공습 '완료' 발표 — 유가 하락 전환",
  "oneLineSummary":"미군이 이란에 대한 추가 공습을 '완료했다'고 밝히면서, 전쟁이 곧 진정될 거란 기대가 커졌어요. 어젯밤 한때 3% 넘게 뛰었던 국제유가는 다시 내림세로 돌아섰고, 안전자산인 금도 약세를 보였어요.",
  "summary":"미군이 이란 표적에 대한 공습을 완료했다고 발표하면서 위험회피 심리가 빠르게 누그러졌습니다. 전일 밤 브렌트유가 한때 +3.4%(96$ 돌파)까지 올랐던 유가는 하락 전환했고, 금도 약세를 보였습니다. 이란은 호르무즈 해협 봉쇄를 주장하고 있어 변동성은 남아 있습니다.",
  "ourImpact":"유가 하락은 인플레 부담을 덜어 성장주 전반에 우호적이에요. 다만 전력주 TLN(탈렌에너지)에는 상대적으로 부담이 될 수 있어 흐름을 지켜보면 좋아요.",
  "impact":"positive",
  "sources":[{"name":"Yahoo Finance","url":"https://finance.yahoo.com/markets/live/stock-market-today-thursday-june-11-dow-sp-500-nasdaq-222511784.html"}]
 }
]

# prepend (newest first), de-dup by headline
existing_heads={n.get("headline") for n in r.get("news",[])}
add=[n for n in new_news if n["headline"] not in existing_heads]
r["news"]=add + r.get("news",[])

r["session"]="US_OPEN"
r["marketStatus"]="🟢 美 증시 반등 출발 — 이란 공습 종료·오라클 AI 투자 기대에 반도체 반등 (S&P500 ~7,306 +0.5%, 나스닥선물 +1.2%, VIX 20.8). 5월 PPI +1.1%(전년비 6.5%)로 물가 부담은 잔존."
r["marketSummary"]=("美 증시 22:30 KST 개장 — 어제 CPI 쇼크·이란 리스크 급락 뒤 반등 출발. S&P500 약 7,306(+0.5%)·나스닥100 선물 +1.2%·VIX 20.8(-6%). "
 "미군 이란 공습 '완료' 발표로 위험선호 회복, 유가 하락 전환. 오라클은 클라우드 매출 부진+차입 부담으로 -10% 급락했으나 대규모 AI 데이터센터 투자(약 700억$)가 칩·서버 수요 신호로 읽혀 반도체 반등 주도 "
 "(MRVL +5.0%·SNDK +3.6%·MU +2.0%·AMD +1.9%·TSM +0.9%·NVDA +0.6%). META -1.4% 약세. 5월 PPI 전월비 +1.1%·전년비 6.5%(2022.11 이후 최고)로 인플레 부담은 잔존. "
 "DELL·CLS·CRDO·TLN은 개장가 데이터 지연으로 6/10 종가 기준.")
r["lastUpdated"]=iso
r["dataQualityNote"]="가격은 stockanalysis.com(CNBC/Yahoo 데이터) 개장가·프리마켓 호가 기준. DELL·CLS·CRDO·TLN 4종목은 6/11 개장가 미확보로 6/10 종가 기준(차기 캡처 시 갱신)."
json.dump(r, open(RP,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("REPORT updated. news count now:", len(r["news"]))
print("lastUpdated:", iso)
