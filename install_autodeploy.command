#!/bin/bash
# Mobri 자동 배포 — 원클릭 설치기
# 이 파일을 Finder에서 더블클릭하면 macOS가 매일 7:50에 자동 배포하도록 설정됩니다.

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

clear
cat << 'BANNER'
========================================================
  📱 Mobri PWA — 자동 배포 설치기
========================================================
  매일 오전 7:50에 자동으로 PWA를 갱신합니다.
  설치 후엔 신경 안 쓰셔도 돼요.
========================================================

BANNER

PLIST_NAME="com.mobri.daily-deploy.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
PLIST_SRC="$(pwd)/$PLIST_NAME"
PLIST_DST="$LAUNCH_AGENTS/$PLIST_NAME"

# 1. LaunchAgents 폴더 준비
mkdir -p "$LAUNCH_AGENTS"

# 2. plist 복사
cp "$PLIST_SRC" "$PLIST_DST"
echo "✓ 설정 파일 복사: $PLIST_DST"

# 3. 기존 등록 해제 (재설치 대비)
launchctl unload "$PLIST_DST" 2>/dev/null

# 4. 새로 등록
if launchctl load "$PLIST_DST"; then
  echo "✓ macOS에 자동 실행 등록 완료"
else
  echo "❌ 등록 실패 (이미 등록돼 있을 수 있음 — 무시 가능)"
fi

# 5. 시운전 — 즉시 한 번 실행해서 잘 되는지 확인
echo ""
echo "========================================================"
echo "  🧪 설치 확인 — 지금 한 번 실행해 봅니다"
echo "========================================================"
echo ""

bash "$(pwd)/deploy.sh"
DEPLOY_RC=$?

echo ""
echo "========================================================"
if [[ $DEPLOY_RC -eq 0 ]]; then
  cat << 'SUCCESS'
  ✅ 설치 + 시운전 성공!

  앞으로 매일 오전 7:50에 자동으로 폰 PWA가 갱신됩니다.
  사용자가 별도로 할 일 없습니다.

  로그 확인:
    cat /Users/hanseung-o/project/agent/claude/portfolio-pwa/logs/deploy-stdout.log

  자동 배포 중단하고 싶을 때:
    launchctl unload ~/Library/LaunchAgents/com.mobri.daily-deploy.plist
SUCCESS
else
  cat << 'FAILURE'
  ⚠️ 시운전 실패

  설정은 됐지만 첫 배포가 실패했어요. 위쪽 에러 메시지 확인 후
  Cowork 채팅에서 도움 요청하세요.

  로그 확인:
    cat /Users/hanseung-o/project/agent/claude/portfolio-pwa/logs/deploy-stderr.log
FAILURE
fi
echo "========================================================"
echo ""
echo "[Enter 키를 누르면 창이 닫힙니다]"
read -r
