# Mobri (모브리)

매일 아침 받는 내 자산 브리핑 — 미국·한국 주식 포트폴리오 일일 보고서 + 부동산 캘린더 PWA.

> Mobri = "Morning Briefing"의 줄임. 매일 아침 7:37, 자동으로 어제 미국 시장 마감 브리핑이 도착합니다.

## 폴더 구조

```
portfolio-pwa/
├── index.html              메인 진입점
├── styles.css              스타일시트
├── app.js                  앱 로직
├── manifest.json           PWA 매니페스트
├── service-worker.js       오프라인 캐시
├── icons/                  앱 아이콘
│   ├── icon-192.png
│   ├── icon-512.png
│   ├── icon-512-maskable.png
│   └── apple-touch-icon.png
├── data/                   데이터 (스케줄 작업이 자동 갱신)
│   ├── portfolio.json      보유 종목
│   ├── calendar-events.json 캘린더 점·일정
│   ├── real-estate.json    부동산 카테고리
│   └── reports/
│       ├── index.json      보고서 인덱스
│       └── YYYY-MM-DD.json 일자별 보고서
└── README.md
```

## 배포 (Netlify Drop — 가장 빠른 방법)

1. https://app.netlify.com/drop 접속
2. `portfolio-pwa` 폴더 전체를 브라우저 창에 드래그&드롭
3. 약 30초 후 HTTPS URL 발급 (예: `https://random-name-123.netlify.app`)
4. 첫 화면에 나오는 `Site overview`에서 사이트 이름을 원하는 것으로 변경 가능 (예: `my-portfolio-daily`)
5. 발급된 URL을 폰 Safari/Chrome으로 접속

## 폰에 앱처럼 설치하기

### iPhone (Safari)
1. Safari로 발급받은 URL 접속
2. 하단 공유 버튼 (네모+화살표) 탭
3. **"홈 화면에 추가"** 선택
4. 이름 확인 후 **"추가"** 탭
5. 홈 화면에 앱 아이콘이 추가됨 → 일반 앱처럼 실행

### Android (Chrome)
1. Chrome으로 URL 접속
2. 우측 상단 점 세 개 메뉴
3. **"홈 화면에 추가"** 또는 **"앱 설치"** 선택
4. 홈 화면에 앱 아이콘 생성

## 데이터 갱신

매일 오전 7:37(KST)에 Cowork 스케줄 작업이 다음 파일들을 자동 갱신합니다.

- `data/portfolio.json` — 종목 가격, 등락률, 신호등
- `data/calendar-events.json` — 그날 발생한 호재/악재/실적/일정
- `data/reports/YYYY-MM-DD.json` — 일자별 풀 보고서
- `data/reports/index.json` — 보고서 목록 갱신

**주의**: PWA는 정적 호스팅이라 데이터 갱신 후 호스팅에 다시 업로드해야 합니다.

### 자동 동기화 옵션

데이터 자동 동기화를 원하시면 다음 중 하나로 업그레이드 가능합니다.

1. **GitHub Pages + GitHub API**: 스케줄 작업이 GitHub repo에 commit → 자동 배포
2. **Netlify CLI**: 스케줄 작업이 `netlify deploy` 실행
3. **Firebase Hosting**: 비슷한 방식

이 부분은 배포 후 별도로 셋업할 수 있습니다.

## 사용자가 직접 변경하는 것

PWA 안에서 사용자가 직접 추가·삭제할 수 있는 항목들 (브라우저 localStorage에 저장):

- 미국·한국 주식 종목 추가/삭제/이동/메모
- 부동산 카테고리별 정보 추가
- 캘린더에 부동산 일정 자동 표시

브라우저 데이터를 지우면 초기 데이터(`data/*.json`)로 복귀합니다.

## 로컬 테스트

```bash
cd portfolio-pwa
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000 접속
```

PWA 설치 가능 여부는 Chrome 개발자도구 → Application 탭 → Manifest에서 확인.
