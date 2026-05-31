import json, shutil, datetime

BASE='/sessions/sleepy-great-ptolemy/mnt/claude/portfolio-pwa/data'
TODAY='2026-06-01'
NOW='2026-06-01T03:50:00+09:00'

# ---- load prior report (5/31) for stockSnapshot carry-forward ----
prev=json.load(open(f'{BASE}/reports/2026-05-31.json'))
snap=prev['stockSnapshot']
# update dataQualityNote for Monday pre-open (US session opens ~22:30 KST tonight)
for s in snap:
    s['dataQualityNote']='월요일 개장 전 — 美 증시 5/29(금) 종가 그대로, 정규장은 6/1(월) 밤(KST) 개장. 가격 변동 없음'

news=[
 {
  "category":"미국 증시",
  "headline":"美 3대 지수 사상 최고로 5월 마감 — 6/1(월) 새 거래주 시작",
  "oneLineSummary":"지난 금요일(5/29) 미국 다우·S&P500·나스닥 3대 지수가 모두 역대 최고로 5월을 마감했어요. 토·일 휴장이라 가격은 그대로 멈춰 있고, 새 거래는 한국시간 오늘(월) 밤 10시 반쯤 시작돼요. 보유 15종목 모두 강세 상태가 유지되고 있어요.",
  "summary":"5/29 다우 51,032.46(+0.72%, 첫 51,000 돌파)·S&P500 7,580.06(+0.22%, 9주 연속 상승)·나스닥 26,972.62(+0.20%, 5월 월간 +8%) 3대 지수가 사상 최고로 마감했습니다. 주말 휴장으로 가격 변동은 없으며, 6/1(월) 정규장은 한국시간 22:30 개장 예정입니다.",
  "ourImpact":"보유 15종목 모두 금요일 강세 마감이 그대로 유지돼요. 새 흐름은 오늘 밤 미국장 개장 후에 확인하면 됩니다.",
  "impact":"positive",
  "sources":[{"name":"TheStreet (5/29)","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-may-29-2026"}]
 },
 {
  "category":"미국 증시",
  "headline":"6월 계절성 주의 — 중간선거 해 '가장 약한 달'",
  "oneLineSummary":"역사적으로 6월은 중간선거가 있는 해에 증시가 가장 약했던 달이에요. 9주 연속 오른 만큼 잠깐 쉬어가는(가격이 옆으로 횡보하는) 구간이 올 수 있다는 전망이에요. 다만 유가 하락·금리 안정·AI 열기는 여전히 상승 쪽을 받쳐줘요.",
  "summary":"중간선거 해의 6월은 통계적으로 증시 수익률이 가장 낮은 달로, 9주 연속 상승 후 단기 조정·횡보 가능성이 거론됩니다. 다만 미·이란 평화 기대, 약 20%대 유가 하락, 국채금리 안정이 강세 배경을 유지하고 있어 방향성은 이번 주 지표 결과에 좌우될 전망입니다.",
  "ourImpact":"단기 횡보가 와도 보유 종목의 큰 그림(AI 인프라·반도체 수요)은 유지돼요. 변동이 커질 수 있는 한 주라 조급하게 반응하기보다 흐름을 지켜보는 게 좋아요.",
  "impact":"neutral",
  "sources":[{"name":"CNBC 주간전망 (5/29)","url":"https://www.cnbc.com/2026/05/29/stock-market-next-week-outlook-for-june-1-5-2026.html"}]
 },
 {
  "category":"정책·금리",
  "headline":"오늘(6/1) ISM 제조업 PMI — 이번 주 고용 '빅위크' 개막",
  "oneLineSummary":"오늘 밤 미국의 5월 ISM 제조업 지표(공장 경기를 보여주는 설문)와 4월 건설지출이 나와요. 이어 수요일(6/3) ADP 민간고용, 금요일(6/5) 5월 고용보고서(가장 중요)가 줄줄이 대기 중이에요. 고용이 너무 뜨거우면 금리 인하 기대가 줄어 성장주에 부담이 될 수 있어요.",
  "summary":"6/1 5월 ISM 제조업 PMI·4월 건설지출을 시작으로, 6/3 ADP 민간고용·ISM 비제조업, 6/5 5월 비농업고용(NFP)·실업률·시간당 임금이 발표됩니다. 6/10 CPI(소비자물가)도 대기 중입니다. 새 연준 의장 케빈 워시 체제에서 맞는 첫 주요 고용 데이터라 시장 주목도가 높습니다.",
  "impact":"warning",
  "sources":[{"name":"CNBC 주간전망 (5/29)","url":"https://www.cnbc.com/2026/05/29/stock-market-next-week-outlook-for-june-1-5-2026.html"}]
 },
 {
  "category":"개별 종목",
  "headline":"DELL +32.4% '역대 최고의 날' 여운 — 오늘 경쟁사 HPE 실적",
  "oneLineSummary":"보유 종목 DELL(델)이 금요일 AI 서버 실적 폭발로 +32.4% $423.40, 회사 역사상 하루 최대 상승을 기록했어요. AI 서버 매출이 1년 전보다 757% 급증($16.1B)했고 연간 가이던스도 크게 올렸어요. 오늘(6/1)은 같은 서버를 만드는 경쟁사 HPE 실적이 나와서, AI 서버 수요가 계속 강한지 확인할 수 있는 자리예요.",
  "summary":"DELL은 5/29 AI 서버 매출 +757%($16.1B)·가이던스 상향으로 +32.4% $423.40 사상 최고 마감(조정 EPS $4.86, 예상 $2.94 상회). 현지 6/1(월) HPE(휴렛팩커드 엔터프라이즈) 실적이 예정돼 AI 인프라 서버 수요의 지속성을 가늠하는 참고 지표가 됩니다.",
  "ourImpact":"HPE 실적이 좋으면 DELL·CLS·서버·하드웨어 종목에 우호적, 부진하면 차익실현(오른 김에 일부 파는 것) 빌미가 될 수 있어 오늘 밤 흐름을 지켜보면 좋아요.",
  "impact":"positive",
  "sources":[{"name":"CNBC (5/29)","url":"https://www.cnbc.com/2026/05/29/dell-stock-earnings-ai-servers.html"}]
 },
 {
  "category":"글로벌·지정학",
  "headline":"트럼프-이란 합의 주말에도 미서명 — 협상 진행 중",
  "oneLineSummary":"미국과 이란이 호르무즈 해협(중동 원유가 지나는 핵심 길목)을 60일간 다시 여는 합의에 근접했지만, 주말까지도 최종 서명은 안 됐어요. 이란이 해외 동결자산 즉시 해제를 요구하고, 미국은 '해협이 먼저 열려야 푼다'고 맞서며 핵 조건도 미해결이에요. 합의되면 유가가 더 내려 물가 부담이 줄 수 있어요.",
  "summary":"미·이란은 60일 휴전 연장과 호르무즈 해협 재개방(통행료 없음·이란 기뢰 제거 vs 미국 항구 봉쇄 해제·일부 제재 면제)을 골자로 한 양해각서(MoU)에 근접했으나 5/30~31까지 서명되지 않았습니다. 이란의 동결자산 해제 시점, 핵 농축 조건 등이 쟁점으로 남아 결렬 가능성도 상존합니다.",
  "ourImpact":"합의가 확정되면 유가 추가 하락→물가·금리 안정으로 기술주 전반에 우호적이에요. 보유 종목 중 TLN(원전·전력)은 에너지 흐름에 민감해 변동이 있을 수 있으니 가볍게 지켜보면 좋아요.",
  "impact":"neutral",
  "sources":[{"name":"CNN (5/29-30)","url":"https://www.cnn.com/2026/05/29/world/live-news/iran-trump-war-news"},{"name":"Axios (5/24)","url":"https://www.axios.com/2026/05/24/iran-deal-strait-hormuz-sanctions-nuclear"}]
 },
 {
  "category":"아시아 증시",
  "headline":"코스피 8,476 사상 최고로 5월 마감 — 오늘 6/1 거래 재개",
  "oneLineSummary":"한국 코스피가 금요일(5/29) 8,476.15로 사상 최고를 찍고 5월을 마감했어요. 한 달 동안 무려 +28% 오른 거예요. 미·이란 긴장 완화와 반도체 강세가 상승을 이끌었어요. 오늘(월) 한국 증시가 새로 거래를 시작해요.",
  "summary":"코스피는 5/29 8,476.15(+3.55%)로 사상 최고 마감, 5월 월간 +28.45%를 기록했습니다. 기관 순매수가 역대 7위 규모였고 개인·외국인은 순매도했습니다. 미·이란 휴전 기대와 반도체 랠리가 동력이었으며, 6/1(월) 정규장이 재개됩니다.",
  "ourImpact":"한국 증시 강세는 같은 반도체 사이클의 보유 종목(TSM·MU·NVDA 등)에도 우호적 신호예요. 다만 한국·미국은 별개 시장이라 직접 연동되진 않으니 분위기 참고 정도로 보면 좋아요.",
  "impact":"positive",
  "sources":[{"name":"머니투데이 (5/26)","url":"https://www.mt.co.kr/stock/2026/05/26/2026052519453344148"}]
 }
]

