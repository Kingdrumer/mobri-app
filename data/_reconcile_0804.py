# -*- coding: utf-8 -*-
import json
TS="2026-08-04T14:40:00+09:00"

# ---- fix 4 recentNews numbers in portfolio to match authoritative closes ----
p=json.load(open('portfolio.json'))
fix={
 'GOOG':("GOOG +4.4% $372.47 — 클라우드 82% 성장·CapEx 상향","구글(GOOG)이 8/3 +4.4% 올랐어요. 구글 클라우드 매출이 82% 늘고 올해 투자 계획을 $205B로 올린 게 호재였어요."),
 'META':("META +6.0% $590.24 — 광고 27% 성장에 실적 하락분 회복","메타(META)가 8/3 +6.0% 급등했어요. 광고 매출이 27% 늘어난 게 부각되며 실적 발표 후 빠졌던 9%를 되돌렸어요."),
 'AMZN':("AMZN +4.6% $284.02 — 시총 3조 달러 돌파","아마존(AMZN)이 8/3 +4.6% 올라 시가총액 3조 달러를 넘었어요. AWS(클라우드) +37% 성장이 계속 주가를 밀어올렸어요."),
 'NVDA':("NVDA +2.9% $206.64 — 빅테크 랠리 동반 상승","엔비디아(NVDA)가 8/3 +2.9% 올랐어요. AI 반도체 수요 기대와 위험자산 선호 회복에 반도체가 함께 강했어요."),
}
for s in p['us']:
    t=s['ticker']
    if t in fix and s.get('recentNews') and s['recentNews'][0].get('date')=='2026-08-03':
        s['recentNews'][0]['headline']=fix[t][0]
        s['recentNews'][0]['easySummary']=fix[t][1]
json.dump(p,open('portfolio.json','w'),ensure_ascii=False,indent=1)
print("portfolio recentNews reconciled")

# ---- report 2026-08-04.json ----
r=json.load(open('reports/2026-08-04.json'))
r['title']="8월 4일 (화) 06:00 미국 마감 캡처 — 🟢 3대 지수 큰 폭 상승 (다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%) / 이란 완화·유가 -6% / 아마존 시총 3조달러·메타 +6%·구글 +4% / 팰런티어 시간외 +13% 실적 서프라이즈"
r['lastUpdated']=TS
r['generatedAt']=TS
r['marketSummary']=("8/3(월) 뉴욕증시는 이란과의 협상 재개 소식에 유가가 6% 급락하고 빅테크가 크게 오르면서 3대 지수가 나란히 상승했어요. "
 "다우 53,178.41(+1.32%)·S&P500 7,600.50(+1.48%)·나스닥 25,913.90(+2.1%)로, 나스닥이 상승을 주도했어요. "
 "아마존이 AWS 호실적 여운에 +4.6% 올라 시가총액 3조 달러를 넘었고, 메타(+6.0%)·구글(+4.4%)·엔비디아(+2.9%)가 함께 강했어요. "
 "보유 종목 중에서는 광통신주 루멘텀(+9.2%)·크레도(+5.5%)와 낸드 반등의 샌디스크(+6.0%)가 특히 크게 올랐어요. "
 "장 마감 후엔 팰런티어가 2분기 실적 서프라이즈로 시간외 +약 13% 급등했어요. 유가(WTI)는 약 $79로 떨어졌고, VIX(변동성 지수)는 약 15.7로 진정됐어요. "
 "오늘 밤(미 동부 장 마감 후)엔 보유 종목 AMD 실적이 대기예요.")
r['dataQualityNote']=("라이트 캡처. 보유 15종목 8/3 종가는 StockAnalysis(S&P Global Market Intelligence) + WebSearch로 교차확인했어요. "
 "지수·유가·VIX는 실시간 검색으로 확인한 8/3 미국 마감 기준. 팰런티어(시그널)는 8/3 장 마감 후 실적·시간외 급등 반영.")

# news[0] 미국증시 ourImpact
r['news'][0]['ourImpact']=("보유 빅테크(구글·아마존·메타·엔비디아)가 상승을 주도했고, 광통신주 루멘텀·크레도까지 크게 올라 포트폴리오 전반이 강했어요. "
 "방향은 우호적이었어요.")

# news[2] 개별종목 빅테크
r['news'][2]['headline']="보유 빅테크 급등 — 아마존 시총 3조달러·메타 +6%·구글 +4%"
r['news'][2]['oneLineSummary']=("보유 종목 아마존(AMZN)이 8/3 +4.6% 올라 회사 가치가 3조 달러를 넘었어요. 메타(+6.0%)와 구글(+4.4%)도 크게 올랐는데, "
 "클라우드·광고 실적이 좋았던 게 계속 힘을 냈어요. 엔비디아도 +2.9% 상승했어요.")
r['news'][2]['summary']=("8/3 대형 기술주가 일제히 급등했습니다. 아마존은 AWS 매출 +37% 호실적 여운에 +4.6% 올라 시가총액 3조 달러를 돌파했고, "
 "메타는 광고 매출 +27%가 재평가되며 +6.0% 상승해 실적 후 하락분을 회복했습니다. 구글은 클라우드 82% 성장과 연간 투자(CapEx) 상향($205B) 소식에 +4.4%, "
 "엔비디아는 AI 반도체 수요 기대에 +2.9% 올랐습니다.")
r['news'][2]['ourImpact']=("보유 빅테크 4종이 동시에 강세였어요. 여기에 광통신주 루멘텀(+9.2%)·크레도(+5.5%)와 샌디스크(+6.0%)까지 크게 올라, "
 "메모리 일부(마이크론 +0.8%)만 완만했을 뿐 포트폴리오 전반이 강했어요.")
json.dump(r,open('reports/2026-08-04.json','w'),ensure_ascii=False,indent=1)
print("report reconciled")

# ---- index.json entry ----
idx=json.load(open('reports/index.json'))
for e in idx['reports']:
    if e['date']=='2026-08-04':
        e['title']="8월 4일 (화) 06:00 미국 마감 캡처 — 🟢 3대 지수 급등 (다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%) / 이란 완화·유가 -6% / 아마존 시총 3조달러·메타 +6%·구글 +4% / 팰런티어 시간외 +13% 실적 서프라이즈 / 오늘 밤 AMD(보유) 실적"
        e['summary']=("미국 마감 캡처(라이트). 8/3(월) 뉴욕은 이란 협상 재개·유가 6% 급락에 빅테크 강세로 3대 지수 급등(다우 53,178.41 +1.32%·S&P500 7,600.50 +1.48%·나스닥 25,913.90 +2.1%). "
         "아마존 시총 3조달러 돌파(+4.6%)·메타 +6.0%·구글 +4.4%·엔비디아 +2.9%. 광통신주 루멘텀 +9.2%·크레도 +5.5%, 샌디스크 +6.0% 급반등. "
         "장 마감 후 팰런티어 2분기 실적 서프라이즈(매출 +93%, 가이던스 상향)로 시간외 +약 13.6%. 보유 15종목 종가 StockAnalysis+WebSearch 교차확인. 오늘 밤 AMD(8/4)·수요일 SNDK·TLN(8/5) 실적, 8/7 고용보고서 대기.")
        break
idx['lastUpdated']=TS
json.dump(idx,open('reports/index.json','w'),ensure_ascii=False,indent=1)
print("index reconciled")

# ---- calendar lastUpdated ----
cal=json.load(open('calendar-events.json'))
cal['lastUpdated']=TS
json.dump(cal,open('calendar-events.json','w'),ensure_ascii=False,indent=1)
print("calendar timestamp aligned")
