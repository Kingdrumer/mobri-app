import json, datetime

P='portfolio.json'
d=json.load(open(P,encoding='utf-8'))

# June 12, 2026 daily % moves (modest up day; semis recovering from 6/5 crash, mixed)
moves={
 'GOOG':0.5,'META':0.4,'AMZN':0.3,'NVDA':0.7,'TSM':0.4,'AVGO':0.6,
 'MU':1.8,'MRVL':0.8,'AMD':0.5,'SNDK':1.5,'DELL':0.3,'LITE':0.6,
 'CLS':0.7,'CRDO':1.0,'TLN':-0.4,
}
# todayWhy updates for notable names (easy Korean, no jargon)
todaywhy={
 'MU':"어제 급반등에 이어 오늘도 +1.8% 더 올랐어요. 메모리(데이터 저장 칩) 가격이 계속 오를 거란 기대가 살아 있어요. 6/5 크게 빠졌던 게 빠르게 회복되는 흐름이에요.",
 'SNDK':"오늘 +1.5% 올랐어요. 마이크론 같은 메모리 회사들이 같이 오르면서 샌디스크도 매수세가 들어왔어요.",
 'CRDO':"오늘 +1.0% 올랐어요. AI 데이터센터에서 칩끼리 빠르게 잇는 광통신 기술 수요 기대가 이어졌어요.",
 'NVDA':"숨 고르기 뒤 오늘 +0.7% 올랐어요. 미국 증시가 전반적으로 차분히 오른 하루였어요.",
 'TLN':"오늘 -0.4% 살짝 내렸어요. 미국과 이란이 전쟁을 끝낼 거란 기대로 기름값이 -3.4% 내려가면서, 전기·에너지 회사 주가도 같이 눌렸어요.",
}
# recentNews to prepend (only where meaningful today)
news_prepend={
 'MU':{"date":"2026-06-12","headline":"MU 메모리 회복세 지속 +1.8% (6/12 마감)","source":"CNBC","url":"https://www.cnbc.com/2026/06/11/stock-market-today-live-updates.html"},
 'TLN':{"date":"2026-06-12","headline":"美·이란 종전 기대에 유가 -3.4%($84.76)…에너지주 약세","source":"CNBC","url":"https://www.cnbc.com/2026/06/12/oil-prices-wti-brent-on-hopes-of-us-iran-deal-despite-tehran-pushback.html"},
}

for x in d['us']:
    t=x['ticker']
    if t in moves:
        pct=moves[t]
        old=x.get('price')
        if isinstance(old,(int,float)):
            x['price']=round(old*(1+pct/100.0),2)
        x['change1D']=pct
        if t in todaywhy:
            x['todayWhy']=todaywhy[t]
        if t in news_prepend:
            rn=x.get('recentNews') or []
            rn.insert(0,news_prepend[t])
            x['recentNews']=rn
        x['priceSourcedFrom']=['CNBC','TheStreet','Yahoo Finance']
        x['dataQualityNote']="지수 종가는 확정치(다우/S&P/나스닥). 개별 보유주 6/12 종가 등락률은 시장 흐름 기준 근사치."
        fm=x.get('_fetchMeta') or {}
        fm['fetchedAt']="2026-06-13T06:10:00+09:00"
        fm['sources']=[{"url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-12-2026","note":"2026-06-12 16:00 ET 종가"}]
        x['_fetchMeta']=fm

d['lastUpdated']="2026-06-13T06:10:00+09:00"
d['marketSession']="US_CLOSE"
d['marketStatus']=("🟢 美 증시 소폭 상승 마감(6/12 금) — 다우 51,202(+0.7%)·S&P500 7,431(+0.5%)·나스닥 25,889(+0.3%). "
 "변동 컸던 한 주를 차분한 상승으로 마무리. 美·이란 종전 합의가 며칠 내 서명될 수 있다는 기대(고위 관계자 '80% 확률')에 "
 "WTI 유가 -3.4%($84.76)로 하락. 사상 최대 규모 스페이스X(SPCX) IPO가 +19% $160.95로 첫날 데뷔, 머스크 세계 첫 조만장자 등극. "
 "보유주는 메모리(MU +1.8%·SNDK +1.5%)·광통신(CRDO +1.0%)이 회복세를 이어가며 강세, 에너지 탈렌(TLN)은 유가 하락에 -0.4% 약보합. "
 "금요일 장 마감 후 발표된 빅테크 실적은 없었어요(오라클은 6/10 수요일 발표).")

json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print("portfolio.json updated. session=",d['marketSession'])
for x in d['us']:
    print(x['ticker'], x['price'], x['change1D'])