report={
 "date":TODAY,
 "session":"mon-morning-watchdog",
 "title":"6/1(월) 모닝 — 美 3대 지수 사상 최고로 새 주 시작, 오늘 ISM·HPE로 '고용 빅위크' 개막, 이란 합의 미서명",
 "marketStatus":"6/1(월) 03:50 KST 자가복구 브리핑 — 美 증시는 주말 휴장으로 5/29(금) 종가 그대로이며, 6/1(월) 정규장은 한국시간 오늘 밤 22:30 개장합니다. 5/29 다우 51,032.46(+0.72%)·S&P 7,580.06(+0.22%)·나스닥 26,972.62(+0.20%) 3대 지수 모두 사상 최고로 5월을 마감했고(나스닥 월간 +8%), DELL이 AI 서버 실적 폭발로 +32.4% $423.40 '역대 최고의 날'을 기록했습니다. 보유 15종목 모두 강세 유지 중입니다. 이번 주는 매크로 빅위크입니다 — 오늘(6/1) 5월 ISM 제조업·4월 건설지출과 경쟁사 HPE 실적, 6/3 ADP 민간고용, 6/5 5월 고용보고서(NFP), 6/10 CPI가 줄줄이 대기합니다. 미·이란 호르무즈 합의는 주말까지도 서명되지 않아 협상이 이어지고 있고, WTI는 $87대로 연중 고점 대비 약 20% 낮은 수준입니다. 6월은 중간선거 해 계절성상 약세 경향이 있어 9주 연속 상승 후 단기 횡보 가능성도 거론됩니다.",
 "lastUpdated":NOW,
 "generatedAt":NOW,
 "stockSnapshot":snap,
 "news":news,
 "signals":prev.get('signals',{}),
 "asiaSummary":"코스피 5/29 8,476.15(+3.55%) 사상 최고 마감, 5월 월간 +28.45%. 주말 휴장으로 가격 변동 없음, 6/1(월) 거래 재개. 미국 증시도 6/1(월) 밤 22:30 KST 개장 예정."
}

