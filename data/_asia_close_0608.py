# -*- coding: utf-8 -*-
import json, io, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
def rd(p):
    with io.open(p, encoding='utf-8') as f: return json.load(f)
def wr(p, d):
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

asOf = "2026-06-08T15:45:00+09:00"
genAt = "2026-06-08T15:45:00+09:00"

# ---------- NEWS (카테고리 순서, 카테고리당 최대 2개, 아시아 prepend) ----------
news = [
  # ===== 아시아 증시 =====
  {
    "category": "아시아 증시",
    "headline": "'검은 월요일' 코스피 -8.29% 7,484 — 서킷브레이커 발동",
    "oneLineSummary": "오늘 한국 코스피가 -8.29%(-676포인트) 떨어진 7,484.41로 마감했어요. 개장 직후 8% 넘게 빠지면서 거래를 20분간 멈추는 '서킷브레이커'까지 걸렸어요. 지난 금요일 미국 반도체가 폭락한 충격이 그대로 옮겨붙었고, 외국인과 기관이 합쳐서 2조 원 넘게 팔아치우면서 지수를 끌어내렸어요.",
    "summary": "6/8(월) 코스피는 -8.29%(-676.18p) 7,484.41로 마감했어요. 장 초반 한때 -8.4%(7,442.73)까지 밀려 오전 9시 3분 서킷브레이커(20분 매매중지)가 발동됐고, 코스닥도 사이드카가 걸렸어요. 하락률은 역대 9위 수준. 외국인이 코스피에서 약 2,766억 원, 기관이 약 1조9,422억 원을 순매도했고, 개인이 1조9,478억 원을 받아냈어요. 원/달러 환율은 1,535~1,555원까지 치솟았어요.",
    "ourImpact": "한국 반도체 폭락은 오늘 밤 미국 반도체(NVDA·AVGO·MU·MRVL·TSM) 프리마켓(정규장 전 거래)에 약세 신호로 작용할 수 있어요. 다만 패닉성 급락이라, 개장 직후 가격 흐름만 차분히 지켜보면 좋아요.",
    "impact": "negative",
    "sources": [
      {"name": "시대일보(마감시황)", "url": "https://n.news.naver.com/mnews/article/417/0001146651?sid=101"},
      {"name": "이데일리", "url": "https://n.news.naver.com/mnews/article/018/0006300871?sid=101"}
    ]
  },
  {
    "category": "아시아 증시",
    "headline": "아시아 동반 급락 — 코스닥 -9.1%·니케이 -3.9%·대만 -3.5%",
    "oneLineSummary": "한국뿐 아니라 아시아 시장이 다 같이 내렸어요. 코스닥은 -9.08%(911.39)로 더 크게 빠졌고, 일본 니케이는 -3.9%대(약 64,000), 대만 가권 -3.5%, 홍콩 항셍 -1.2% 수준이었어요. 지난주 미국 반도체 폭락에 더해, 이란-이스라엘 충돌로 기름값이 오른 게 아시아 전체 투자 심리를 얼어붙게 만들었어요.",
    "summary": "6/8 아시아 증시가 동반 급락했어요. 코스닥 -9.08%(911.39)로 사이드카 발동, 일본 니케이225는 약 -3.9%(64,000선)로 키오시아 -10%·소프트뱅크 -8.6% 등 기술주가 무너졌어요. 대만 가권 -3.5%, 홍콩 항셍 -1.2% 수준(장중·마감 시점차)이었어요. 미국 반도체 약세 + 이란발 유가 급등 + 미 금리 상승 우려가 겹친 위험회피 장세였어요.",
    "ourImpact": "일본·대만의 반도체주(키오시아·TSMC) 약세는 보유 TSM·MU 같은 메모리·파운드리 종목과 같은 흐름이에요. 아시아 전반이 위험회피라, 오늘 밤 미국도 변동성이 클 수 있어 관망이 편해요.",
    "impact": "negative",
    "sources": [
      {"name": "아주경제(마감)", "url": "https://www.ajunews.com/view/20260608152443588"},
      {"name": "TradingKey(Nikkei)", "url": "https://www.tradingkey.com/analysis/stocks/more/261951483-nikkei225-semiconductor-selloff-fed-hike-usdjpy-outflow-boj-policy-tradingkey"}
    ]
  },
  # ===== 개별 종목 =====
  {
    "category": "개별 종목",
    "headline": "젠슨 황 방한 \"AI 수요 여전히 강력…급락은 곧 할인된 가격\"",
    "oneLineSummary": "엔비디아 CEO 젠슨 황이 방한 마지막 날인 오늘, 폭락장에 대해 \"전 세계 AI 수요는 여전히 강력하고, 급락은 곧 할인된 가격\"이라고 말했어요. SK하이닉스와는 차세대 AI 컴퓨터 '베라 루빈'용 HBM(고대역폭 메모리) 협력을 확인했어요. 삼성·SK·현대차·LG와 잇따라 만나며 AI 동맹을 다졌어요.",
    "summary": "방한 마지막 날 젠슨 황 엔비디아 CEO가 SK·삼성·현대차·LG 총수들과 연쇄 회동하며 AI 협력을 확대했어요. SK하이닉스는 엔비디아 차세대 AI 슈퍼컴 '베라 루빈'의 HBM 공급사로 부각됐고, 황 CEO는 \"AI 수요는 강력하며 이번 급락은 할인된 가격\"이라고 평가했어요. 이 기대에 NAVER(+9.2%)·SK텔레콤 등 일부 AI 인프라주는 폭락장에서도 올랐어요.",
    "ourImpact": "황 CEO의 'AI 수요 강력' 발언은 보유 NVDA(엔비디아)·MU(마이크론)·TSM에 중장기 긍정 신호예요. 메모리 수요가 탄탄하다는 메시지라, 단기 급락 속에서도 흐름을 지켜보면 좋아요.",
    "impact": "positive",
    "sources": [
      {"name": "경향신문", "url": "https://n.news.naver.com/mnews/article/032/0003450622?sid=101"},
      {"name": "아시아타임즈", "url": "https://www.asiatime.co.kr/article/20260608500324"}
    ]
  },
  {
    "category": "개별 종목",
    "headline": "한국 반도체 대형주 폭락 — 삼성전자 -10.2%·SK하이닉스 -7.7%",
    "oneLineSummary": "오늘 한국 반도체 대형주가 크게 빠졌어요. 삼성전자 -10.18%, SK하이닉스 -7.68%, SK스퀘어 -11.13%, 한미반도체 -10.42%까지 무너졌어요. 지난 금요일 미국에서 브로드컴의 AI 칩 전망 실망으로 반도체가 폭락한 충격이 한국 메모리 대장주로 그대로 번진 거예요.",
    "summary": "6/8 삼성전자 -10.18%, SK하이닉스 -7.68%, SK스퀘어 -11.13%, 한미반도체 -10.42% 등 반도체가 지수 하락을 주도했어요. 6/5 미국 브로드컴(AVGO)의 다음 분기 AI 칩 매출 가이던스(회사가 직접 한 예상) 160억 달러가 시장 기대(172억 달러)에 못 미친 'AI 거품론'이 한국 메모리로 전이된 결과예요.",
    "ourImpact": "한국 메모리 폭락은 보유 MU(마이크론)·NVDA·AVGO에 부정적 프리마켓 신호일 수 있어요. 다만 브로드컴 이슈는 이미 지난주 반영됐던 재료라, 추가 충격인지 단순 동조인지 가볍게 지켜보면 좋아요.",
    "impact": "negative",
    "sources": [
      {"name": "매일경제(속보)", "url": "https://n.news.naver.com/mnews/article/009/0005690785?sid=101"},
      {"name": "전자신문", "url": "https://n.news.naver.com/mnews/article/030/0003435513?sid=101"}
    ]
  },
  # ===== 정책·금리 =====
  {
    "category": "정책·금리",
    "headline": "5월 美 고용 깜짝 호조 → 금리 인상 우려, 6월 FOMC 대기",
    "oneLineSummary": "지난주 나온 미국 5월 고용지표가 예상의 2배로 너무 좋게 나오면서, 오히려 시장엔 악재가 됐어요. 경기가 뜨거우면 물가가 잡히기 어려워 미국 중앙은행(Fed)이 금리를 안 내리거나 올릴 수도 있다는 걱정이 커졌거든요. 이번 주 6월 FOMC(금리 결정 회의)를 앞두고 투자 심리가 잔뜩 움츠러들었어요.",
    "summary": "예상의 2배에 달한 5월 미국 고용 서프라이즈로 'AI 둔화 + 금리 상승' 우려가 동시에 부각됐어요. CME 기준 6월 인하 전망은 후퇴하고 연말 인상 가능성까지 거론돼요. 간밤 미 10년물 국채금리는 4.54%를 돌파, 30년물은 5.0%대로 올라섰어요. 이번 주 6월 FOMC가 최대 분수령이에요.",
    "ourImpact": "금리가 오르면 밸류에이션 부담이 큰 성장주·반도체(NVDA·AVGO·AMD)에 불리해요. FOMC 결과 전까지는 변동성이 이어질 수 있어, 무리한 대응보다 관망이 편한 구간이에요.",
    "impact": "negative",
    "sources": [
      {"name": "내일신문", "url": "https://www.naeil.com/news/read/591097?ref=naver"},
      {"name": "SBS Biz", "url": "https://n.news.naver.com/mnews/article/374/0000514706?sid=101"}
    ]
  },
  # ===== 글로벌·지정학 =====
  {
    "category": "글로벌·지정학",
    "headline": "이란-이스라엘 충돌 100일째 격화 — 유가 급등(WTI 약 $93)",
    "oneLineSummary": "이란과 이스라엘의 충돌이 오늘로 100일째를 맞으며 더 격해졌어요. 주말 사이 이란이 미사일을 쐈고, 이스라엘도 이란 도시를 공습했어요. 중동 긴장에 기름값이 뛰어 미국 대표 원유(WTI)가 약 $93, 국제 기준 브렌트유가 약 $96까지 올랐어요. 기름값이 오르면 물가 걱정이 커져 증시엔 부담이에요.",
    "summary": "이란-이스라엘 분쟁이 100일째 격화됐어요. 주말 이란의 미사일 공격에 이어 이스라엘이 이란 3개 도시를 공습했고, 호르무즈 해협 봉쇄 우려까지 가격에 반영됐어요. WTI는 +3%대 약 $93, 브렌트유 약 $96으로 급등. 유가 상승은 인플레이션 우려를 키워 금리 상승 압력과 맞물리며 위험회피 심리를 자극했어요.",
    "ourImpact": "유가 급등과 중동 불안은 증시 전반의 변동성을 키워 보유 빅테크·반도체에 단기 부담이에요. 지정학 뉴스에 따라 출렁일 수 있으니 흐름을 차분히 지켜보면 좋아요.",
    "impact": "negative",
    "sources": [
      {"name": "Business Upturn", "url": "https://www.businessupturn.com/finance/stock-market/asian-markets-crash-on-june-8-kospi-down-5-2-nikkei-falls-4-taiwan-drops-3-5-as-iran-israel-war-enters-day-100-and-nasdaq-selloff-spills-over"}
    ]
  },
  # ===== 미국 증시 (프리뷰) =====
  {
    "category": "미국 증시",
    "headline": "미국 선물·프리마켓 약세 흐름 — 간밤 6/5 폭락 여파 지속",
    "oneLineSummary": "오늘 밤 열릴 미국 시장도 출발이 약할 가능성이 높아요. 지난 금요일(6/5) 나스닥이 -4.18%, 반도체지수(SOX)가 -10.26% 폭락했는데, 그 충격이 주말과 아시아 폭락장으로 이어지고 있어요. 미국 선물(개장 전 분위기를 보여주는 거래)도 약세 쪽이라, 미국 증시도 변동성 큰 출발이 예상돼요.",
    "summary": "6/5(금) 다우 -1.35%·S&P500 -2.64%·나스닥 -4.18%, 필라델피아 반도체지수 -10.26% 폭락에 이어, 6/8 아시아 동반 급락과 이란발 유가 급등이 겹치며 미국 선물(ES·NQ)은 약세 분위기예요. 6월 FOMC를 앞둔 경계감까지 더해져, 오늘 밤 미국 정규장도 변동성 확대 출발 가능성이 높아요.",
    "ourImpact": "미국 개장 직후 보유 반도체·빅테크가 약세로 출발할 수 있어요. 패닉 구간에선 가격이 빠르게 출렁이니, 무리한 매매보다 개장 흐름을 가볍게 지켜보는 게 편해요.",
    "impact": "negative",
    "sources": [
      {"name": "TheStreet(6/5)", "url": "https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-05-2026"},
      {"name": "중기일보", "url": "https://www.junggi.co.kr/news/articleView.html?idxno=36681"}
    ]
  },
]

