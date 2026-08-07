#!/usr/bin/env python3
import json, urllib.request, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
NOW="2026-08-08T08:20:00+09:00"
def fj(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req,timeout=15).read().decode())

# extra PLTR related
def price(t,sufs):
    for s in sufs:
        try:
            b=fj(f"https://api.stock.naver.com/stock/{t}{s}/basic"); return b['closePrice'],b['fluctuationsRatio'],b['stockExchangeName']
        except: pass
    return None,None,None
crwd=price('CRWD',['','.O','.K']); snow=('330.49',3.93,'NYSE')
print("CRWD",crwd)

p=json.load(open("portfolio.json"))

# ---- KR foreign flow rows ----
def flow(name,code):
    d=fj(f"https://m.stock.naver.com/api/stock/{code}/integration")
    ti={it['code']:it['value'] for it in (d.get('totalInfos') or [])}
    dts=d.get('dealTrendInfos') or []
    rows=[]
    for r in dts[:5]:
        bd=r.get('bizdate'); q=str(r.get('foreignerPureBuyQuant')).replace(',','').replace('+','')
        md=f"{int(bd[4:6])}/{int(bd[6:8])}"
        rows.append({"date":md,"shares":int(q)})
    rows=list(reversed(rows))
    net5=sum(x['shares'] for x in rows)
    last=rows[-1]['shares']; prev4=sum(x['shares'] for x in rows[:-1])
    if last>0 and prev4<0: trend,tone=f"매도→매수 전환 ({rows[-1]['date']})","positive"
    elif last>0: trend,tone="매수세","positive"
    elif all(x['shares']<0 for x in rows[-3:]): trend,tone=f"매도세 (3일 순매도)","negative"
    elif last<0: trend,tone="매도세","negative"
    else: trend,tone="중립","neutral"
    fr=ti.get('foreignRate')
    frv=float(fr.replace('%','')) if fr else None
    return {"ticker":code,"name":name,"foreignHoldRatio":frv,"netBuy5d":net5,"dailyNetBuy":rows,"trend":trend,"trendTone":tone}, ti, d

r_hanwha, ti_h, _ = flow("한화에어로스페이스","012450")
r_hynix, ti_x, _ = flow("SK하이닉스","000660")
r_hanmi, ti_m, _ = flow("한미반도체","042700")

krForeignFlow={
 "asOf":"2026-08-07","lookbackDays":"5거래일 (8/1~8/7)",
 "rows":[r_hanwha,r_hynix,r_hanmi],
 "insights":[
   "8/7 국내 증시는 외국인 순매도로 코스피가 2거래일 연속 하락했어요(6,250선 후퇴).",
   f"한화에어로스페이스는 최근 5거래일 외국인이 모두 순매수(+{r_hanwha['netBuy5d']:,}주)하며 방산주 중 가장 강한 매수세를 보였어요.",
   f"SK하이닉스는 5일 합계 외국인 {r_hynix['netBuy5d']:,}주로 대량 순매도가 집중됐어요 — '루빈 GPU의 HBM 채용 축소' 우려와 차익실현이 겹친 결과예요.",
   f"한미반도체도 5일 합계 {r_hanmi['netBuy5d']:,}주로 외국인이 계속 팔았어요. HBM 장비 수요 불확실성이 반영됐어요.",
   "메모리·HBM 관련주(하이닉스·한미반도체)에 외국인 매도가 몰린 반면, 방산·이차전지 등 비반도체로 순환매가 나타났어요.",
 ],
 "sources":[
   {"name":"네이버 금융 dealTrendInfos API","url":"https://m.stock.naver.com/api/stock/000660/integration"},
   {"name":"핀포인트뉴스 주간 외국인(8/8)","url":"https://www.pinpointnews.co.kr/news/articleView.html?idxno=475483"},
   {"name":"뉴시안 '삼전닉스 쏠림'(8/8)","url":"http://www.newsian.co.kr/news/articleView.html?idxno=93463"},
 ],
}

# flowReason
r_hanwha["flowReason"]={"summary":"방산 순환매 + 지정학 긴장에 외인 5일 연속 순매수",
 "detail":"호르무즈 해협 긴장이 이어지는 가운데 8/7 코스피에서 방산·이차전지로 순환매가 유입됐어요. 한화에어로스페이스는 +4.08% 오르며 외국인이 5거래일 연속 순매수했어요.",
 "sources":[{"name":"비즈니스코리아 마감시황(8/7)","url":"https://www.businesskorea.co.kr/news/articleView.html?idxno=274390"}]}
