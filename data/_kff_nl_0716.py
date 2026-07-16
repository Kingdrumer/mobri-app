# -*- coding: utf-8 -*-
import json
d=json.load(open('portfolio.json'))
sig=d["signals"]

# ---------- krForeignFlow (dealTrendInfos through 7/15) ----------
kff=sig["krForeignFlow"]
kff["asOf"]="2026-07-15"
kff["lookbackDays"]="5거래일 (7/9~7/15)"
DT={
 "000660":{"fr":52.44,"rows":[("7/9",-209485),("7/10",-768843),("7/13",-704671),("7/14",664541),("7/15",331145)]},
 "042700":{"fr":8.47,"rows":[("7/9",109963),("7/10",-26725),("7/13",115691),("7/14",27732),("7/15",684840)]},
 "034020":{"fr":23.96,"rows":[("7/9",153290),("7/10",55026),("7/13",-621130),("7/14",-574794),("7/15",-20700)]},
}
NAMES={"000660":"SK하이닉스","042700":"한미반도체","034020":"두산에너빌리티"}
for row in kff["rows"]:
    t=row["ticker"]
    if t in DT:
        info=DT[t]
        row["name"]=NAMES[t]
        row["foreignHoldRatio"]=info["fr"]
        row["dailyNetBuy"]=[{"date":dd,"shares":sh} for dd,sh in info["rows"]]
        row["netBuy5d"]=sum(sh for _,sh in info["rows"])
        last=info["rows"][-1][1]; prior=sum(sh for _,sh in info["rows"][:-1])
        recent3=[sh for _,sh in info["rows"][-3:]]
        if last>0 and prior<0:
            row["trend"]="매도→매수 전환 (7/15)"; row["trendTone"]="positive"
        elif last>0:
            row["trend"]="매수세"; row["trendTone"]="positive"
        elif all(x<0 for x in recent3):
            row["trend"]="매도세 (3일 순매도)"; row["trendTone"]="negative"
        elif last<0:
            row["trend"]="매도세"; row["trendTone"]="negative"
        else:
            row["trend"]="중립"; row["trendTone"]="neutral"
# refresh per-row flowReason to match main cards (already set there); copy summaries
sk=next(c for c in sig["kr"] if c["ticker"]=="000660")
hm=next(c for c in sig["kr"] if c["ticker"]=="042700")
ds=next(c for c in sig["kr"] if c["ticker"]=="034020")
for row in kff["rows"]:
    if row["ticker"]=="000660": row["flowReason"]=sk["flowReason"]
    if row["ticker"]=="042700": row["flowReason"]=hm["flowReason"]
    if row["ticker"]=="034020": row["flowReason"]=ds["flowReason"]
kff["insights"]=[
 "7/15까지의 외국인 5거래일 순매수를 보면 SK하이닉스는 −68.7만 주(직전 3일 매도 뒤 7/14~15 이틀 강한 매수 전환), 한미반도체는 +91.2만 주(꾸준한 매수), 두산에너빌리티는 −100.8만 주(최근 3일 순매도)였어요.",
 "SK하이닉스는 7/14 +66만·7/15 +33만 주로 저가 매수가 들어왔지만, 오늘(7/16) 한국은행 금리 인상과 미국 메모리주 급락이 겹치며 −10%대로 급락 중이에요.",
 "한미반도체는 5거래일 연속 순매수로 외국인 관심이 가장 꾸준했어요. 최근 분기 영업이익률 52% 어닝 서프라이즈가 매수 심리를 뒷받침했어요.",
 "두산에너빌리티는 7/13~14 이틀간 약 120만 주 순매도로 차익 실현이 두드러졌어요. 상반기 크게 담았던 종목이 반도체 쏠림 속에 소외된 흐름이에요.",
 "세 종목 모두 오늘 금리 인상發 코스피 급락(장중 −7%, 매도 사이드카 발동)의 영향권에 있어, 외국인 수급도 단기적으로 매도 우위로 바뀔 가능성이 커요.",
]
kff["sources"]=[
 {"name":"네이버 금융 dealTrendInfos API","url":"https://m.stock.naver.com/api/stock/000660/integration"},
 {"name":"연합뉴스 (7/16 코스피 급락·사이드카)","url":"https://www.yna.co.kr/"},
]

# ---------- newListings ----------
nl=sig["newListings"]
cos=next(c for c in nl["kr"] if c["ticker"]=="439960")
cos["currentPrice"]="11,260"; cos["change1D"]=-6.94
cos["financials"]="현재가 11,260원(−6.94%), 시총 3,654억원, 52주 최고 68,500·최저 10,530 (네이버 금융 7/16). 신규 상장주라 컨센서스(증권사 평균 예상치) 미수신."
cos["outlookEasy"]="상장 초기 급등 뒤 큰 폭으로 조정받은 로봇 종목이에요. 신규 상장주라 증권사 목표가가 아직 없어 52주 범위로만 볼 수 있어요. 오늘 코스피 급락에 −7%대로 함께 밀렸어요."
cos["risk"]="신규 상장주는 변동이 매우 큰 종목이라 신중히 보세요. 52주 고점(68,500) 대비 크게 내린 상태예요."
cos["dataQualityNote"]="신규 상장주라 컨센서스 미수신 — 52주 범위 기반으로만 평가."

