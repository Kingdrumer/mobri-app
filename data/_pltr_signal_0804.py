# -*- coding: utf-8 -*-
import json
p = json.load(open('portfolio.json'))
sig = p.get('signals',{})
sig['asOf'] = "2026-08-04T06:10:00+09:00"
for u in sig.get('us',[]):
    if u.get('ticker')=='PLTR':
        u['currentPrice'] = 124.96
        u['change1D'] = 1.54
        u['afterHoursPrice'] = 142.01
        u['afterHoursChange1D'] = 13.6
        u['afterHoursNote'] = ("8/3(월) 장 마감 후 발표한 2분기 실적이 시장 예상을 크게 웃돌았어요. 매출 $1.94B(예상 $1.8B), 조정 주당순이익 $0.41(예상 $0.35), "
        "매출이 1년 전보다 +93% 늘었고 미국 민간 매출은 +149% 급증했어요. 올해 매출 전망도 $8.16B로 올려 시간외에서 +약 13.6% 급등($142)했어요.")
json.dump(p, open('portfolio.json','w'), ensure_ascii=False, indent=1)
print("PLTR signal updated")