r_hynix["flowReason"]={"summary":"'루빈 GPU HBM 축소' 우려 + 차익실현에 외인 대량 매도",
 "detail":"엔비디아 차기 '루빈' GPU가 HBM(고대역폭 메모리)을 덜 쓸 수 있다는 우려에 반도체주가 급락했어요. SK하이닉스는 -4.88% 내렸고 외국인 순매도가 가장 컸어요.",
 "sources":[{"name":"핀포인트뉴스 주간 외국인(8/8)","url":"https://www.pinpointnews.co.kr/news/articleView.html?idxno=475483"},
  {"name":"00뉴스 '클릭 증시'(8/7)","url":"http://www.00news.co.kr/news/articleView.html?idxno=105729"}]}
r_hanmi["flowReason"]={"summary":"HBM 장비 수요 불확실성에 외인 매도 지속",
 "detail":"'루빈 GPU HBM 축소' 우려가 HBM 본딩 장비 대장주인 한미반도체에도 번졌어요. -4.09% 내렸고 외국인이 5거래일 연속 순매도했어요.",
 "sources":[{"name":"00뉴스 '클릭 증시'(8/7)","url":"http://www.00news.co.kr/news/articleView.html?idxno=105729"}]}

# ---- signal cards ----
def easy_grade(m):
    m=float(m)
    if m>=4.4: return "적극 매수"
    if m>=3.8: return "매수"
    if m>=3.0: return "보유(중립)"
    return "매도 우세"

