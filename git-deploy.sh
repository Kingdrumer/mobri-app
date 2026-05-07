#!/bin/bash
# Mobri 자동 배포 스크립트 (GitHub 경유)
# 1. PWA 폴더의 변경 사항을 GitHub에 push
# 2. Netlify가 GitHub push 감지 → 자동 빌드·배포
# 3. 폰 PWA가 자동 새로고침

set -e

# 환경변수 자동 로드 (GITHUB_TOKEN, GITHUB_USER, GITHUB_REPO)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "$GITHUB_TOKEN" ]]; then
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

if [[ -z "$GITHUB_TOKEN" || -z "$GITHUB_USER" || -z "$GITHUB_REPO" ]]; then
  echo "❌ GITHUB_TOKEN/USER/REPO 환경변수 미설정"
  echo "  파일 위치: /Users/hanseung-o/project/agent/claude/.config/netlify.env"
  exit 1
fi

# 1. 임시 작업 디렉토리에 fresh clone (안전성 + lock 회피)
WORK_DIR=$(mktemp -d -t mobri-deploy.XXXXXX)
trap "rm -rf $WORK_DIR" EXIT

echo "📥 GitHub repo 클론 중..."
git clone --quiet --depth=1 \
  "https://${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git" \
  "$WORK_DIR" 2>&1 | tail -3

# 2. PWA 폴더의 변경 사항을 작업 디렉토리에 복사
PWA_DIR="$SCRIPT_DIR"
echo "📋 변경 파일 복사 중..."

# 주요 코드/설정 파일
for f in app.js styles.css index.html service-worker.js manifest.json \
         README.md ROADMAP.md netlify.toml SETUP_GUIDE.md .gitignore; do
  if [[ -f "$PWA_DIR/$f" ]]; then
    cp "$PWA_DIR/$f" "$WORK_DIR/$f"
  fi
done

# 데이터 디렉토리 (전체)
if [[ -d "$PWA_DIR/data" ]]; then
  rm -rf "$WORK_DIR/data"
  cp -r "$PWA_DIR/data" "$WORK_DIR/data"
fi

# 아이콘 (거의 안 바뀌지만 안전하게)
if [[ -d "$PWA_DIR/icons" ]]; then
  rm -rf "$WORK_DIR/icons"
  cp -r "$PWA_DIR/icons" "$WORK_DIR/icons"
fi

# .github 폴더 (workflow 등)
if [[ -d "$PWA_DIR/.github" ]]; then
  rm -rf "$WORK_DIR/.github"
  cp -r "$PWA_DIR/.github" "$WORK_DIR/.github"
fi

# 3. git 작성자 (Netlify가 인식하는 noreply 이메일)
cd "$WORK_DIR"
git config user.email "134570529+Kingdrumer@users.noreply.github.com"
git config user.name "Kingdrumer"

# 4. 변경 사항 확인
if [[ -z $(git status -s) ]]; then
  echo "변경사항 없음. 종료."
  exit 0
fi

echo "📝 변경된 파일:"
git status -s | head -10

# 5. commit + push
TODAY=$(date "+%Y-%m-%d %H:%M KST")
git add -A
git commit --quiet -m "Auto update · $TODAY"
git push --quiet origin main

echo ""
echo "✓ GitHub push 완료. Netlify가 1~2분 안에 자동 배포합니다."
echo "  사이트: https://mobri-app.netlify.app"
