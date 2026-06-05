#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
TS = "2026-06-06T06:00:00+09:00"
BASE = os.path.dirname(os.path.abspath(__file__))
def p(f): return os.path.join(BASE, f)

pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
byT = {s["ticker"]: s for s in pf["us"]}

rep = json.load(open(p("reports/2026-06-05.json"), encoding="utf-8"))
rep["lastUpdated"] = TS
rep["generatedAt"] = TS
rep["session"] = "fri-usclose"
rep["marketStatus"] = pf["marketStatus"]
rep["title"] = ("6/5(금) 美 정규장 마감 — 5월 고용 +17.2만 예상 2배 깜짝 + 'AI 거품' 경계로 기술주 급락. "
                "나스닥 -4.18%(작년 4월 이후 최악)·S&P -2.64%·다우 -1.35%, 필라델피아 반도체지수 -10.26%. "
                "보유 반도체 폭락(MRVL -16.7%·MU -13.2%·SNDK -11.4%·AVGO -7.9%·NVDA -6.2%), 메타 증자설 -5.5%")

# sync stockSnapshot to close prices
TR = "TradingKey 종가집계"
for snap in rep.get("stockSnapshot", []):
    t = snap["ticker"]
    if t in byT:
        s = byT[t]
        for f in ("price","change1D","change1W","change1M","changeYTD","signal","priceSourcedFrom","dataQualityNote"):
            snap[f] = s[f]

SRC = lambda name,url: {"name":name,"url":url}
TK = "https://www.tradingkey.com/analysis/stocks/us-stocks/261950389-nasdaq-sp500-ai-sndk-broadcom-sox-google-meta-fmcc-fnma-fed-rate-tradingkey"
YF = "https://ca.finance.yahoo.com/news/stock-market-today-sp-500-nasdaq-slide-as-jobs-report-fuels-fed-hike-bets-230134469.html"