kr_hanwha={
 "ticker":"012450","name":"한화에어로스페이스","market":"KOSPI","category":"관련주",
 "thesis":"국내 대표 방산주예요. 호르무즈 해협 긴장이 이어지며 방산으로 순환매(돈이 옮겨오는 것)가 들어왔고, 8/7 +4.08% 올랐어요. 외국인이 최근 5거래일 연속 순매수한 점이 눈에 띄어요.",
 "currentPrice":"1,097,000","change1D":4.08,
 "company":{"ceo":"손재일 (대표이사)","business":"항공기 엔진·정밀유도무기·방산 시스템을 만드는 국내 1위 방산 기업. K9 자주포·천무 등 수출.","hq":"대한민국 경기 성남","employees":"-","homepage":"https://www.hanwhaaerospace.com/","ceoSource":"네이버 뉴스 검증 (2026/08 보도)"},
 "financials":f"PER 34.45배·추정PER 24.64배, 시총 56조5,651억원, 52주 최고 1,713,000·최저 783,000 (네이버 금융 8/7). 외인소진율 45.39%.",
 "comparable":"8/7 방산주 동반 강세 — LIG넥스원 +5.56%·현대로템 +1.87% (네이버 금융 8/7 종가).",
 "outlookEasy":"증권사 분석가 평균 목표가는 약 163만원으로 지금(약 110만원)에서 여력이 있어요. 추천 등급은 매수(4.00)예요. 다만 지정학 이슈에 따라 오르내림이 큰 종목이라 흐름을 가볍게 지켜보면 좋아요.",
 "outlook":"컨센서스 목표가 평균 1,628,235원(등급 4.00 매수) 대비 현재가 약 +48% 여력. 외인 5일 순매수 + 지정학 프리미엄이 단기 수급 지지. 단기 변수: 호르무즈 긴장 완화 시 방산 프리미엄 축소.",
 "risk":"지정학 뉴스에 따라 변동이 큰 종목이에요. 긴장이 풀리면 방산 프리미엄이 빠르게 줄 수 있어요.",
 "horizon":"3~6개월 (중기)",
 "relatedStocks":[
   {"code":"079550","name":"LIG넥스원","market":"KOSPI","relation":"정밀유도무기 경쟁사 — 방산 테마 동행","currentPrice":"741,000","change1D":5.56},
   {"code":"064350","name":"현대로템","market":"KOSPI","relation":"지상장비 방산주 — 수출 모멘텀 동행","currentPrice":"146,900","change1D":1.87}],
 "flowReason":r_hanwha["flowReason"],
 "sources":[{"name":"네이버 금융 (실시간)","url":"https://m.stock.naver.com/domestic/stock/012450"},
  {"name":"비즈니스코리아 마감시황(8/7)","url":"https://www.businesskorea.co.kr/news/articleView.html?idxno=274390"}],
}
kr_hynix={
 "ticker":"000660","name":"SK하이닉스","market":"KOSPI","category":"관련주",
 "thesis":"HBM(고대역폭 메모리) 세계 1위예요. 8/7 '엔비디아 차기 루빈 GPU가 HBM을 덜 쓸 수 있다'는 우려에 -4.88% 내렸고 외국인이 대량으로 팔았어요. 보유 종목 마이크론(MU)·샌디스크(SNDK)와 같은 메모리 사이클을 타요.",
 "currentPrice":"1,422,000","change1D":-4.88,
 "company":{"ceo":"곽노정 (대표이사)","business":"D램·낸드·HBM을 만드는 세계 2위 메모리 반도체 기업. AI용 HBM에서 세계 1위.","hq":"대한민국 경기 이천","employees":"-","homepage":"https://www.skhynix.com/","ceoSource":"네이버 뉴스 검증 (2026/08 보도)"},
 "financials":"PER 13.74배·추정PER 4.11배, 시총 1,038조원, 52주 최고 3,002,000·최저 244,000 (네이버 금융 8/7). 외인소진율 50.84%.",
 "comparable":"8/7 메모리·장비주 동반 약세 — 한미반도체 -4.09%·주성엔지니어링 -4.20% (네이버 금융 8/7 종가).",
 "outlookEasy":"증권사 분석가 평균 목표가는 약 332만원으로 지금(약 142만원)보다 크게 높아요(추정PER 4배 수준의 저평가 매력). 추천 등급은 매수(4.00). 다만 'HBM 수요가 줄 수 있다'는 단기 우려로 변동이 큰 상태예요.",
 "outlook":"컨센서스 목표가 평균 3,322,083원(등급 4.00) 대비 큰 상방 여력이나, 52주 최고 대비 -53% 위치로 조정폭도 컸어요. 추정PER 4.11배는 저평가 신호. 단기 변수: 루빈 GPU HBM 채용 물량 확인.",
 "risk":"HBM 수요 관련 뉴스에 따라 변동이 매우 큰 종목이에요. 외국인 매도세가 이어지면 추가 조정 가능성도 있어요.",
 "horizon":"6~12개월 (장기)",
 "relatedStocks":[
   {"code":"005930","name":"삼성전자","market":"KOSPI","relation":"HBM 경쟁사 — 메모리 사이클 같이 움직임","currentPrice":"231,000","change1D":0.22},
   {"code":"042700","name":"한미반도체","market":"KOSPI","relation":"HBM 본딩 장비 공급 — 하이닉스 투자에 연동","currentPrice":"192,300","change1D":-4.09}],
 "flowReason":r_hynix["flowReason"],
 "sources":[{"name":"네이버 금융 (실시간)","url":"https://m.stock.naver.com/domestic/stock/000660"},
  {"name":"뉴시안 '삼전닉스 쏠림'(8/8)","url":"http://www.newsian.co.kr/news/articleView.html?idxno=93463"}],
}
kr_hanmi={
 "ticker":"042700","name":"한미반도체","market":"KOSPI","category":"관련주",
 "thesis":"HBM을 쌓아 붙이는 '본딩' 장비의 대장주예요. 8/7 '루빈 GPU HBM 축소' 우려가 장비주로 번지며 -4.09% 내렸고 외국인이 계속 팔았어요. 보유 종목 마이크론·SK하이닉스 투자 흐름과 연결돼요.",
 "currentPrice":"192,300","change1D":-4.09,
 "company":{"ceo":"곽동신 (대표이사 회장)","business":"HBM용 본딩 장비(반도체를 쌓아 붙이는 기계)를 만드는 국내 대표 반도체 장비 회사.","hq":"대한민국 경기 인천","employees":"-","homepage":"https://www.hanmisemi.com/","ceoSource":"네이버 뉴스 검증 (2026/08 보도)"},
 "financials":"PER 103.00배, 시총 18조3,285억원, 52주 최고 426,000·최저 81,400 (네이버 금융 8/7). 외인소진율 7.88%.",
 "comparable":"8/7 반도체 장비주 동반 약세 — 주성엔지니어링 -4.20%·원익IPS -4.64% (마감시황 보도).",
 "outlookEasy":"증권사 분석가 평균 목표가는 약 38만원으로 지금(약 19만원)보다 높아요(등급 매수 4.00). 다만 PER 103배로 비싼 편이고 HBM 장비 수요 불확실성으로 변동이 큰 상태예요.",
 "outlook":"컨센서스 목표가 평균 380,000원(등급 4.00) 대비 큰 상방이나 PER 103배로 밸류 부담. 52주 최고 대비 -55% 위치. 단기 변수: HBM 증설 발주 확인, 외인 매도세 지속 여부.",
 "risk":"PER이 높고 HBM 장비 수요 뉴스에 민감해 변동이 매우 큰 종목이에요.",
 "horizon":"3~6개월 (중기)",
 "relatedStocks":[
   {"code":"000660","name":"SK하이닉스","market":"KOSPI","relation":"핵심 고객사 — HBM 증설 발주에 직접 연동","currentPrice":"1,422,000","change1D":-4.88},
   {"code":"036930","name":"주성엔지니어링","market":"KOSPI","relation":"반도체 장비 동종 — 투자 사이클 동행","currentPrice":"127,800","change1D":-4.20}],
 "flowReason":r_hanmi["flowReason"],
 "sources":[{"name":"네이버 금융 (실시간)","url":"https://m.stock.naver.com/domestic/stock/042700"},
  {"name":"00뉴스 '클릭 증시'(8/7)","url":"http://www.00news.co.kr/news/articleView.html?idxno=105729"}],
}

