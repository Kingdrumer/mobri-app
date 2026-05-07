#!/bin/bash
# Mobri 일일 자동 배포 스크립트 — Netlify API 직접 호출
# 환경변수 NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID 자동 로드

set -e

# 스크립트가 위치한 폴더로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 환경변수 자동 로드 (여러 경로 시도)
if [[ -z "$NETLIFY_AUTH_TOKEN" || -z "$NETLIFY_SITE_ID" ]]; then
  for ENV_PATH in \
    "/Users/hanseung-o/project/agent/claude/.config/netlify.env" \
    "$SCRIPT_DIR/../.config/netlify.env" \
    "$HOME/project/agent/claude/.config/netlify.env"
  do
    if [[ -f "$ENV_PATH" ]]; then
      set -a
      source "$ENV_PATH"
      set +a
      echo "✓ 환경변수 로드: $ENV_PATH"
      break
    fi
  done
fi

if [[ -z "$NETLIFY_AUTH_TOKEN" || -z "$NETLIFY_SITE_ID" ]]; then
  echo "❌ NETLIFY_AUTH_TOKEN 또는 NETLIFY_SITE_ID 환경변수가 설정되지 않았습니다"
  echo "  파일 위치: /Users/hanseung-o/project/agent/claude/.config/netlify.env"
  exit 1
fi

# 임시 zip 만들기 (디렉토리에 만든 뒤 zip 생성)
TMP_DIR=$(mktemp -d -t pwa-deploy.XXXXXX)
TMP_ZIP="$TMP_DIR/site.zip"
trap "rm -rf $TMP_DIR" EXIT

zip -r -q "$TMP_ZIP" . \
  -x "*.git*" \
  -x "*.DS_Store" \
  -x "deploy.sh" \
  -x "install_autodeploy.command" \
  -x "*.plist" \
  -x "logs/*" \
  -x "SETUP_GUIDE.md" \
  -x "README.md" \
  -x ".env"

ZIP_SIZE=$(wc -c < "$TMP_ZIP")
echo "📦 업로드 준비: $((ZIP_SIZE / 1024)) KB"

# Netlify Deploy API 호출
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Content-Type: application/zip" \
  -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN" \
  --data-binary "@$TMP_ZIP" \
  "https://api.netlify.com/api/v1/sites/$NETLIFY_SITE_ID/deploys")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "201" ]]; then
  echo "❌ 배포 실패 (HTTP $HTTP_CODE)"
  echo "$BODY" | head -c 500
  exit 1
fi

# 응답에서 deploy URL 추출
DEPLOY_URL=$(echo "$BODY" | grep -o '"deploy_url":"[^"]*"' | cut -d'"' -f4)
SITE_URL=$(echo "$BODY" | grep -o '"ssl_url":"[^"]*"' | cut -d'"' -f4)

echo "✓ Netlify 배포 시작됨"
echo "  사이트: ${SITE_URL:-(URL 파싱 실패)}"
echo "  배포 ID: ${DEPLOY_URL:-(파싱 실패)}"
echo "  → 약 20~40초 후 폰에서 새 데이터 확인 가능"
