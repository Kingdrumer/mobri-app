# -*- coding: utf-8 -*-
import json, io

TS = "2026-08-04T15:45:00+09:00"

# ---------- 1) reports/2026-08-04.json ----------
rp = "reports/2026-08-04.json"
d = json.load(io.open(rp, encoding="utf-8"))

d["lastUpdated"] = TS

# asiaSummary (신규)
d["asiaSummary"] = (
    "8/4(화) 한국 증시는 간밤 뉴욕 급등을 따라 코스피가 +1.5%(6,351.38) 갭상승(전날 종가보다 크게 점프)으로 출발했지만, "
    "삼성전자·SK하이닉스 등 반도체 대형주가 3~4%씩 밀리면서 상승분을 반납하고 약 6,100선(-1~2%대)으로 약세 마감했어요. "
    "지난주 급등한 반도체가 쉬어가자, 돈이 제약·바이오·로봇·방산 같은 코스닥 성장주로 옮겨가는 순환매가 나왔어요. "
    "그 덕에 코스닥은 +5%대 급등하며 3거래일 연속 매수 사이드카(급등 안정장치)가 발동됐어요(올해 30번째). "
    "외국인은 코스피에서 소폭 순매수했지만 기관이 팔면서 지수를 눌렀어요. "
    "일본 니케이225는 약 63,719(-1.0%)로 소폭 하락, 홍콩 항셍은 약 26,009(+0.5%)로 강보합 마감했어요. "
    "오늘 밤 미국 선물은 나스닥 선물(개장 전 분위기)이 반도체 약세로 약 -1.4% 밀린 상태예요. "
    "보유 종목 AMD가 미국장 마감 후 2분기 실적을 내는데, 옵션시장은 실적 뒤 ±8.5% 정도 큰 움직임을 예상하고 있어요."
)

# dataQualityNote 보강
d["dataQualityNote"] = (
    d.get("dataQualityNote","") +
    " [15:45 아시아 마감 캡처] 코스피/코스닥 마감 확정 수치는 마감 직후 미확정 구간이라 장중·근사치(approx)로 표기했어요. "
    "니케이·항셍은 Trading Economics 기준, 미국 선물은 실적 프리뷰 기사 기준이에요."
)

# 아시아 증시 마감 뉴스 갱신 (기존 placeholder IDX 교체)
asia_close_news = {
    "category": "아시아 증시",
    "impact": "neutral",
    "headline": "코스피 반도체 조정에 약세 반전·코스닥 +5%대 사이드카",
    "oneLineSummary": (
        "8/4 코스피는 간밤 뉴욕 강세를 따라 +1.5% 높게 출발했지만, 삼성전자·SK하이닉스 같은 반도체 대형주가 3~4%씩 "
        "밀리면서 상승분을 반납하고 약 6,100선(-1~2%대)으로 약세 마감했어요. 반대로 돈이 제약·바이오·로봇으로 옮겨간 "
        "코스닥은 +5%대 급등하며 3거래일 연속 매수 사이드카(급등 안정장치)가 나왔어요."
    ),
    "summary": (
        "8/4 코스피는 +1.50%(6,351.38) 갭상승 출발 후 반도체 대형주(삼성전자·SK하이닉스 -3~4%) 차익실현에 "
        "상승분을 반납, 약 6,100선(-1~2%대)으로 약세 마감했습니다(전일 종가 6,257.45). 외국인은 코스피에서 소폭 순매수했으나 "
        "기관 순매도가 지수를 눌렀습니다. 반면 코스닥은 반도체→성장주 순환매로 +5%대 급등, 3거래일 연속 매수 사이드카가 "
        "발동(올해 30번째)됐고 제약·바이오·로봇·방산이 상승을 주도했습니다. 니케이225 약 63,719(-1.0%), 항셍 약 26,009(+0.5%)."
    ),
    "ourImpact": (
        "한국 반도체(삼성전자·SK하이닉스)의 조정은 지난주 급등에 따른 되돌림 성격이라, 우리 미국 반도체 보유주(NVDA·AVGO·MU·MRVL)에도 "
        "오늘 밤 프리마켓(정규장 전 거래) 분위기가 조금 무거울 수 있어요. 실제로 나스닥 선물이 -1.4%가량 밀렸고, 오늘 밤 AMD 실적이 나오니 "
        "가격 흐름만 가볍게 지켜보면 좋아요."
    ),
    "sources": [
        {"name":"뉴스핌(코스닥 사이드카)","url":"https://www.newspim.com/news/view/20260804000579"},
        {"name":"파이낸셜뉴스(코스피 6100선)","url":"https://www.fnnews.com/news/202608041004290726"}
    ]
}

replaced = False
for i,n in enumerate(d["news"]):
    if n.get("category")=="아시아 증시" and ("갭상승" in n.get("headline","") or "코스피" in n.get("headline","")):
        d["news"][i] = asia_close_news
        replaced = True
        break
