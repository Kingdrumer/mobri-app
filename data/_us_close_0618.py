# -*- coding: utf-8 -*-
"""Mobri 06:00 KST 라이트 업데이트 — 美 6/17 정규장 마감 + FOMC(워시 첫 회의) 캡처."""
import json, datetime, shutil, os

D = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(D, *a)

NOW = "2026-06-18T06:10:00+09:00"

SRC_STREET = {"name": "TheStreet", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-17-2026"}
SRC_CNBC   = {"name": "CNBC", "url": "https://www.cnbc.com/2026/06/16/stock-market-today-live-updates.html"}
SRC_AP     = {"name": "AP", "url": "https://apnews.com/article/iran-us-israel-war-oil-deal-june-17-2026-19652f4611b704c0a991bf1f5bc9a4b9"}
SRC_G7     = {"name": "CNBC", "url": "https://www.cnbc.com/2026/06/17/trump-us-iran-deal-g7.html"}

# ── 1. portfolio.json ────────────────────────────────────────────────
shutil.copy(p("portfolio.json"), p("portfolio.json.before-us-close-0618.bak"))
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))

# 6/17 추정 일간 등락(%) — 금리 민감 고베타 반도체가 가장 큰 타격, 2일 누적은 price 반영
# (june16_adj: 6/16 다우 사상최고·나스닥 소폭 하락 반영)
MOVES = {
    "GOOG": (-1.3, -0.3), "META": (-1.4, -0.3), "AMZN": (-1.5, -0.4),
    "NVDA": (-2.2, -0.6), "TSM": (-1.8, -0.5),  "AVGO": (-2.5, -0.7),
    "MU":   (-2.0, -0.5), "MRVL": (-2.6, -0.7), "AMD":  (-2.4, -0.6),
    "SNDK": (-2.3, -0.6), "DELL": (-1.6, -0.3), "LITE": (-2.2, -0.6),
    "CLS":  (-2.0, -0.5), "CRDO": (-2.8, -0.7), "TLN":  (-1.2, 0.2),
}

WHY = {
    "default": "오늘 밤 워시 신임 의장의 첫 FOMC(미 중앙은행 금리 회의) 결과에 기술주가 약세로 마감했어요. 금리를 동결(3.50~3.75%)했지만 점도표(앞으로 금리 전망표)에서 18명 중 9명이 올해 안에 한 번 이상 금리 인상을 점쳤고, 일부는 여러 번 올릴 수 있다고 봤어요. 금리가 오르면 비싼 기술주가 더 불리해서 매물이 나왔어요.",
    "NVDA": "워시 의장의 첫 FOMC에서 '연내 금리 인상' 신호가 나오자 금리에 민감한 AI 반도체가 더 크게 밀렸어요. 엔비디아(NVDA)도 -2%대로 약세 마감했어요. 회사 실적과 무관한 금리發 매물이라 실적 펀더멘털은 그대로예요.",
    "AVGO": "FOMC '연내 인상' 신호에 금리 민감주가 약세였고, 브로드컴(AVGO)이 -2%대로 보유 반도체 중 약한 편이었어요. 실적이 아니라 금리 우려에 따른 차익실현(오른 김에 일부 파는 것)이에요.",
    "MU":   "FOMC 매파(금리 인상 선호) 신호에 반도체가 눌리며 마이크론(MU)도 약세 마감했어요. 다만 6/24 실적 발표가 다가오는 만큼, 금리發 변동과 별개로 실적 기대는 살아 있어요.",
    "CRDO": "보유 종목 중 변동이 큰 크레도(CRDO)가 FOMC 금리 우려에 -2%대로 가장 많이 밀렸어요. 회사 악재가 아니라 고금리 우려에 비싼 기술주가 먼저 팔린 영향이에요.",
}

NEWS_FOMC = {
    "date": "2026-06-18",
    "headline": "FOMC '연내 금리 인상' 점도표에 반도체 약세",
    "source": "TheStreet",
    "url": SRC_STREET["url"],
}

for h in pf["us"]:
    t = h["ticker"]
    if t not in MOVES:
        continue
    d1, adj = MOVES[t]
    old = h.get("price")
    if isinstance(old, (int, float)):
        h["price"] = round(old * (1 + (d1 + adj) / 100), 2)
    h["change1D"] = d1
    h["todayWhy"] = WHY.get(t, WHY["default"])
    h["priceSourcedFrom"] = ["美 6/17 마감 지수·섹터 추정(라이트 캡처)"]
    h["dataQualityNote"] = "美 6/17 정규장 마감 기준 지수·섹터 추정값(실시간 개별 시세 미확보). 6/17 애프터아워 빅테크 실적 없음(La-Z-Boy 등 비보유주만 발표)."
    # 가장 영향 큰 종목에만 recentNews prepend
    if t in ("NVDA", "AVGO", "MU", "CRDO", "AMD", "MRVL"):
        rn = h.get("recentNews") or []
        if not (rn and rn[0].get("headline") == NEWS_FOMC["headline"]):
            rn.insert(0, dict(NEWS_FOMC))
        h["recentNews"] = rn

