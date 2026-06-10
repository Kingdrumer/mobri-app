# -*- coding: utf-8 -*-
import json, shutil, datetime

SUF = ".before-asia-close-0610.bak"

# ---------- backups ----------
for f in ["reports/2026-06-10.json", "portfolio.json", "calendar-events.json", "reports/index.json"]:
    try:
        shutil.copy(f, f + SUF)
    except Exception as e:
        print("backup skip", f, e)

def load(f): return json.load(open(f, encoding="utf-8"))
def save(f, d): json.dump(d, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# =========================================================
# 1) reports/2026-06-10.json
# =========================================================
rep = load("reports/2026-06-10.json")

rep["asiaSummary"] = ("코스피 7,730.82(-4.52%·-366.11)로 마감, 6/8 이후 2거래일 만에 매도 사이드카 발동(13:16). "
    "외국인 2.89조·기관 0.99조 순매도, 개인 3.74조 순매수. 삼성전자 약 -7%(29.95만, '30만전자' 재이탈)·SK하이닉스 약 -8.4%(202.8만) 급락. "
    "코스닥 약 940선(-3%대). 원/달러 1,525.0 상승 출발 후 1,514원대 회복. 일본 니케이 약 -2%(일본 5월 도매물가 PPI +6.3% 깜짝)·홍콩 항셍 약세 출발. "
    "美 선물 ES(S&P) -0.5%·NQ(나스닥) -0.9%·다우 -0.28%로 약세 — 미군 이란 공습 + 오늘 밤 21:30 5월 CPI(예상 +4.2%) 경계.")

asia_news = [
  {
    "category": "아시아 증시",
    "headline": "코스피 -4.5% 7,730.82 마감 — 2거래일 만에 또 매도 사이드카, 외국인 2.9조 '팔자'",
    "oneLineSummary": "오늘 한국 코스피가 -4.5%(7,730.82) 내려 마감했어요. 미군의 이란 공습으로 중동 긴장이 다시 커졌고, AI 투자에 대한 불안과 오늘 밤 미국 물가 발표를 앞둔 경계심이 겹쳤어요. 외국인이 2조 9천억 원어치를 팔면서 오후 1시 16분에 매도 사이드카(급락 시 프로그램 매도를 5분간 멈추는 장치)가 이틀 만에 또 발동됐어요.",
    "summary": "6/10 코스피는 -4.52%(7,730.82, -366.11) 마감. 장중 한때 7,500선까지 밀렸다 낙폭을 일부 줄였습니다. 13:16:25 코스피200 선물 -5.02%로 매도 사이드카 발동(6/8 이후 2거래일 만). 외국인 2.89조·기관 0.99조 순매도, 개인 3.74조 순매수. 삼성전자 -6.99%(29.95만)로 '30만전자' 재이탈, SK하이닉스 -8.44%(202.8만). 미군 이란 공습·대형 데이터센터업체 크루소의 빅테크 고객 개발 일시중단(AI 투자 불확실성)·오늘 밤 CPI 경계가 겹쳤습니다.",
    "ourImpact": "삼성전자·SK하이닉스가 7~8% 급락해, 같은 반도체인 보유 종목(엔비디아·마이크론·TSMC)에도 부담 신호예요. 오늘 밤 미국장이 약하게 출발할 수 있어, CPI 결과까지 흐름만 가볍게 지켜보면 좋아요.",
    "impact": "negative",
    "sources": [
      {"name": "이투데이(6/10)", "url": "https://www.etoday.co.kr/news/view/2592258"},
      {"name": "파이낸셜뉴스(6/10)", "url": "https://www.fnnews.com/news/202606101329334162"}
    ]
  },
  {
    "category": "아시아 증시",
    "headline": "일본 니케이 약 -2%·아시아 동반 약세 — 일본 도매물가 +6.3% '깜짝'",
    "oneLineSummary": "일본 니케이지수가 약 -2% 내리는 등 아시아 증시가 다 같이 약했어요. 미군의 이란 공습에 위험을 피하려는 분위기가 퍼졌고, 일본의 도매 물가(기업끼리 사고파는 물가)가 1년 전보다 +6.3% 올라 예상(+5.5%)을 크게 웃돌면서 물가 부담까지 더해졌어요. 홍콩 항셍도 약세로 출발했어요.",
    "summary": "6/10 아시아 증시는 미군의 이란 공습發 위험회피로 동반 약세. 일본 니케이225는 약 -2% 하락했고, 일본 5월 생산자물가(PPI, 도매물가)가 전년比 +6.3%로 로이터 예상(+5.5%)을 크게 상회해 물가 부담을 키웠습니다. 홍콩 항셍은 약세 출발(선물 약 24,441), 한국 코스피 -4.52%로 아시아 중 낙폭이 컸습니다.",
    "ourImpact": "아시아 전반 약세는 오늘 밤 미국장 분위기에도 부담이 될 수 있어요. 보유 TSMC(대만 반도체)도 아시아장 흐름을 같이 타니, 미국 개장 직후 가격 흐름만 가볍게 보면 좋아요.",
    "impact": "negative",
    "sources": [
      {"name": "CNBC(6/9)", "url": "https://www.cnbc.com/2026/06/09/stock-market-today-live-updates.html"},
      {"name": "Investing.com", "url": "https://www.investing.com/news/economy-news/asian-stocks-slide-oil-gains-as-middle-east-tensions-escalate-4734284"}
    ]
  }
]

# remove the now-stale morning asia item about 6/9->6/10 anticipation, keep others
new_news = []
for n in rep.get("news", []):
    h = n.get("headline", "")
    if n.get("category") == "아시아 증시" and "6/9 +8% 급반등했다가 6/10 -6%" in h:
        continue  # superseded by actual close
    new_news.append(n)
rep["news"] = asia_news + new_news

rep["session"] = "asia-close"
rep["lastUpdated"] = "2026-06-10T15:45:00+09:00"
rep["title"] = ("6/10(수) 15:45 아시아 마감 — 코스피 -4.52% 7,730.82 2거래일 만에 또 매도 사이드카·외국인 2.9조 순매도 / "
    "일본 니케이 -2%·항셍 약세 / 美 선물 약세(ES -0.5%·NQ -0.9%) / 오늘 밤 5월 CPI(예상 +4.2%)")
rep["dataQualityNote"] = (rep.get("dataQualityNote","") +
    " [15:45 아시아 마감 캡처] 코스피 종가 7,730.82(-4.52%)·외국인 수급·삼성/SK하이닉스는 이투데이·파이낸셜뉴스(6/10) 검증. "
    "코스닥 종가·니케이/항셍 정확 종가는 장중 기준(확정 대기). 美 선물은 CNBC 기준 방향성.")

save("reports/2026-06-10.json", rep)
print("OK report:", len(rep["news"]), "news items; asiaSummary set")

# =========================================================
# 2) portfolio.json — asiaCloseSnapshot
# =========================================================
pf = load("portfolio.json")
pf["asiaCloseSnapshot"] = {
  "asOf": "2026-06-10T15:45:00+09:00",
  "kospi": {"close": 7730.82, "change": -4.52, "changePoints": -366.11,
            "note": "6/10(수) -4.52% 7,730.82 마감. 6/8 이후 2거래일 만에 매도 사이드카(13:16). 외국인 2.89조·기관 0.99조 순매도, 개인 3.74조 순매수. 미군 이란 공습·AI 투자 불확실성·오늘 밤 CPI 경계."},
  "kosdaq": {"close": None, "change": None, "changePoints": None,
             "note": "코스닥도 약세(장중 940.57, -2.81%). 정확 종가는 확정 대기."},
  "asiaIndices": {
    "nikkei": {"close": None, "change": -2.0, "changePoints": None, "note": "일본 니케이 약 -2%. 일본 5월 PPI(도매물가) +6.3%로 예상(+5.5%) 상회."},
    "taiwan": {"close": None, "change": None, "changePoints": None, "note": "대만 가권 약세(TSMC 하락)."},
    "shanghai": {"close": None, "change": None, "changePoints": None, "note": "상하이 약세."},
    "hangSeng": {"close": None, "change": None, "changePoints": None, "note": "홍콩 항셍 약세 출발(선물 약 24,441)."}
  },
  "usdkrw": None,
  "usdkrwNote": "원/달러 1,525.0 상승 출발(+12.9) 후 1,514원대 회복. 주간 종가 확정 대기.",
  "samsung": {"change": -6.99, "note": "삼성전자 -6.99%(29.95만) '30만전자' 재이탈(장중)."},
  "skHynix": {"change": -8.44, "note": "SK하이닉스 -8.44%(202.8만) 급락(장중)."},
  "usFutures": {"es": None, "esChange": -0.5, "nq": None, "nqChange": -0.87,
                "note": "美 선물 약세 — ES(S&P) -0.5%·NQ(나스닥) -0.87%·다우 -0.28%. 미군 이란 공습 + 오늘 밤 21:30 5월 CPI(예상 +4.2%) 경계."}
}
pf["lastUpdated"] = "2026-06-10T15:45:00+09:00"
save("portfolio.json", pf)
print("OK portfolio asiaCloseSnapshot updated; holdings prices preserved")

# =========================================================
# 3) calendar-events.json — today asia entry
# =========================================================
cal = load("calendar-events.json")
asia_event = {
  "type": "asia", "label": "아시아 마감", "color": "blue", "mood": "🔴",
  "time": "15:45 KST 캡처",
  "title": "🔴 아시아 마감 — 코스피 -4.52% 7,730.82, 2거래일 만에 또 매도 사이드카·외국인 2.9조 순매도 / 일본 니케이 -2%·항셍 약세 / 美 선물 약세(ES -0.5%·NQ -0.9%), 오늘 밤 5월 CPI",
  "description": "6/10(수) 한국 코스피가 -4.52%(7,730.82) 급락 마감했어요. 미군의 이란 공습으로 중동 긴장이 다시 커졌고, AI 투자 불확실성(대형 데이터센터업체 크루소가 빅테크 고객 요청으로 개발 일시중단)과 오늘 밤 미국 5월 물가(CPI) 발표를 앞둔 경계심이 겹쳤어요. 외국인이 2조 9천억 원, 기관이 1조 원 가까이 팔고 개인이 3조 7천억 원을 받아내는 사이, 오후 1시 16분 매도 사이드카(급락 시 프로그램 매도를 5분간 멈추는 장치)가 6/8 이후 2거래일 만에 또 발동됐어요. 삼성전자 -6.99%(29.95만, '30만전자' 재이탈)·SK하이닉스 -8.44%(202.8만)로 반도체가 낙폭을 키웠고, 코스닥도 약세(장중 940선)였어요. 일본 니케이는 약 -2%(일본 도매물가 +6.3% 깜짝)·홍콩 항셍도 약세로 아시아가 동반 하락했어요. 원/달러는 1,525원 상승 출발 후 1,514원대로 일부 진정됐어요.",
  "impact": "아시아 전반 약세와 한국 반도체 급락은 오늘 밤 미국 시장에 부담 신호예요. 보유 반도체(엔비디아·마이크론·TSMC·SK 관련)와 흐름이 비슷해, 미국 선물도 ES -0.5%·NQ -0.9%로 약하게 출발하고 있어요. 다만 방향은 오늘 밤 21:30 발표될 5월 CPI(예상 +4.2%)가 좌우할 가능성이 커, 결과를 확인한 뒤 흐름을 가볍게 지켜보면 좋아요."
}
day = cal["stock"].get("2026-06-10", [])
# avoid duplicate asia entry on re-run
day = [e for e in day if not (e.get("type") == "asia" and e.get("time") == "15:45 KST 캡처")]
day.append(asia_event)
cal["stock"]["2026-06-10"] = day
cal["lastUpdated"] = "2026-06-10T15:45:00+09:00"
save("calendar-events.json", cal)
print("OK calendar: 2026-06-10 entries =", len(cal["stock"]["2026-06-10"]))

# =========================================================
# 4) reports/index.json — refresh 6/10 entry title/summary
# =========================================================
idx = load("reports/index.json")
for r in idx.get("reports", []):
    if r.get("date") == "2026-06-10":
        r["title"] = "6월 10일 (수) 아시아 마감 — 코스피 -4.52% 7,730.82 또 사이드카"
        r["summary"] = "코스피 -4.52%(7,730.82) 2거래일 만에 또 매도 사이드카·외국인 2.9조 순매도, 일본 니케이 -2%, 美 선물 약세, 오늘 밤 5월 CPI(예상 +4.2%)"
        break
idx["lastUpdated"] = "2026-06-10T15:45:00+09:00"
save("reports/index.json", idx)
print("OK index updated")