# US signals
pltr_rel=[{"code":"SNOW","name":"스노우플레이크 (Snowflake)","market":"NYSE","relation":"AI·데이터 분석 SW — 같은 테마 동행","currentPrice":"330.49","change1D":3.93}]
if crwd[0]: pltr_rel.append({"code":"CRWD","name":"크라우드스트라이크 (CrowdStrike)","market":"NASDAQ","relation":"미 정부·기업용 SW 대표주 — AI SW 동행","currentPrice":crwd[0],"change1D":crwd[1]})

us_pltr={
 "ticker":"PLTR","name":"팰런티어 (Palantir)","market":"NASDAQ","category":"실적기대",
 "thesis":"미국 정부·기업용 AI 데이터 분석 소프트웨어 회사예요. 8/4 발표한 2분기 매출이 1년 전보다 +93% 늘어난 19억3,500만 달러로 깜짝 실적을 냈고, 그 여파로 8/7 +10.32% 급등했어요. AI 플랫폼(AIP) 수요가 계속 커지고 있어요.",
 "currentPrice":172.01,"change1D":10.32,
 "company":{"ceo":"Peter A. Thiel (창업자·회장)","business":"AI 데이터 분석 소프트웨어 회사. 미국 국방·정보기관용 Gotham·Foundry·AIP 플랫폼 운영.","hq":"미국 콜로라도 덴버","employees":"4,395명 (2026-03-31 기준)","homepage":"https://www.palantir.com/","ceoSource":"네이버 금융 integration API summaries"},
 "financials":"PER 193.80배, 시총 4,134억 달러, 52주 최고 $207.52·최저 $106.37 (네이버 금융 8/7). 2Q 매출 +93%(19.35억$, 8/4 발표).",
 "comparable":"8/7 AI 소프트웨어주 동반 강세 — 스노우플레이크 +3.93% 등 (네이버 금융 8/7 종가).",
 "outlookEasy":"분석가 평균 목표가는 $185.36로 지금($172.01)에서 +8% 근처예요 — 거의 도달했고 추가 상승 여력은 제한적. 추천 등급은 매수(3.88). 다만 분석가별 의견이 $70~$255로 크게 갈려요. PER 194배로 비싸서 8/12 미국 물가(CPI)가 높게 나오면 크게 흔들릴 수 있어요.",
 "outlook":"컨센서스 목표가 평균 $185.36(등급 3.88 매수) 대비 +7.8% 여력. 분포 $70~$255로 매우 넓어 의견 양분. 단기 트리거: 8/12 미 7월 CPI. 시나리오: 최고 도달 시 +48%, 최저 도달 시 -59%.",
 "risk":"PER 194배로 비싼 종목이라 물가·금리 뉴스에 변동이 매우 커요. 실적 급등 뒤 차익실현도 나올 수 있어요.",
 "horizon":"3~6개월 (중기)",
 "relatedStocks":pltr_rel,
 "sources":[{"name":"네이버 금융 (실시간)","url":"https://m.stock.naver.com/worldstock/stock/PLTR.O"},
  {"name":"서울경제 '아마존 3조달러'(8/4, 팰런티어 2Q +93% 언급)","url":"https://www.sedaily.com/article/20075680"}],
}
us_aaoi={
 "ticker":"AAOI","name":"어플라이드 옵토일렉트로닉스 (Applied Optoelectronics)","market":"NASDAQ","category":"관련주",
 "thesis":"AI 데이터센터용 광통신(빛으로 데이터를 주고받는 기술) 부품을 수직통합(부품부터 완제품까지 직접)으로 만드는 회사예요. 8/7 +9.19% 급등했어요. 보유 종목 루멘텀(LITE)·크레도(CRDO)·셀레스티카(CLS)와 같은 광통신 테마를 타요.",
 "currentPrice":135.63,"change1D":9.19,
 "company":{"ceo":"Chih-Hsiang (Thompson) Lin","business":"광섬유 네트워킹 제품을 수직통합으로 설계·제조. 데이터센터·통신·CATV용 광 모듈 공급.","hq":"미국 텍사스 슈가랜드","employees":"4,691명 (2025-12-31 기준)","homepage":"https://ao-inc.com/","ceoSource":"네이버 금융 integration API summaries"},
 "financials":"PER N/A(순이익 적자, EPS -0.55), 시총 115억 달러, 52주 최고 $233.67·최저 $18.50 (네이버 금융 8/7).",
 "comparable":"8/7 광통신주 동반 강세 — 보유 종목 LITE +6.22%·CRDO +8.45%, 코히어런트 +13.44%·파브리넷 +3.39% (네이버 금융 8/7 종가).",
 "outlookEasy":"분석가 평균 목표가는 $137.92로 지금($135.63)과 거의 같아요 — 추가 상승 여력은 제한적. 추천 등급은 보유(중립, 3.57). 아직 적자 회사라 변동이 매우 크고, 분석가 의견도 $41~$220으로 크게 갈려요.",
 "outlook":"컨센서스 목표가 평균 $137.92(등급 3.57 보유) 대비 +1.7%로 거의 도달. 분포 $41~$220으로 매우 넓음. 적자 기업이라 밸류 부담. 단기 트리거: 광통신 수요·실적, 8/12 CPI. 시나리오: 최고 도달 시 +62%, 최저 도달 시 -70%.",
 "risk":"아직 적자인 회사라 변동이 매우 큰 종목이에요. 광통신 수요 뉴스에 급등락할 수 있어요.",
 "horizon":"1~3개월 (단기)",
 "relatedStocks":[
   {"code":"COHR","name":"코히어런트 (Coherent)","market":"NYSE","relation":"광통신·레이저 경쟁사 — 데이터센터 광 수요 동행","currentPrice":"379.13","change1D":13.44},
   {"code":"FN","name":"파브리넷 (Fabrinet)","market":"NYSE","relation":"광 모듈 위탁생산 — 광통신 밸류체인 동행","currentPrice":"562.38","change1D":3.39}],
 "sources":[{"name":"네이버 금융 (실시간)","url":"https://m.stock.naver.com/worldstock/stock/AAOI.O"}],
}

p['signals']={
 "asOf":NOW,
 "kr":[kr_hanwha,kr_hynix,kr_hanmi],
 "us":[us_pltr,us_aaoi],
 "newListings":{"kr":[],"us":[]},
 "krForeignFlow":krForeignFlow,
 "weekendNote":"주말(토) 회차예요. 8/7 금 미국·국내 종가를 기준으로 보유 15종목과 시그널을 갱신했어요. 신규 상장주 섹션은 다음 평일 회차에서 보강해요.",
 "dataQualityNote":"시그널 5종목(국내 3·미국 2)은 8/7 금 확정 종가와 네이버 금융 API·검증 매체로 교차확인했어요. 신규 상장주(newListings)는 주말 데이터 한계로 이번 회차에서 비워두고 다음 평일에 채워요.",
}
json.dump(p, open("portfolio.json","w"), ensure_ascii=False, indent=2)
print("signals rebuilt. kr=3 us=2 flow rows=3")
print("hanwha net5:",r_hanwha['netBuy5d'],"hynix net5:",r_hynix['netBuy5d'],"hanmi net5:",r_hanmi['netBuy5d'])