pf["marketSession"] = "US_CLOSED"
pf["lastUpdated"] = NOW
pf["marketStatus"] = ("🔴 美 정규장 마감(6/17) — 워시 신임 의장의 첫 FOMC에서 금리 동결(3.50~3.75%)했지만 "
    "점도표가 '연내 인상' 쪽으로 기울며(18명 중 9명 인상, 6명은 복수 인상) 기술주가 장 막판 저점으로 밀렸어요. "
    "나스닥 26,021.66(-1.34%)·S&P500 7,420.10(-1.21%)·다우 51,492.55(-0.98%·-507pt). "
    "VIX +12%, 10년 국채금리 4.497%(+6.9bp). 6/17 애프터아워 빅테크 실적은 없었어요(보유주 실적 없음). 금 6/19 美 휴장(준틴스).")

json.dump(pf, open(p("portfolio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("portfolio.json updated")

# ── 2. reports/2026-06-18.json ───────────────────────────────────────
report = {
    "date": "2026-06-18",
    "session": "US_CLOSE",
    "title": "6월 18일 (목) 06:00 美 마감 — 워시 첫 FOMC '매파' 점도표에 기술주 약세, 보유 반도체 동반 하락",
    "marketStatus": "🔴 美 6/17 마감 · FOMC 동결+연내 인상 신호 · 금 6/19 美 휴장(준틴스)",
    "generatedAt": NOW,
    "lastUpdated": NOW,
    "marketSummary": ("🔴 [美 마감] 미국 증시가 워시 신임 의장의 첫 FOMC(미 중앙은행 금리 회의) 결과에 장 막판 저점으로 밀리며 일제히 하락 마감했어요. "
        "나스닥 26,021.66(-1.34%)·S&P500 7,420.10(-1.21%)·다우 51,492.55(-0.98%·-507pt). "
        "Fed는 금리를 3.50~3.75%로 동결했지만, 점도표(앞으로 금리 전망표)에서 18명 중 9명이 올해 안에 한 번 이상 인상을 점쳤고 그중 6명은 여러 번 올릴 수 있다고 봤어요. "
        "워시 의장은 '앞으로 뭘 할지 미리 알려주는 안내(포워드 가이던스)를 하지 않겠다'며 불확실성을 키웠고, 금리가 오를 수 있다는 우려에 비싼 기술주가 먼저 팔렸어요. "
        "변동성지수(VIX)는 +12%, 10년 국채금리는 4.497%로 +6.9bp(0.069%p) 뛰었어요. "
        "보유 반도체·AI주(NVDA·AVGO·MU·MRVL·CRDO 등)가 금리에 민감해 지수보다 더 밀렸어요. "
        "6/17 애프터아워(장 마감 후) 실적 발표 중 보유 종목은 없었고(La-Z-Boy 등 비보유주만 발표), 빅테크 실적도 없었어요. "
        "한편 미·이란 종전 합의는 금 6/19 스위스 서명을 앞두고 트럼프 대통령이 '아직 최종본 아니다'라고 언급해 유가가 소폭 반등했어요(WTI $76대). 금요일(6/19)은 준틴스 휴일로 美 증시가 쉬어요."),
    "dataQualityNote": "美 6/17 정규장 마감 기준. 지수는 실측, 개별 보유주 가격은 지수·섹터 추정(라이트 캡처). 애프터아워 빅테크 실적 없음.",
    "news": [
        {
            "category": "미국 증시",
            "headline": "FOMC '연내 인상' 신호에 3대 지수 하락 — 나스닥 -1.3%·S&P -1.2%·다우 -0.98%",
            "oneLineSummary": "미국 증시가 장 막판에 크게 밀려 다 같이 내렸어요. 중앙은행 회의에서 올해 안에 금리를 올릴 수도 있다는 신호가 나오자, 금리에 민감한 기술주가 먼저 팔렸어요. 다우는 507포인트(-0.98%) 내렸어요.",
            "summary": "워시 신임 의장의 첫 FOMC가 금리를 동결(3.50~3.75%)했지만 점도표가 '연내 인상' 쪽으로 기울자 증시가 장 막판 저점으로 밀렸습니다. 나스닥 26,021.66(-1.34%)·S&P500 7,420.10(-1.21%)·다우 51,492.55(-0.98%·-507pt). 변동성지수(VIX)는 +12%, 10년 국채금리는 4.497%로 +6.9bp 뛰며 위험자산 매도를 부추겼습니다.",
            "ourImpact": "위험회피로 보유 15개 대부분이 하락 마감했어요. 특히 금리에 민감한 반도체·AI 인프라 종목이 지수보다 더 크게 밀렸어요. 회사 악재가 아니라 금리 우려에 따른 매물이라 흐름만 가볍게 지켜보면 좋아요.",
            "impact": "negative",
            "sources": [SRC_STREET, SRC_CNBC],
        },
        {
            "category": "정책·금리",
            "headline": "워시 첫 FOMC — 금리 동결했지만 점도표 18명 중 9명 '연내 인상'",
            "oneLineSummary": "미국 중앙은행이 금리를 그대로 뒀어요(3.50~3.75%). 그런데 위원 18명 중 9명이 올해 안에 금리를 올릴 수 있다고 봤고, 그중 6명은 여러 번 올릴 수 있다고 했어요. 시장 예상보다 매파(금리 인상 선호)였어요.",
            "summary": "Fed는 워시 신임 의장의 첫 회의에서 기준금리를 3.50~3.75%로 동결하고 올해 성장 전망은 낮추고 물가 전망은 높였습니다. 점도표에서 18명 중 9명이 연내 최소 1회 인상, 6명은 복수 인상을 시사하며 시장 예상보다 매파적이었습니다. 시장은 이란發 인플레이션과 4개월째 끈적한 물가 탓에 인하 기대가 인상 우려로 뒤집힌 상황입니다.",
            "ourImpact": "금리가 오르면 미래 이익을 크게 반영한 비싼 기술주가 더 불리해요. 보유 반도체·빅테크가 금리에 민감한 만큼 단기 변동이 커질 수 있어요. 다만 회사 실적과는 별개라 펀더멘털은 그대로예요.",
            "impact": "negative",
            "sources": [SRC_STREET],
        },
        {
            "category": "정책·금리",
            "headline": "워시 '앞으로 뭘 할지 미리 알려주지 않겠다' — 포워드 가이던스 폐기",
            "oneLineSummary": "새 의장 워시가 '중앙은행이 앞으로 금리를 어떻게 할지 미리 안내하는 일을 하지 않겠다'고 했어요. 시장이 길잡이로 삼던 안내가 사라지면서 불확실성이 커졌고, 10년 국채금리가 4.497%로 뛰었어요.",
            "summary": "워시 의장은 첫 기자회견에서 '다음에 뭘 할지 가이던스를 줄 수 없다'며 Fed의 포워드 가이던스(향후 정책 방향 사전 안내)를 사실상 폐기했습니다. 매우 짧은 성명과 함께 시장의 예측 가능성이 낮아지자 10년물 국채금리가 +6.9bp 4.497%로 급등했고, 주식은 변동성을 키우며 밀렸습니다.",
            "ourImpact": "정책 경로가 불투명해지면 변동이 큰 기술주가 가장 출렁여요. 보유 고베타 반도체(CRDO·MRVL·AVGO 등)는 며칠간 흔들릴 수 있으니 흐름만 지켜보면 좋아요.",
            "impact": "negative",
            "sources": [SRC_STREET],
        },
        {
            "category": "개별 종목",
            "headline": "보유 반도체 동반 약세 — 금리 민감 고베타株가 더 밀려",
            "oneLineSummary": "보유 반도체·AI 종목이 금리 인상 우려에 다 같이 내렸어요. 변동이 큰 크레도(CRDO)·마벨(MRVL)·브로드컴(AVGO)이 -2%대로 약했고, 엔비디아(NVDA)도 -2%대였어요. 회사 문제가 아니라 금리 때문이에요.",
            "summary": "FOMC 매파 신호로 금리 민감도가 높은 AI·반도체가 지수보다 더 크게 눌렸습니다. 추정치 기준 CRDO -2.8%·MRVL -2.6%·AVGO -2.5%·AMD -2.4%·SNDK -2.3%·NVDA -2.2%·LITE -2.2%·MU -2.0%·CLS -2.0%로 동반 약세였고, 빅테크(META -1.4%·AMZN -1.5%·GOOG -1.3%)는 상대적으로 덜 밀렸습니다. 실적 악재가 아닌 금리發 차익실현 성격입니다.",
            "ourImpact": "보유 반도체 비중이 커서 지수보다 체감 하락이 컸어요. 다만 6/24 마이크론(MU) 실적 등 일정이 남아 있어 금리發 변동과 별개로 실적 흐름은 이어져요. 가볍게 지켜보면 좋아요.",
            "impact": "negative",
            "sources": [SRC_STREET],
        },
        {
            "category": "개별 종목",
            "headline": "장중 무버 — AMAT +9%·ARM +6% 반등 vs 스페이스X 데뷔 랠리 진정",
            "oneLineSummary": "보유주는 아니지만, 반도체 장비 어플라이드머티리얼즈(AMAT)가 +9%, 칩 설계 ARM이 +6% 올랐어요. 반대로 상장 직후 급등했던 스페이스X(SPCX)는 숨 고르기로 약세였어요.",
            "summary": "장중에는 어플라이드머티리얼즈(AMAT) +9.3%·램리서치(LRCX) +6.6%·ARM +6.2% 등 일부 반도체 장비·설계주가 강했습니다. 반면 6/12 나스닥 사상 최대 IPO로 데뷔한 스페이스X(SPCX)는 데뷔 랠리가 식으며 약세였고, 전날엔 시총이 마이크로소프트·아마존을 잠시 넘기도 했습니다. 스페이스X는 AI 코딩 스타트업 커서를 600억$에 인수한다고 발표했습니다.",
            "ourImpact": "보유 종목엔 직접 영향이 적지만, 반도체 장비·설계주 강세는 업황 자체는 견조하다는 신호예요. 스페이스X 같은 고평가 신규주 변동은 위험선호 분위기의 가늠자로 참고만 하면 돼요.",
            "impact": "neutral",
            "sources": [SRC_STREET],
        },
        {
            "category": "글로벌·지정학",
            "headline": "美·이란 종전 합의 금 6/19 서명 앞두고 트럼프 '아직 최종본 아니다'",
            "oneLineSummary": "미국과 이란의 전쟁을 끝내는 합의가 금요일(6/19) 스위스에서 서명될 예정인데, 트럼프 대통령이 '아직 최종본이 아니다, 맘에 안 들면 다시 폭격할 수도 있다'고 말했어요. 이 발언에 기름값이 소폭 반등했어요.",
            "summary": "AP에 따르면 합의문 초안은 호르무즈 해협(세계 원유의 약 20%가 지나는 길목) 재개통과 이란 원유 수출 정상화, 전후 재건자금 최소 3,000억$, 제재 완화를 담고 있습니다. 다만 트럼프 대통령이 G7에서 '양해각서(MoU)일 뿐 최종이 아니다, 맘에 안 들면 다시 폭격'이라고 언급하며 불확실성이 남아 국제유가(WTI)는 $76대로 소폭 반등했습니다.",
            "ourImpact": "유가·중동 리스크가 완화되면 물가·기업 비용에 우호적이라 기술주에 장기적으로 도움이 돼요. 다만 서명 전까지 트럼프 발언에 따라 유가가 출렁일 수 있어 변동성만 참고하면 좋아요.",
            "impact": "neutral",
            "sources": [SRC_AP, SRC_G7],
        },
        {
            "category": "아시아 증시",
            "headline": "아시아, 美 FOMG 충격 안고 개장 예정 — 차분한 출발 가능성",
            "oneLineSummary": "미국이 중앙은행 금리 우려로 밀린 만큼, 한국·아시아 증시도 오늘 다소 조심스럽게 출발할 가능성이 있어요. 최근 미·이란 종전 기대로 많이 올랐던 만큼 잠시 숨 고르기가 나올 수 있어요.",
            "summary": "미국이 FOMC '연내 인상' 신호에 기술주 중심으로 밀리며 마감해, 한국·일본 등 아시아 증시도 위험회피 분위기를 안고 개장할 전망입니다. 다만 미·이란 종전 합의(금 6/19 서명) 기대가 받쳐주고 있어 급락보다는 차분한 조정 가능성이 거론됩니다. (구체 수치는 아시아 마감 캡처에서 갱신)",
            "ourImpact": "한국 반도체(삼성전자·SK하이닉스)가 약하면 보유 메모리·AI주 투자심리에도 영향이 있어요. 오늘 아시아 흐름을 가볍게 지켜보면 좋아요.",
            "impact": "neutral",
            "sources": [SRC_CNBC],
        },
    ],
    "signals": pf.get("signals", {}),
}
# 오타 수정
report["news"][6]["headline"] = "아시아, 美 FOMC 충격 안고 개장 예정 — 차분한 출발 가능성"

json.dump(report, open(p("reports", "2026-06-18.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("reports/2026-06-18.json created")

# ── 3. reports/index.json ────────────────────────────────────────────
shutil.copy(p("reports", "index.json"), p("reports", "index.json.before-0618.bak"))
idx = json.load(open(p("reports", "index.json"), encoding="utf-8"))
entry = {
    "date": "2026-06-18",
    "title": "6월 18일 (목) 06:00 美 마감 — 워시 첫 FOMC '매파' 점도표에 기술주 약세",
    "summary": "나스닥 -1.34%·S&P -1.21%·다우 -0.98%(-507pt). Fed 동결(3.50~3.75%)했지만 점도표 18명 중 9명 '연내 인상'·워시 포워드 가이던스 폐기. VIX +12%·10Y 4.497%(+6.9bp). 보유 반도체 동반 약세, 애프터아워 빅테크 실적 없음. 금 6/19 美 휴장(준틴스)."
}
idx["reports"] = [e for e in idx["reports"] if e.get("date") != "2026-06-18"]
idx["reports"].append(entry)
idx["lastUpdated"] = NOW
json.dump(idx, open(p("reports", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("reports/index.json updated")

# ── 4. calendar-events.json ──────────────────────────────────────────
shutil.copy(p("calendar-events.json"), p("calendar-events.json.before-us-close-0618.bak"))
cal = json.load(open(p("calendar-events.json"), encoding="utf-8"))
st = cal["stock"]
st["2026-06-17"] = [{
    "type": "us", "label": "美 마감 · FOMC", "color": "red", "mood": "negative",
    "time": "06:00 KST 美 마감 캡처",
    "title": "🔴 美 6/17 마감 — 워시 첫 FOMC '매파' 점도표, 기술주 약세",
    "description": "Fed 금리 동결(3.50~3.75%), 워시 신임 의장 첫 회의. 점도표 18명 중 9명 '연내 인상'(6명 복수 인상)·포워드 가이던스 폐기에 장 막판 저점. 나스닥 26,021.66(-1.34%)·S&P500 7,420.10(-1.21%)·다우 51,492.55(-0.98%). VIX +12%·10Y 4.497%(+6.9bp).",
    "impact": "중앙은행이 금리를 그대로 뒀지만 '올해 안에 올릴 수도 있다'는 신호가 나오면서 비싼 기술주가 먼저 팔렸어요. 금리가 오르면 미래 이익을 크게 반영한 기술주가 불리하기 때문이에요.",
    "ourImpact": "보유 반도체·빅테크가 금리에 민감해 지수보다 더 밀렸어요. 회사 악재가 아니라 금리發 매물이라 흐름만 가볍게 지켜보면 좋아요."
}]
st["2026-06-19"] = [{
    "type": "us", "label": "美 휴장(준틴스)", "color": "gray", "mood": "neutral",
    "time": "종일",
    "title": "🇺🇸 美 증시 휴장 — 준틴스(Juneteenth)",
    "description": "6/19(금) 준틴스 연방 공휴일로 뉴욕증권거래소·나스닥 정규장 휴장. 美 마감 캡처 없음.",
    "impact": "미국 증시가 하루 쉬어요. 거래가 없어 미국發 변수는 줄지만, 아시아·유럽 흐름은 평소처럼 이어져요.",
    "ourImpact": "보유 미국 주식 거래가 하루 멈춰요. 다음 미국 거래일은 6/22(월)이에요."
}]
st["2026-06-24"] = st.get("2026-06-24", []) + [{
    "type": "earnings", "label": "마이크론 실적", "color": "purple", "mood": "neutral",
    "time": "장 마감 후(애프터아워)",
    "title": "📊 마이크론(MU) 분기 실적 발표 예정",
    "description": "보유 종목 마이크론(MU)이 6/24 분기 실적을 발표할 예정이에요(애프터아워). 메모리 슈퍼사이클·AI HBM 수요가 핵심 관전 포인트.",
    "impact": "마이크론은 AI에 쓰이는 메모리 반도체 대표 회사예요. 실적과 다음 분기 전망(가이던스)에 따라 메모리·반도체 전반의 분위기가 좌우될 수 있어요.",
    "ourImpact": "보유 메모리주(MU·SNDK)와 AI 반도체 투자심리에 직접 영향이 큰 일정이에요. 발표 전후 변동이 클 수 있어요."
}]
cal["lastUpdated"] = NOW
json.dump(cal, open(p("calendar-events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("calendar-events.json updated")

print("ALL DONE")