if not replaced:
    # prepend
    d["news"].insert(0, asia_close_news)

json.dump(d, io.open(rp,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("report updated. news cats:", [n['category'] for n in d['news']], "asiaSummary set:", 'asiaSummary' in d)

# ---------- 2) portfolio.json ----------
pp = "portfolio.json"
p = json.load(io.open(pp, encoding="utf-8"))
had_memo = "userMemo" in p
p["lastUpdated"] = TS
p["asiaCloseSnapshot"] = {
    "asOf": TS,
    "intraday": True,
    "koreaHoliday": False,
    "kospi": {
        "level": "약 6,100선(-1~2%대)",
        "change": "-약 1.8%",
        "approx": True,
        "prevClose": "6,257.45",
        "note": "코스피 +1.50%(6,351.38) 갭상승 출발 후 삼성전자·SK하이닉스 등 반도체 대형주 3~4% 차익실현에 상승분 반납, 약 6,100선 약세 마감. 외국인 소폭 순매수·기관 순매도. 마감 확정 수치는 15:45 캡처 시점 미확정(근사치)."
    },
    "kosdaq": {
        "level": "약 775선(+5%대)",
        "change": "+약 5%",
        "approx": True,
        "prevClose": "737.35",
        "note": "반도체→제약·바이오·로봇·방산 순환매로 +5%대 급등. 3거래일 연속 매수 사이드카 발동(올해 30번째). 코스닥150 +6.5%."
    },
    "asiaIndices": {
        "nikkei": {"level":"약 63,719","change":"-1.0%","approx":True,"note":"니케이225 — 반도체 약세 속 소폭 하락 마감(Trading Economics 기준)."},
        "hangseng": {"level":"약 26,009","change":"+0.5%","approx":True,"note":"항셍 — 강보합 마감."},
        "csi300": {"level":None,"change":None,"approx":True,"note":"상해종합 — 8/4 마감 확정 수치 미확정."},
        "taiwan": {"level":"조정 흐름","change":None,"approx":True,"note":"대만 가권 — TSMC 등 대형주 차익실현 조정 흐름. 마감 확정 수치 미확정."}
    },
    "usFutures": {
        "es": "소폭 약세",
        "nq": "약 -1.4%(약세)",
        "note": "나스닥 선물(개장 전 분위기)이 반도체 약세로 약 -1.4% 하락. 오늘 밤 미국장은 AMD 2분기 실적(장 마감 후)과 주 후반 고용지표 대기. AMD 옵션시장은 실적 뒤 ±8.5% 변동 예상."
    }
}
json.dump(p, io.open(pp,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio updated. userMemo preserved/absent:", had_memo, "userMemo still:", 'userMemo' in p)

# ---------- 3) calendar-events.json ----------
cp = "calendar-events.json"
c = json.load(io.open(cp, encoding="utf-8"))
c["lastUpdated"] = TS
day = c["stock"].setdefault("2026-08-04", [])
# 중복 방지: label '아시아 마감' 이미 있으면 교체
asia_evt = {
    "type": "asia",
    "label": "아시아 마감",
    "color": "blue",
    "mood": "🟡",
    "time": "15:45 KST 라이트",
    "title": "🟡 아시아 마감 캡처(8/4 화 15:45) — 코스피 반도체 조정에 약세(약 6,100선)·코스닥 +5%대 사이드카 / 니케이 -1.0%·항셍 +0.5%",
    "description": "8/4 코스피는 +1.5% 갭상승 출발 후 삼성전자·SK하이닉스 등 반도체 대형주가 3~4% 밀리며 상승분을 반납, 약 6,100선(-1~2%대) 약세 마감했어요. 돈이 제약·바이오·로봇으로 옮겨간 코스닥은 +5%대 급등해 3거래일 연속 매수 사이드카(올해 30번째)가 발동됐어요. 외국인은 코스피에서 소폭 순매수, 기관은 순매도였어요. 니케이225 약 63,719(-1.0%)·항셍 약 26,009(+0.5%).",
    "impact": "neutral",
    "ourImpact": "한국 반도체 조정은 지난주 급등 되돌림 성격이에요. 오늘 밤 나스닥 선물이 -1.4%가량 밀린 상태라 미국 반도체 보유주(NVDA·AVGO·MU·MRVL) 프리마켓 분위기가 다소 무거울 수 있어요. 오늘 밤 AMD 실적(장 마감 후)이 다음 변수예요.",
    "stockImpacts": "삼성전자·SK하이닉스 -3~4%(반도체 차익실현) → 미국 반도체 보유주 프리마켓 참고 신호 / AMD: 오늘 밤 실적 대기(옵션시장 ±8.5% 예상)"
}
day[:] = [e for e in day if e.get("label")!="아시아 마감"]
day.append(asia_evt)
json.dump(c, io.open(cp,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar updated. 8/4 events:", [e.get('label') for e in c['stock']['2026-08-04']])
