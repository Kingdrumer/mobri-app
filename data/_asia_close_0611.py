# -*- coding: utf-8 -*-
# Mobri 15:45 KST 아시아 마감 라이트 업데이트 — 2026-06-11
import json, shutil, os

BASE = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(BASE, *a)

ASOF = "2026-06-11T15:45:00+09:00"

# ---------- sources ----------
SRC_YNA = {"name": "연합뉴스", "url": "https://www.yna.co.kr/view/PYH20260611163700013"}
SRC_CHOSUN = {"name": "조선비즈", "url": "https://biz.chosun.com/stock/stock_general/2026/06/11/Y2TPMW7ICVCWHMGG4SDXDJEC7U/"}
SRC_HANKOOKI = {"name": "한국일보", "url": "https://weekly.hankooki.com/news/articleView.html?idxno=7168935"}
SRC_SBS = {"name": "SBS Biz", "url": "https://biz.sbs.co.kr/article_hub/20000315974"}
SRC_KBS = {"name": "KBS", "url": "https://news.kbs.co.kr/news/pc/view/view.do?ncd=8584035"}

# ---------- new Asia news items (prepend) ----------
asia_news = [
    {
        "category": "아시아 증시",
        "headline": "코스피 롤러코스터 끝 +0.43% 7,763.95 마감 — 코스닥은 +4.76% 급등",
        "oneLineSummary": "오늘 한국 코스피는 미국 물가 충격과 중동 긴장에 장 초반 4% 넘게 빠졌다가, 오후 들어 반도체가 살아나며 결국 +0.43%(7,763.95)로 올라서 마감했어요. 특히 중소형 반도체·소부장(장비·소재) 회사가 많은 코스닥은 +4.76%(996.93) 급등하며 1,000선을 코앞에 뒀어요.",
        "summary": "코스피는 6/11 전장보다 +33.13p(+0.43%) 오른 7,763.95로 마감했어요. 7,509.62(-2.86%)로 급락 출발해 장중 4% 넘게 밀렸지만 오후 반도체 반등에 상승 전환했어요(오늘은 선물·옵션이 한꺼번에 만기를 맞는 '네 마녀의 날'). 코스닥은 +4.76% 996.93로 급등했고, SK하이닉스는 +2%대로 200만원을 회복, 삼성전자는 1%대 약세로 30만원을 밑돌았어요. 외국인은 순매도를 이어갔고 기관·개인이 받아냈습니다.",
        "ourImpact": "한국 반도체가 오후에 살아난 건 보유 반도체(NVDA(엔비디아)·MU(마이크론)·AVGO(브로드컴)·MRVL(마벨)) 투자심리에 우호적인 신호예요. 다만 외국인 매도가 이어지는 만큼 오늘 밤 미국 개장 흐름만 가볍게 지켜보면 좋아요.",
        "impact": "positive",
        "sources": [SRC_YNA, SRC_CHOSUN],
    },
    {
        "category": "개별 종목",
        "headline": "韓 SK하이닉스 +2%·200만원 회복 / 삼성전자 1%대 약세 — 반도체 소부장 강세",
        "oneLineSummary": "한국 대표 메모리 반도체 SK하이닉스가 오후에 +2% 넘게 오르며 주가 200만 원대를 회복했어요. 삼성전자는 1% 넘게 빠져 30만 원을 못 넘었지만, 중소형 반도체 장비·소재(소부장) 주식들이 일제히 오르며 코스닥을 +4.76%까지 끌어올렸어요.",
        "summary": "장 초반 부진했던 SK하이닉스가 오후 +2%대 반등으로 200만원을 회복했고, 알테오젠 등 바이오·소부장도 강세를 보이며 코스닥 +4.76% 급등을 이끌었어요. 삼성전자는 -1%대로 30만원을 회복하지 못했습니다. AI·메모리 수급 기대가 여전히 살아있다는 신호로 풀이됩니다.",
        "ourImpact": "한국 메모리(SK하이닉스)·소부장 강세는 보유 마이크론(MU)·브로드컴(AVGO)·마벨(MRVL)의 분위기에 참고가 돼요. 종목별 온도차가 크니 개별 흐름을 나눠 보면 좋아요.",
        "impact": "positive",
        "sources": [SRC_HANKOOKI, SRC_SBS],
    },
]