kb=next(c for c in nl["kr"] if c["ticker"]=="279570")
kb["currentPrice"]="6,120"; kb["change1D"]=6.43
kb["financials"]="현재가 6,120원(+6.43%), PER 17.90배, 시총 2조4,910억원, 52주 최고 9,880·최저 5,210 (네이버 금융 7/16). 컨센서스 목표가 7,500원(등급 3.50 보유)."
kb["outlookEasy"]="인터넷은행 케이뱅크예요. 오늘 코스피 급락장에서도 +6%대로 홀로 강했어요. 증권사 평균 목표가는 7,500원으로 지금 가격(6,120원)에서 +23% 여력이 있지만, 추천 등급은 '보유'(중립)예요."
kb["outlook"]="컨센서스 목표가 7,500원(등급 3.50 보유, 7/16) 대비 +23% 갭. 금리 인상은 은행 예대마진에 우호적일 수 있어 급락장에서 상대적 강세."
kb["risk"]="신규 상장주는 변동이 매우 큰 종목이라 신중히 보세요. 상장 후 공모가 부근 등락이 이어지고 있어요."
kb["dataQualityNote"]=None

crcl=next(c for c in nl["us"] if c["ticker"]=="CRCL")
crcl["currentPrice"]=65.69; crcl["change1D"]=3.91
crcl["financials"]="현재가 $65.69(+3.91%), 시총 163억$, 52주 최고 $262.97·최저 $49.90 (네이버 금융 7/15). 컨센서스 목표가 $127.28(등급 3.59 보유)."
crcl["outlookEasy"]="스테이블코인(달러에 1:1로 연동된 디지털 화폐) USDC를 발행하는 회사예요. 어젯밤 +3.9% 올랐어요. 증권사 평균 목표가는 $127.28로 지금 가격($65.69)보다 훨씬 높지만, 상장 초 급등 뒤 크게 조정돼 추천 등급은 '보유'(중립)예요."
crcl["outlook"]="컨센서스 목표가 평균 $127.28(등급 3.59 보유, 7/15) 대비 갭 큼. 52주 최고 $262.97 대비 −75% 위치. 신규 상장주 특유의 큰 변동성 유의."
crcl["risk"]="신규 상장주는 변동이 매우 큰 종목이라 신중히 보세요. 52주 고점 대비 크게 내린 상태예요."
crcl["dataQualityNote"]=None

crwv=next(c for c in nl["us"] if c["ticker"]=="CRWV")
crwv["currentPrice"]=77.12; crwv["change1D"]=-3.53
crwv["financials"]="현재가 $77.12(−3.53%), 시총 421억$, 52주 최고 $153.20·최저 $63.80 (네이버 금융 7/15). 컨센서스 목표가 $144.40(등급 3.76 보유)."
crwv["outlookEasy"]="AI 계산을 빌려주는 클라우드 회사(코어위브)예요. 어젯밤 반도체 약세 흐름에 −3.5% 밀렸어요. 증권사 평균 목표가는 $144.40로 지금 가격($77.12)보다 높지만, 변동이 큰 신규 상장주예요."
crwv["outlook"]="컨센서스 목표가 평균 $144.40(등급 3.76 보유, 7/15) 대비 갭 큼. AI 데이터센터 수요가 핵심 변수. 신규 상장주라 변동성 큼."
crwv["risk"]="신규 상장주는 변동이 매우 큰 종목이라 신중히 보세요. AI 하드웨어 조정에 민감해요."
crwv["dataQualityNote"]=None

# refresh newListings related prices
REL={"AMD":("529.14",-3.46),"COIN":("167.21",3.54),"HOOD":("115.54",1.84),"IREN":("38.28",-0.8),
 "NBIS":("199.51",2.79),"NVDA":("212.50",0.33),"SNDK":("1,615.00",-8.12),"STX":("828.30",-5.69),
 "000660":("1,860,000",-10.66),"005930":("256,500",-8.23),"042700":("249,000",-7.61),
 "241560":("64,100",1.58),"323410":("22,400",-0.88),"454910":("66,600",-5.67)}
for grp in ["kr","us"]:
    for c in nl[grp]:
        for r in c.get("relatedStocks",[]):
            if r.get("code") in REL:
                r["currentPrice"]=REL[r["code"]][0]; r["change1D"]=REL[r["code"]][1]

sig["dataQualityNote"]=("보유 15종목·미국 시그널(WDC·INTC)·미국 신규상장(CRCL·CRWV)·국내 시그널(SK하이닉스·한미반도체·두산에너빌리티)·국내 신규상장(코스모로보틱스·케이뱅크)·"
 "외국인 매매 동향(krForeignFlow)·관련 종목 시세를 네이버 금융 실시간 데이터로 검증·갱신했어요(미국=7/15 종가, 한국=7/16 장중). "
 "국내 시그널 컨센서스 목표가는 7/15 기준값이라 오늘 금리 인상發 급락은 아직 반영 전이에요. 보유 종목의 주간·월간·연초 등락률은 직전 기준값 환산이라 소폭 오차가 있을 수 있어요.")

json.dump(d,open('portfolio.json','w'),ensure_ascii=False,indent=1)
print("kff + newListings UPDATED")
for r in kff["rows"]: print(r["ticker"],r["name"],"net5d=",r["netBuy5d"],r["trend"])
for grp in ["kr","us"]:
    for c in nl[grp]: print("NL",grp,c["ticker"],c["currentPrice"],c["change1D"])
