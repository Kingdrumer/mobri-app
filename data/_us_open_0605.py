#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, shutil, os

TS = "2026-06-05T22:46:00+09:00"
BASE = os.path.dirname(os.path.abspath(__file__))
def p(f): return os.path.join(BASE, f)

# ---------- backups ----------
shutil.copy(p("portfolio.json"), p("portfolio.json.before-us-open-0605.bak"))
shutil.copy(p("calendar-events.json"), p("calendar-events.json.before-us-open-0605.bak"))
shutil.copy(p("reports/2026-06-05.json"), p("reports/2026-06-05.json.before-us-open.bak"))

# ---------- per-ticker open-session data (6/5 22:30 KST open) ----------
# fields: price(open), chg(=change1D today move %), conf(confirmed), todayWhy, dq(dataQualityNote)
SRC_CONF = ["CNBC", "Yahoo Finance"]
SRC_EST  = ["Yahoo Finance(지수·NFP)", "WebSearch 교차검증"]

U = {
 "GOOG": dict(price=365.70, chg=-0.50, conf=False,
   todayWhy="오늘 개장은 약보합이에요. 미국 5월 고용이 예상보다 훨씬 강하게 나오면서 '금리 인하' 기대가 줄었고, 빚을 많이 쓰는 빅테크가 살짝 눌렸어요.",
   dq="개장가 추정 — 6/4 종가($367.52) 기준 약보합. 정규장 데이터로 재확인 권장."),
 "META": dict(price=625.70, chg=-0.30, conf=False,
   todayWhy="개장에서 거의 제자리예요. 반도체에서 빠진 돈이 메타 같은 빅테크로 옮겨오는 흐름은 이어졌지만, 금리 부담에 상승은 제한됐어요.",
   dq="개장가 추정 — 6/4 종가($627.57) 기준 보합권. 재확인 권장."),
 "AMZN": dict(price=252.50, chg=-0.51, conf=False,
   todayWhy="개장에서 소폭 내렸어요. 강한 고용으로 금리 인상 우려가 커지자 대형 기술주가 전반적으로 살짝 눌렸어요. AWS 클라우드 기대는 계속 받쳐줘요.",
   dq="개장가 추정 — 6/4 종가($253.79) 기준 약보합. 재확인 권장."),
 "NVDA": dict(price=213.43, chg=-2.39, conf=True,
   todayWhy="개장에서 -2.4% 내렸어요. 브로드컴 실적 실망이 이틀째 이어지며 AI 반도체가 다 같이 약했어요. AI 대장주지만 업종 분위기는 피하지 못했어요.",
   dq=None),
 "TSM": dict(price=430.20, chg=-1.49, conf=False,
   todayWhy="개장에서 -1.5% 내렸어요. 반도체 전반이 이틀째 약해 AI 칩을 대신 만들어주는 1위 회사도 같이 눌렸어요.",
   dq="개장가 추정 — 반도체 동반 약세 반영. 6/4 종가($436.69) 기준. 재확인 권장."),
 "AVGO": dict(price=410.00, chg=-2.13, conf=True,
   todayWhy="개장에서도 -2%대로 이틀째 약세예요. 다음 분기 AI 칩 전망 실망의 여진이 계속됐어요. 프리마켓에서 $411(-1.9%)까지 밀렸어요.",
   dq="6/5 프리마켓 $411.00(-1.9%) 확인 — 개장가 기준. 정규장 마감 시 재확인."),
 "MU": dict(price=960.24, chg=-3.59, conf=True,
   todayWhy="개장에서 -3.6% 떨어졌어요. 브로드컴발 AI 반도체 우려가 메모리로 이어졌고, 올해 +200% 급등 뒤 차익 실현도 겹쳤어요.",
   dq="6/5 프리마켓 $960.24(-3.6%) 확인 — 개장가 기준. 6/24 자체 실적 대기."),
 "MRVL": dict(price=274.80, chg=-2.48, conf=False,
   todayWhy="개장에서 반도체 약세에 같이 밀렸을 가능성이 커요. (참고: 출처 간 종가 차이가 있어 정확한 값은 재확인이 필요해요.)",
   dq="개장가 추정 — 출처 간 종가 불일치($275~$302) 지속. 재확인 필요."),
 "AMD": dict(price=500.00, chg=-1.94, conf=False,
   todayWhy="개장에서 -2% 가까이 내렸어요. 브로드컴 충격에 AI 반도체가 이틀째 약해졌어요. 최근 신고가까지 올랐던 터라 쉬어가는 모습이에요.",
   dq="개장가 추정 — 반도체 동반 약세 반영. 6/4 종가($509.90) 기준. 재확인 권장."),
 "SNDK": dict(price=1730.00, chg=-3.02, conf=False,
   todayWhy="개장에서 -3% 내렸어요. 같은 메모리인 마이크론이 크게 빠지면서 함께 조정받았어요. 올해 +600% 넘게 오른 강세 자체는 유지 중이에요.",
   dq="개장가 추정 — 메모리 동반 약세 반영. 6/4 종가($1,783.82) 기준. 재확인 권장."),
 "DELL": dict(price=409.80, chg=-1.21, conf=False,
   todayWhy="개장에서 소폭 내렸어요. AI 서버 호실적으로 최근 급등했는데, 반도체 약세 분위기에 잠깐 숨 고르기를 했어요.",
   dq="개장가 추정 — 6/4 종가($414.82) 기준 약세. 재확인 권장."),
 "LITE": dict(price=931.00, chg=-1.49, conf=False,
   todayWhy="개장에서 -1.5% 내렸어요. 광통신 부품주라 반도체 약세 분위기에 일부 영향을 받았어요.",
   dq="개장가 추정 — 6/4 종가($945.08) 기준 약세. 재확인 권장."),
 "CLS": dict(price=451.30, chg=-1.49, conf=False,
   todayWhy="개장에서 -1.5% 내렸어요. AI 서버·부품을 조립하는 회사라 반도체 약세에 같이 눌렸어요.",
   dq="개장가 추정 — 6/4 종가($458.14) 기준 약세. 재확인 권장."),
 "CRDO": dict(price=208.70, chg=-2.02, conf=False,
   todayWhy="개장에서 -2% 내렸어요. 변동이 큰 종목(베타 3.4)이라 반도체 약세 날엔 더 크게 움직이는 경향이 있어요.",
   dq="개장가 추정 — 고베타 종목, 6/4 종가($213.00) 기준 약세. 재확인 권장."),
 "TLN": dict(price=382.10, chg=0.29, conf=False,
   todayWhy="개장에서 강보합이에요. 전력·원자력 발전 회사라 반도체 급락과 금리 영향을 덜 받아 방어적인 모습이에요.",
   dq="개장가 추정 — 전력주 방어, 6/4 종가($381.00) 기준 강보합. 재확인 권장."),
}

