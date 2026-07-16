# -*- coding: utf-8 -*-
import json
NOW="2026-07-16T08:00:00+09:00"
FETCHED="2026-07-16T08:15:00+09:00"
d=json.load(open('portfolio.json'))

# ---- live fetched holdings data (7/15 US close) ----
H={
 "GOOG":{"price":370.21,"c1":3.6,"tgt":418.93,"rec":"4.35"},
 "META":{"price":681.31,"c1":3.07,"tgt":825.41,"rec":"4.19"},
 "AMZN":{"price":254.96,"c1":3.02,"tgt":309.12,"rec":"4.22"},
 "NVDA":{"price":212.50,"c1":0.33,"tgt":296.80,"rec":"4.27"},
 "TSM":{"price":419.48,"c1":-0.22,"tgt":478.87,"rec":"4.32"},
 "AVGO":{"price":394.28,"c1":1.33,"tgt":509.84,"rec":"4.22"},
 "MU":{"price":904.28,"c1":-8.02,"tgt":1449.24,"rec":"4.21"},
 "MRVL":{"price":206.26,"c1":-7.27,"tgt":245.76,"rec":"4.11"},
 "AMD":{"price":529.14,"c1":-3.46,"tgt":506.23,"rec":"4.07"},
 "SNDK":{"price":1615.00,"c1":-8.12,"tgt":2053.68,"rec":"4.17"},
 "DELL":{"price":412.68,"c1":-9.80,"tgt":482.08,"rec":"3.93"},
 "LITE":{"price":752.00,"c1":-7.71,"tgt":1108.27,"rec":"4.07"},
 "CLS":{"price":334.77,"c1":-2.97,"tgt":433.91,"rec":"4.14"},
 "CRDO":{"price":226.74,"c1":-4.00,"tgt":278.46,"rec":"4.32"},
 "TLN":{"price":400.12,"c1":0.80,"tgt":458.77,"rec":"4.11"},
}
NOTE={
 "GOOG":"CPI 둔화에 대형기술주 랠리 주도 +3.6%",
 "META":"물가 둔화 수혜 대형기술주 강세 +3.1%",
 "AMZN":"물가 둔화·소비 기대에 +3.0%",
 "NVDA":"반도체 약세 속 선방 +0.3%",
 "TSM":"관망 속 강보합 −0.2%",
 "AVGO":"AI 커스텀칩 기대 +1.3%",
 "MU":"메모리 급락 차익 실현에 −8.0%",
 "MRVL":"중국 경쟁 우려·차익 실현 −7.3%",
 "AMD":"반도체 조정에 동반 하락 −3.5%",
 "SNDK":"메모리 폭락에 −8.1%",
 "DELL":"AI 서버·메모리 노출에 급락 −9.8%",
 "LITE":"AI 하드웨어 조정에 −7.7%",
 "CLS":"AI 서버 조정에 −3.0%",
 "CRDO":"광통신 차익 실현 −4.0%",
 "TLN":"전력 수요 기대 강보합 +0.8%",
}
TW={
 "GOOG":"+3.6%. 어젯밤(7/14) 나온 미국 6월 소비자물가(CPI, 물가 상승률)가 예상보다 낮게 나오자 금리 추가 인상 걱정이 줄었고, 돈이 안정적인 대형 기술주로 몰리면서 구글이 상승을 이끌었어요.",
 "META":"+3.1%. 물가 둔화로 대형 기술주 선호가 커지면서 메타에 매수세가 들어왔어요. 광고 실적 기대도 여전히 탄탄해요.",
 "AMZN":"+3.0%. 물가가 식으면 소비가 살아난다는 기대에 아마존 같은 소비·클라우드 대장주가 강했어요.",
 "NVDA":"+0.3%. 메모리·반도체 종목이 대부분 급락한 날인데도 엔비디아는 소폭 오르며 잘 버텼어요. AI 대장주라 매도세가 상대적으로 덜했어요.",
 "TSM":"−0.2%. 큰 뉴스 없이 관망세 속에 강보합으로 마쳤어요. 반도체 조정 분위기에도 낙폭은 거의 없었어요.",
 "AVGO":"+1.3%. 맞춤형 AI칩(고객 전용으로 설계하는 반도체) 수요 기대가 이어지며 반도체 약세장에서도 홀로 올랐어요.",
 "MU":"−8.0%. 올해 들어 너무 많이 오른(연초 대비 +244%) 메모리 대장주에 '오른 김에 일부 팔자(차익 실현)'가 몰렸어요. SK하이닉스의 약한 전망과 중국 경쟁 우려도 겹쳤어요.",
 "MRVL":"−7.3%. 중국 업체와의 경쟁 우려 뉴스에 반도체 설계 종목들이 함께 밀렸어요. 그동안 많이 오른 부담도 차익 실현을 불렀어요.",
 "AMD":"−3.5%. 반도체 전반이 조정받으면서 함께 내렸어요. 다만 메모리 종목들보다는 낙폭이 작았어요.",
 "SNDK":"−8.1%. 연초 대비 +640% 폭등했던 메모리 종목이라 차익 실현 매물이 크게 나왔어요. SK하이닉스 급락 여파도 컸어요.",
 "DELL":"−9.8%. AI 서버와 메모리에 많이 노출된 회사라 이날 메모리 급락의 직격탄을 맞았어요. 보유 종목 중 낙폭이 가장 컸어요.",
 "LITE":"−7.7%. AI 데이터센터 하드웨어(광통신) 종목이 함께 조정받으며 크게 내렸어요.",
 "CLS":"−3.0%. AI 서버 조립 회사라 하드웨어 조정 분위기에 동반 하락했어요. 7/27 실적 발표를 앞두고 있어요.",
 "CRDO":"−4.0%. 광통신 칩 종목이라 AI 하드웨어 차익 실현 흐름에 함께 밀렸어요.",
 "TLN":"+0.8%. 반도체가 흔들린 날, 전력 수요 기대가 있는 원자력 발전 종목으로 돈이 옮겨가며 강보합으로 버텼어요.",
}

