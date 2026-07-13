#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
pf=json.load(open("portfolio.json",encoding="utf-8"))
rp=json.load(open("reports/2026-07-13.json",encoding="utf-8"))
sig=pf["signals"]

NAMES={"GOOG":"알파벳(구글)","META":"메타","AMZN":"아마존","NVDA":"엔비디아","TSM":"TSMC","AVGO":"브로드컴","MU":"마이크론","MRVL":"마벨","AMD":"AMD","SNDK":"샌디스크","DELL":"델","LITE":"루멘텀","CLS":"셀레스티카","CRDO":"크레도","TLN":"탈렌에너지"}
EMO={"green":"🟢","yellow":"🟡","red":"🔴"}

L=[]
L.append("# 📈 미국증시 일일보고서 — 2026년 7월 13일 (월) 풀 모닝 브리핑\n")
L.append("> 한국시간 08:00 기준 · 주식 초보자용 쉬운 브리핑 · 투자 추천이 아니라 정보 제공용이에요.\n")

# A. 학습 용어
L.append("## A. 오늘의 학습 용어 5개\n")
L.append("| 용어 | 쉬운 뜻 |")
L.append("|---|---|")
L.append("| 서킷브레이커 | 주가가 너무 급하게 떨어지면 거래를 잠시 멈추는 안전장치예요. |")
L.append("| ADR(미국주식예탁증서) | 외국 회사가 미국 증시에서 거래되게 만든 '분신' 주식이에요. |")
L.append("| 컨센서스 | 여러 증권사 분석가들의 평균 예상치예요. |")
L.append("| 차익 실현 | 오른 김에 일부 팔아 이익을 챙기는 거예요. |")
L.append("| CPI(소비자물가) | 물가가 1년 전보다 얼마나 올랐는지 보여주는 지표예요. |\n")

# B. 시장 한눈에
ms=rp["marketSummary"]
L.append("## B. 시장 한눈에 (지난 7/10 금요일 미국 종가)\n")
L.append("| 지표 | 종가 | 등락 | 한줄 |")
L.append("|---|---|---|---|")
def row(k,label):
    m=ms.get(k,{})
    c=m.get("close"); ch=m.get("change")
    cs=f"{c:,}" if isinstance(c,(int,float)) else "-"
    chs=(f"{ch:+.2f}%" if isinstance(ch,(int,float)) else "-")
    return f"| {label} | {cs} | {chs} | {m.get('note','')} |"
L.append(row("dow","다우"))
L.append(row("sp500","S&P500"))
L.append(row("nasdaq","나스닥"))
L.append(row("vix","공포지수(VIX)"))
L.append(row("wti","국제유가(WTI)"))
L.append(row("us10y","미 10년물 금리"))
L.append(f"| 공포·탐욕 지수 | {ms['fearGreed']['value']} | {ms['fearGreed']['label']} | {ms['fearGreed']['note']} |")
L.append(row("kospi","코스피(오늘 월)"))
L.append("")
L.append("> ⚠️ **오늘(월) 아시아 '블랙 먼데이'**: 코스피가 −8.95%(6,806.93) 폭락하며 올해 7번째 서킷브레이커가 걸렸어요. 삼성전자 −9.2%·SK하이닉스 −13.4%. 미 지수선물도 −0.4~−1.4% 하락 예고로, 오늘 밤 뉴욕은 약세 출발이 예상돼요.\n")

# C. 뉴스
L.append("## C. 오늘의 뉴스 (카테고리별)\n")
cur=None
for n in rp["news"]:
    if n["category"]!=cur:
        cur=n["category"]; L.append(f"### {cur}\n")
    badge={"positive":"🟢","negative":"🔴","neutral":"⚪"}.get(n["impact"],"")
    L.append(f"**{badge} {n['headline']}**\n")
    L.append(n["oneLineSummary"]+"\n")
    L.append(f"- 📌 내 포트폴리오 영향: {n['ourImpact']}")
    srcs=" · ".join(f"[{x['name']}]({x['url']})" for x in n.get("sources",[]))
    L.append(f"- 🔗 출처: {srcs}\n")

