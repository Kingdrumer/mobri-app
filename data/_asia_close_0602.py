# -*- coding: utf-8 -*-
import json, shutil, os

D = os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(D, *a)

ASOF = "2026-06-02T15:45:00+09:00"

# ---------- backups ----------
for f in ["portfolio.json", "calendar-events.json"]:
    shutil.copy(p(f), p(f + ".before-asia-close.bak"))

# ============================================================
# NEWS (categorized, max 2 each, 3-field required)
# ============================================================
news = [
  # ----- 1. 미국 증시 -----
  {
    "category": "미국 증시",
    "headline": "美 3대 지수 또 사상 최고(6/1) — 나스닥 첫 27,000 돌파",
    "oneLineSummary": "간밤(한국시간 6/1 밤~2일 새벽) 미국 S&P500이 +0.3% 올라 7,599.96, 나스닥은 +0.4% 올라 처음으로 27,000선을 넘은 27,086.81로 마감했어요. AI 반도체와 에너지(유가 상승) 종목이 끌어올리며 두 지수 모두 또 사상 최고예요.",
    "summary": "6/1(현지) 미국 증시는 S&P500 7,599.96(+0.26%)·나스닥 27,086.81(+0.42%)로 두 지수 모두 종가 기준 사상 최고를 경신했습니다. 나스닥은 처음으로 27,000선을 넘었고, 필라델피아 반도체지수도 +1.06% 강세였습니다. AI 인프라·반도체주와 유가 급등에 따른 에너지주가 상승을 견인했습니다.",
    "ourImpact": "보유 반도체·AI 종목(NVDA·AVGO·MU·MRVL·TSM·AMD)에 좋은 분위기예요. 다만 이미 많이 오른 자리라, 오늘 밤 미국 개장 후 흐름이 이어지는지만 가볍게 보면 좋아요.",
    "impact": "positive",
    "sources": [{"name": "TheStreet (6/1)", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-01-2026"},
                {"name": "뉴스탑코리아", "url": "https://www.newstopkorea.com/news/articleView.html?idxno=45268"}]
  },
  {
    "category": "미국 증시",
    "headline": "美 선물 소폭 하락 — 사상 최고 뒤 숨고르기",
    "oneLineSummary": "오늘 아시아 시간대에 미국 S&P500 선물(개장 전 분위기)이 -0.2%, 나스닥100 선물도 약보합으로 살짝 밀렸어요. 어제 사상 최고를 찍은 뒤라 잠깐 쉬어가는 분위기예요. 큰 악재라기보다 '오른 김에 일부 파는' 차익실현 성격이에요.",
    "summary": "6/2 아시아 거래 시간대 미국 야간 선물은 S&P500 선물 약 -0.24%, 나스닥100 선물 약보합으로 소폭 하락했습니다. 전일 3대 지수 사상 최고 마감 이후의 숨고르기·차익실현 성격으로 해석됩니다. 정규장은 한국시간 오늘 밤 22:30 개장합니다.",
    "ourImpact": "선물이 살짝 밀렸지만 폭은 작아요. 오늘 밤 미국 개장 때 보유 종목들이 약하게 출발할 수 있다는 정도만 미리 알아두면 충분해요.",
    "impact": "neutral",
    "sources": [{"name": "한국경제 글로벌마켓", "url": "https://n.news.naver.com/mnews/article/215/0001254054?sid=101"}]
  },
  # ----- 2. 아시아 증시 -----
  {
    "category": "아시아 증시",
    "headline": "코스피 또 사상 최고 마감 +0.15% 8,801.49",
    "oneLineSummary": "오늘 한국 코스피가 장중에 8,900선까지 갔다가 8,500선까지 출렁인 끝에 +0.15%(+13.11p) 오른 8,801.49로 또 사상 최고로 마감했어요. 외국인이 6조 원 넘게(역대 3번째 규모) 팔았지만, 개인·기관이 받아내며 신고가를 지켰어요.",
    "summary": "코스피는 6/2 장중 8,900선 돌파 후 8,500선까지 밀리는 변동성 장세 끝에 전일 대비 +13.11p(+0.15%) 오른 8,801.49로 종가 기준 사상 최고를 다시 경신했습니다. 외국인이 약 6.6조 원(역대 3번째 규모)·18거래일 연속 순매도했지만 개인·기관 매수가 이를 흡수했습니다. 코스닥은 대형 반도체 쏠림에 따른 중소형주 차익실현으로 약 2~3% 하락해 1,050선 부근에서 마감했습니다.",
    "ourImpact": "외국인이 크게 팔아도 지수가 신고가일 만큼 한국 반도체 쪽 매수세가 강해요. 이 열기는 보유 반도체주에 우호적 신호지만, 변동성이 큰 하루였던 점은 참고하면 좋아요.",
    "impact": "positive",
    "sources": [{"name": "뉴스1 (6/2)", "url": "https://www.news1.kr/finance/general-stock/6185265"},
                {"name": "YTN (6/2)", "url": "https://www.ytn.co.kr/_ln/0102_202606021633058161"}]
  },
  {
    "category": "아시아 증시",
    "headline": "니케이 -1.3%·항셍·상해 보합 — 아시아 혼조",
    "oneLineSummary": "오늘 일본 니케이225는 -1.3% 내렸고, 홍콩 항셍과 중국 상해종합은 +0.1% 안팎 보합으로 마감했어요. 한국만 반도체 힘으로 신고가였고, 나머지 아시아 시장은 방향 없이 엇갈린 하루였어요.",
    "summary": "6/2 아시아 증시는 혼조였습니다. 일본 니케이225 약 -1.3%, 홍콩 항셍지수 약 +0.1%, 중국 상해종합(CSI300 기준) 약 +0.1%로 보합권에 머물렀고, 호주 ASX200도 약세였습니다. 한국 코스피만 반도체 강세에 힘입어 사상 최고를 기록하며 차별화된 흐름을 보였습니다.",
    "ourImpact": "아시아 전반은 잠잠했고 한국 반도체만 뜨거웠어요. 미국 반도체 포트폴리오엔 한국 쪽 온도가 더 직접적인 신호라, 일본·중국 약세는 크게 신경 쓰지 않아도 돼요.",
    "impact": "neutral",
    "sources": [{"name": "CNBC Asia (6/2)", "url": "https://www.cnbc.com/2026/06/02/asia-pacific-markets-today-kospi-nikkei-225-hang-seng-index.html"}]
  },
  # ----- 3. 개별 종목 -----
  {
    "category": "개별 종목",
    "headline": "삼성전자 +3.3% 또 신고가 — HBM4E 첫 공급 호재",
    "oneLineSummary": "삼성전자가 오늘 +3.3% 올라 360,500원으로 또 신고가를 썼어요. 세계 첫 HBM4E(AI에 쓰는 초고속 메모리) 공급 소식이 이어진 덕분이에요. 엔비디아가 컴퓨텍스 2026에서 AI 노트북·CPU 진출을 발표하며 반도체 열기를 더 키웠어요.",
    "summary": "삼성전자는 6/2 +3.30% 오른 360,500원으로 2018년 액면분할 이후 종가 최고가를 경신했습니다(시총 2,000조 원대 유지). HBM4E 최초 공급 호재가 이어졌고, 엔비디아가 컴퓨텍스 2026에서 AI 노트북·CPU 시장 진출을 발표하며 반도체 전반의 투자심리를 끌어올렸습니다. 다만 SK하이닉스는 -0.13% 약보합으로 마감했습니다.",
    "ourImpact": "삼성 HBM4E·엔비디아 신제품 소식은 보유 메모리·반도체주(MU(마이크론)·NVDA(엔비디아)·AVGO(브로드컴)·MRVL(마벨)·TSM)에 좋은 읽을거리예요. 오늘 밤 미국 반도체주 출발을 가볍게 지켜보면 좋아요.",
    "impact": "positive",
    "sources": [{"name": "연합뉴스 (6/2)", "url": "https://www.yna.co.kr/view/AKR20260602043951008"},
                {"name": "전남일보 (6/2)", "url": "https://www.jnilbo.com/news/articleView.html?idxno=90000039349"}]
  },
  {
    "category": "개별 종목",
    "headline": "구글(GOOG) 약 120조 원 초대형 유상증자 — 반도체 랠리 변수",
    "oneLineSummary": "보유 종목인 구글(알파벳)이 약 120조 원 규모의 초대형 유상증자(회사가 새 주식을 찍어 돈을 모으는 것)를 발표했어요. AI 투자 자금을 모으려는 거지만, 주식 수가 늘면 기존 주주 몫이 옅어질 수 있어 반도체 랠리에 돌발 변수로 거론됐어요.",
    "summary": "알파벳(구글)이 약 120조 원 규모의 초대형 유상증자 계획을 발표했습니다. AI·인프라 투자 재원 확보 목적으로 풀이되지만, 대규모 신주 발행은 주당 가치 희석 우려가 있어 시장에서는 진행 중이던 반도체·AI 랠리의 돌발 변수로 받아들였습니다.",
    "ourImpact": "보유 종목인 GOOG(구글)에 직접 영향이 있는 소식이에요. 자금조달 자체는 AI 투자 확대 신호지만, 주식 수 증가에 시장이 어떻게 반응하는지 오늘 밤 개장 흐름을 지켜보면 좋아요.",
    "impact": "neutral",
    "sources": [{"name": "한국경제 글로벌마켓 (6/2)", "url": "https://n.news.naver.com/mnews/article/215/0001254054?sid=101"}]
  },
  # ----- 4. 정책·금리 -----
  {
    "category": "정책·금리",
    "headline": "이번 주 美 고용지표 줄줄이 — 금요일 NFP가 고비",
    "oneLineSummary": "이번 주는 미국 고용지표가 줄줄이 나오는 '빅위크'예요. 화요일 제조업·구인 지표를 시작으로 금요일 고용보고서(NFP, 한 달간 일자리가 얼마나 늘었는지)가 핵심이에요. 이 숫자가 금리 인하 기대에 영향을 줘서 증시 방향을 흔들 수 있어요.",
    "summary": "이번 주 미국은 ISM 제조업 PMI·JOLTS 구인 등에 이어 금요일 5월 비농업 고용보고서(NFP)가 예정돼 있어 고용 '빅위크'로 꼽힙니다. 고용 강도가 Fed의 금리 경로 기대에 직접 영향을 주는 만큼, 지표 결과에 따라 사상 최고 부근 증시의 변동성이 커질 수 있습니다.",
    "ourImpact": "고용지표는 기술주 전반의 금리 민감도에 영향을 줘요. 금요일 NFP 전까지는 큰 베팅보다 흐름을 지켜보는 구간이라고 알아두면 좋아요.",
    "impact": "neutral",
    "sources": [{"name": "뉴시스 (6/2)", "url": "https://n.news.naver.com/mnews/article/003/0013980929?sid=101"}]
  },
  # ----- 5. 글로벌·지정학 -----
  {
    "category": "글로벌·지정학",
    "headline": "트럼프-이란 호르무즈 합의 기대 vs 이란 '협상 중단' 위협 — 유가 변수",
    "oneLineSummary": "트럼프 대통령이 일주일 안에 이란과 휴전 연장·호르무즈 해협(원유가 많이 지나는 길목) 재개방에 합의할 수 있다는 관측이 나왔어요. 반면 이란은 비공식 협상 중단과 해협 폐쇄를 위협해, 국제 유가가 출렁이는 변수로 남아 있어요.",
    "summary": "트럼프 대통령이 향후 1주일 내 이란과 휴전 연장 및 호르무즈 해협 재개방 합의 가능성을 시사했지만, 이란은 미국과의 비공식 협상 중단과 해협 폐쇄를 거론하며 맞서고 있습니다. 불확실성에 국제 유가가 급등락하며 에너지·운송·물가 경로의 변수로 작용하고 있습니다.",
    "ourImpact": "유가가 오르면 보유 전력주 TLN(탈렌에너지) 같은 에너지 쪽엔 우호적일 수 있어요. 다만 유가 급등은 물가·금리 부담으로 기술주엔 양날의 검이라, 합의 소식 여부를 지켜보면 좋아요.",
    "impact": "neutral",
    "sources": [{"name": "뉴시스 (6/2)", "url": "https://n.news.naver.com/mnews/article/003/0013980929?sid=101"},
                {"name": "연합뉴스 마켓뷰 (6/2)", "url": "https://n.news.naver.com/mnews/article/001/0016112945?sid=101"}]
  },
]

# ============================================================
# asiaSummary
# ============================================================
asiaSummary = {
  "asOf": ASOF,
  "kospi": {"close": 8801.49, "change": 0.15, "changePoints": 13.11,
            "note": "6/2 변동성 장세(장중 8,900 돌파 후 8,500선까지) 끝에 +0.15%(+13.11p) 8,801.49 종가 사상 최고 재경신. 외국인 약 6.6조 원(역대 3번째)·18거래일 연속 순매도에도 개인·기관이 흡수하며 신고가 방어."},
  "kosdaq": {"close": None, "change": -2.3, "changePoints": None,
             "note": "대형 반도체 쏠림에 따른 중소형주 차익실현으로 약 2~3% 하락, 1,050선 부근 약세 마감."},
  "usdkrw": 1508.0,
  "samsung": {"change": 3.30, "note": "삼성전자 +3.30% 360,500원 신고가(2018년 액면분할 이후 종가 최고) — 세계 첫 HBM4E 공급 호재 지속, 시총 2,000조 원대 유지."},
  "skHynix": {"change": -0.13, "note": "SK하이닉스 -0.13% 약보합 2,360,000원 — 전일 급등 후 숨고르기."},
  "asia": {"nikkei": "약 -1.3%", "hangSeng": "약 +0.1%", "csi300": "약 +0.1%", "note": "한국만 반도체 힘으로 신고가, 나머지 아시아는 혼조."},
  "usFutures": {"es": None, "esChange": -0.24, "nq": None, "nqChange": None,
                "note": "美 야간 선물 S&P500 약 -0.24%·나스닥100 약보합으로 소폭 하락 — 사상 최고 뒤 숨고르기. 美 정규장 22:30 KST 개장 대기."}
}

# ============================================================
# 1) reports/2026-06-02.json
# ============================================================
tmpl = json.load(open(p("reports", "2026-06-01.json"), encoding="utf-8"))
rep = dict(tmpl)  # carry stockSnapshot/signals forward (US prices unchanged pre-open)
rep["date"] = "2026-06-02"
rep["session"] = "tue-asia-close"
rep["title"] = "6/2(화) 아시아 마감 — 코스피 또 사상 최고 8,801.49(+0.15%), 외국인 6.6조 매도에도 개인·기관 방어, 美 증시 오늘 밤 22:30 개장"
rep["marketStatus"] = ("6/2(화) 15:45 KST 아시아 마감 캡처 — 코스피가 장중 8,900선까지 올랐다가 8,500선까지 밀리는 출렁임 끝에 +0.15%(+13.11p) 8,801.49로 또 사상 최고로 마감했어요. "
  "외국인이 약 6조6천억 원(역대 3번째 규모)·18거래일 연속 팔았지만 개인·기관이 받아내며 신고가를 지켰어요. 삼성전자는 +3.3% 360,500원 신고가(HBM4E 첫 공급 호재)였고, SK하이닉스는 -0.13% 약보합이었어요. "
  "코스닥은 중소형주 차익실현으로 약 2~3% 내려 1,050선 부근이었어요. 일본 니케이는 -1.3%, 홍콩 항셍·중국 상해는 +0.1% 안팎 보합으로 아시아는 혼조였어요. "
  "미국은 간밤 S&P500 7,599.96(+0.26%)·나스닥 27,086.81(+0.42%, 첫 27,000 돌파) 또 사상 최고로 마감했고, 오늘 아시아 시간대 미국 선물은 -0.2%대로 살짝 숨고르기예요. 美 정규장은 오늘 밤 22:30 KST 개장합니다.")
rep["lastUpdated"] = ASOF
rep["generatedAt"] = ASOF
rep["news"] = news
rep["asiaSummary"] = asiaSummary
# update stockSnapshot dataQualityNote to reflect pre-open state
if isinstance(rep.get("stockSnapshot"), list):
    for s in rep["stockSnapshot"]:
        s["dataQualityNote"] = "6/2(화) 아시아 마감 시점 — 美 정규장 개장 전(22:30 KST). 가격은 6/1(월) 美 종가 그대로, 변동 없음."
json.dump(rep, open(p("reports", "2026-06-02.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote reports/2026-06-02.json, news items:", len(news))

# ============================================================
# 2) portfolio.json — update asiaCloseSnapshot, marketStatus, lastUpdated (preserve userMemo + US prices)
# ============================================================
pf = json.load(open(p("portfolio.json"), encoding="utf-8"))
memo_before = pf.get("userMemo", "")
pf["asiaCloseSnapshot"] = {
  "asOf": ASOF,
  "kospi": {"close": 8801.49, "change": 0.15, "changePoints": 13.11,
            "note": "6/2(화) 또 사상 최고 8,801.49(+0.15%). 외국인 약 6.6조(역대 3번째)·18거래일 연속 순매도에도 개인·기관 방어. 장중 8,900~8,500 변동성."},
  "kosdaq": {"close": None, "change": -2.3, "changePoints": None, "note": "중소형주 차익실현 약 2~3% 하락, 1,050선 부근."},
  "usdkrw": 1508.0,
  "samsung": {"change": 3.30, "note": "삼성전자 +3.30% 360,500원 신고가 — HBM4E 첫 공급 호재."},
  "skHynix": {"change": -0.13, "note": "SK하이닉스 -0.13% 약보합 — 전일 급등 후 숨고르기."},
  "usFutures": {"es": None, "esChange": -0.24, "nq": None, "nqChange": None,
                "note": "美 야간 선물 S&P500 -0.24%·나스닥100 약보합 소폭 하락. 22:30 KST 개장 대기."}
}
pf["marketStatus"] = rep["marketStatus"]
pf["lastUpdated"] = ASOF
assert pf.get("userMemo", "") == memo_before, "userMemo changed!"
json.dump(pf, open(p("portfolio.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("updated portfolio.json (userMemo preserved:", repr(memo_before[:30]), ")")

# ============================================================
# 3) calendar-events.json — add today's asia event
# ============================================================
cal = json.load(open(p("calendar-events.json"), encoding="utf-8"))
ev = {
  "type": "asia",
  "label": "아시아 마감 — 코스피 또 사상 최고 8,801.49 (+0.15%)",
  "color": "blue",
  "time": "15:45 KST",
  "title": "🟢 코스피 또 사상 최고 마감 8,801.49 (+0.15%, +13.11p) — 외국인 6.6조 매도(역대 3번째)에도 개인·기관 방어, 삼성전자 +3.3% 신고가",
  "description": ("오늘 한국 코스피가 장중 8,900선까지 올랐다가 8,500선까지 밀리는 출렁임 끝에 +0.15%(+13.11p) 8,801.49로 또 사상 최고로 마감했어요. "
    "외국인이 약 6조6천억 원(역대 3번째 규모)·18거래일 연속 팔았지만 개인·기관이 받아내며 신고가를 지켰어요. 삼성전자는 +3.3% 360,500원 신고가(HBM4E 첫 공급 호재), SK하이닉스는 -0.13% 약보합이었어요. "
    "코스닥은 중소형주 차익실현으로 약 2~3% 내려 1,050선 부근. 일본 니케이 -1.3%, 홍콩 항셍·중국 상해는 +0.1% 안팎 보합으로 아시아는 혼조였어요. "
    "미국은 간밤 또 사상 최고(나스닥 첫 27,000 돌파)였고, 오늘 아시아 시간대 미국 선물은 -0.2%대 숨고르기예요. 美 정규장은 오늘 밤 22:30 KST 개장합니다.")
}
cal.setdefault("stock", {})
existing = cal["stock"].get("2026-06-02")
if isinstance(existing, list):
    existing.insert(0, ev)
else:
    cal["stock"]["2026-06-02"] = [ev]
cal["lastUpdated"] = ASOF
json.dump(cal, open(p("calendar-events.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("updated calendar-events.json 2026-06-02")

# ============================================================
# 4) reports/index.json — add 2026-06-02 entry
# ============================================================
idx = json.load(open(p("reports", "index.json"), encoding="utf-8"))
entry = {"date": "2026-06-02",
         "title": "6월 2일 (화) 아시아 마감 — 코스피 또 사상 최고 8,801.49",
         "summary": "코스피 +0.15% 8,801.49 사상 최고, 외국인 6.6조 매도에도 개인·기관 방어. 삼성전자 +3.3% 신고가, 코스닥 약세. 美 나스닥 첫 27,000 돌파."}
reports_list = idx.get("reports", [])
reports_list = [r for r in reports_list if r.get("date") != "2026-06-02"]
reports_list.append(entry)
reports_list.sort(key=lambda r: r.get("date", ""))
idx["reports"] = reports_list
idx["lastUpdated"] = ASOF
json.dump(idx, open(p("reports", "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("updated reports/index.json, total reports:", len(reports_list))
print("DONE")