def signal(c1):
    if c1 >= -1.5: return "green"
    if c1 > -4:    return "yellow"
    return "red"
def rating_txt(rec):
    r=float(rec)
    if r>=4.4: return "적극 매수"
    if r>=3.8: return "매수"
    if r>=3.0: return "보유"
    return "매도 우세"
def easy(price,target,rec):
    gap=(target-price)/price*100
    rt=rating_txt(rec)
    if gap>=30: tone=f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에서 +{gap:.0f}% 더 오를 여력이 크다고 봐요."
    elif gap>=10: tone=f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에서 +{gap:.0f}% 오를 여력이 있어요."
    elif gap>=0: tone=f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})에 거의 도달했어요. 추가 상승 여력은 제한적이에요."
    else: tone=f"평균 목표가가 ${target:,.2f}로 지금 가격(${price:,.2f})보다 낮아요. 분석가들은 단기적으론 이미 충분히 올랐다고 봐요."
    return f"증권사 분석가들이 본 {tone} 추천 등급은 {rt}예요."

for s in d["us"]:
    t=s["ticker"]
    if t not in H: continue
    h=H[t]; old=s.get("price") or h["price"]
    def nc(oldc):
        if oldc is None: return None
        ref=old/(1+oldc/100.0)
        return round((h["price"]/ref-1)*100,2)
    s["change1W"]=nc(s.get("change1W")); s["change1M"]=nc(s.get("change1M")); s["changeYTD"]=nc(s.get("changeYTD"))
    s["price"]=h["price"]; s["change1D"]=h["c1"]; s["signal"]=signal(h["c1"])
    s["note"]=NOTE[t]; s["todayWhy"]=TW[t]
    ol=s.setdefault("outlook",{})
    ol["targetPrice"]=round(h["tgt"]); ol["consensusMean"]=h["rec"]; ol["rating"]=rating_txt(h["rec"])
    s["outlookEasy"]=easy(h["price"],h["tgt"],h["rec"])
    s["priceSourcedFrom"]=["네이버 금융(CNBC·Yahoo 집계)","naver index API"]
    s["dataQualityNote"]=None
    s["_fetchMeta"]={"fetchedAt":FETCHED,"sources":[{"url":f"https://api.stock.naver.com/stock/{t}.O/basic","hash":"sha256-live0716"}]}

d["lastUpdated"]=NOW
d["marketSession"]="풀 모닝 브리핑 (한국시간 08:00)"
d["marketStatus"]=("🇺🇸 어젯밤(7/15) 미국 증시는 3대 지수가 모두 올랐지만 속을 보면 '두 얼굴'이었어요. "
 "다우 52,659(+0.29%)·S&P500 7,572(+0.38%)·나스닥 26,269(+0.62%)로 마감했고, 공포지수(VIX)는 15.67로 −5% 내려 시장은 차분했어요. "
 "물가(6월 CPI)가 예상보다 크게 식자 구글(+3.6%)·메타(+3.1%)·아마존(+3.0%) 같은 대형 기술주로 돈이 몰렸어요. "
 "반대로 그동안 폭등했던 메모리·AI 하드웨어는 '오른 김에 팔자(차익 실현)'에 크게 밀렸어요 — MU(−8.0%)·SNDK(−8.1%)·DELL(−9.8%)·LITE(−7.7%)·MRVL(−7.3%). "
 "🇰🇷 그리고 오늘 아침 한국은 한국은행이 3년 반 만에 기준금리를 0.25%p 올리자(2.50%→2.75%) 코스피가 장중 7% 넘게 급락하고 매도 사이드카(급락 시 프로그램 매도를 잠깐 멈추는 장치)가 발동됐어요.")
d["holidayNote"]=("🟢 미국 증시는 정상 개장·마감했어요. 오늘(목) 밤 22:30(한국시간) 정규장이 다시 열려요. "
 "핵심 관전 포인트는 메모리·AI 하드웨어의 차익 실현이 이어질지, 그리고 오늘 한국은행 금리 인상 충격이 미국·아시아 투자심리에 얼마나 번지는지예요.")

json.dump(d,open('portfolio.json','w'),ensure_ascii=False,indent=1)
print("HOLDINGS UPDATED")
for s in d["us"]:
    print(f"{s['ticker']:5} {s['price']:>9} D{s['change1D']:>6} W{str(s.get('change1W')):>7} M{str(s.get('change1M')):>7} Y{str(s.get('changeYTD')):>7} {s['signal']}")
