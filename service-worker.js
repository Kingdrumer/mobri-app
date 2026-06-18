// 포트폴리오 데일리 PWA — Service Worker
// 캐시 전략: 앱 셸은 cache-first, 데이터는 network-first

const CACHE_VERSION = 'pwa-v41';
const APP_SHELL_CACHE = `app-shell-${CACHE_VERSION}`;
const DATA_CACHE = `data-${CACHE_VERSION}`;

const APP_SHELL_FILES = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(APP_SHELL_CACHE).then((cache) => {
      return cache.addAll(APP_SHELL_FILES).catch(() => {
        // 일부 파일이 누락돼도 설치는 진행
      });
    })
  );
  self.skipWaiting();
});

// 메인 페이지에서 보낸 SKIP_WAITING 메시지 → 즉시 활성화
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      // 옛 캐시 전부 삭제 — 현재 버전 캐시 외에 모든 cache 강제 제거
      // (iOS Safari가 옛 캐시 끈질기게 들고 있는 문제 회피)
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((k) => k !== APP_SHELL_CACHE && k !== DATA_CACHE)
          .map((k) => caches.delete(k))
      );
      // 추가: 현재 버전의 DATA_CACHE도 비워서 매번 fresh 데이터 받게
      // (앱 셸은 캐시 유지 — 오프라인 폴백용)
      try {
        await caches.delete(DATA_CACHE);
      } catch (e) { /* ignore */ }
      await self.clients.claim();
      // 모든 클라이언트(폰 PWA)에 새 버전 알림 → 자동 새로고침 트리거
      const clients = await self.clients.matchAll({ type: 'window' });
      clients.forEach((c) => c.postMessage({ type: 'NEW_VERSION', version: CACHE_VERSION }));
    })()
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // GET 요청만 캐시
  if (request.method !== 'GET') return;

  // 데이터 요청 (data/*.json) — network-first
  if (url.pathname.includes('/data/')) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const clone = res.clone();
          caches.open(DATA_CACHE).then((cache) => cache.put(request, clone));
          return res;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // 앱 셸 — stale-while-revalidate (캐시 즉시 반환 + 백그라운드에서 새 버전 갱신)
  // index.html / app.js / styles.css 는 network-first (새로고침 시 즉시 새 버전)
  const path = url.pathname;
  const isCriticalAsset = path === '/' || path.endsWith('/') ||
                          path.endsWith('/index.html') ||
                          path.endsWith('/app.js') || path.endsWith('/styles.css');

  if (isCriticalAsset) {
    // network-first — 네트워크 우선, 실패 시 캐시
    event.respondWith(
      fetch(request)
        .then((res) => {
          const clone = res.clone();
          caches.open(APP_SHELL_CACHE).then((cache) => cache.put(request, clone));
          return res;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  // 그 외 자원 — stale-while-revalidate
  event.respondWith(
    caches.match(request).then((cached) => {
      const fetchPromise = fetch(request).then((res) => {
        const clone = res.clone();
        caches.open(APP_SHELL_CACHE).then((cache) => cache.put(request, clone));
        return res;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
