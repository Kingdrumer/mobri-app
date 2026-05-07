# 🚀 Mobri 셋업 가이드 — 3분 컷

GitHub 같은 거 필요없어요. Netlify 1개 사이트로 모든 자동화가 끝납니다.

**예상 소요 시간**: 3~5분 (전부 웹 클릭, 명령어 없음)

---

## 1단계: Netlify 가입 + PWA 배포 (2분)

### 1-1. Netlify 가입
https://app.netlify.com/signup — Google 계정으로 가입하면 1초.

### 1-2. PWA 폴더 드래그&드롭으로 배포
1. 로그인 후 https://app.netlify.com/drop 페이지로 이동
2. Finder에서 `portfolio-pwa` 폴더를 통째로 브라우저 창에 **드래그&드롭**
3. 약 20초 후 자동으로 사이트가 만들어지고 URL 발급
4. 상단 **Site overview → Site name → Change site name**으로 원하는 이름 변경
   - 예: `elise-portfolio` → 최종 URL `https://elise-portfolio.netlify.app`

✅ **확인**: 발급된 URL을 PC 브라우저에서 열어 PWA가 정상 동작하는지 확인.

---

## 2단계: Netlify 액세스 토큰 + 사이트 ID 받기 (1분)

이 두 값을 Cowork에 알려주면, 매일 자동 배포가 가능해집니다.

### 2-1. 액세스 토큰 발급
1. Netlify 우측 상단 프로필 → **User settings**
2. 좌측 **OAuth** 또는 **Applications** → **Personal access tokens**
3. **New access token** 클릭
4. Description: `cowork-pwa-deploy`, Expiration: 원하는 기간 (없음 추천)
5. **Generate token** 클릭
6. **이 페이지를 떠나기 전에 토큰을 복사** (다시 못 봄)
   - 형식: `nfp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 2-2. 사이트 ID 확인
1. Netlify 메인 → 만든 사이트 클릭
2. 좌측 메뉴 **Site configuration** → **General**
3. **Site information** 섹션에서 **Site ID** 복사
   - 형식: `12345678-abcd-1234-abcd-123456789012` (UUID)

---

## 3단계: 폰에 PWA 설치 (1분)

### iPhone (Safari)
1. Safari로 발급받은 URL 열기
2. 하단 공유 버튼 (네모 + 위 화살표) 탭
3. **"홈 화면에 추가"** 선택 → **추가**
4. 홈 화면에 앱 아이콘 추가 → 일반 앱처럼 실행

### Android (Chrome)
1. Chrome으로 URL 열기
2. 우측 상단 점 세 개 메뉴 → **"홈 화면에 추가"** 또는 **"앱 설치"**

---

## 4단계: Cowork에 토큰·ID 알려주기

이 메시지를 그대로 Cowork에 보내주세요:

```
Netlify 토큰: nfp_여기에토큰
Netlify 사이트 ID: 여기에사이트ID
```

⚠️ **보안**: 이 토큰은 사이트 배포 권한만 가져요. 그래도 노출되지 않게 주의. 노출되면 위 단계에서 즉시 **Revoke**.

---

## 🎉 끝!

이후로는 매일 오전 7:37에 모든 게 자동:

1. 보고서 작성
2. PWA 데이터 갱신
3. **Netlify에 자동 배포** (약 30초)
4. 폰에서 PWA 새로고침 → 새 내용

**사용자가 일상에서 하는 일**:
- 폰에서 앱 열기
- 종목 추가/삭제 (PWA 안에서)
- 부동산 정보 추가 (PWA 안에서)

---

## 💡 자주 묻는 질문

**Q. 토큰 한 번 노출되면 어떻게 해요?**
Netlify에서 즉시 Revoke 후 새 토큰 발급해 알려주시면 됩니다.

**Q. 폰에서 추가한 종목이 다른 폰에서도 보이나요?**
현재는 폰별 저장(localStorage)이에요. 여러 기기 동기화 원하면 추후 구글 로그인 추가 가능 (지금은 보류).

**Q. 매일 데이터 누적하면 사이트가 무거워지지 않나요?**
365개 보고서 = 약 4MB, 10년치 = 40MB. Netlify 무료 한도(100GB 대역폭/월)의 0.04%. 걱정 무.

**Q. Netlify 비용은요?**
무료. 이 정도 사용량으론 평생 무료 한도 안 넘어요.

---

## 🆘 막힐 때

각 단계 어디서 막히면 화면 캡처 + 단계 번호 알려주세요. 같이 풀게요.
