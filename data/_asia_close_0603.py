# -*- coding: utf-8 -*-
import json, io

asOf = "2026-06-03T15:45:00+09:00"

# ---------- 1. report 2026-06-03.json ----------
rp = "reports/2026-06-03.json"
r = json.load(open(rp, encoding="utf-8"))

r["asiaSummary"]["asOf"] = asOf
r["asiaSummary"]["asia"] = {
    "nikkei": "+2.57% 68,452.45",
    "hangSeng": "-1.38% 25,677.91",
    "csi300": "상하이종합 +0.19% 4,082.66",
    "taiwan": "+1.82% 46,386.84",
    "note": "6/3(수) 아시아: 일본·대만 반도체 급등 vs 홍콩 약세(중국-일본 긴장). 한국은 지방선거 휴장."
}
r["asiaSummary"]["kospi"]["note"] = "6/3(수) 지방선거 휴장 — 한국 증시 미개장. 직전 거래일(6/2) +0.15% 8,801.49 사상 최고. 다음 거래일 6/4(목)."

asia_news = {
    "category": "아시아 증시",
    "headline": "아시아 마감 — 니케이 +2.6% 급등·대만 +1.8% 반도체 강세 / 홍콩 -1.4%",
    "oneLineSummary": "오늘 일본 니케이가 +2.6%(68,452) 크게 오르고 대만 증시도 +1.8% 뛰면서 아시아 반도체·AI 종목이 강하게 마감했어요. 반대로 홍콩 항셍은 중국-일본 갈등 우려로 -1.4% 내렸고, 중국 상하이는 +0.2% 강보합이었어요. 한국은 지방선거로 오늘 하루 휴장이라 거래가 없었어요.",
    "summary": "6/3(수) 아시아 증시는 일본·대만 강세 vs 홍콩 약세로 엇갈렸습니다. 니케이225 +2.57%(+1,718.21p) 68,452.45로 지역 최고 성과, 대만 가권 +1.82% 46,386.84, 상하이종합 +0.19% 4,082.66, 선전 +1.64%로 마감했습니다. 반면 홍콩 항셍은 중국-일본 지정학 긴장 우려로 -1.38%(-360.41p) 25,677.91로 지역 최약세였습니다. 한국은 제9회 전국동시지방선거로 휴장(직전 6/2 코스피 8,801.49). 미국 야간 선물은 사상 최고 마감 뒤 보합권에서 움직였습니다.",
    "ourImpact": "일본·대만 반도체 급등은 보유 칩 종목(NVDA·TSM·AVGO·MU·MRVL·AMD)에 좋은 신호예요. 특히 대만 강세는 보유 종목 TSM(대만 TSMC)과 직결돼요. 오늘 밤 미국 프리마켓 출발이 우호적일 가능성이 있어 가볍게 지켜보면 좋아요.",
    "impact": "positive",
    "sources": [
        {"name": "Business Upturn (6/3)", "url": "https://www.businessupturn.com/finance/stock-market/asian-markets/asia-markets-today-june-3-nikkei-surges-over-2-57-taiex-gains-nearly-2-hang-seng-falls"},
        {"name": "SCMP (6/3)", "url": "https://www.scmp.com/business/china-business/article/3338982/hong-kong-stocks-strong-2026-start-loses-steam-rising-china-japan-tensions"}
    ]
}

