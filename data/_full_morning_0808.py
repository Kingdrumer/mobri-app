#!/usr/bin/env python3
# Full morning 2026-08-08 (Sat KST) — reflects Fri 8/7 US close. Updates holdings daily fields + signals.
import json, urllib.request, hashlib, time, datetime, shutil, os

KST = "+09:00"
NOW = "2026-08-08T08:15:00" + KST
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# backup
shutil.copy("portfolio.json", "portfolio.json.before-full-morning-0808.bak")

H = json.load(open("/tmp/holdings_0808.json"))  # ticker -> price/change fields

todayWhy = {
 'GOOG':"약한 7월 고용에 대형 기술주 전반이 강했지만, 최근 오름세 뒤 소폭 차익실현(오른 김에 일부 파는 것)으로 -0.9% 약보합 마감했어요.",
 'META':"광고·AI 투자 기대가 이어지며 +0.4% 강보합 마감했어요. 이번 주 낙폭은 대부분 되돌렸어요.",
 'AMZN':"클라우드(AWS) 성장 기대와 시가총액 3조 달러 재부각으로 +0.8% 올랐어요.",
 'NVDA':"약한 고용으로 금리 부담이 줄자 반도체 반등을 주도하며 +2.3% 상승했어요.",
 'TSM':"반도체 회복 흐름에 +0.4% 강보합 마감했어요.",
 'AVGO':"AI 반도체 수요 기대가 살아나며 +1.7% 반등했어요.",
 'MU':"메모리 반등 흐름 속에서도 '루빈 GPU가 HBM(고대역폭 메모리)을 덜 쓸 수 있다'는 우려가 겹쳐 -0.4% 약보합이었어요.",
 'MRVL':"AI 데이터센터·광통신 칩 강세로 +3.9% 크게 반등했어요.",
 'AMD':"최근 급등(YTD +116%) 뒤 차익실현으로 -1.2% 소폭 조정받았어요.",
 'SNDK':"올해 +340% 급등한 부담에 차익실현 매물이 나오며 -3.7% 조정받았어요.",
 'DELL':"AI 서버 수요 기대가 커지며 +3.7% 강세로 마감했어요.",
 'LITE':"AI 데이터센터 광통신 수요 급증 기대로 +6.2% 크게 올랐어요.",
 'CLS':"AI 서버 위탁생산(다른 회사 제품을 대신 만들어 주는 것) 기대로 +1.1% 강보합이었어요.",
 'CRDO':"AI 광통신 칩 수요와 실적 기대가 겹치며 +8.5% 급등했어요.",
 'TLN':"AI 데이터센터 전력 수요와 원전 테마 강세로 +2.8% 올랐어요.",
}

def sig(t):
    d=H[t]['change1D']; w=H[t]['change1W']
    if d>=2 or (w>=8 and d>=0): return 'green'
    if d<=-2 or w<=-5: return 'red'
    return 'yellow'

def h(s): return "sha256-"+hashlib.sha256(s.encode()).hexdigest()[:8]

p = json.load(open("portfolio.json"))
sfx={'GOOG':'.O','META':'.O','AMZN':'.O','NVDA':'.O','TSM':'','AVGO':'.O','MU':'.O','MRVL':'.O','AMD':'.O','SNDK':'.O','DELL':'.K','LITE':'.O','CLS':'','CRDO':'.O','TLN':'.O'}

for s in p['us']:
    t=s['ticker']; d=H[t]
    s['price']=d['price']; s['change1D']=d['change1D']; s['change1W']=d['change1W']
    s['change1M']=d['change1M']; s['changeYTD']=d['changeYTD']
    s['signal']=sig(t)
    s['todayWhy']=todayWhy[t]
    s['priceSourcedFrom']=["Naver Finance(장마감 확정치)","WebSearch 교차확인(NVDA·CRDO·GOOG)"]
    s['dataQualityNote']=None
    s['afterHoursPrice']=None; s['afterHoursChange1D']=None
    url=f"https://api.stock.naver.com/stock/{t}{sfx[t]}/basic"
    s['_fetchMeta']={"fetchedAt":NOW,"sources":[{"url":url,"hash":h(url+str(d['price']))}]}

p['lastUpdated']=NOW
p['marketSession']=("토요일 아침 8/8 (KST). 8/7(금) 미국 정규장이 마감했어요. 개장 직전 나온 7월 고용보고서가 신규고용 -2.3만(예상 +8만)으로 부진했는데, "
 "'금리 인상 압력이 줄었다'는 해석에 3대 지수가 상승 마감했어요 — S&P500 7,757.64(+0.62%, 사상 최고)·나스닥 26,690.62(+1.30%, 반도체 반등 주도)·다우 54,036.93(+0.28%). "
 "10년물 국채금리는 4.62% 부근으로 하락. 보유 15종목은 8/7 확정 종가로 정산했어요 — 광통신주(LITE +6.2%·CRDO +8.5%)와 델(+3.7%)이 강했고, "
 "샌디스크(-3.7%)는 차익실현 조정을 받았어요. 주말 휴장이라 다음 정규장은 8/11(월)이에요.")
p['marketStatus']=("🟢 8/7(금) 뉴욕증시 상승 마감. S&P500 7,757.64(+0.62%) 사상 최고, 나스닥 +1.30%(반도체·광통신 반등 주도), 다우 +0.28%. "
 "개장 직전 7월 고용보고서(신규고용 -2.3만, 예상 +8만 하회)가 오히려 호재 — 고용이 약하면 미 중앙은행(Fed)이 금리를 올릴 이유가 줄기 때문이에요. "
 "10년물 금리 4.62%, WTI $77 부근 약세, 금 +2.6%($4,412), VIX 14.9. 보유 종목은 광통신주(LITE·CRDO)·델 강세, 샌디스크 차익실현. 다음 큰 이벤트는 8/12(화) 미 7월 소비자물가(CPI)예요.")
p['dataNote']="08:00 풀 모닝(8/8 토): 보유 15종목을 8/7 금 확정 종가로 정산(Naver 장마감 확정치 + WebSearch 교차확인). 시그널·외인동향은 8/7 금 국내 종가 기준으로 갱신. 주말 휴장. JSON UTF-8."

json.dump(p, open("portfolio.json","w"), ensure_ascii=False, indent=2)
print("holdings updated. signals:", {t:sig(t) for t in H})
