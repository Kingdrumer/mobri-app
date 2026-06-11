#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, shutil, datetime, os

BASE = "/sessions/inspiring-epic-pascal/mnt/claude/portfolio-pwa/data"
PF = os.path.join(BASE, "portfolio.json")

# backup
shutil.copy(PF, PF + ".before-us-open-0611.bak")

now_kst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
iso = now_kst.strftime("%Y-%m-%dT%H:%M:%S+09:00")

# ticker -> (prevClose_6_10, today_quote, quote_kind)
# fresh = real 6/11 live/premarket; stale = 6/10 close only (cache lag)
DATA = {
 "GOOG": dict(prev=353.32, px=356.15, kind="pre",   note="프리마켓 04:14 ET 호가"),
 "META": dict(prev=570.98, px=563.14, kind="live",  note="정규장 개장 직후 09:35 ET"),
 "AMZN": dict(prev=238.00, px=240.12, kind="pre",   note="프리마켓 06:06 ET 호가"),
 "NVDA": dict(prev=200.42, px=201.69, kind="live",  note="정규장 개장 직후 09:37 ET"),
 "TSM":  dict(prev=408.75, px=412.30, kind="pre",   note="프리마켓 09:14 ET 호가"),
 "AVGO": dict(prev=372.10, px=370.69, kind="pre",   note="프리마켓 09:17 ET 호가"),
 "MU":   dict(prev=891.88, px=910.00, kind="pre",   note="프리마켓 09:14 ET 호가"),
 "MRVL": dict(prev=252.59, px=265.16, kind="pre",   note="프리마켓 09:14 ET 호가"),
 "AMD":  dict(prev=452.40, px=461.10, kind="pre",   note="프리마켓 09:13 ET 호가"),
 "SNDK": dict(prev=1643.23, px=1702.02, kind="pre", note="프리마켓 09:11 ET 호가"),
 "LITE": dict(prev=853.26, px=865.35, kind="pre",   note="프리마켓 08:45 ET 호가"),
 # stale (6/11 개장가 미확보 — CNBC/Yahoo/stockanalysis 캐시 지연, 6/10 종가 기준)
 "DELL": dict(prev=381.78, px=369.83, kind="stale", note="6/11 개장가 미확보 — 6/10 종가 기준(프리마켓 강세 보도). 차기 캡처 시 갱신"),
 "CLS":  dict(prev=371.86, px=361.60, kind="stale", note="6/11 개장가 미확보 — 6/10 종가 기준"),
 "CRDO": dict(prev=234.32, px=237.68, kind="stale", note="6/11 개장가 미확보 — 6/10 종가 기준(시간외 233.00 약세)"),
 "TLN":  dict(prev=358.74, px=336.59, kind="stale", note="6/11 개장가 미확보 — 6/10 종가 기준(시간외 330.79 약세)"),
}

# todayWhy (쉬운 한국어, 카톡 톤)
WHY = {
 "GOOG": "어제 물가 충격에 빠졌던 빅테크가 오늘은 진정세예요. 구글은 프리마켓에서 +0.8% 살짝 반등하며 개장했어요.",
 "META": "메타는 오늘 시장 반등 속에서도 홀로 약했어요. 개장 직후 -1.4%. AI 경쟁에서 뒤처진다는 우려와 구독 사업 의문이 발목을 잡았어요.",
 "AMZN": "아마존은 +0.9%로 반등 출발. AI 투자용으로 175억 달러를 추가로 빌렸다는 소식이 있었지만 시장 분위기가 좋아 같이 올랐어요.",
 "NVDA": "엔비디아는 +0.6%로 반등하며 개장. 오라클이 AI 데이터센터에 돈을 더 쓴다고 해서 'GPU 수요는 여전하다'는 안도감이 돌았어요.",
 "TSM": "TSMC는 +0.9% 반등 출발. 어제 -4.5% 급락분을 일부 되돌렸어요. 5월 매출도 30% 늘며 견조했어요.",
 "AVGO": "브로드컴은 -0.4%로 소폭 약세 출발. 반도체가 전반적으로 반등하는 가운데 실적 우려가 남아 상대적으로 무거웠어요.",
 "MU": "마이크론은 +2.0% 반등 출발. 'AI 메모리 공급 부족이 오래 간다'는 분석에 목표가가 줄줄이 올랐어요(울프리서치 1,250달러).",
 "MRVL": "마벨은 +5.0%로 보유 종목 중 가장 강하게 반등 출발. S&P500 편입 효과와 AI 네트워크 수요 기대가 겹쳤어요.",
 "AMD": "AMD는 +1.9% 반등 출발. 오라클의 AI 투자 확대가 'AMD 칩 수요도 좋다'는 기대로 이어졌어요.",
 "SNDK": "샌디스크는 +3.6%로 강하게 반등 출발. NAND 메모리 공급 부족 수혜 기대와 목표가 상향이 이어졌어요.",
 "LITE": "루멘텀은 +1.4% 추가 상승 출발. 어제도 +3.8% 오른 광통신 강세가 이어졌어요. AI 데이터센터 광부품 수요 덕분이에요.",
 "DELL": "델은 6/11 개장가를 아직 못 잡았어요(데이터 지연). 다만 오라클 호실적·xAI 주문설로 프리마켓에서 강세였다는 보도가 있어요.",
 "CLS": "셀레스티카는 6/11 개장가 미확보(데이터 지연). 6/10 종가 기준 -2.8%였고, AI 서버 위탁생산 수요는 견조해요.",
 "CRDO": "크레도는 6/11 개장가 미확보(데이터 지연). 6/10엔 +1.4%였지만 시간외에서 -2.0%로 눌렸어요.",
 "TLN": "탈렌에너지는 6/11 개장가 미확보(데이터 지연). 이란 공습 종료로 유가가 내리면서 전력주에는 부담이 있었어요.",
}