# remove prior 아시아 증시 Korea-휴장 placeholder if it duplicates, keep max 2 in category
news = r.get("news", [])
# prepend asia close; keep existing korea-휴장 item (limit category to 2)
asia_existing = [n for n in news if n.get("category") == "아시아 증시"]
others = [n for n in news if n.get("category") != "아시아 증시"]
new_asia = [asia_news] + asia_existing[:1]  # max 2
r["news"] = new_asia + others
r["lastUpdated"] = asOf
json.dump(r, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("report updated. news count:", len(r["news"]))

# ---------- 2. portfolio.json ----------
pp = "portfolio.json"
p = json.load(open(pp, encoding="utf-8"))
p["asiaCloseSnapshot"] = {
    "asOf": asOf,
    "kospi": {"close": None, "change": None, "changePoints": None,
              "note": "6/3(수) 지방선거 휴장 — 미개장. 직전 6/2 +0.15% 8,801.49 사상 최고. 다음 거래일 6/4(목)."},
    "kosdaq": {"close": None, "change": None, "changePoints": None,
               "note": "6/3 휴장. 직전 1,050선 부근."},
    "asiaIndices": {
        "nikkei": {"close": 68452.45, "change": 2.57, "changePoints": 1718.21,
                   "note": "일본 니케이 +2.57% 68,452.45 — 지역 최고 성과, AI·반도체 강세."},
        "taiwan": {"close": 46386.84, "change": 1.82, "changePoints": 829.53,
                   "note": "대만 가권 +1.82% 46,386.84 — TSMC 등 반도체 급등."},
        "shanghai": {"close": 4082.66, "change": 0.19, "changePoints": 7.56,
                     "note": "상하이종합 +0.19% 4,082.66 강보합 / 선전 +1.64%."},
        "hangSeng": {"close": 25677.91, "change": -1.38, "changePoints": -360.41,
                     "note": "홍콩 항셍 -1.38% 25,677.91 — 중국-일본 긴장 우려로 지역 최약세."}
    },
    "usdkrw": 1508.0,
    "samsung": {"change": None, "note": "6/3 휴장. 직전 +3.3% 360,500원 신고가."},
    "skHynix": {"change": None, "note": "6/3 휴장. 직전 -0.13% 약보합."},
    "usFutures": {"es": None, "esChange": None, "nq": None, "nqChange": None,
                  "note": "美 3대 지수 사상 최고(6/2) 마감 뒤 야간 선물 보합권. 일본·대만 반도체 강세로 프리마켓 우호적 출발 가능성. 22:30 KST 개장 대기."}
}
p["marketStatus"] = ("6/3(수) 15:45 KST 아시아 마감 캡처 — 한국은 제9회 지방선거로 휴장이라 거래가 없었어요. "
    "일본 니케이가 +2.6%(68,452) 크게 오르고 대만 증시도 +1.8% 뛰며 아시아 반도체·AI가 강하게 마감했어요. "
    "특히 대만 강세는 보유 종목 TSM(대만 TSMC)과 직결돼요. 반대로 홍콩 항셍은 중국-일본 갈등 우려로 -1.4% 내렸고, "
    "중국 상하이는 +0.2% 강보합이었어요. 미국은 간밤 3대 지수가 사상 최고로 마감했고 야간 선물은 보합권이라, "
    "오늘 밤 미국 프리마켓 출발이 우호적일 가능성이 있어 보유 반도체주 흐름을 가볍게 지켜보면 좋아요.")
p["lastUpdated"] = asOf
json.dump(p, open(pp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio updated.")

# ---------- 3. calendar-events.json ----------
cp = "calendar-events.json"
c = json.load(open(cp, encoding="utf-8"))
day = c["stock"].get("2026-06-03", [])
asia_event = {
    "type": "asia",
    "label": "아시아 마감",
    "color": "blue",
    "mood": "🟢",
    "time": "15:45 KST 캡처",
    "title": "🔵 아시아 마감 — 니케이 +2.6%·대만 +1.8% 반도체 급등 / 홍콩 -1.4%, 한국은 지방선거 휴장",
    "description": ("6/3(수) 아시아 증시는 일본·대만 강세 vs 홍콩 약세로 엇갈렸어요. 일본 니케이가 +2.57%(68,452.45) 크게 올라 "
        "지역에서 가장 강했고, 대만 가권도 +1.82%(46,386.84) 뛰며 반도체·AI 종목이 장을 끌었어요. 중국 상하이는 +0.19%(4,082.66) 강보합, "
        "선전은 +1.64%였어요. 반대로 홍콩 항셍은 중국-일본 갈등 우려로 -1.38%(25,677.91) 내려 지역에서 가장 약했어요. "
        "한국은 제9회 전국동시지방선거로 오늘 하루 휴장이라 거래가 없었어요(직전 6/2 코스피 8,801.49 사상 최고)."),
    "impact": "아시아 반도체 강세 — 미국 프리마켓에 우호적 신호.",
    "ourImpact": "일본·대만 반도체 급등은 보유 칩 종목(NVDA·TSM·AVGO·MU·MRVL·AMD)에 좋은 신호예요. 특히 대만 강세는 보유 종목 TSM과 직결돼요. 오늘 밤 미국장 출발을 가볍게 지켜보면 좋아요.",
    "stockImpacts": [
        {"ticker": "TSM", "note": "대만 가권 +1.82% — TSMC 본거지 강세, 직접 수혜"},
        {"ticker": "NVDA", "note": "아시아 AI·반도체 동반 강세로 프리마켓 우호적 분위기"},
        {"ticker": "AVGO", "note": "아시아 반도체 모멘텀 연장 — 우호적 신호"}
    ],
    "sources": [
        {"name": "Business Upturn (6/3)", "url": "https://www.businessupturn.com/finance/stock-market/asian-markets/asia-markets-today-june-3-nikkei-surges-over-2-57-taiex-gains-nearly-2-hang-seng-falls"}
    ]
}
c["stock"]["2026-06-03"] = [asia_event] + day
c["lastUpdated"] = asOf
json.dump(c, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar updated. 6/3 events:", len(c["stock"]["2026-06-03"]))
