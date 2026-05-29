#!/usr/bin/env python3
"""5/28 美 4월 PCE + Q1 GDP 2차 + 美 정규장 개장 calendar-events.json 추가."""
import json
from pathlib import Path

ROOT = Path("/sessions/stoic-nifty-pasteur/mnt/claude/portfolio-pwa/data")
CAL = ROOT / "calendar-events.json"

with open(CAL) as f:
    cal = json.load(f)

new_events = [
    {
        "type": "indicator",
        "label": "4월 PCE 3.8% — 컨센 3.9% 하회 안도",
        "color": "green",
        "time": "21:30 KST (08:30 ET)",
        "title": "美 4월 PCE 물가 헤드라인 3.8% YoY (컨센 3.9% 하회) + 한 달 +0.4% (컨센 +0.5% 하회)",
        "description": "Fed(미국 중앙은행)가 가장 신뢰하는 물가 지표인 4월 PCE 헤드라인 인플레이션이 3.8% YoY로 나왔어요. 시장 평균 예상(컨센) 3.9%보다 0.1%p 낮았고, 한 달 변동도 +0.4%로 컨센 +0.5%보다 낮았어요. 컨센보다 약간 낮게 나온 건 안도 신호예요. 채권 10년물 금리도 4.5%대에서 안정 유지했어요.",
        "impact": "PCE는 물가 안정을 책임지는 미국 중앙은행이 가장 신뢰하는 지표예요. 컨센보다 살짝 낮게 나오면 금리(은행이 돈을 빌려줄 때 받는 이자) 인하 기대가 살아나서 빚을 많이 쓰는 기술주(빅테크·AI 성장주)에 우호적인 환경이에요. 다만 3.8%는 Fed 목표(2.0%)보다 여전히 한참 높아서 본격적인 호재는 아니에요.",
        "ourImpact": "보유 빅테크(GOOG·META·AMZN)와 성장주(NVDA·AMD·MU)에 약간 우호적. 다만 동시에 발표된 Q1 GDP 1.6% 하향이 부담을 줘서 시장은 보합권 출발이에요.",
        "stockImpacts": [
            {"ticker": "GOOG", "tone": "positive", "magnitude": "+0.3%", "text": "빅테크 멀티플 압축 우려 후퇴 — 우호적"},
            {"ticker": "META", "tone": "neutral", "magnitude": "-0.2%", "text": "어제 +3.95% Meta AI 구독 catalyst 후 보합"},
            {"ticker": "AMZN", "tone": "positive", "magnitude": "+1.7%", "text": "빅테크 중 가장 강한 출발 — SNOW AWS 60억$ 후광"},
            {"ticker": "NVDA", "tone": "neutral", "magnitude": "-0.6%", "text": "성장주 우호적이나 메모리 차익실현 분위기에 눌림"},
            {"ticker": "AMD", "tone": "positive", "magnitude": "+1.2%", "text": "MRVL 비트 후광 + AI 가속기 모멘텀 유지"},
        ],
    },
    {
        "type": "indicator",
        "label": "Q1 GDP 1.6% — 1차 2.0%에서 하향",
        "color": "amber",
        "time": "21:30 KST (08:30 ET)",
        "title": "美 1Q26 GDP 2차 추정치 1.6% (1차 2.0%에서 -0.4%p 하향) — 성장 둔화 신호",
        "description": "美 1분기 GDP(국내총생산) 2차 추정치가 1.6%로 발표됐어요. 4월 30일 1차 추정치(2.0%)에서 -0.4%p 낮아진 거예요. 투자와 소비 지출이 예상보다 약하게 나온 영향이 컸어요. 즉 미국 경제가 1분기에 생각보다 둔화됐다는 신호예요.",
        "impact": "성장이 약하면 ① 금리 인하 기대가 살아나서 빅테크·성장주에 호재가 될 수 있어요. ② 동시에 AI CapEx(대규모 투자) 사이클 둔화 우려가 커서 AI 인프라 종목엔 부담이 될 수 있어요. 양날의 칼이에요.",
        "ourImpact": "보유 AI 인프라(DELL·NVDA·LITE·CLS·CRDO) 단기 부담 vs 빅테크(GOOG·META·AMZN) 우호적. 다만 PCE 안도가 동시에 나와서 GDP 약세는 일단 흡수되는 분위기예요.",
        "stockImpacts": [
            {"ticker": "DELL", "tone": "neutral", "magnitude": "혼합", "text": "AI 서버 수요 우려 vs 펜타곤 9.7B$ 계약 호재로 +4.5% 갭업"},
            {"ticker": "NVDA", "tone": "negative", "magnitude": "-0.6%", "text": "AI CapEx 둔화 우려 소폭 노출"},
            {"ticker": "LITE", "tone": "negative", "magnitude": "-2.6%", "text": "광통신 차익실현 가속"},
            {"ticker": "GOOG", "tone": "positive", "magnitude": "+0.3%", "text": "금리 인하 기대로 우호적"},
        ],
    },
    {
        "type": "us-open",
        "label": "美 정규장 개장 — S&P -0.02%·NASDAQ -0.16%·Dow -0.63% 보합/약세",
        "color": "amber",
        "time": "22:30 KST",
        "title": "美 5/28 22:30 KST 개장 — 보합/약세 출발 + MRVL +9.7% 갭업·DELL +4.5%·TLN +2.0% 갭업 + MU -2.5%·LITE -2.6% 차익실현",
        "description": "美 정규장이 22:30 KST 개장했어요. 지수는 S&P 500 -0.02%·NASDAQ -0.16%·Dow -0.63%로 보합~약세 출발. VIX(공포 지수) 17선·10년 국채 4.5%대 안정. 4월 PCE 3.8% YoY 컨센 하회 안도 + Q1 GDP 1.6% 하향 + 美·이란 재교전 + 유가 +1.78% 부담이 혼재돼요. 개별주는 마벨(MRVL) +9.7% 갭업($218.04, 어제 실적 비트)·델(DELL) +4.5% 갭업($318.40, 펜타곤 9.7B$ 계약)·탈렌(TLN) +2.0% 강세, 반대로 마이크론(MU) -2.5%·루멘텀(LITE) -2.6% 차익실현이 두드러져요.",
        "impact": "neutral",
        "ourImpact": "보유 15종목 중 ① 갭업 강세 3개: MRVL +9.7%·DELL +4.5%·TLN +2.0% (개별 호재 직접 반영). ② 강보합 7개: AMZN +1.7%·SNDK +1.6%·AMD +1.2%·CRDO +1.0%·TSM +0.4%·GOOG +0.3%·AVGO +0.3%. ③ 약세 4개: MU -2.5%·LITE -2.6%·NVDA -0.6%·META -0.2%. 양극화 흐름이고 한국시간 5/29 06:00 DELL Q1 실적이 추가 변수예요.",
        "stockImpacts": [
            {"ticker": "MRVL", "tone": "positive", "magnitude": "+9.7% 갭업", "text": "어제 ET AMC Q1 비트·FY27 가이던스 $11.5B 상향이 정규장에 그대로 반영"},
            {"ticker": "DELL", "tone": "positive", "magnitude": "+4.5% 갭업", "text": "펜타곤 9.7B$ Microsoft 라이센스 5년 계약 호재 + 5/29 06:00 Q1 실적 기대"},
            {"ticker": "TLN", "tone": "positive", "magnitude": "+2.0%", "text": "원전·천연가스 + 호르무즈 긴장 후광 (유가 +1.78%)"},
            {"ticker": "MU", "tone": "negative", "magnitude": "-2.5%", "text": "5/26 +19.29% UBS PT $1,625·시총 1조$ 진입 후 누적 +25% 차익실현"},
            {"ticker": "LITE", "tone": "negative", "magnitude": "-2.6%", "text": "광통신 차익실현 가속·5/29 PCE 결과 대기 영향"},
            {"ticker": "AMZN", "tone": "positive", "magnitude": "+1.7%", "text": "SNOW AWS 60억$ 계약 후광 + AWS·소비재 견조"},
        ],
    },
]

# Insert in front of existing 5/28 events to put US open at top of day
existing = cal["stock"].get("2026-05-28", [])
cal["stock"]["2026-05-28"] = new_events + existing

with open(CAL, "w", encoding="utf-8") as f:
    json.dump(cal, f, ensure_ascii=False, indent=2)

print(f"[calendar-events.json] 5/28 항목 추가 — 새 이벤트 3개 prepend (PCE, GDP, US 개장). 5/28 총 항목 {len(cal['stock']['2026-05-28'])}개.")
