# -*- coding: utf-8 -*-
import json, shutil
BASE='/sessions/friendly-peaceful-brown/mnt/claude/portfolio-pwa/data'
def load(p):
    with open(p,encoding='utf-8') as f: return json.load(f)
def save(p,o):
    with open(p,'w',encoding='utf-8') as f: json.dump(o,f,ensure_ascii=False,indent=1)

# ---- index.json ----
idx=load(f'{BASE}/reports/index.json')
shutil.copy(f'{BASE}/reports/index.json', f'{BASE}/reports/index.json.before-us-close-0627.bak')
entry={
 "date":"2026-06-27",
 "title":"6월 27일 (토) 06:00 미국 마감 캡처 — 지수 보합·나스닥 5일째 하락, 빅테크 막판 반등 vs 반도체 약세(SNDK -10%)",
 "summary":"다우 -0.09%·S&P -0.05%·나스닥 -0.24%(5일째↓). 메타·아마존 반등, 엔비디아·알파벳·반도체 약세. 보유 메모리·광통신 차익실현(SNDK -10%·LITE -8.5%·MU -5.5%). 금요일이라 애프터아워 실적 없음."
}
idx['reports']=[r for r in idx['reports'] if r.get('date')!='2026-06-27']
idx['reports'].append(entry)
idx['lastUpdated']="2026-06-27T06:00:00+09:00"
save(f'{BASE}/reports/index.json', idx)
print('index.json reports now:', len(idx['reports']), '| last:', idx['reports'][-1]['date'])

# ---- calendar-events.json ----
cal=load(f'{BASE}/calendar-events.json')
shutil.copy(f'{BASE}/calendar-events.json', f'{BASE}/calendar-events.json.before-us-close-0627.bak')
ev={
 "type":"us",
 "label":"美 마감(6/26)",
 "color":"red",
 "mood":"🔴",
 "time":"06:00 KST 美 마감(6/26) 캡처",
 "title":"🔴 美 6/26 마감 — 지수 보합·나스닥 5일째↓, 빅테크 반등 vs 반도체 약세(SNDK -10%)",
 "description":"6/26(금) 다우 51,876.11(-0.09%)·S&P500 7,354.02(-0.05%)·나스닥 25,297.62(-0.24%, 5일 연속↓). 개장 -1%대 빠졌다 메타·아마존 등 빅테크 반등에 낙폭 만회. 엔비디아·알파벳·반도체는 'AI 인프라 비용'·'OpenAI 상장 내년 연기' 보도에 약세. 보유 메모리·광통신 차익실현: SNDK -10%·LITE -8.5%·CRDO -6.0%·MU -5.5%·MRVL -5.0%. META +1.5%·AMZN +1.6%. VIX 18.4(-2.7%), WTI $69.3(-3.6%). 금요일이라 애프터아워 실적 없음."
}
cal['stock']['2026-06-27']=[ev]
cal['lastUpdated']="2026-06-27T06:00:00+09:00"
save(f'{BASE}/calendar-events.json', cal)
print('calendar 2026-06-27 added. stock keys:', len(cal['stock']))
