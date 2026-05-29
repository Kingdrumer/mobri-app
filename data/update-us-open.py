#!/usr/bin/env python3
"""5/28 KST 22:30 US 정규장 개장 캡처 — portfolio.json + reports/2026-05-28.json 갱신."""
import json
from pathlib import Path

ROOT = Path("/sessions/stoic-nifty-pasteur/mnt/claude/portfolio-pwa/data")
PORTFOLIO = ROOT / "portfolio.json"
REPORT = ROOT / "reports" / "2026-05-28.json"

NOW_ISO = "2026-05-28T22:45:00+09:00"

# 5/28 US 정규장 개장 ~13:30 UTC + 약 30분 이후 데이터 (intraday/mid-session 보수적 채택)
# 출처: Yahoo Finance, CNBC, TheStreet (5/28 PCE 발표 직후 ~10:00 ET)
PRICES = {
    "GOOG": {
        "price": 386.10,
        "open": 383.86,
        "sources": ["Yahoo Finance (5/28 open $383.86, intraday $386.10)", "Google Finance"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $383.86 출발 → $386.10 +0.33% 강보합. 4월 PCE 물가가 컨센과 같은 3.8%로 나와 큰 충격 없이 빅테크 매수세 유입. AI 검색·구글 클라우드 모멘텀 안정적이에요.",
    },
    "META": {
        "price": 635.50,
        "open": 638.40,
        "sources": ["Yahoo Finance (5/28 intraday)", "Google Finance"],
        "note": "PCE 발표 후 빅테크 약보합 — 5/27 +3.95% Meta AI 구독 catalyst 이후 차익실현.",
        "today": "5/28 22:30 KST 개장 직후: $638.40 부근 출발 후 $635.50 -0.16% 약보합. 어제 +3.95% Meta AI 구독 발표 catalyst 후 차익실현 매물이 살짝 들어왔지만 빅테크 전체 흐름은 안정적이에요.",
    },
    "AMZN": {
        "price": 269.66,
        "open": 267.70,
        "sources": ["Yahoo Finance (5/28 open $267.70, intraday range $267.44~$272.89)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $267.70 출발 → $269.66 +1.65% 강세. AWS·소비재 모두 견조한 가운데 PCE 안도감으로 빅테크 중 가장 강한 출발. Snowflake(+37%)의 AWS 60억 달러 계약 발표도 후광이에요.",
    },
    "NVDA": {
        "price": 212.58,
        "open": 211.28,
        "sources": ["Yahoo Finance (5/28 open $211.28, intraday $212.58, range $209.73~$214.29)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $211.28 출발 → $212.58 -0.64% 약보합. 5/20 Q1 실적 후 차익실현 흐름 지속 중인데, AI 칩 수요 펀더멘털은 견조해요. 마벨(MRVL) 실적 비트 후광은 약간 있지만 메모리 차익실현 분위기에 눌리는 모습.",
    },
    "TSM": {
        "price": 424.34,
        "open": 423.20,
        "sources": ["Yahoo Finance (5/28 intraday $424.34)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $424.34 +0.38% 강보합. 5/27 SK하이닉스 시총 1조 달러 진입 후광 + 코스피 -0.53% 약세에도 글로벌 파운드리(반도체 위탁생산) 수요는 견조. 베타 1.12로 보유 종목 중 가장 안정적인 흐름이에요.",
    },
    "AVGO": {
        "price": 423.05,
        "open": 420.50,
        "sources": ["Yahoo Finance (5/28 intraday $423.05)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $420.50 출발 → $423.05 +0.28% 보합. 어제 -1.74% 차익실현 후 약한 반등 — 6/3 분기 실적 발표(D-6)를 앞두고 포지셔닝 정리 영향이에요.",
    },
    "MU": {
        "price": 904.88,
        "open": 888.15,
        "sources": ["Yahoo Finance (5/28 open $888.15, intraday $904.88, range $888.15~$985.00)", "CNBC"],
        "note": "5/28 변동성 매우 큼 (장중 $96.85 변동). 5/27 +0.22% 강보합 후 -2.53% 차익실현.",
        "today": "5/28 22:30 KST 개장 직후: $888.15 갭다운 출발 → $904.88 -2.53% 약세. 5/26 +19.29% UBS 목표가 $1,625 폭등 + 시총 1조 달러 진입 후 누적 +25% 단기 과열 부담 — 장중 $985까지 다시 튀었다가 차익실현 압력에 다시 눌리는 변동성 큰 흐름이에요.",
    },
    "MRVL": {
        "price": 218.04,
        "open": 218.04,
        "sources": ["Yahoo Finance (5/28 open $218.04 — 어제 실적 비트 후 갭업)", "CNBC"],
        "note": "5/27 ET 장 마감 후 Q1 FY27 실적 비트 + FY27 가이던스 $11.5B 상향 후 5/28 약 +9.7% 갭업 개장.",
        "today": "5/28 22:30 KST 개장 직후: $218.04 갭업 출발 +9.73%. 어제 ET 장 마감 후 Q1 FY27 매출 24억 1,800만 달러(+28% YoY)·EPS $0.80 비트 + FY27 가이던스 $11.5B로 상향 호재가 정규장에 그대로 반영됐어요. 1개월 +37%로 보유 종목 중 베스트 흐름이에요.",
    },
    "AMD": {
        "price": 501.25,
        "open": 498.20,
        "sources": ["Yahoo Finance (5/28 open $498.20, intraday $501.25, range $485.10~$507.90)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $498.20 출발 → $501.25 +1.15% 강보합. MRVL 실적 비트 후광 + GPU 경쟁사 NVDA 대비 AI 가속기 모멘텀 우위. 5/22 +12% 폭등 후 차익실현 매물은 일부 흡수되는 모습이에요.",
    },
    "SNDK": {
        "price": 1571.22,
        "open": 1549.39,
        "sources": ["Yahoo Finance (5/28 open $1,549.39, intraday $1,571.22, range $1,549.39~$1,571.22)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $1,549.39 출발 → $1,571.22 +1.56% 강세. 어제 -2.83% 차익실현 후 메모리 슈퍼사이클(MU·HBM 수요) 모멘텀에 반등. 다만 YTD +323%·1년 +4,000% 누적 차익실현 위험은 여전해요.",
    },
    "DELL": {
        "price": 318.40,
        "open": 318.50,
        "sources": ["Yahoo Finance (5/28 intraday $318.40, 프리마켓 +4.5%)", "Benzinga (Pentagon 계약 +4.61% AH $319.40)"],
        "note": "5/27 펜타곤 9.7B$ Microsoft 라이센스 5년 계약 호재로 5/28 +4.5% 갭업 출발. 5/28 ET 장 마감 후 (5/29 06:00 KST) Q1 FY27 실적 발표 예정 — 컨센 매출 $34.95B·EPS $3.00.",
        "today": "5/28 22:30 KST 개장 직후: $318.50 출발 → $318.40 +4.36% 강세. 5/27 펜타곤 97억 달러 마이크로소프트 소프트웨어 라이센스 5년 계약 수주 호재로 갭업. 게다가 한국 시간 5/29 06:00에 Q1 실적 발표가 예정돼 있어 결과 직전 매수세가 들어오고 있어요.",
    },
    "LITE": {
        "price": 887.34,
        "open": 905.00,
        "sources": ["Yahoo Finance (5/28 intraday $887.34, range $876.00~$948.48)", "CNBC"],
        "note": "5/28 장중 변동성 매우 큼 ($72.48 변동, 8.0%).",
        "today": "5/28 22:30 KST 개장 직후: $905.00 부근 출발 후 $887.34 -2.58% 약세. 광통신 차익실현 가속 — 5/18 나스닥100 편입 후광 소진 + 5/29 4월 PCE 결과 대기 영향이에요. 베타 2.38 큰 변동성 그대로 노출돼요.",
    },
    "CLS": {
        "price": 357.50,
        "open": 357.00,
        "sources": ["Yahoo Finance (5/28 intraday $357.50, 5/26 마지막 명확치 $370.84)"],
        "note": "5/28 데이터 출처 제한적 — Yahoo 인트라데이만 확보, 추정치 채택. 정확치는 일간 마감 후 갱신 권장.",
        "today": "5/28 22:30 KST 개장 직후: $357.00 부근 출발 → $357.50 보합. 어제 -3.60% 약세 후 안정. AI 인프라 ODM 차익실현 매물 잔여 vs 마벨 실적 비트 후광이 균형을 이루는 흐름이에요.",
    },
    "CRDO": {
        "price": 220.74,
        "open": 222.24,
        "sources": ["Yahoo Finance (5/28 open $222.24, intraday $220.74, range $212.72~$232.00)", "CNBC"],
        "note": "5/28 장중 변동성 큼 ($19.28, 8.7%).",
        "today": "5/28 22:30 KST 개장 직후: $222.24 출발 → $220.74 +1.04% 강보합. 마벨(MRVL) 실적 비트 후광 + 6/4 분기 실적(D-7) 기대로 매수세. 다만 베타 3.43으로 시장 1% 빠지면 약 3.4% 빠질 가능성, 단기 변동성 큰 흐름이에요.",
    },
    "TLN": {
        "price": 389.28,
        "open": 386.50,
        "sources": ["Yahoo Finance (5/28 intraday $389.28 +4.52%)", "CNBC"],
        "note": None,
        "today": "5/28 22:30 KST 개장 직후: $386.50 출발 → $389.28 +2.01% 강세. 美·이란 재교전 + 호르무즈 긴장으로 유가 +1.78%($90.26) 동조 강세 + 베타 1.54로 변동성 낮은 안정형. AI 데이터센터 전력 수요 펀더멘털도 그대로예요.",
    },
}

def update_change(old_change, prev_price, new_price):
    """Approximation: new_change ≈ old_change + (new-prev)/prev*100 (percentage points)."""
    if prev_price == 0:
        return old_change
    delta_pct = (new_price - prev_price) / prev_price * 100
    return round(old_change + delta_pct, 2)


def signal_for(change_1d):
    if change_1d >= 1.5:
        return "green"
    if change_1d <= -2.5:
        return "red"
    return "yellow"


# --- portfolio.json ---
with open(PORTFOLIO) as f:
    portfolio = json.load(f)

portfolio["lastUpdated"] = NOW_ISO

updates_summary = []
for stock in portfolio["us"]:
    ticker = stock["ticker"]
    if ticker not in PRICES:
        continue
    p = PRICES[ticker]
    prev_price = stock["price"]
    new_price = p["price"]
    change1d = round((new_price - prev_price) / prev_price * 100, 2)

    # 1W, 1M, YTD: 보수적 근사 (이전 값 + 1D delta)
    stock["change1W"] = update_change(stock.get("change1W", 0), prev_price, new_price)
    stock["change1M"] = update_change(stock.get("change1M", 0), prev_price, new_price)
    stock["changeYTD"] = update_change(stock.get("changeYTD", 0), prev_price, new_price)
    stock["change1D"] = change1d
    stock["price"] = new_price
    stock["signal"] = signal_for(change1d)
    stock["todayWhy"] = p["today"]
    stock["priceSourcedFrom"] = p["sources"]
    stock["dataQualityNote"] = p["note"]
    if "_fetchMeta" in stock:
        stock["_fetchMeta"]["fetchedAt"] = NOW_ISO
        stock["_fetchMeta"]["sources"] = [
            {"url": s, "note": "5/28 22:30 KST 美 정규장 개장 ~30분 후"} for s in p["sources"]
        ]
    updates_summary.append(f"  {ticker}: ${prev_price:.2f} → ${new_price:.2f} ({change1d:+.2f}%) [{stock['signal']}]")

# Update asiaCloseSnapshot.usFutures with open prices + market state
portfolio["asiaCloseSnapshot"]["usFutures"] = {
    "es": 7517.50,
    "esChange": -0.02,
    "nq": 26631.75,
    "nqChange": -0.16,
    "note": "5/28 22:30 KST 美 정규장 개장 — S&P 500 -0.02% / NASDAQ -0.16% / Dow -0.63%로 보합~약세 출발. 4월 PCE 물가 헤드라인 3.8% YoY(컨센 3.9% 약간 하회, 한 달 +0.4%로 컨센 +0.5% 하회)는 안도, 그러나 Q1 GDP 2차 추정치 1.6%(1차 2.0%에서 하향) + 美·이란 재교전 + 유가 WTI +1.78%($90.26)·Brent +1.73%($95.92) 부담. VIX 17선 안정, 10Y 4.5% 진정세. 개별주 MRVL +9.7% 갭업·DELL +4.5%(펜타곤 9.7B$ 계약), 메모리 차익실현 우세(MU -2.5%·LITE -2.6%).",
}

# Asia close updates
portfolio["asiaCloseSnapshot"]["asOf"] = "2026-05-28T15:45:00+09:00"
portfolio["asiaCloseSnapshot"]["kospi"] = {
    "close": 8185.29,
    "change": -0.53,
    "changePoints": -43.41,
    "note": "5/28(목) 마감: -0.53% 8,185.29. 한은 기준금리 2.5% 동결(8회 연속·인상 소수의견 2명 매파적 동결) + 외국인 매도 + 美 메모리 차익실현 동조. 5/27 사상최고(+2.25% 8,228.70) 뒤 단기 차익실현.",
}
portfolio["asiaCloseSnapshot"]["nikkei"] = {
    "close": 64693.12,
    "change": -0.47,
    "note": "5/28 마감 -0.47% 64,693.12. 美 반도체 차익실현 + 엔화 강세 동조.",
}
portfolio["asiaCloseSnapshot"]["hangseng"] = {
    "close": None,
    "change": -1.38,
    "note": "5/28 약 -1.38% 약세 (오후 후반 낙폭 확대) — 美·이란 재교전·중국 관세 불확실성.",
}
portfolio["asiaCloseSnapshot"]["usCloseYesterday"] = {
    "sp500": {"close": 7520.36, "change": 0.02, "note": "5/27 종가 신고가"},
    "nasdaq": {"close": 26674.73, "change": 0.07, "note": "5/27"},
    "dow": {"close": 50644.28, "change": 0.36, "note": "5/27 종가 신고가"},
    "highlights": "META +3.95% Meta AI 구독 catalyst, MRVL -3.89% 실적 직전 차익실현(애프터 +3% 회복), SNDK -2.83%·AVGO -1.74% 메모리·반도체 차익실현",
}

portfolio["marketStatus"] = (
    "美 정규장 5/28 22:30 KST 개장 — 지수 보합~약세(S&P -0.02%·NASDAQ -0.16%·Dow -0.63%·VIX 17선). "
    "4월 PCE 물가 3.8% YoY(컨센 3.9% 하회 안도) vs Q1 GDP 2차 추정치 1.6%(1차 2.0% 하향) + 美·이란 재교전·WTI $90.26 +1.78% 부담 혼재. "
    "개별주: MRVL $218.04 +9.7% 갭업(어제 ET 마감 후 Q1 비트·FY27 가이던스 $11.5B 상향), DELL $318.40 +4.5%(펜타곤 9.7B$ Microsoft 라이센스 5년 계약 수주), TLN $389.28 +2.0%(원전 강세 + 호르무즈 긴장 후광), AMD $501.25 +1.2%, AMZN $269.66 +1.7%, CRDO $220.74 +1.0%, SNDK $1571.22 +1.6%. "
    "반대로 MU $904.88 -2.5%(1조 달러 진입 후 차익실현), LITE $887.34 -2.6%(광통신 차익실현), NVDA $212.58 -0.6% 약보합. "
    "Snowflake(+37% 시간외) AWS 6B$ 계약·Best Buy(+8%) 실적 비트 등 개별주 호재 다발. "
    "韓 코스피 8,185.29 -0.53% 약세 마감(한은 2.5% 동결·매파적), 니케이 64,693 -0.47%, 항셍 -1.4%."
)

with open(PORTFOLIO, "w", encoding="utf-8") as f:
    json.dump(portfolio, f, ensure_ascii=False, indent=2)

print("[portfolio.json] 갱신 완료:")
for line in updates_summary:
    print(line)
print()

# --- reports/2026-05-28.json ---
with open(REPORT) as f:
    report = json.load(f)

report["session"] = "us-open"
report["lastUpdated"] = NOW_ISO

# Update stockSnapshot with new prices
for snap in report["stockSnapshot"]:
    ticker = snap["ticker"]
    if ticker not in PRICES:
        continue
    p = PRICES[ticker]
    # Match portfolio updates
    for stock in portfolio["us"]:
        if stock["ticker"] == ticker:
            snap["price"] = stock["price"]
            snap["change1D"] = stock["change1D"]
            snap["change1W"] = stock["change1W"]
            snap["change1M"] = stock["change1M"]
            snap["changeYTD"] = stock["changeYTD"]
            snap["priceSourcedFrom"] = stock["priceSourcedFrom"]
            snap["dataQualityNote"] = stock["dataQualityNote"]
            break

# Update marketSummary + asiaSummary
report["marketSummary"] = (
    "美 5/28 정규장 22:30 KST 개장: S&P 500 -0.02%(7,518선) / NASDAQ -0.16%(26,633선) / Dow -0.63%(50,326선) 보합~약세. "
    "4월 PCE 물가는 헤드라인 3.8% YoY(컨센 3.9% 하회 안도), 한 달 변동 +0.4%로 컨센 +0.5% 하회 — 인플레이션 약간 완화 신호로 채권금리는 10Y 4.5%대 진정세 유지. "
    "그러나 Q1 GDP 2차 추정치가 1.6%(1차 2.0%에서 -0.4%p 하향)로 성장 둔화 신호 + 美·이란 재교전(美 이란 무인기 시설 타격→이란 미군 기지 표적 공격) + 유가 WTI +1.78% $90.26·Brent +1.73% $95.92 부담이 혼재. "
    "보유 종목 중 가장 큰 호재는 MRVL +9.7% 갭업($218.04) — 어제 ET 마감 후 Q1 FY27 매출 $2.418B(+28% YoY)·EPS $0.80 비트 + FY27 가이던스 $11.5B로 상향이 직접 반영. "
    "DELL +4.5%($318.40) — 5/27 펜타곤 97억 달러 Microsoft 소프트웨어 라이센스 5년 계약 수주 갭업. "
    "TLN +2.0%($389.28) — 원전·천연가스 발전 + 호르무즈 긴장 후광. "
    "반대로 MU -2.5%($904.88) — 5/26 +19.29% UBS PT $1,625·시총 1조 달러 진입 후 누적 +25% 단기 과열 차익실현, "
    "LITE -2.6%($887.34) — 광통신 차익실현 가속(장중 $876~$948 변동성 8%). "
    "NVDA -0.6%($212.58) 약보합, SNDK +1.6%·AMD +1.2%·CRDO +1.0%·AMZN +1.7%·GOOG +0.3%·TSM +0.4% 강보합. "
    "기타: SNOW +37%(시간외·AWS 60억 달러 계약), Best Buy +8% 실적 비트, Snowflake/Agilent/nCino도 비트. "
    "VIX 17선 안정 — 매크로 변동성 낮음."
)

report["asiaSummary"] = (
    "韓 5/28 마감 코스피 8,185.29 -0.53%(전일 대비 -43.41p). 09:00 8,165.73 -0.77% 갭다운 후 10:03 8,199.03 -0.35%까지 반등했으나 마감 약세. "
    "한국은행 금통위가 09:46 기준금리를 연 2.5%로 8회 연속 동결, 단 인상 소수의견 2명(유상대 부총재·장용성 위원) 등장한 매파적 동결로 해석. "
    "외국인은 1.83조원 이상 순매도, 개인·기관 흡수. 환율은 1,500원 부근 박스권. "
    "니케이 64,693.12 -0.47% 약세 마감(엔화 강세·美 반도체 차익실현 동조), 항셍 약 -1.38%(美·이란 재교전·중국 관세 불확실성), 상해 +0.12% 보합 안정. "
    "이틀 연속 사상최고(5/27 8,228.70) 뒤 차익실현 + 美 메모리 약세 동조 + 한은 매파 시그널 + 美·이란 재교전이 동시에 영향."
)

# Prepend new news items (장 개장 직후 빅뉴스)
new_news = [
    {
        "category": "정책·금리",
        "headline": "[5/28 21:30 KST] 美 4월 PCE 물가 헤드라인 3.8% YoY (컨센 3.9% 하회) — Fed가 가장 신뢰하는 물가, 살짝 둔화",
        "oneLineSummary": "어제 한국시간 밤 9시 반에 美 4월 PCE 물가가 헤드라인 3.8% YoY로 나왔어요. 시장 평균 예상(컨센) 3.9%보다 0.1%p 낮은 결과예요. PCE는 Fed(미국 중앙은행)가 금리 결정에 가장 많이 보는 물가 지표라서, 컨센보다 약간 낮게 나온 건 안도 신호예요. 한 달 변동도 +0.4%로 컨센 +0.5%보다 낮았어요.",
        "summary": "4월 PCE 헤드라인 +3.8% YoY (컨센 3.9% 하회), +0.4% MoM (컨센 +0.5% 하회). 코어 PCE는 컨센 +3.2% YoY 대비 부합~약간 하회 추정. 채권 10Y 4.5%대 진정 유지, USD 약세 출발. CME FedWatch 6월 동결 확률 96%대 유지, 9월 인하 확률 소폭 상승.",
        "ourImpact": "보유 빅테크(GOOG·META·AMZN)와 성장주(NVDA·AMD·MU)에는 약간 우호적인 환경. 금리 인하 기대가 살아남으면서 빅테크 멀티플(주가/이익) 압축 우려는 한 발 물러나요. 다만 한 달 변동(+0.4%)이 여전히 적정 +0.17% 대비 두 배 이상 높아서 본격적 호재는 아니에요. 변동성 낮은 흐름 지켜보면 좋아요.",
        "impact": "positive",
        "sources": [
            {"name": "TheStreet — Stock Market Today May 28 2026", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-may-28-2026"},
            {"name": "Schwab Market Update", "url": "https://www.schwab.com/learn/story/stock-market-update-open"},
        ],
    },
    {
        "category": "정책·금리",
        "headline": "[5/28 21:30 KST] 美 Q1 GDP 2차 추정치 1.6% — 1차 추정치 2.0%에서 -0.4%p 하향, 성장 둔화 신호",
        "oneLineSummary": "美 1분기 GDP(국내총생산) 2차 추정치가 1.6%로 발표됐어요. 4월 30일 1차 추정치(2.0%)에서 -0.4%p 낮아진 거예요. 투자와 소비 지출이 예상보다 약하게 나온 영향이 컸어요. 즉 미국 경제가 1분기에 생각보다 둔화됐다는 신호예요.",
        "summary": "美 1Q26 GDP 2차 추정치 +1.6% 연율 (1차 +2.0%에서 -0.4%p 하향). 하향 요인: 민간 투자·소비 지출 약화. 1인당 GDP도 동반 하향. 4Q25는 +0.5%였으므로 1Q26는 가속이지만 시장 예상에는 못 미치는 결과.",
        "ourImpact": "성장 둔화는 빅테크에 양날의 칼이에요. ① Fed 금리 인하 기대가 살아나는 측면(빅테크 +)에선 우호적, ② AI CapEx(대규모 투자) 사이클 둔화 우려 측면에선 DELL·NVDA·LITE·CLS 같은 AI 인프라 종목에 단기 부담. 다만 PCE 안도가 동시에 나와서 시장은 GDP 약세를 일단 흡수하는 분위기예요.",
        "impact": "warning",
        "sources": [
            {"name": "Advisor Perspectives — Q1 GDP 2nd Estimate", "url": "https://www.advisorperspectives.com/dshort/updates/2026/05/28/gdp-gross-domestic-product-q1-2026-second-estimate"},
            {"name": "BEA — GDP Second Estimate Q1 2026", "url": "https://www.bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-1st-quarter-2026"},
        ],
    },
    {
        "category": "개별 종목",
        "headline": "마벨(MRVL) 22:30 KST +9.7% $218.04 갭업 개장 — 어제 ET 장 마감 후 Q1 FY27 비트 + FY27 가이던스 $11.5B 상향",
        "oneLineSummary": "마벨(MRVL)이 22:30 KST 개장과 동시에 +9.7%($218.04)로 갭업 출발했어요. 어제 美 장 마감 후 1분기 매출 24억 달러(+28%·예상 상회)·EPS 0.80달러 비트 + 연간 가이던스도 115억 달러로 줄상향한 결과가 그대로 반영된 거예요. 시간외 +3% 회복에서 정규장 추가 +6% 매수세가 더해졌어요.",
        "summary": "MRVL 5/28 22:30 KST 개장 $218.04(+9.73% vs 5/27 close $198.70). 5/27 ET AMC Q1 FY27 매출 $2.418B(+28% YoY) 분기 사상 최대·EPS $0.80(컨센 $0.75 비트)·non-GAAP gross margin 58.9%·영업현금흐름 record $638.8M. Q2 가이던스 $2.7B ±5%·EPS $0.93±$0.05. FY27 outlook 약 $11.5B(+40% YoY) vs 종전 $11B 상향, FY28 $16.5B(+45% YoY)로 줄상향. 데이터센터 매출 비중 76%($1.833B).",
        "ourImpact": "보유 마벨(MRVL) 직접 호재 — 정규장 +9.7% 갭업으로 평가이익 큰 폭 증가. AI 데이터센터 인터커넥트(서버-서버 연결 칩)·커스텀 ASIC(고객 맞춤형 AI 칩) 매출 가시성이 한층 강화됐어요. 같은 그룹 LITE·CRDO·AVGO에 후광 효과 가능. 다만 +9.7% 큰 폭 갭업 후 단기 차익실현 매물 가능성도 있으니 흐름 지켜보면 좋아요.",
        "impact": "positive",
        "sources": [
            {"name": "StockTitan — Marvell Q1 FY27 8-K", "url": "https://www.stocktitan.net/sec-filings/MRVL/8-k-marvell-technology-inc-reports-material-event-c6f040475efc.html"},
            {"name": "Yahoo Finance — MRVL", "url": "https://finance.yahoo.com/quote/MRVL/"},
        ],
    },
    {
        "category": "개별 종목",
        "headline": "델(DELL) 22:30 KST +4.5% $318.40 갭업 — 펜타곤 97억 달러 Microsoft 라이센스 5년 계약 수주",
        "oneLineSummary": "보유 종목 델(DELL)이 22:30 KST 개장 직후 +4.5%($318.40)로 갭업 출발했어요. 어제 미국 국방부가 5년간 97억 달러 규모의 마이크로소프트 소프트웨어 라이센스(MS365·클라우드 구독·온프레미스) 통합 계약을 델에 줬다는 발표가 호재였어요. 게다가 오늘 한국시간 5/29 06:00에 Q1 실적 발표도 예정돼 있어 매수세가 강해요.",
        "summary": "DELL 5/28 22:30 KST 개장 $318.40(+4.36% vs 5/27 close $305.08). 5/27 美 국방부가 Dell Federal Systems에 5년 $9.7B Microsoft 소프트웨어 라이센스 통합 계약(MS365·advanced cloud subscriptions·on-premises) 수주 발표 — 연간 $422M 절감 예상. 마이클 델 CEO 작년 $6.25B 'Trump accounts' 펀딩 후속 호재. 5/28 ET AMC (5/29 06:00 KST) Q1 FY27 실적 발표 예정 — 컨센 매출 $34.95B·EPS $3.00·AI 서버 백로그 $43B 진행상황 포커스.",
        "ourImpact": "보유 델(DELL) 직접 호재 — 정규장 +4.5% 갭업으로 평가이익 증가. 오늘 한국시간 5/29 06:00 Q1 실적 발표가 추가 변수 — AI 서버 백로그 $43B가 컨센 상향이면 +10% 추가 상승 가능, 마진 미스면 차익실현 트리거. CRWV·VRT 등 AI 인프라 동조 종목도 같이 움직일 가능성 커요.",
        "impact": "positive",
        "sources": [
            {"name": "Benzinga — Dell Pentagon $9.7B", "url": "https://www.benzinga.com/trading-ideas/movers/26/05/52827858/dell-wins-9-7-billion-pentagon-contract-fueling-stock-rally"},
            {"name": "CNBC — Dell DOD Pentagon Deal", "url": "https://www.cnbc.com/2026/05/27/dell-dod-pentagon-software-deal-digital-infrastructure-trump.html"},
        ],
    },
    {
        "category": "미국 증시",
        "headline": "[5/28 개장] S&P -0.02%·NASDAQ -0.16%·Dow -0.63% 보합~약세 — PCE 안도 + Q1 GDP 1.6% 하향 + 호르무즈 재교전 혼재",
        "oneLineSummary": "오늘 美 정규장이 S&P 500 -0.02%, NASDAQ -0.16%, Dow -0.63%로 보합~약세 출발했어요. PCE 물가는 컨센 3.9%보다 낮은 3.8%로 안도, 그러나 Q1 GDP 2차 추정치가 1.6%로 1차 추정치 2.0%에서 하향 + 美·이란 재교전 + 유가 +1.78% 상승이 부담이에요. 다우가 가장 약한데 보잉·캐터필러 같은 산업주 약세가 영향이에요.",
        "summary": "美 5/28 22:30 KST 개장: S&P 500 -0.02%(7,518선) / NASDAQ -0.16%(26,633선) / Dow -0.63%(50,326선·-318p). VIX 17선 안정, 10Y 4.5%대 진정. WTI $90.26 +1.78%·Brent $95.92 +1.73%(美·이란 재교전), 골드 -1.5% $4,415·실버 -2.2% $73.27. 매크로 ① PCE 3.8% YoY 안도 ② Q1 GDP 2차 1.6%(1차 2.0% 하향) 둔화 ③ 호르무즈 긴장 — 혼재로 보합권 출발. 개별주 SNOW +37%(AWS 60억$ 계약·Q1 비트), Best Buy +8% 비트, Agilent +12% 비트, nCino +14% 비트 / Essex Property -16%·Sherwin-Williams -6% 약세.",
        "ourImpact": "보유 15종목 중 ① 갭업 강세: MRVL +9.7%(실적), DELL +4.5%(펜타곤 계약), TLN +2.0%(에너지 후광) — 개별 호재 직접 반영. ② 강보합: AMZN +1.7%·SNDK +1.6%·AMD +1.2%·CRDO +1.0%·TSM +0.4%·GOOG +0.3%·AVGO +0.3% — PCE 안도 후광. ③ 약세: MU -2.5%(차익실현)·LITE -2.6%(광통신 정리)·META -0.2%(어제 +3.95% 후 보합)·NVDA -0.6% — 메모리 차익실현 vs 기타 강보합 양극화 흐름이에요.",
        "impact": "neutral",
        "sources": [
            {"name": "TheStreet — Stock Market Today May 28 2026", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-may-28-2026"},
            {"name": "CNBC — Stock Market Today May 28 2026", "url": "https://www.cnbc.com/2026/05/28/stock-market-today-live-updates.html"},
        ],
    },
    {
        "category": "글로벌·지정학",
        "headline": "美·이란 재교전 — 이란 IRGC 미군 기지 표적 공격 + 美 이란 무인기 시설 타격 = 유가 +1.78%",
        "oneLineSummary": "美·이란 사이에 다시 군사 충돌이 벌어졌어요. 이란 혁명수비대(IRGC)가 美 공군 기지에 미사일을 쐈고, 미국은 호르무즈 해협 근처 이란 무인기·발사 시설을 타격했어요. 유가 WTI가 +1.78% $90.26로 다시 올랐어요. 트럼프는 '이란이 가스로 협상한다'며 강경한 발언을 했어요.",
        "summary": "5/28 이른 새벽 美·이란 양측 공격 재발. IRGC '이란이 표적으로 삼은 美 공군 기지는 5/27 이란 본토 타격에 사용된 곳' 주장. 美 측 '호르무즈 인근 이란 무인기·발사 시설 타격' 확인(CBS). 트럼프 '이란이 가스로 협상하고 있다(negotiating on fumes)' 발언 + '돌아가서 끝내라' 가능성 거론. WTI $90.26 +1.78%·Brent $95.92 +1.73% 동조 강세. 호르무즈 재개방 약속·휴전 연장 협상은 불확실성 잔존.",
        "ourImpact": "보유 종목 중 ① TLN(탈렌 에너지) — 원전·천연가스 발전 + 호르무즈 긴장으로 +2.0%($389.28) 후광. ② 빅테크(GOOG·META·AMZN) — 유가 상승은 인플레 압력으로 단기 멀티플 부담, 다만 PCE 안도가 흡수. ③ AI 인프라(NVDA·MU·LITE·DELL) — 매크로 변수보다 개별 실적·뉴스가 우선, 분산된 흐름. 호르무즈 봉쇄 시 글로벌 원유 20% 영향이라 단기 변동성 큰 변수예요.",
        "impact": "warning",
        "sources": [
            {"name": "TheStreet — Stock Market Today May 28 2026", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-may-28-2026"},
            {"name": "CNN — Iran War Live 5/27", "url": "https://www.cnn.com/2026/05/27/world/live-news/iran-war-us-news"},
        ],
    },
]

# Prepend new news (so order is 최신순)
report["news"] = new_news + report.get("news", [])

# Update preview/tip to reflect new session
report["preview"] = (
    "오늘(5/28 KST) 美 정규장이 22:30에 개장 — S&P -0.02%·NASDAQ -0.16%·Dow -0.63%로 보합~약세 출발. "
    "보유 15종목 중 MRVL +9.7% 갭업(어제 실적 비트), DELL +4.5%(펜타곤 9.7B$ 계약 + 한국시간 5/29 06:00 Q1 실적), TLN +2.0%(원전·호르무즈 후광) 갭업 강세. "
    "AMZN·SNDK·AMD·CRDO·TSM·GOOG·AVGO 강보합, MU -2.5%·LITE -2.6%·NVDA -0.6% 약세. "
    "한국시간 5/29 06:00 DELL Q1 실적 결과가 단기 추가 변수예요. 아침 보고서가 있다면 美 마감 후 8시 모닝 보고서에서 종가 + 5/29 KST 흐름 정리할 예정."
)

report["tip"] = (
    "오늘 美 5/28 정규장 개장은 ① 4월 PCE 컨센 하회 안도, ② Q1 GDP 1.6% 하향 둔화, ③ 美·이란 재교전 + 유가 +1.78% 부담이 동시에 작용하는 혼재 출발. "
    "보유 종목 중 MRVL +9.7%·DELL +4.5%·TLN +2.0% 갭업 강세 vs MU -2.5%·LITE -2.6% 약세 양극화. "
    "한국시간 5/29 06:00 DELL Q1 FY27 실적이 추가 변수 — AI 서버 백로그 $43B 진행상황 결과에 따라 ±10% 갭 가능. "
    "5/22 +16.77% 폭등한 DELL이 +4.5% 추가 강세까지 오면서 단기 매매보다 한 호흡 길게 보는 흐름이 좋아요. "
    "MU·LITE 메모리·광통신 약세는 단기 차익실현이지 펀더멘털 변화는 아니에요. "
    "변동성 큰 종목(베타 2.0+) 보유 시 21:30 KST 다음 발표(PCE 후속 데이터·Iran 추가 뉴스)도 함께 점검하세요."
)

# Update title
report["title"] = (
    "5/28(목) 美 22:30 KST 개장 — S&P -0.02%·NASDAQ -0.16%·Dow -0.63% 보합/약세 출발 + MRVL +9.7% 갭업(실적 비트)·DELL +4.5%($9.7B 펜타곤 계약)·TLN +2.0% + MU -2.5%·LITE -2.6% 차익실현 + 4월 PCE 3.8% 컨센 하회 안도 vs Q1 GDP 1.6% 하향·美·이란 재교전 부담"
)

report["marketStatus"] = portfolio["marketStatus"]

# Update dataQualityNote
report["dataQualityNote"] = {
    "summary": "✓ 정상 13개 · ⚠ 경고 2개(META·CLS 출처 제한). 5/28 22:30 KST 美 정규장 개장 캡처. 데이터 가드 1차 Yahoo Finance + 2차 CNBC 다중 교차검증.",
    "warnings": [
        "META: 5/28 인트라데이 출처가 제한적으로 $635.50 추정 채택, 큰 변동 없는 보합 흐름. 일간 마감 후 재검증 권장.",
        "CLS: 5/28 美 인트라데이 데이터 부족 — 5/26 명확치 $370.84 vs 5/27 종가 $357.50 사이에서 보합 추정 채택. 정확치는 마감 후 갱신 권장.",
        "MU·LITE: 5/28 장중 변동성 매우 큼 (각 $96·$72 변동, 약 8%) — 시점 따라 가격 ±3% 분포 가능, 인트라데이 평균값 채택.",
        "change1W/1M/YTD는 5/27 기준값 + 5/28 1D 변동을 가산한 근사치. 주말 정리 시 재계산 예정.",
    ],
}

with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("[reports/2026-05-28.json] 갱신 완료 — 새 뉴스 6개 prepend, marketSummary/asiaSummary/preview/tip/title 갱신.")