asiaSummary = {
  "asOf": asOf,
  "kospi": {
    "close": 7484.41, "change": -8.29, "changePoints": -676.18,
    "note": "6/8(월) -8.29% 7,484.41 '검은 월요일'. 장 초반 -8.4%(7,442.73)로 서킷브레이커 발동. 외국인 -2,766억·기관 -1조9,422억 순매도, 개인 +1조9,478억 순매수. 역대 9위 하락률. 원/달러 1,535~1,555원 급등."
  },
  "kosdaq": {
    "close": 911.39, "change": -9.08, "changePoints": -91.05,
    "note": "6/8 -9.08% 911.39, 사이드카 발동. 외국인은 코스닥에서 순매수(약 2,800억), 개인·기관 순매도. 에코프로비엠 -11.3%·알테오젠 -12.9%."
  },
  "nikkei": {
    "close": 64000.0, "change": -3.9,
    "note": "6/8 약 -3.9% 64,000선. 키오시아 -10%·소프트뱅크 -8.6% 등 기술주 급락(개장 기준, 마감 변동 가능)."
  },
  "hangseng": {
    "note": "6/8 약 -1.2% 약세(장중). 미국·아시아 반도체 약세 여파."
  },
  "taiwan": {
    "note": "6/8 가권 약 -3.5%(장중). TSMC 등 반도체 약세."
  }
}