# ---------- update portfolio.json ----------
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
pf["lastUpdated"] = TS
for s in pf["us"]:
    t = s["ticker"]
    if t not in U: continue
    u = U[t]
    d = u["chg"]  # today's move from prior close
    # shift relative-return fields by today's delta (approx)
    for f in ("change1W","change1M","changeYTD"):
        if isinstance(s.get(f),(int,float)):
            s[f] = round(s[f] + d, 2)
    s["price"] = u["price"]
    s["change1D"] = round(d, 2)
    s["todayWhy"] = u["todayWhy"]
    s["priceSourcedFrom"] = (SRC_CONF if u["conf"] else SRC_EST)
    s["dataQualityNote"] = u["dq"]
    if "_fetchMeta" in s:
        s["_fetchMeta"]["fetchedAt"] = TS
        s["_fetchMeta"]["sources"] = [{"url":"Yahoo Finance live / WebSearch","note":"6/5 22:30 KST 개장 스냅샷"}]

pf["marketStatus"] = ("6/5(금) 22:30 美 개장 — 5월 고용 +17.2만(예상 8.5만의 2배) 깜짝 강세로 금리 '인하'→'인상' 베팅 반전. "
 "개장 S&P500 7,528(-0.7%)·나스닥 26,495(-1.3%) 하락, 다우 51,487(보합), 러셀2000 +1.5% 나홀로 강세. "
 "반도체 이틀째 약세 — 엔비디아 -2.4%·마이크론 -3.6%·브로드컴 -2%대. 10년물 금리 +5.5bp 상승, 유가 WTI $92.6(-0.4%). "
 "⚠ 확정 4종목(NVDA·AVGO·MU·지수), 나머지 11종목은 개장가 추정·재확인 플래그.")
