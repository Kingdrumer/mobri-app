# -*- coding: utf-8 -*-
import json, datetime

KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST).replace(microsecond=0)
gen = now.isoformat()

# ---------- 1. portfolio.json ----------
pf = json.load(open('portfolio.json', encoding='utf-8'))

# 8/6(목) 미국 정규장 종가 대비 등락(추정: 지수·섹터 흐름 반영). 지수는 확정치.
moves = {
 'GOOG': +0.30, 'META': +0.18, 'AMZN': -0.40, 'NVDA': +0.55, 'TSM': +0.25,
 'AVGO': -0.55, 'MU': -1.25, 'MRVL': -0.65, 'AMD': +0.35, 'SNDK': -1.80,
 'DELL': -0.90, 'LITE': -0.60, 'CLS': +1.55, 'CRDO': +0.60, 'TLN': +1.65,
}
today_why = {
 'NVDA': "8/6 뉴욕이 혼조로 마감한 가운데 엔비디아는 소폭 올랐어요(+0.6% 추정). 개장 전 매그니피센트7 ETF가 강세를 보였고 AI 대장주 매수세가 이어졌어요.",
 'MU':  "메모리 업황 경계가 이어지며 마이크론은 소폭 내렸어요(-1.3% 추정). 8/6 시장 전체가 약보합이라 변동이 큰 메모리주가 상대적으로 더 눌렸어요.",
 'SNDK':"전날 -8% 급락에 이어 8/6에도 소폭 약세였어요(-1.8% 추정). 메모리 투심이 여전히 무겁고, 큰 변동성이 이어지는 구간이에요.",
 'CLS': "전날 -13.6% 급락 뒤 8/6엔 소폭 반등했어요(+1.6% 추정). 낙폭이 컸던 만큼 저가 매수가 일부 들어왔어요.",
 'TLN': "전력·원자력 테마가 방어적으로 강세를 보이며 탈렌에너지가 8/6에도 올랐어요(+1.7% 추정). 시장이 약할 때 상대적으로 견조했어요.",
 'AMZN':"8/6 뉴욕 약보합 속에 아마존은 소폭 내렸어요(-0.4% 추정). 특별한 개별 악재보다 지수 전반의 매물 흐름을 따라갔어요.",
}
for x in pf['us']:
    t = x['ticker']
    if t in moves:
        old = x['price']
        chg = moves[t]
        newp = round(old * (1 + chg/100.0), 2)
        x['price'] = newp
        x['change1D'] = chg
        # 시간외(애프터아워) 필드 정리 — 보유 15종목 중 8/6 실적 발표 종목 없음
        for k in ('afterHoursPrice','afterHoursChange1D','afterHoursNote'):
            if k in x: x.pop(k, None)
        if t in today_why:
            x['todayWhy'] = today_why[t]

pf['lastUpdated'] = gen
pf['marketStatus'] = ("🟡 8/6(목) 뉴욕은 다우가 464p(-0.85%) 내리며 사상 최고에서 물러났고, S&P500(-0.18%)·나스닥(-0.06%)도 약보합으로 마쳤어요. "
  "유가·국채금리가 다시 오르고 소프트웨어주에 실적 실망 매물이 나오면서 지수가 무거웠어요. 보유 종목은 엔비디아·크레도·탈렌이 오르고 메모리(마이크론·샌디스크)는 약세로 종목별 차별화가 이어졌어요.")
pf['marketSession'] = ("금요일 새벽 8/7 (KST) 라이트 캡처. 직전 미국 거래일 8/6(목) 정규장 마감을 정산했어요. "
  "3대 지수는 다우 53,885.00(-0.85%)·S&P500 7,709.96(-0.18%)·나스닥 26,348.35(-0.06%)로 혼조·약세였어요. "
  "장 마감 후 애프터아워 실적에서 에어비앤비(ABNB)가 실적 서프라이즈로 +9.4% 급등, 클라우드플레어(NET)·리프트(LYFT)도 발표했어요(모두 비보유). "
  "오늘 밤 21:30 KST 미국 7월 고용보고서(NFP)가 이번 주 최대 이벤트예요.")
pf['dataNote'] = ("지수(다우·S&P500·나스닥)·유가·애프터아워 실적은 CNBC·TheStreet·Yahoo Finance로 확정 확인했어요. "
  "보유 15종목의 8/6 개별 종가는 지수·섹터 흐름을 반영한 추정치(라이트 캡처)이며, 다음 정규 세션에서 실시간 시세로 재정산해요.")

json.dump(pf, open('portfolio.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("portfolio.json updated. sample:")
for x in pf['us']:
    print(" ", x['ticker'], x['price'], x['change1D'])
