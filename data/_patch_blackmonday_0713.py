#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def s(name,url): return {"name":name,"url":url}

STATUS = ("🇺🇸 지난 7/10(금) 미국 증시는 3대 지수 모두 상승 마감했어요 — 다우 52,637(+0.29%)·S&P500 7,575(+0.42%)·나스닥 26,282(+0.29%). "
 "SK하이닉스가 나스닥에 외국 기업 사상 최대(265억$) 규모로 데뷔해 +14% 급등하며 AI 메모리 열기를 지폈어요. "
 "보유 종목은 META(+6.0%)·NVDA(+4.0%)·SNDK(+3.1%)가 강했어요. "
 "⚠️ 하지만 오늘(월) 아시아가 급락했어요 — 코스피가 −8.95%(6,806.93) '블랙 먼데이'로 올해 7번째 서킷브레이커(거래 일시정지)가 걸렸고, 삼성전자 −9.2%·SK하이닉스 −13.4%가 폭락했어요. "
 "SK하이닉스 미국 상장 후 국내 주식이 상대적으로 비싸 보이는 차익 실현, 반도체 고점 우려, 중동(호르무즈) 긴장이 겹쳤어요. "
 "미 지수선물도 −0.4~−1.4% 하락 출발을 예고해, 오늘 밤(월) 뉴욕은 약세로 열릴 가능성이 커요.")

HOLIDAY = ("🟡 지난 금요일 미국 증시는 상승 마감했지만, 오늘(월) 아시아 반도체 급락과 미국 선물 하락으로 오늘 밤 22:30(한국시간) 뉴욕은 약세 출발이 예상돼요. "
 "이번 주 핵심은 7/14(화) 밤 21:30 6월 소비자물가(CPI)와 같은 날 시작되는 대형 은행 실적이에요.")

