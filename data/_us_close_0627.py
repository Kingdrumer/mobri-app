# -*- coding: utf-8 -*-
import json, copy

BASE='/sessions/friendly-peaceful-brown/mnt/claude/portfolio-pwa/data'
def load(p):
    with open(p,encoding='utf-8') as f: return json.load(f)
def save(p,o):
    with open(p,encoding='utf-8') as f: pass
    with open(p,'w',encoding='utf-8') as f: json.dump(o,f,ensure_ascii=False,indent=1)

# ---- close changes for Fri 6/26 (close), key=ticker -> close change1D %
close_chg = {
 'GOOG':-2.2,'META':1.5,'AMZN':1.6,'NVDA':-2.2,'TSM':-3.0,'AVGO':-3.6,
 'MU':-5.5,'MRVL':-5.0,'AMD':-4.5,'SNDK':-10.0,'DELL':-3.2,'LITE':-8.5,
 'CLS':-4.0,'CRDO':-6.0,'TLN':-3.2,
}
# new todayWhy at close
today_why = {
 'GOOG':"알파벳은 -2.2%로 마감했어요. 메타·아마존 같은 다른 빅테크는 반등했지만, 알파벳은 엔비디아와 함께 반등에 동참하지 못하고 약세였어요.",
 'META':"메타는 +1.5%로 반등 마감했어요. 반도체가 흔들린 와중에도 메타·아마존 같은 빅테크로 돈이 몰리는 방어적 매수가 들어왔어요.",
 'AMZN':"아마존은 +1.6%로 반등 마감했어요. 칩이 약했던 하루였지만 대형 빅테크로 자금이 이동하면서 강보합으로 버텼어요.",
 'NVDA':"엔비디아는 -2.2%로 마감했어요. 다른 빅테크가 반등할 때 알파벳과 함께 동참하지 못하고, AI 인프라 비용 우려에 칩과 같이 약세였어요.",
 'TSM':"TSMC는 -3.0%로 마감했어요. AI 반도체 전반이 약했던 하루라 같이 조정받았어요.",
 'AVGO':"브로드컴은 -3.6%로 마감했어요. AI 인프라 비용 우려가 칩 전반을 짓누르면서 약세를 이어갔어요.",
 'MU':"마이크론은 -5.5%로 마감했어요. 전날 실적 호조로 +15.7% 급등했던 만큼 차익실현(오른 김에 파는 것) 매물이 이어졌어요.",
 'MRVL':"마벨은 -5.0%로 마감했어요. 메모리·AI 칩 차익실현 흐름에 변동이 큰 종목이라 낙폭이 컸어요.",
 'AMD':"AMD는 -4.5%로 마감했어요. 반도체 전반 약세에 같이 밀렸어요.",
 'SNDK':"샌디스크는 -10%로 보유주 중 가장 크게 빠지며 마감했어요. 그동안 가장 많이 오른 메모리주라 차익실현 매물이 가장 크게 몰렸어요.",
 'DELL':"델은 -3.2%로 마감했어요. AI 서버 관련주라 칩 약세 분위기에 같이 눌렸어요.",
 'LITE':"루멘텀은 -8.5%로 크게 빠지며 마감했어요. 변동이 큰 광통신주라 AI 칩 차익실현에 낙폭이 컸어요.",
 'CLS':"셀레스티카는 -4.0%로 마감했어요. AI 서버·인프라 관련주라 칩 약세에 동반 조정받았어요.",
 'CRDO':"크레도는 -6.0%로 마감했어요. 변동이 큰 광통신 칩 종목이라 AI 인프라 비용 우려에 크게 출렁였어요.",
 'TLN':"탈렌에너지는 -3.2%로 마감했어요. AI 데이터센터 전력 테마가 약해진 분위기에 같이 내렸어요.",
}
# recentNews to prepend (date 2026-06-26)
recent = {
 'SNDK':{"date":"2026-06-26","headline":"SNDK -10% — 보유주 중 최대 낙폭, 메모리 차익실현 지속","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'MU':{"date":"2026-06-26","headline":"MU -5.5% — 실적 급등 뒤 차익실현 되돌림","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'NVDA':{"date":"2026-06-26","headline":"NVDA -2.2% — 빅테크 반등에 동참 못 하고 칩과 동반 약세","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'GOOG':{"date":"2026-06-26","headline":"GOOG -2.2% — 엔비디아와 함께 메가캡 반등서 소외","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'META':{"date":"2026-06-26","headline":"META +1.5% — 칩 약세 속 방어적 빅테크 매수에 반등","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'AMZN':{"date":"2026-06-26","headline":"AMZN +1.6% — 메가캡 반등에 강보합 마감","source":"CNBC","url":"https://www.cnbc.com/2026/06/26/global-tech-stocks-ai-infrastructure-costs-selloff-softbank-apple.html"},
 'LITE':{"date":"2026-06-26","headline":"LITE -8.5% — 광통신주 변동성 확대","source":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-26-2026"},
 'CRDO':{"date":"2026-06-26","headline":"CRDO -6.0% — AI 인프라 비용 우려에 광통신 칩 약세","source":"TheStreet","url":"https://www.thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-june-26-2026"},
}

# ===== portfolio.json =====
pf=load(f'{BASE}/portfolio.json')
import shutil
shutil.copy(f'{BASE}/portfolio.json', f'{BASE}/portfolio.json.before-us-close-0627.bak')
for s in pf['us']:
    t=s['ticker']
    if t in close_chg:
        oc=s.get('change1D',0)
        op=s.get('price')
        base = op/(1+oc/100) if op is not None else None  # prior(6/25) close
        nc=close_chg[t]
        if base is not None:
            np_=round(base*(1+nc/100), 2)
            s['price']=np_
        s['change1D']=nc
        s['todayWhy']=today_why[t]
        if t in recent:
            rn=s.get('recentNews',[])
            # avoid dup
            if not (rn and rn[0].get('date')=='2026-06-26'):
                rn.insert(0, recent[t])
            s['recentNews']=rn
        # userMemo untouched (preserve)
pf['marketSession']="US_CLOSED"
pf['lastUpdated']="2026-06-27T06:00:00+09:00"
pf['marketStatus']=("🔴 6/26(금) 美 정규장 마감 — 지수는 보합, 반도체는 약세. 다우 51,876.11(-0.09%)·S&P500 7,354.02(-0.05%)·나스닥 25,297.62(-0.24%, 5일 연속 하락). 장 막판 메타·아마존 등 빅테크 반등에 지수는 낙폭을 대부분 만회했지만, 엔비디아·알파벳과 반도체는 AI 인프라 비용 우려·'OpenAI 상장 내년 연기' 보도에 약세. 보유 메모리·광통신주 SNDK -10%·LITE -8.5%·CRDO -6.0%·MU -5.5%·MRVL -5.0% 조정. VIX 18.4(-2.7%)로 진정, 유가(WTI) $69.3(-3.6%) 4일째 하락. 금요일이라 빅테크 애프터아워 실적은 없었어요.")
save(f'{BASE}/portfolio.json', pf)
print('portfolio.json updated. sample:')
for s in pf['us']:
    print(' ',s['ticker'], s['price'], s['change1D'])