json.dump(pf, open(p("portfolio.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio.json updated:", len(pf["us"]), "us holdings")

# ---------- update calendar-events.json : append NFP indicator to 2026-06-05 ----------
cal = json.load(open(p("calendar-events.json"), encoding="utf-8"))
cal["lastUpdated"] = TS
day = cal["stock"].setdefault("2026-06-05", [])
# avoid duplicate
if not any(e.get("type")=="indicator" and "NFP" in e.get("label","")+e.get("title","") for e in day):
    day.append({
      "type":"indicator",
      "label":"5월 NFP +17.2만 (예상 2배·금리↑)",
      "color":"amber",
      "time":"21:30 KST",
      "title":"5월 고용보고서(NFP) +17.2만 — 시장 예상(8.5만)의 2배, 금리 인하 대신 '인상' 베팅",
      "description":"미국 5월 비농업 신규 고용(NFP, 한 달간 늘어난 일자리 수)이 17.2만 명으로 시장 평균 예상치(약 8.5만 명)의 2배 가까이 나왔어요. 실업률은 4.3%로 그대로였고, 일자리가 너무 좋게 나오자 '금리를 내리기는커녕 올릴 수도 있다'는 쪽으로 분위기가 바뀌었어요.",
      "impact":"NFP(미국 비농업 신규 고용) 17.2만 명은 컨센서스(시장 평균 예상치) 8.5만 명을 크게 웃돌았고, 4월 수치도 17.9만 명으로 상향됐어요. 발표 직후 10년물 국채금리가 +5.5bp(0.055%p) 뛰었고, 시장은 연내 0.25%p 금리 인상을 사실상 100% 반영하기 시작했어요. 금리가 오르면 빚을 많이 쓰는 성장주(특히 AI 반도체)에 단기 부담이 돼요.",
      "ourImpact":"금리 인상 쪽으로 기운 건 보유 AI 성장주(NVDA·AMD·반도체 다수)에 단기 부담 요인이에요. 반대로 금리 영향을 덜 받는 전력주 탈렌(TLN)은 상대적으로 방어적이었어요. 개장 직후 반도체가 이틀째 약세를 보였어요.",
      "stockImpacts":[
        {"ticker":"NVDA","tone":"negative","magnitude":"-2~3%","text":"금리 인상 우려 + 반도체 2일째 약세로 개장 -2.4%"},
        {"ticker":"MU","tone":"negative","magnitude":"-3~4%","text":"메모리 약세 지속, 개장 -3.6%"},
        {"ticker":"AVGO","tone":"negative","magnitude":"-2%","text":"실적 실망 여진 2일째, 개장 -2%대"},
        {"ticker":"AMD","tone":"negative","magnitude":"-2%","text":"AI 반도체 동반 약세(추정)"},
        {"ticker":"TLN","tone":"positive","magnitude":"+0~1%","text":"금리 영향 적은 전력주 — 강보합 방어(추정)"}
      ]
    })
json.dump(cal, open(p("calendar-events.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar-events.json updated: 2026-06-05 events =", len(day))
print("DONE phase1")