# ---------- 1) reports/2026-06-08.json ----------
rep = {
  "date": "2026-06-08",
  "session": "asia-close",
  "title": "6/8(월) 15:45 아시아 마감 — '검은 월요일' 코스피 -8.29% 7,484 서킷브레이커·코스닥 -9.1%, 美 반도체 폭락 + 이란 격화 여파",
  "marketStatus": "6/8(월) 아시아 '검은 월요일'. 코스피 -8.29%(7,484.41)·코스닥 -9.08%(911.39) 동반 급락, 서킷브레이커·사이드카 발동. 외국인+기관 코스피 2조+ 순매도, 개인 1.9조 순매수. 삼성전자 -10.18%·SK하이닉스 -7.68%. 니케이 -3.9%·대만 -3.5%·항셍 -1.2%. 원인: 6/5 美 반도체 폭락(나스닥 -4.18%·SOX -10.26%, 브로드컴 가이던스 쇼크)+5월 고용 서프라이즈發 금리 우려+이란-이스라엘 100일 격화·유가 급등(WTI~$93). 호재: 젠슨 황 방한 'AI 수요 강력' 발언, NAVER +9.2%. 오늘 밤 美 선물 약세·변동성 확대 예상.",
  "generatedAt": genAt,
  "lastUpdated": genAt,
  "news": news,
  "asiaSummary": asiaSummary,
  "dataQualityNote": "코스피·코스닥 종가는 6/8(월) 15:30 정규장 마감 확정치(네이버 뉴스 마감시황 집계). 니케이·대만·항셍은 캡처 시점(15:45 KST) 장중/마감 혼재 — 일부 추정. 미국 선물 방향은 정성적 추정(구체 수치 미확정). 외국인/기관 수급은 잠정치로 보도사별 소폭 차이 있음."
}
wr(os.path.join(BASE,'reports','2026-06-08.json'), rep)
print("wrote reports/2026-06-08.json")

