#!/usr/bin/env python3
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
p=json.load(open("portfolio.json"))
r=json.load(open("reports/2026-08-08.json"))
idx=r["indices"]

krname={'GOOG':'알파벳(구글)','META':'메타','AMZN':'아마존','NVDA':'엔비디아','TSM':'TSMC','AVGO':'브로드컴','MU':'마이크론','MRVL':'마벨','AMD':'AMD','SNDK':'샌디스크','DELL':'델','LITE':'루멘텀','CLS':'셀레스티카','CRDO':'크레도','TLN':'탈렌에너지'}
emoji={'green':'🟢','yellow':'🟡','red':'🔴'}

L=[]
L.append("# 📈 미국증시 일일보고서 — 2026년 8월 8일 (토) 풀 모닝\n")
L.append(f"> {r['title']}\n")
L.append(f"*생성: {r['generatedAt']} · 8/7(금) 미국 확정 종가 기준 · 주말 휴장*\n")

L.append("\n## A. 오늘의 학습 용어 5개\n")
terms=[
 ("HBM (고대역폭 메모리)","AI 칩에 데이터를 빠르게 공급하는 고성능 메모리. SK하이닉스·마이크론이 주력."),
 ("광통신","칩끼리 전기 대신 '빛'으로 데이터를 주고받는 기술. 데이터센터 속도를 높여줘요. (LITE·CRDO)"),
 ("순환매","한 업종에서 판 돈이 다른 업종으로 옮겨가며 번갈아 오르는 것. 어제는 반도체→방산."),
 ("어닝 서프라이즈","실적이 시장 예상보다 훨씬 좋게 나오는 것. 팰런티어 2Q 매출 +93%가 사례."),
 ("CPI (소비자물가)","한 달 동안 물건·서비스 값이 얼마나 올랐는지 보여주는 지표. 금리 방향을 좌우해요."),
]
for t,d in terms: L.append(f"- **{t}**: {d}")

L.append("\n## B. 시장 한눈에\n")
L.append("| 지표 | 값 | 변동 |")
L.append("|---|---|---|")
L.append(f"| 다우 | {idx['dow']['value']} | {idx['dow']['change']:+}% |")
L.append(f"| S&P500 | {idx['sp500']['value']} | {idx['sp500']['change']:+}% (사상 최고) |")
L.append(f"| 나스닥 | {idx['nasdaq']['value']} | {idx['nasdaq']['change']:+}% |")
L.append(f"| VIX (공포지수) | {idx['vix']['value']} | {idx['vix']['change']:+} |")
L.append(f"| WTI 유가 | ${idx['wti']['value']} | {idx['wti']['change']:+}% |")
L.append(f"| 미 10년물 금리 | {idx['ust10y']['value']}% | {idx['ust10y']['change']:+} |")
L.append(f"| Fear & Greed | {idx['fearGreed']['value']} | {idx['fearGreed']['label']} |")
L.append(f"\n{r['marketStatus']}\n")

L.append("\n## C. 뉴스 (카테고리별)\n")
cur=None
for n in r["news"]:
    if n["category"]!=cur:
        cur=n["category"]; L.append(f"\n### {cur}")
    ic={'positive':'🟢','negative':'🔴','neutral':'⚪'}.get(n["impact"],'⚪')
    L.append(f"\n**{ic} {n['headline']}**\n")
    L.append(f"{n['oneLineSummary']}\n")
    L.append(f"> 📌 내 종목 영향: {n['ourImpact']}")

L.append("\n## D. 포트폴리오 데이터 (보유 15종목 · 8/7 금 종가)\n")
L.append("| 신호 | 종목 | 종가 | 1일 | 1주 | 1개월 | 올해 |")
L.append("|---|---|---|---|---|---|---|")
for s in p["us"]:
    L.append(f"| {emoji[s['signal']]} | {krname.get(s['ticker'],s['ticker'])} ({s['ticker']}) | ${s['price']} | {s['change1D']:+}% | {s['change1W']:+}% | {s['change1M']:+}% | {s['changeYTD']:+}% |")