new_asia_summary = (
    "코스피 7,763.95(+0.43%·+33.13)로 강보합 마감 — 7,509.62(-2.86%) 급락 출발 후 장중 4%대 하락했다가 "
    "오후 반도체 반등에 상승 전환(네 마녀의 날·선물옵션 동시 만기). 코스닥 996.93(+4.76%·+45.30) 급등, 1,000선 목전. "
    "SK하이닉스 +2%대 200만원 회복·삼성전자 -1%대 30만원 밑. 외국인 순매도 지속, 기관·개인 순매수. 원/달러 1,530원 턱밑. "
    "일본 니케이는 전일 -1.89%(64,179)로 마감한 아시아 약세 흐름 속, 한국만 오후 반등에 성공. "
    "미국 선물(ES·NQ)은 韓 장중 낙폭 축소와 함께 안정 시도(정확 수치 미확보)."
)

# ---------- 1. reports/2026-06-11.json ----------
rep_path = p("reports", "2026-06-11.json")
shutil.copy(rep_path, rep_path + ".before-asia-close-0611.bak")
rep = json.load(open(rep_path, encoding="utf-8"))
rep["news"] = asia_news + rep.get("news", [])
rep["asiaSummary"] = new_asia_summary
rep["lastUpdated"] = ASOF
rep["dataQualityNote"] = (
    rep.get("dataQualityNote", "")
    + " | [15:45 아시아 마감 캡처] 코스피·코스닥 종가는 연합뉴스·조선비즈·한국일보·SBS Biz·KBS 교차 검증(7,763.95/996.93). "
    "니케이 6/11 종가·홍콩 항셍 종가·미국 ES/NQ 선물 정확 수치는 라이트 캡처 시점 미확보로 방향성만 기재."
)
json.dump(rep, open(rep_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK reports/2026-06-11.json — news:", len(rep["news"]))

# ---------- 2. portfolio.json ----------
pf_path = p("portfolio.json")
shutil.copy(pf_path, pf_path + ".before-asia-close-0611.bak")
pf = json.load(open(pf_path, encoding="utf-8"))
USER_MEMO_BEFORE = pf.get("userMemo", "__MISSING__")  # preserve as-is

pf["asiaCloseSnapshot"] = {
    "asOf": ASOF,
    "kospi": {"close": 7763.95, "change": 0.43, "changePoints": 33.13,
              "note": "6/11(목) +0.43% 7,763.95 마감. 7,509.62(-2.86%) 급락 출발 후 장중 4%대 하락, 오후 반도체 반등에 상승 전환. 선물·옵션 동시 만기(네 마녀의 날). 외국인 순매도, 기관·개인 순매수."},
    "kosdaq": {"close": 996.93, "change": 4.76, "changePoints": 45.30,
               "note": "코스닥 +4.76% 996.93 급등 — 반도체 소부장·바이오 강세로 1,000선 목전."},
    "asiaIndices": {
        "nikkei": {"close": 64179, "change": -1.89, "changePoints": None,
                   "note": "일본 니케이 전일(6/10) -1.89% 64,179 마감. 6/11 종가 라이트 캡처 시점 미확보."},
        "topix": {"close": None, "change": None, "changePoints": None,
                  "note": "토픽스 전일 -1.25% 3,848. 6/11 미확보."},
        "taiwan": {"close": None, "change": None, "changePoints": None, "note": "대만 가권 6/11 종가 미확보."},
        "shanghai": {"close": None, "change": None, "changePoints": None, "note": "상하이 6/11 종가 미확보."},
        "hangSeng": {"close": None, "change": None, "changePoints": None, "note": "홍콩 항셍 전일 24,408. 6/11 장중·종가 미확보."},
    },
    "usdkrw": None,
    "usdkrwNote": "원/달러 1,530원 턱밑(전일 대비 상승). 주간 종가 정확치 미확보.",
    "samsung": {"change": -1.2, "note": "삼성전자 -1%대 약세, 30만원 회복 실패(장중)."},
    "skHynix": {"change": 2.0, "note": "SK하이닉스 +2%대 반등, 200만원 회복(장중)."},
    "usFutures": {"es": None, "esChange": None, "nq": None, "nqChange": None,
                  "note": "미국 선물(ES·NQ)은 한국 장중 낙폭 축소와 함께 안정 시도. 정확 수치 라이트 캡처 시점 미확보."},
}
pf["lastUpdated"] = ASOF
# preserve userMemo exactly
if USER_MEMO_BEFORE != "__MISSING__":
    pf["userMemo"] = USER_MEMO_BEFORE
json.dump(pf, open(pf_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK portfolio.json — userMemo preserved:", USER_MEMO_BEFORE)

# ---------- 3. calendar-events.json ----------
cal_path = p("calendar-events.json")
shutil.copy(cal_path, cal_path + ".before-asia-close-0611.bak")
cal = json.load(open(cal_path, encoding="utf-8"))
asia_event = {
    "type": "asia",
    "label": "아시아 마감",
    "color": "blue",
    "time": "15:45 KST",
    "title": "코스피 롤러코스터 끝 +0.43% 7,763.95 마감 · 코스닥 +4.76% 급등",
    "description": "장 초반 4% 넘게 빠졌던 코스피가 오후 반도체 반등에 상승 전환해 7,763.95(+0.43%)로 마감했고, 코스닥은 +4.76%(996.93) 급등했습니다. 오늘은 선물·옵션이 한꺼번에 만기를 맞는 '네 마녀의 날'이었습니다.",
    "impact": "오후 들어 한국 반도체가 살아나면서 지수가 마이너스에서 플러스로 돌아섰습니다. 특히 중소형 반도체 장비·소재(소부장) 종목이 몰린 코스닥이 +4.76%나 올라 1,000선에 바짝 다가섰습니다. 외국인은 계속 팔았지만 기관과 개인이 받아내며 낙폭을 메웠습니다.",
    "ourImpact": "한국 메모리·반도체가 오후에 반등한 건 보유 반도체(NVDA·MU·AVGO·MRVL)의 투자심리에 우호적인 신호입니다. 다만 외국인 매도가 이어지는 만큼 오늘 밤 미국 개장 흐름만 가볍게 지켜보면 됩니다.",
    "stockImpacts": [
        {"ticker": "000660", "tone": "positive", "magnitude": "+2%대", "text": "SK하이닉스 오후 반등, 200만원 회복 — 코스피 상승 전환 견인"},
        {"ticker": "005930", "tone": "negative", "magnitude": "-1%대", "text": "삼성전자 약세, 30만원 회복 실패"},
        {"ticker": "KOSDAQ", "tone": "positive", "magnitude": "+4.76%", "text": "반도체 소부장·바이오 강세로 996.93, 1,000선 목전"},
    ],
}
day = cal["stock"].get("2026-06-11", [])
day.insert(0, asia_event)   # prepend latest
cal["stock"]["2026-06-11"] = day
cal["lastUpdated"] = ASOF
json.dump(cal, open(cal_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK calendar-events.json — 2026-06-11 events:", len(day))

# ---------- 4. reports/index.json (append asia note to today summary) ----------
idx_path = p("reports", "index.json")
shutil.copy(idx_path, idx_path + ".before-asia-close-0611.bak")
idx = json.load(open(idx_path, encoding="utf-8"))
for r in idx.get("reports", []):
    if r.get("date") == "2026-06-11":
        if "[15:45 아시아]" not in r.get("summary", ""):
            r["summary"] = r.get("summary", "") + " [15:45 아시아] 코스피 +0.43% 7,763.95·코스닥 +4.76% 996.93 마감(장중 4%대 급락 후 오후 반도체 반등)."
        break
idx["lastUpdated"] = ASOF
json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("OK reports/index.json")
print("DONE")