# ---------- 2) reports/index.json ----------
idx = rd(os.path.join(BASE,'reports','index.json'))
entry = {
  "date": "2026-06-08",
  "title": "6월 8일 (월) 아시아 마감 — '검은 월요일' 코스피 -8.29% 서킷브레이커",
  "summary": "코스피 7,484(-8.29%)·코스닥 911(-9.08%) 동반 폭락, 美 반도체發 충격+이란 격화. 젠슨 황 'AI 수요 강력'"
}
reports = idx.get('reports', [])
reports = [r for r in reports if r.get('date') != '2026-06-08']
reports.append(entry)
reports.sort(key=lambda r: r.get('date',''))
idx['reports'] = reports
idx['lastUpdated'] = genAt
wr(os.path.join(BASE,'reports','index.json'), idx)
print("updated reports/index.json")

# ---------- 3) portfolio.json (asiaCloseSnapshot 갱신, 나머지 보존) ----------
pf = rd(os.path.join(BASE,'portfolio.json'))
pf['asiaCloseSnapshot'] = {
  "asOf": asOf,
  "kospi": {"close": 7484.41, "change": -8.29, "changePoints": -676.18,
            "note": "6/8(월) -8.29% 7,484.41 '검은 월요일'. 서킷브레이커 발동(장 초반 -8.4%). 외국인 -2,766억·기관 -1.94조 순매도, 개인 +1.95조 순매수."},
  "kosdaq": {"close": 911.39, "change": -9.08, "changePoints": -91.05,
             "note": "6/8 -9.08% 911.39, 사이드카 발동. 외국인 코스닥 순매수, 개인·기관 순매도."},
  "asiaIndices": {
    "nikkei": {"close": 64000.0, "change": -3.9, "changePoints": None, "note": "약 -3.9% 64,000선, 키오시아·소프트뱅크 급락."},
    "taiwan": {"close": None, "change": -3.5, "changePoints": None, "note": "가권 약 -3.5%(장중), TSMC 약세."},
    "shanghai": {"close": None, "change": None, "changePoints": None, "note": "상하이 약세(15:45 캡처 시점 거래 중)."},
    "hangSeng": {"close": None, "change": -1.2, "changePoints": None, "note": "항셍 약 -1.2%(장중)."}
  },
  "usdkrw": 1545.0,
  "samsung": {"change": -10.18, "note": "6/8 -10.18% — 외국인 매도·美 반도체 폭락 전이."},
  "skHynix": {"change": -7.68, "note": "6/8 -7.68% — 젠슨 황 HBM 협력에 낙폭은 상대적 방어."},
  "usFutures": {"es": None, "esChange": None, "nq": None, "nqChange": None,
                "note": "美 선물(ES·NQ) 약세 분위기 — 6/5 폭락 여파+아시아 급락+이란發 유가 급등. 22:30 KST 개장 대기, 변동성 확대 예상."}
}
pf['lastUpdated'] = genAt
pf['marketStatus'] = "🔴 아시아 '검은 월요일' — 코스피 -8.29%(7,484.41)·코스닥 -9.08% 서킷브레이커 발동, 외국인+기관 2조+ 순매도. 삼성전자 -10.18%·SK하이닉스 -7.68%. 6/5 美 반도체 폭락(나스닥 -4.18%·SOX -10.26%)+5월 고용 서프라이즈發 금리 우려+이란-이스라엘 100일 격화·유가 급등이 원인. 젠슨 황 방한 'AI 수요 강력' 발언은 NVDA·MU·SK하이닉스에 중장기 긍정. 오늘 밤 美 선물 약세·변동성 확대 예상. ⚠ 미국 보유 종목 가격은 6/5(금) 종가 기준, 프리마켓 미반영."
wr(os.path.join(BASE,'portfolio.json'), pf)
print("updated portfolio.json (asiaCloseSnapshot)")