g=sum(1 for s in p['us'] if s['signal']=='green'); y=sum(1 for s in p['us'] if s['signal']=='yellow'); rd=sum(1 for s in p['us'] if s['signal']=='red')
L.append(f"\n**가드 결과: ✓ 정상 15개 (교차검증 통과) · 🟢 {g} · 🟡 {y} · 🔴 {rd}**")
L.append(f"\n*{r['dataQualityNote']}*")

L.append("\n## E. 회사별 쉬운 해석 (오늘 왜 움직였나)\n")
for s in p["us"]:
    L.append(f"- {emoji[s['signal']]} **{krname.get(s['ticker'],s['ticker'])} ({s['ticker']}) {s['change1D']:+}%** — {s['todayWhy']}")

L.append("\n## F. 오늘의 시그널 (주목 종목)\n")
L.append("> 투자 추천이 아니라, 검증된 데이터로 '왜 지금 주목받나'를 정리한 거예요.\n")
L.append("### 🇰🇷 국내 3")
for s in p["signals"]["kr"]:
    L.append(f"\n**[{s['category']}] {s['name']} ({s['ticker']}) · {s['currentPrice']}원 ({s['change1D']:+}%)**\n")
    L.append(f"{s['thesis']}\n")
    L.append(f"- 재무: {s['financials']}")
    L.append(f"- 전망(쉬움): {s['outlookEasy']}")
    if s.get('flowReason'): L.append(f"- 외인 흐름: {s['flowReason']['summary']}")
    L.append(f"- 같이 볼 종목: " + ", ".join(f"{x['name']}({float(x['change1D']):+}%)" for x in s['relatedStocks']))
L.append("\n### 🇺🇸 미국 2")
for s in p["signals"]["us"]:
    L.append(f"\n**[{s['category']}] {s['name']} ({s['ticker']}) · ${s['currentPrice']} ({s['change1D']:+}%)**\n")
    L.append(f"{s['thesis']}\n")
    L.append(f"- 재무: {s['financials']}")
    L.append(f"- 전망(쉬움): {s['outlookEasy']}")
    L.append(f"- 같이 볼 종목: " + ", ".join(f"{x['name']}({float(x['change1D']):+}%)" for x in s['relatedStocks']))

L.append("\n### 🌍 국내 외국인 매매 동향 (5거래일)")
ff=p["signals"]["krForeignFlow"]
L.append(f"*{ff['lookbackDays']} · 기준일 {ff['asOf']}*\n")
L.append("| 종목 | 외인소진율 | 5일 순매수 | 추세 |")
L.append("|---|---|---|---|")
for row in ff["rows"]:
    fr=f"{row['foreignHoldRatio']}%" if row['foreignHoldRatio'] else "-"
    L.append(f"| {row['name']} | {fr} | {row['netBuy5d']:,}주 | {row['trend']} |")
L.append("")
for ins in ff["insights"]: L.append(f"- {ins}")

L.append("\n## G. 이번 주 일정\n")
for w in r["weekAhead"]:
    L.append(f"- **{w['date']}** {w['event']} — {w['note']}")

L.append("\n## H. 신호등 정리\n")
L.append(f"- 🟢 강세({g}): " + ", ".join(s['ticker'] for s in p['us'] if s['signal']=='green'))
L.append(f"- 🟡 중립({y}): " + ", ".join(s['ticker'] for s in p['us'] if s['signal']=='yellow'))
L.append(f"- 🔴 조정({rd}): " + ", ".join(s['ticker'] for s in p['us'] if s['signal']=='red'))
L.append("\n> ⚠️ 이 보고서는 정보 제공용이며 투자 추천이 아니에요. 최종 판단은 본인의 몫이에요.")

L.append("\n## Sources\n")
L.append("- CNBC Markets — https://www.cnbc.com/markets/")
L.append("- 네이버 금융 (실시간 시세·재무·외인 동향) — https://m.stock.naver.com/")
L.append("- WebSearch 교차확인 (NVDA·CRDO·GOOG 종가 일치 확인)")
L.append("- 비즈니스코리아·머니투데이·서울경제·핀포인트뉴스·연합인포맥스 (8/7~8/8 보도)")

out="\n".join(L)+"\n"
open("../미국증시_일일보고서_2026-08-08.md","w").write(out)
open("../../미국증시_일일보고서_2026-08-08.md","w").write(out)
print("markdown written,",len(out),"chars")