close_news = [
 {"category":"미국 증시",
  "headline":"나스닥 -4.18% 마감 — 작년 4월 이후 최악, 기술주 급락",
  "oneLineSummary":"미국 증시가 정규장에서 크게 떨어졌어요. 5월 일자리가 예상의 2배로 나와 '금리를 올릴 수도 있다'는 걱정이 커진 데다 'AI에 돈이 너무 몰렸다'는 경계까지 겹쳤어요. 나스닥은 -4.18%로 작년 4월 이후 가장 많이 빠졌어요.",
  "summary":"6/5 정규장 마감 다우 50,866.78(-1.35%), S&P500 7,383.74(-2.64%), 나스닥 25,709.43(-4.18%). 5월 고용(NFP) +17.2만으로 예상(약 8.5만)의 2배, 3·4월 수치도 합쳐 +9.3만 상향돼 금리 인상 베팅이 강해짐. 'AI 거품' 경계와 엔비디아 메모리 축소설이 겹치며 기술주 전반 급락.",
  "ourImpact":"보유 종목 대부분이 금리에 민감한 AI 성장주라 이날 낙폭이 컸어요. 반대로 구글(-1.0%)·아마존(-3.1%) 같은 빅테크는 상대적으로 잘 버텼어요. 하루 변동이 큰 날이라 흐름만 가볍게 지켜보면 좋아요.",
  "impact":"negative",
  "sources":[SRC("TradingKey(종가집계)",TK),SRC("Yahoo Finance",YF)]},
 {"category":"미국 증시",
  "headline":"공포지수 VIX +40% 급등, 금·비트코인도 동반 하락",
  "oneLineSummary":"시장의 불안을 나타내는 공포지수(VIX)가 하루 만에 +40% 뛴 21.5가 됐어요. 주식뿐 아니라 금과 비트코인도 같이 내려서, 투자자들이 위험한 자산을 일제히 줄이는 하루였어요.",
  "summary":"6/5 VIX 21.51(약 +40%)로 한 달여 만에 20선 위로 복귀. 위험 회피 속에 금 현물은 $4,375(-2.2%)로 3/27 이후 최저, 비트코인도 $60,463(-5.2%)까지 급락. 강한 고용에 금리 인상 우려가 커지며 안전자산·위험자산이 동반 약세.",
  "ourImpact":"특정 종목 이슈라기보다 시장 전체가 위험을 피한 날이라, 보유 종목도 분위기에 함께 눌렸어요. 이런 날은 개별 회사 펀더멘털보다 시장 심리의 영향이 더 커요.",
  "impact":"negative",
  "sources":[SRC("TradingKey(종가집계)",TK)]},
 {"category":"개별 종목",
  "headline":"보유 반도체 일제히 폭락 — 마벨 -16.7%, 마이크론 -13.2%",
  "oneLineSummary":"보유 반도체 종목들이 크게 빠졌어요. '엔비디아가 차세대 칩에서 메모리를 덜 쓸 수 있다'는 소문이 메모리 회사들을 직접 때렸고, 변동이 큰 AI 반도체가 가장 세게 흔들렸어요. 마벨 -16.7%, 마이크론 -13.2%였어요.",
  "summary":"6/5 마감 MRVL -16.74%, MU -13.21%, SNDK -11.39%($1,559.32), AVGO -7.92%($385.73, 이틀 -19.51%), TSM -6.68%, NVDA -6.20%($205대), AMD 약 -9%. 필라델피아 반도체지수 -10.26%로 30개 전 종목 하락. 엔비디아 루빈 플랫폼 메모리 용량 축소설(랙당 55TB→28TB)이 도화선.",
  "ourImpact":"반도체 비중이 큰 우리 포트폴리오엔 부담이 큰 하루였어요. 다만 이들 대부분은 올해 크게 오른 종목이라 변동이 큰 편이에요. (9종목은 확정 종가, AMD·CRDO·LITE·CLS는 섹터 추정치예요.) 하루 등락보다 흐름을 가볍게 보면 좋아요.",
  "impact":"negative",
  "sources":[SRC("TradingKey(종가집계)",TK)]},
 {"category":"개별 종목",
  "headline":"메타 -5.5% — AI 투자용 '대규모 증자설'(FT 보도)",
  "oneLineSummary":"보유 종목 메타가 -5.5% 내렸어요. AI 시설에 쓸 돈을 마련하려고 '새 주식을 수백억 달러어치 찍을 수 있다'는 보도(파이낸셜타임스)가 나왔어요. 주식 수가 늘면 내 몫이 줄어들 수 있어 매도가 몰렸어요.",
  "summary":"6/5 META -5.51%(약 $593). FT는 메타가 알파벳의 850억$ 증자 성공에 자극받아 수백억$ 규모 주식 발행을 검토 중이라고 보도(회사 공식 발표 아님, 은행 미선임·철회 가능). 2026년 설비투자 가이던스 최대 1,450억$ 부담과 겹쳐 희석 우려가 부각됨.",
  "ourImpact":"메타 단독 악재성 뉴스였어요. 다만 '검토 단계' 보도라 실제 증자로 이어질지는 아직 불확실해요. 같은 빅테크인 구글·아마존은 이 이슈와 무관하게 상대적으로 잘 버텼어요.",
  "impact":"negative",
  "sources":[SRC("TradingKey(종가집계)",TK)]},
 {"category":"정책·금리",
  "headline":"5월 고용 +17.2만 예상 2배 — 연은 '금리 인상 곧 적절할 수도'",
  "oneLineSummary":"미국 5월 일자리가 17.2만 개 늘어 예상(약 8.5만)의 2배로 나왔어요. 고용이 너무 좋자 '금리를 내리기는커녕 올릴 수도 있다'는 쪽으로 분위기가 바뀌었고, 한 연방준비제도 인사는 '곧 인상이 적절할 수 있다'고 말했어요.",
  "summary":"5월 NFP +17.2만(컨센 약 8.5만), 실업률 4.3%로 2개월 연속 유지, 3·4월 합산 +9.3만 상향. 클리블랜드 연은 해맥 총재는 '추세가 이어지면 곧 금리 인상이 적절할 수 있다'고 발언. 시장은 연내 금리 인하 기대를 사실상 접고 인상 가능성을 반영하기 시작.",
  "ourImpact":"금리가 오르면 빚을 많이 쓰는 AI 성장주에 단기 부담이 돼요. 보유 종목 다수가 여기에 해당해 이날 약세의 큰 배경이 됐어요. 앞으로 물가(CPI·PCE) 지표가 이 방향을 굳힐지 가를 변수예요.",
  "impact":"negative",
  "sources":[SRC("TradingKey(종가집계)",TK)]},
 {"category":"글로벌·지정학",
  "headline":"호르무즈 해협 통행 거의 멈춰 — 미·이란 협상 교착",
  "oneLineSummary":"세계 원유의 길목인 호르무즈 해협에 배가 거의 다니지 못하고 있어요. 미국과 이란의 협상이 진전이 없자 긴장이 이어지고 있어요. 다만 이날 미국 대표 원유(WTI) 가격은 소폭 내렸어요.",
  "summary":"블룸버그에 따르면 미·이란 협상 교착 속에 6/5 오전 호르무즈 해협 상업 운항이 사실상 제로 수준(전날 양방향 각 3척→0). 다만 유가는 WTI $92.63(-0.44%)로 소폭 하락. 지정학 긴장과 협상 기대가 엇갈리는 국면.",
  "ourImpact":"유가가 다시 크게 뛰면 물가 부담이 커져 금리 인상 우려가 더 강해질 수 있어 보유 성장주엔 간접 변수예요. 반대로 보유 전력주 탈렌(TLN)은 에너지 흐름과는 별개로 전력 수요 테마로 움직이는 편이에요.",
  "impact":"neutral",
  "sources":[SRC("TradingKey(종가집계)",TK)]},
]
rep["news"] = close_news + rep.get("news", [])

json.dump(rep, open(p("reports/2026-06-05.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("report updated. news items:", len(rep["news"]), "| snapshot:", len(rep["stockSnapshot"]))

# ---------- index.json ----------
idx = json.load(open(p("reports/index.json"), encoding="utf-8"))
idx["lastUpdated"] = TS
for e in idx["reports"]:
    if e["date"] == "2026-06-05":
        e["title"] = "6월 5일 (금) 美 마감 — 나스닥 -4.18%(작년 4월 이후 최악)·반도체지수 -10.3%, 보유 반도체 폭락(마벨 -16.7%·마이크론 -13.2%), 메타 증자설 -5.5%"
        e["summary"] = ("6/5 정규장 마감 다우 50,866.78(-1.35%)·S&P500 7,383.74(-2.64%)·나스닥 25,709.43(-4.18%)·필라델피아 반도체지수 -10.26%(30종목 전 하락). "
                        "5월 고용 +17.2만(예상 2배)+'AI 거품' 경계+엔비디아 메모리 축소설로 기술주 급락. 보유 반도체 동반 폭락 — MRVL -16.7%·MU -13.2%·SNDK -11.4%·AVGO -7.9%(이틀 -19.5%)·NVDA -6.2%·TSM -6.7%·AMD 약 -9%. 메타 AI 증자설(FT)로 -5.5%. VIX 21.5(+40%), 금·비트코인 동반 급락. ⚠ 9종목 확정·6종목 섹터 추정 플래그.")
        break
json.dump(idx, open(p("reports/index.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("index.json updated for 2026-06-05")
print("DONE phase2")