# D. 포트폴리오 표
L.append("## D. 내 보유 종목 15개 (7/10 금요일 미국 종가)\n")
L.append("| 신호 | 종목 | 종가($) | 당일 | 주간 | 월간 | 연초대비 | 한줄 |")
L.append("|---|---|---|---|---|---|---|---|")
grn=yel=red=0
for s in pf["us"]:
    sg=s["signal"]; grn+=sg=="green"; yel+=sg=="yellow"; red+=sg=="red"
    def p(v): return (f"{v:+.1f}%" if isinstance(v,(int,float)) else "-")
    L.append(f"| {EMO[sg]} | {s['ticker']} {NAMES.get(s['ticker'],'')} | {s['price']:,} | {p(s['change1D'])} | {p(s.get('change1W'))} | {p(s.get('change1M'))} | {p(s.get('changeYTD'))} | {s['note']} |")
L.append("")
L.append(f"**🛡️ 데이터 가드 결과**: 보유 15종목 당일 등락·현재가는 CNBC/Yahoo·stockanalysis(CBOE) 교차 검증값이에요(정상). 주간·월간·연초 등락률은 직전 검증 기준값에서 환산해 소폭 오차 가능성이 있어요. 국내 시그널·외국인 매매 동향은 이번 실행 환경에서 네이버 금융 접근이 막혀 직전 검증 데이터를 유지했어요.\n")

# E. 회사별 쉬운 해석
L.append("## E. 회사별 쉬운 해석 (왜 움직였나)\n")
for s in pf["us"]:
    L.append(f"- **{EMO[s['signal']]} {s['ticker']} {NAMES.get(s['ticker'],'')}**: {s['todayWhy']}")
L.append("")

# F. 이번 주 일정
L.append("## F. 이번 주 일정\n")
for w in rp["weekAhead"]:
    L.append(f"- **{w['date']}** — {w['event']}  \n  ↳ {w['impact']}")
L.append("")

# G. 신호등 정리
L.append("## G. 신호등 정리\n")
L.append(f"- 🟢 초록(양호) {grn}개 · 🟡 노랑(관망) {yel}개 · 🔴 빨강(주의) {red}개")
L.append("- 지난 금요일 미국 장은 양호했지만, 오늘(월) 아시아 급락과 미 선물 하락으로 **오늘 밤 뉴욕은 약세 출발 가능성**이 커요. 하루 등락보다 주간 흐름으로 보는 게 마음이 편해요.\n")

# 시그널 요약
L.append("## 🎯 오늘의 주목 종목 (참고용, 추천 아님)\n")
L.append("**미국 시그널**")
for x in sig["us"]:
    L.append(f"- **{x['ticker']} {x['name']}** ({x.get('category','')}, ${x.get('currentPrice')} {x.get('change1D'):+.2f}%): {x.get('thesis','')[:120]}")
L.append("\n**미국 신규 상장주**")
for x in sig["newListings"]["us"]:
    L.append(f"- **{x['ticker']} {x['name']}** (상장 {x.get('listedAt')}, ${x.get('currentPrice')} {x.get('change1D'):+.2f}%): {x.get('thesis','')[:120]}")
L.append(f"\n> 국내 시그널(SK하이닉스·한미반도체·두산에너빌리티)·외국인 매매·국내 신규상장은 네이버 금융 접근 제한으로 직전 검증 데이터를 유지했어요.\n")

# H. Sources
L.append("## H. 주요 출처\n")
L.append("- 시세: [stockanalysis.com](https://stockanalysis.com) (CBOE 실시간), [Yahoo Finance](https://finance.yahoo.com), [CNBC](https://www.cnbc.com/markets/)")
L.append("- 지수/심리: [CNN Markets](https://www.cnn.com/markets), [CNN Fear & Greed](https://www.cnn.com/markets/fear-and-greed)")
L.append("- 뉴스: 각 뉴스 항목의 출처 링크 참조 (CNBC·Bloomberg·Reuters·Invezz 등)\n")
L.append(f"\n---\n*생성: 2026-07-13 08:00 KST · Mobri 풀 모닝 브리핑 · 폰 앱: https://mobri-app.netlify.app*")

open("../미국증시_일일보고서_2026-07-13.md","w",encoding="utf-8").write("\n".join(L))
print("markdown written:", sum(len(x) for x in L), "chars,", len(L), "lines")
print(f"signals: green {grn}, yellow {yel}, red {red}")