with open(f'{BASE}/reports/{TODAY}.json','w') as f:
    json.dump(report,f,ensure_ascii=False,indent=1)
print('✓ report written')

# ---- index.json ----
idx=json.load(open(f'{BASE}/reports/index.json'))
entry={"date":TODAY,"title":"6/1(월) 모닝 — 美 3대 지수 사상 최고로 새 주 시작, 오늘 ISM·HPE 고용 빅위크 개막","summary":"5/29 다우·S&P·나스닥 신고가 마감(나스닥 월간 +8%), DELL +32.4%. 6/1 ISM·HPE, 6/3 ADP, 6/5 NFP 대기. 이란 합의 미서명, WTI $87대."}
reports_list=idx['reports']
reports_list=[r for r in reports_list if r.get('date')!=TODAY]
reports_list.append(entry)
idx['reports']=reports_list
with open(f'{BASE}/reports/index.json','w') as f:
    json.dump(idx,f,ensure_ascii=False,indent=1)
print('✓ index updated, total reports:',len(reports_list))

# ---- portfolio.json: only lastUpdated, never touch userMemo/prices ----
pf=json.load(open(f'{BASE}/portfolio.json'))
pf['lastUpdated']=NOW
with open(f'{BASE}/portfolio.json','w') as f:
    json.dump(pf,f,ensure_ascii=False,indent=1)
print('✓ portfolio lastUpdated bumped (prices unchanged — weekend close)')

# ---- calendar enrich June 1 ----
cal=json.load(open(f'{BASE}/calendar-events.json'))
for e in cal['stock']:
    if e.get('date')==TODAY:
        e['description']="5월 ISM 제조업 PMI(공장 경기 설문)·4월 건설지출 발표 + HPE(휴렛팩커드 엔터프라이즈) 실적 — DELL 경쟁사로 AI 서버 수요의 지속성을 가늠하는 자리"
        e['ourImpact']="ISM·고용 지표가 강하면 금리 인하 기대 후퇴로 성장주에 단기 부담. HPE 실적이 좋으면 보유 종목 DELL·CLS 등 서버주에 우호적"
        e['stockImpacts']=[
            {"ticker":"DELL","impact":"positive","reason":"경쟁사 HPE 호실적 시 AI 서버 수요 지속 확인 → 동반 강세 가능"},
            {"ticker":"CLS","impact":"positive","reason":"AI 서버 ODM — HPE·서버 수요 지표에 동조"},
            {"ticker":"NVDA","impact":"neutral","reason":"고용·ISM 강세 시 금리 인하 기대 후퇴로 성장주 단기 변동"}
        ]
        break
cal['lastUpdated']=NOW
with open(f'{BASE}/calendar-events.json','w') as f:
    json.dump(cal,f,ensure_ascii=False,indent=1)
print('✓ calendar June 1 enriched')
print('DONE')