def sig(ch, stale=False):
    if ch is None: return "yellow"
    if ch >= 1.5: return "green"
    if ch <= -1.0: return "red"
    return "yellow"

d = json.load(open(PF, encoding="utf-8"))

report = []
for s in d["us"]:
    t = s["ticker"]
    if t not in DATA:
        report.append(f"{t}: SKIP (no data)")
        continue
    info = DATA[t]
    p0 = s["price"]          # prior portfolio price (used to derive historical bases)
    o1w, o1m, oytd = s.get("change1W"), s.get("change1M"), s.get("changeYTD")
    newpx = info["px"]
    prev = info["prev"]
    ch1d = round((newpx/prev - 1)*100, 2)
    # derive historical bases from prior price/percent, then recompute vs new price
    def recompute(prior_pct):
        if prior_pct is None: return None
        base = p0/(1+prior_pct/100.0)
        return round((newpx/base - 1)*100, 1)
    n1w = recompute(o1w)
    n1m = recompute(o1m)
    nytd = recompute(oytd)
    s["price"] = newpx
    s["change1D"] = ch1d
    if n1w is not None: s["change1W"] = n1w
    if n1m is not None: s["change1M"] = n1m
    if nytd is not None: s["changeYTD"] = nytd
    s["signal"] = sig(ch1d, info["kind"]=="stale")
    s["todayWhy"] = WHY[t]
    s["priceSourcedFrom"] = ["stockanalysis.com", "Yahoo"]
    if info["kind"] == "stale":
        s["dataQualityNote"] = "⚠️ " + info["note"]
    elif info["kind"] == "pre":
        s["dataQualityNote"] = "프리마켓 호가 기준(정규장 개장 직후) — " + info["note"]
    else:
        s["dataQualityNote"] = None
    report.append(f"{t}: ${newpx} 1D={ch1d:+.2f}% 1W={s.get('change1W')} 1M={s.get('change1M')} YTD={s.get('changeYTD')} sig={s['signal']} [{info['kind']}]")

# marketStatus 갱신 (개장 스냅샷)
d["marketStatus"] = ("🟢 美 증시 반등 출발 — 어제 CPI 쇼크·이란 공습 급락 뒤, 미군이 이란 공습을 '완료'했다고 밝히며 위험자산 선호 회복. "
 "S&P500 약 7,306(+0.5%)·나스닥 100 선물 +1.2%·VIX 20.8(-6%)로 진정. 오라클의 대규모 AI 데이터센터 투자(약 700억$) 발표로 반도체·AI 하드웨어 반등 주도 "
 "(MRVL +5.0%·SNDK +3.6%·MU +2.0%·AMD +1.9%). 단, 5월 PPI(생산자물가)가 전월비 +1.1%·전년비 6.5%로 2022년 11월 이후 최고치를 기록해 인플레 부담은 잔존. "
 "오라클은 클라우드 매출 부진+차입 부담으로 -10% 급락. 유가는 이란 공습 종료로 하락 전환, 금 약세.")

# meta
d["lastUpdated"] = iso
d["marketSession"] = "US_OPEN"

json.dump(d, open(PF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("UPDATED", PF)
print("lastUpdated:", iso)
print("\n".join(report))