# ---------- 4) calendar-events.json ----------
cal = rd(os.path.join(BASE,'calendar-events.json'))
ev = {
  "type": "asia", "label": "아시아 마감", "color": "blue", "mood": "🔴",
  "time": "15:45 KST 캡처",
  "title": "🔴 아시아 마감 — '검은 월요일' 코스피 -8.29% 7,484 서킷브레이커·코스닥 -9.1%, 美 반도체 폭락+이란 격화",
  "description": "6/8(월) 한국 증시가 '검은 월요일'을 맞았어요. 코스피 -8.29%(7,484.41)·코스닥 -9.08%(911.39)가 동반 폭락해 서킷브레이커(20분 매매중지)와 사이드카가 함께 발동됐어요. 외국인(-2,766억)과 기관(-1.94조)이 코스피를 2조 원 넘게 팔았고, 개인이 1.95조 원을 받아냈어요. 삼성전자 -10.18%·SK하이닉스 -7.68% 등 반도체가 폭락을 주도했고, 일본 니케이 -3.9%·대만 -3.5%·홍콩 항셍 -1.2%로 아시아가 다 같이 내렸어요. 원/달러 환율은 1,535~1,555원까지 치솟았어요.",
  "impact": "지난 금요일(6/5) 미국 반도체 폭락(나스닥 -4.18%·필라델피아 반도체지수 -10.26%, 브로드컴 AI 칩 전망 실망)에 5월 고용 깜짝 호조發 금리 우려, 이란-이스라엘 100일 격화·유가 급등(WTI~$93)이 겹친 위험회피 장세예요. 방한 마지막 날 젠슨 황 엔비디아 CEO는 'AI 수요는 여전히 강력, 급락은 곧 할인된 가격'이라고 평가했고 SK하이닉스 HBM 협력을 확인했는데, 이는 보유 NVDA·MU에 중장기 긍정 신호예요. 다만 한국·아시아 반도체 폭락은 오늘 밤 미국 반도체 프리마켓에 약세 신호로 작용할 수 있어, 개장 흐름을 차분히 지켜보면 좋아요."
}
cal.setdefault('stock', {})['2026-06-08'] = [ev]
cal['lastUpdated'] = genAt
wr(os.path.join(BASE,'calendar-events.json'), cal)
print("updated calendar-events.json (2026-06-08)")
print("ALL DONE")