# ---- patch portfolio.json ----
P="portfolio.json"
pf=json.load(open(P,encoding="utf-8"))
pf["marketStatus"]=STATUS
pf["holidayNote"]=HOLIDAY
json.dump(pf,open(P,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# ---- patch report ----
R="reports/2026-07-13.json"
rp=json.load(open(R,encoding="utf-8"))
rp["marketStatus"]=STATUS
rp["holidayNote"]=None
rp["title"]=("7월 13일 (월) 08:00 풀 모닝 — 지난 금요일 미 3대 지수 상승 마감(SK하이닉스 나스닥 +14% 데뷔)했지만, "
 "오늘(월) 아시아 '블랙 먼데이' 코스피 −8.95%·서킷브레이커 / 美 선물 하락으로 오늘 밤 뉴욕 약세 출발 예상")
rp["afterHoursNote"]=("오늘(월) 아시아 반도체 급락(코스피 −8.95%)과 미 지수선물 하락(−0.4~−1.4%)으로 오늘 밤 22:30 뉴욕은 약세 출발 가능성이 커요. "
 "보유 반도체주(NVDA·AVGO·MU·MRVL·AMD)가 아시아 여파로 흔들릴 수 있어 개장 초반 흐름을 가볍게 지켜보면 좋아요. 7/14 밤 CPI·은행 실적이 다음 분수령이에요.")

# black Monday news (primary Asia item) — replace existing Asia items
blackmonday = {"category":"아시아 증시","impact":"negative",
 "headline":"코스피 '블랙 먼데이' −8.95% 6,806.93 — 올해 7번째 서킷브레이커",
 "oneLineSummary":"오늘(월) 한국 코스피가 하루 만에 −8.95% 폭락한 6,806.93으로 마감했어요. 장중 거래가 잠시 멈추는 서킷브레이커가 올해 7번째로 걸렸어요. SK하이닉스가 미국에 상장하면서 국내 주식이 상대적으로 비싸 보여 차익 실현이 몰렸고, 반도체 고점 우려와 중동 긴장까지 겹쳤어요.",
 "summary":"7/13 코스피가 전장(7,475.94) 대비 −669p(−8.95%) 급락한 6,806.93 마감, 올해 7번째 서킷브레이커가 발동됐습니다. 외국인·기관이 2.8조원 넘게 순매도했고 삼성전자 −9.21%(₩258,750)·SK하이닉스 −13.35%가 폭락했습니다. SK하이닉스 ADR 상장 후 국내주 할인 압력, 한국투자증권의 2분기 이익 컨센서스 −8% 전망(피크아웃 우려), 미·이란 호르무즈 충돌에 따른 유가·환율 상승이 겹쳤습니다. 니케이·CSI300도 약 −2%, 미 지수선물은 −0.4~−1.4% 하락 예고.",
 "ourImpact":"보유 반도체주 NVDA·AVGO·MU·MRVL·AMD가 아시아 급락 여파로 오늘 밤 약하게 출발할 가능성이 커요. 하루 등락보다 주간 흐름을 보며 개장 초반만 가볍게 지켜보면 좋아요.",
 "sources":[s("Invezz","https://invezz.com/news/2026/07/13/heres-why-the-kospi-index-is-in-a-freefall-today-july-13/"),s("BigGo Finance","https://finance.biggo.com/news/adba3e22-c135-4a4d-8157-06aab5e6e5e7"),s("Bloomberg","https://www.bloomberg.com/news/articles/2026-06-23/korean-stocks-fall-more-than-4-from-record-high-on-tech-selloff")]}

friday_asia = {"category":"아시아 증시","impact":"positive",
 "headline":"(지난 금요일) 코스피 +2.5%·니케이 +1.2%·항셍 +0.6% 동반 상승",
 "oneLineSummary":"지난 금요일(7/10)엔 아시아 주요 지수가 모두 올랐어요. 코스피가 +2.5%로 가장 크게 뛰며 SK하이닉스 미국 상장 기대로 반도체가 강했는데, 바로 다음 거래일인 오늘(월) 정반대로 급락하며 변동성이 얼마나 큰지 보여줬어요.",
 "summary":"7/10 코스피 7,475.94(+2.5%)·니케이225 68,558(+1.2%)·항셍 24,175.12(+0.60%)로 동반 상승했으나, 3거래일 만인 7/13 코스피가 −8.95% 급락하며 반전됐습니다.",
 "ourImpact":"이틀 만에 +2.5%→−8.95%로 뒤집힌 만큼, 지금은 하루 등락에 흔들리기보다 주간·월간 흐름으로 보는 게 마음이 편해요.",
 "sources":[s("CNBC Asia","https://www.cnbc.com/2026/07/03/stock-market-today-live-updates.html")]}

news=rp["news"]
news=[n for n in news if n.get("category")!="아시아 증시"]
# insert asia items right after 미국 증시 block (keep order: US, then Asia, then rest)
out=[]
inserted=False
for n in news:
    out.append(n)
    if n.get("category")=="미국 증시" and not inserted and (out.count(n)):
        pass
# simpler: rebuild by category order
order={"미국 증시":0,"아시아 증시":1,"개별 종목":2,"정책·금리":3,"글로벌·지정학":4}
news2=news+[blackmonday,friday_asia]
news2.sort(key=lambda n: order.get(n.get("category"),9))
rp["news"]=news2

# update marketSummary asia to reflect Monday crash (latest close)
ms=rp["marketSummary"]
ms["kospi"]={"close":6806.93,"change":-8.95,"note":"코스피 −8.95%(6,806.93) '블랙 먼데이' — 오늘(월) 서킷브레이커 발동. 지난 금요일은 +2.5%였어요.","approx":False}
ms["nikkei"]={"close":None,"change":-2.0,"note":"니케이도 오늘(월) 약 −2% 약세(지난 금요일 +1.2%에서 반전).","approx":True}
ms["hangseng"]={"close":None,"change":-2.0,"note":"항셍·CSI300도 오늘 약세.","approx":True}
rp["dataQualityNote"]=pf["signals"]["dataQualityNote"]
json.dump(rp,open(R,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# update index title
idx=json.load(open("reports/index.json",encoding="utf-8"))
for r in idx["reports"]:
    if r.get("date")=="2026-07-13":
        r["title"]="7월 13일 (월) 풀 모닝 브리핑"
        r["summary"]="지난 금요일 미 3대 지수 상승(SK하이닉스 나스닥 +14% 데뷔) / 오늘(월) 아시아 블랙먼데이 코스피 −8.95%·美선물 하락 → 밤 뉴욕 약세 출발 예상 / 7/14 CPI·은행 실적"
json.dump(idx,open("reports/index.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)

print("patched. news categories order:", [n["category"] for n in rp["news"]])
print("news count:", len(rp["news"]))
