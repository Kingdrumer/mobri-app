// 포트폴리오 데일리 PWA — 메인 앱 로직

const STORAGE_KEYS = {
  portfolio: 'pwa.portfolio.v1',
  selectedDate: 'pwa.selectedDate.v1',
  calMode: 'pwa.calMode.v1',
  realEstate: 'pwa.realEstate.v1',
};

// 한국 시간(KST, UTC+9) 기준 YYYY-MM-DD 반환
function getKSTToday() {
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Seoul',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  return formatter.format(new Date()); // "2026-05-07"
}

// KST 기준 오늘 날짜의 1일 Date 객체 (월 표시용)
function getKSTCurrentMonth() {
  const today = getKSTToday(); // "YYYY-MM-DD"
  const [y, m] = today.split('-').map(Number);
  return new Date(y, m - 1, 1);
}

const TODAY_KST = getKSTToday();

const State = {
  tab: 'calendar',
  calMode: 'stock',
  currentMonth: getKSTCurrentMonth(),
  selectedDate: TODAY_KST,
  todayDate: TODAY_KST,
  portfolio: { us: [], kr: [] },
  calendarEvents: { stock: {}, realestate: {} },
  realEstate: null,
  reportsIndex: [],
  reportCache: {},
  charts: {},
};

// ------------- 유틸 -------------
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function fmtDate(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function pct(n) {
  if (n === undefined || n === null) return '—';
  const sign = n > 0 ? '+' : '';
  return `${sign}${n.toFixed(1)}%`;
}

function trendColor(n) {
  if (n > 0) return 'var(--positive)';
  if (n < 0) return 'var(--negative)';
  return 'var(--text-tertiary)';
}

function escapeHtml(str) {
  return String(str || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// ------------- 데이터 로드 -------------
async function loadJSON(path) {
  try {
    const res = await fetch(path + '?v=' + Date.now(), { cache: 'no-cache' });
    if (!res.ok) throw new Error(res.status);
    return await res.json();
  } catch (e) {
    console.warn('Failed to load', path, e);
    return null;
  }
}

// === 자동 새로고침 시스템 ===
let refreshTimer = null;
let lastRefreshAt = 0;
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5분

async function refreshAllData(silent = false) {
  // 너무 잦은 호출 방지 (3초 디바운스)
  if (Date.now() - lastRefreshAt < 3000 && silent) return;
  lastRefreshAt = Date.now();

  try {
    const [portfolio, events, reportsIdx, realEstate] = await Promise.all([
      loadJSON('data/portfolio.json'),
      loadJSON('data/calendar-events.json'),
      loadJSON('data/reports/index.json'),
      loadJSON('data/real-estate.json'),
    ]);

    // localStorage 우선이지만, 데이터 새로고침 시 PWA가 추가/메모한 정보는 보존하면서 가격만 갱신
    if (portfolio) {
      // localStorage에 저장된 사용자 종목 추가 분과 PWA에서 변경한 게 있으면 보존
      const local = localStorage.getItem(STORAGE_KEYS.portfolio);
      if (local) {
        try {
          const localPort = JSON.parse(local);
          // 사용자가 추가한 종목과 메모는 보존, 가격은 새 데이터로 덮어쓰기
          State.portfolio = mergePortfolio(localPort, portfolio);
        } catch (e) {
          State.portfolio = portfolio;
        }
      } else {
        State.portfolio = { us: portfolio.us || [], kr: portfolio.kr || [] };
      }
    }
    if (events) State.calendarEvents = events;
    if (reportsIdx) State.reportsIndex = reportsIdx.reports || [];
    if (realEstate) State.realEstate = realEstate;

    // 보고서 캐시 비우기 (새 데이터 받기 위해)
    State.reportCache = {};

    if (!silent) render();
    updateLastUpdatedDisplay();
  } catch (e) {
    console.warn('Refresh failed:', e);
  }
}

function mergePortfolio(local, fresh) {
  // 미국·한국 모두 ticker 기준 머지
  const merge = (localList, freshList) => {
    const result = [];
    const freshMap = {};
    (freshList || []).forEach((s) => { freshMap[s.ticker] = s; });

    (localList || []).forEach((localItem) => {
      const freshItem = freshMap[localItem.ticker];
      if (freshItem) {
        // fresh 데이터로 덮어쓰되 userMemo 같은 사용자 필드는 보존
        result.push({
          ...freshItem,
          userMemo: localItem.userMemo || freshItem.userMemo || '',
          note: localItem.note !== freshItem.note && localItem._userEdited ? localItem.note : freshItem.note,
        });
        delete freshMap[localItem.ticker];
      } else {
        // 사용자가 추가한 종목 (fresh에 없음) — 그대로 유지
        result.push(localItem);
      }
    });
    // fresh에만 있는 종목 (사용자가 삭제한 게 아니면 추가)
    Object.values(freshMap).forEach((s) => result.push(s));
    return result;
  };

  return {
    us: merge(local.us, fresh.us),
    kr: merge(local.kr, fresh.kr),
  };
}

function updateLastUpdatedDisplay() {
  const el = document.querySelector('.last-updated-text');
  if (!el) return;
  const ts = State.portfolio?.lastUpdated;
  if (!ts) {
    el.textContent = '갱신 중...';
    return;
  }
  el.textContent = `마지막 갱신: ${formatTimeAgo(new Date(ts))}`;
}

function formatTimeAgo(date) {
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  const diffHr = Math.floor(diffMin / 60);
  if (diffMin < 1) return '방금 전';
  if (diffMin < 60) return `${diffMin}분 전`;
  if (diffHr < 24) return `${diffHr}시간 전`;
  const days = Math.floor(diffHr / 24);
  return `${days}일 전`;
}

function startAutoRefresh() {
  // 5분마다 자동 새로고침 (탭 보이는 동안만)
  if (refreshTimer) clearInterval(refreshTimer);
  refreshTimer = setInterval(() => {
    if (!document.hidden) refreshAllData(true);
  }, REFRESH_INTERVAL);
}

// 탭 가시성 변경 시 즉시 새로고침
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    const timeSinceLastRefresh = Date.now() - lastRefreshAt;
    // 1분 이상 지났으면 새로고침
    if (timeSinceLastRefresh > 60000) {
      refreshAllData();
    }
  }
});

async function init() {
  // localStorage에서 사용자 변경사항 우선
  const savedPortfolio = localStorage.getItem(STORAGE_KEYS.portfolio);
  if (savedPortfolio) {
    try { State.portfolio = JSON.parse(savedPortfolio); } catch (e) {}
  } else {
    const portfolio = await loadJSON('data/portfolio.json');
    if (portfolio) {
      State.portfolio = { us: portfolio.us || [], kr: portfolio.kr || [] };
      State.portfolio.lastUpdated = portfolio.lastUpdated;
    }
  }
  // localStorage에 저장한 거여도 새로 가져온 데이터의 lastUpdated는 가져옴
  if (!State.portfolio.lastUpdated) {
    const fresh = await loadJSON('data/portfolio.json');
    if (fresh?.lastUpdated) State.portfolio.lastUpdated = fresh.lastUpdated;
  }

  const savedRealEstate = localStorage.getItem(STORAGE_KEYS.realEstate);
  if (savedRealEstate) {
    try { State.realEstate = JSON.parse(savedRealEstate); } catch (e) {}
  } else {
    State.realEstate = await loadJSON('data/real-estate.json');
  }

  const calEvents = await loadJSON('data/calendar-events.json');
  if (calEvents) State.calendarEvents = calEvents;

  const reportsIdx = await loadJSON('data/reports/index.json');
  if (reportsIdx) State.reportsIndex = reportsIdx.reports || [];

  const savedMode = localStorage.getItem(STORAGE_KEYS.calMode);
  if (savedMode) State.calMode = savedMode;

  const savedDate = localStorage.getItem(STORAGE_KEYS.selectedDate);
  if (savedDate) State.selectedDate = savedDate;

  setupTabs();
  render();
  startAutoRefresh();
}

// ------------- 탭 라우팅 -------------
function setupTabs() {
  $$('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      State.tab = btn.dataset.tab;
      $$('.tab-btn').forEach((b) => b.classList.toggle('active', b === btn));
      render();
      window.scrollTo(0, 0);
    });
  });
}

function render() {
  const app = $('#app');
  if (State.tab === 'calendar') return renderCalendar(app);
  if (State.tab === 'portfolio') return renderPortfolio(app);
  if (State.tab === 'charts') return renderCharts(app);
  if (State.tab === 'realestate') return renderRealEstate(app);
  if (State.tab === 'archive') return renderArchive(app);
}

// ------------- 캘린더 탭 -------------
function renderCalendar(app) {
  const month = State.currentMonth;
  const monthLabel = `${month.getFullYear()}년 ${month.getMonth() + 1}월`;

  app.innerHTML = `
    <header class="app-header">
      <div class="meta">Mobri · 월간 기록</div>
      <h1>${monthLabel}</h1>
    </header>

    <div class="refresh-bar">
      <div class="last-updated">
        <span class="live-dot"></span>
        <span class="last-updated-text">갱신 중...</span>
      </div>
      <button class="refresh-btn" id="refreshBtn">
        <span class="ico">↻</span>
        <span>새로고침</span>
      </button>
    </div>

    <div class="toggle-group">
      <div class="toggle-option ${State.calMode === 'stock' ? 'active' : ''}" data-mode="stock">주식</div>
      <div class="toggle-option ${State.calMode === 'realestate' ? 'active' : ''}" data-mode="realestate">부동산</div>
    </div>

    <div class="calendar-nav">
      <div class="month-info">
        <div class="label">선택된 날짜</div>
        <div class="month">${formatKoreanDate(State.selectedDate)}</div>
      </div>
      <div class="row" style="gap:6px;">
        <button class="cal-nav-btn" id="prevMonth">‹</button>
        <button class="cal-nav-btn" id="nextMonth">›</button>
      </div>
    </div>

    <div class="calendar-grid">
      <div class="cal-weekday-row">
        <div class="cal-weekday sun">일</div>
        <div class="cal-weekday">월</div>
        <div class="cal-weekday">화</div>
        <div class="cal-weekday">수</div>
        <div class="cal-weekday">목</div>
        <div class="cal-weekday">금</div>
        <div class="cal-weekday sat">토</div>
      </div>
      <div class="cal-days" id="calDays"></div>
    </div>

    <div class="cal-legend">
      <div><span class="dot green"></span>호재</div>
      <div><span class="dot amber"></span>주요일정</div>
      <div><span class="dot red"></span>악재</div>
      <div><span class="dot indigo"></span>실적·보고서</div>
      <div><span class="dot blue"></span>부동산 일정</div>
    </div>

    <div id="selectedDayPanel"></div>
  `;

  $$('.toggle-option').forEach((el) => {
    el.addEventListener('click', () => {
      State.calMode = el.dataset.mode;
      localStorage.setItem(STORAGE_KEYS.calMode, State.calMode);
      render();
    });
  });

  $('#refreshBtn')?.addEventListener('click', async () => {
    const btn = $('#refreshBtn');
    btn.classList.add('refreshing');
    await refreshAllData();
    btn.classList.remove('refreshing');
  });

  // 마지막 갱신 시간 즉시 표시
  updateLastUpdatedDisplay();
  // 1분마다 "마지막 갱신: X분 전" 텍스트만 갱신
  if (window._timeAgoTimer) clearInterval(window._timeAgoTimer);
  window._timeAgoTimer = setInterval(updateLastUpdatedDisplay, 60000);

  $('#prevMonth').addEventListener('click', () => {
    State.currentMonth = new Date(month.getFullYear(), month.getMonth() - 1, 1);
    render();
  });
  $('#nextMonth').addEventListener('click', () => {
    State.currentMonth = new Date(month.getFullYear(), month.getMonth() + 1, 1);
    render();
  });

  renderCalendarGrid();
  renderSelectedDayPanel();
}

function renderCalendarGrid() {
  const grid = $('#calDays');
  if (!grid) return;
  const month = State.currentMonth;
  const firstDay = new Date(month.getFullYear(), month.getMonth(), 1);
  const lastDay = new Date(month.getFullYear(), month.getMonth() + 1, 0);
  const startWeekday = firstDay.getDay();
  const daysInMonth = lastDay.getDate();
  const prevLastDay = new Date(month.getFullYear(), month.getMonth(), 0).getDate();

  const events = State.calendarEvents[State.calMode] || {};

  let html = '';

  // 이전 달 일자 (회색)
  for (let i = startWeekday - 1; i >= 0; i--) {
    const day = prevLastDay - i;
    const d = new Date(month.getFullYear(), month.getMonth() - 1, day);
    html += renderDay(d, true, events);
  }

  // 이번 달 일자
  for (let day = 1; day <= daysInMonth; day++) {
    const d = new Date(month.getFullYear(), month.getMonth(), day);
    html += renderDay(d, false, events);
  }

  // 다음 달 일자 (회색)
  const totalCells = startWeekday + daysInMonth;
  const nextDays = (7 - (totalCells % 7)) % 7;
  for (let day = 1; day <= nextDays; day++) {
    const d = new Date(month.getFullYear(), month.getMonth() + 1, day);
    html += renderDay(d, true, events);
  }

  grid.innerHTML = html;

  $$('.cal-day', grid).forEach((el) => {
    el.addEventListener('click', () => {
      const date = el.dataset.date;
      if (!date) return;
      State.selectedDate = date;
      localStorage.setItem(STORAGE_KEYS.selectedDate, date);
      // 다른 달이면 그 달로 이동
      const d = new Date(date);
      if (d.getMonth() !== State.currentMonth.getMonth() || d.getFullYear() !== State.currentMonth.getFullYear()) {
        State.currentMonth = new Date(d.getFullYear(), d.getMonth(), 1);
      }
      render();
    });
  });
}

function renderDay(d, muted, events) {
  const dateStr = fmtDate(d);
  const weekday = d.getDay();
  const isToday = dateStr === State.todayDate;
  const isSelected = dateStr === State.selectedDate;
  const dayEvents = events[dateStr] || [];

  const classes = ['cal-day'];
  if (muted) classes.push('muted');
  if (weekday === 0) classes.push('sun');
  if (weekday === 6) classes.push('sat');
  if (isToday) classes.push('today');
  if (isSelected && !isToday) classes.push('selected');

  const dotsHtml = dayEvents.slice(0, 3).map((e) => {
    const c = isToday ? 'background:white;' : '';
    return `<span class="dot ${e.color}" style="${c}"></span>`;
  }).join('');

  return `
    <div class="${classes.join(' ')}" data-date="${dateStr}">
      ${d.getDate()}
      <div class="cal-dots">${dotsHtml}</div>
    </div>
  `;
}

function formatKoreanDate(dateStr) {
  const d = new Date(dateStr);
  const days = ['일', '월', '화', '수', '목', '금', '토'];
  return `${d.getMonth() + 1}월 ${d.getDate()}일 (${days[d.getDay()]})`;
}

// 이벤트 type → 이모지·친근한 라벨 매핑
function eventTypeMeta(type) {
  const map = {
    positive:   { icon: '🟢', kind: '호재' },
    negative:   { icon: '🔴', kind: '악재' },
    earnings:   { icon: '⭐', kind: '실적 발표' },
    report:     { icon: '📊', kind: '주간 보고서' },
    indicator:  { icon: '📈', kind: '경제 지표' },
    schedule:   { icon: '📅', kind: '주요 일정' },
    asia:       { icon: '🌏', kind: '아시아장 마감' },
    'us-open':  { icon: '🇺🇸', kind: '미국장 개장' },
    subscription: { icon: '🏠', kind: '청약' },
    rate:       { icon: '💰', kind: '금리' },
    policy:     { icon: '📜', kind: '정책' },
  };
  return map[type] || { icon: '•', kind: '일정' };
}

// 이벤트 카테고리 분류
function classifyEvent(ev) {
  if (ev.color === 'green' || ev.type === 'positive') return 'positive';
  if (ev.color === 'red' || ev.type === 'negative') return 'negative';
  if (ev.type === 'earnings') return 'earnings';
  return 'schedule';
}

function groupEvents(events) {
  return events.reduce((g, e) => {
    const k = classifyEvent(e);
    g[k] = g[k] || [];
    g[k].push(e);
    return g;
  }, {});
}

// 뉴스 → 한국/미국 분류
function newsCountry(news) {
  if (news.country) return news.country;
  const text = (news.sources || []).map((s) => s.name || '').join(' ');
  const krKeywords = ['한국경제', '한경', '매일경제', '매경', '조선', '머니투데이',
    '이데일리', '네이버', '다음', '서울경제', '뉴시스', '연합', '뉴스1',
    '아시아경제', '아주경제', '인포스탁', '파이낸셜', '데일리안', '머니S'];
  return krKeywords.some((k) => text.includes(k)) ? 'kr' : 'us';
}

// 이벤트의 종목별 영향 리스트 렌더 (stockImpacts 배열)
function renderStockImpacts(impacts) {
  if (!impacts || !impacts.length) return '';

  // 보유 종목인지 확인 (US/KR 모두 검색)
  const isHeld = (ticker) => {
    const all = [...(State.portfolio.us || []), ...(State.portfolio.kr || [])];
    return all.some((s) => s.ticker === ticker);
  };

  const toneIcon = { positive: '🟢', negative: '🔴', neutral: '⚪' };

  const rows = impacts.map((it) => {
    const tone = it.tone || 'neutral';
    const market = (State.portfolio.us || []).some((s) => s.ticker === it.ticker) ? 'us'
                : (State.portfolio.kr || []).some((s) => s.ticker === it.ticker) ? 'kr'
                : null;
    const heldCls = market ? '' : 'not-held';
    return `
      <button class="si-row ${tone} ${heldCls}" type="button" data-ticker="${escapeHtml(it.ticker)}" ${market ? `data-market="${market}"` : ''}>
        <span class="si-tone">${toneIcon[tone]}</span>
        <div class="si-body">
          <div class="si-head">
            <span class="si-ticker">${escapeHtml(it.ticker)}</span>
            ${it.magnitude ? `<span class="si-magnitude">${escapeHtml(it.magnitude)}</span>` : ''}
          </div>
          ${it.text ? `<div class="si-text">${escapeHtml(it.text)}</div>` : ''}
        </div>
      </button>
    `;
  }).join('');

  return `
    <div class="stock-impacts">
      <div class="si-label">종목별 영향</div>
      ${rows}
    </div>
  `;
}

function renderEventTile(ev, idx) {
  const meta = eventTypeMeta(ev.type);
  const colorClass = ev.color || 'gray';
  const hasMore = !!(ev.impact || ev.ourImpact || (ev.stockImpacts && ev.stockImpacts.length));
  const desc = ev.description || (ev.title && ev.title !== ev.label ? ev.title : '');
  const stockImpactsHtml = renderStockImpacts(ev.stockImpacts);

  return `
    <div class="etile color-${colorClass} ${hasMore ? 'has-more' : ''}" data-idx="${idx}">
      <div class="etile-icon">${meta.icon}</div>
      <div class="etile-body">
        <div class="etile-meta">
          <span class="etile-badge">${escapeHtml(meta.kind)}</span>
          ${ev.time ? `<span class="etile-time">${escapeHtml(ev.time)}</span>` : ''}
        </div>
        <div class="etile-title">${escapeHtml(ev.label || ev.title || '')}</div>
        ${desc ? `<div class="etile-desc">${escapeHtml(desc)}</div>` : ''}

        ${hasMore ? `
          <div class="etile-more">
            ${ev.impact ? `
              <div class="erow">
                <div class="erow-label">💡 자세히</div>
                <div class="erow-text">${escapeHtml(ev.impact)}</div>
              </div>
            ` : ''}
            ${(ev.ourImpact || stockImpactsHtml) ? `
              <div class="erow">
                <div class="erow-label">📌 내 종목엔</div>
                ${ev.ourImpact ? `<div class="erow-text">${escapeHtml(ev.ourImpact)}</div>` : ''}
                ${stockImpactsHtml}
              </div>
            ` : ''}
          </div>
          <div class="etile-toggle">
            <span class="t-c">자세히 보기</span>
            <span class="t-o">접기</span>
          </div>
        ` : ''}
      </div>
    </div>
  `;
}

// 이벤트 우선순위 (가장 주목할 헤드라인 1개 결정)
function eventPriority(e) {
  let p = 0;
  if ((e.label || '').includes('★')) p += 100;
  if (e.type === 'earnings') p += 50;
  if (e.color === 'red')     p += 45;
  if (e.color === 'green')   p += 30;
  if (e.color === 'amber')   p += 20;
  if (e.color === 'indigo')  p += 25;
  if (e.impact)              p += 15;
  if (e.ourImpact)           p += 10;
  return p;
}

// 박스 헤더 버튼 (제목 + 통계 + 셰브론) — 클릭하면 펼침/접힘
function dbHead(title, stat, hasMore) {
  return `
    <button class="db-head-btn" type="button">
      <div class="db-title">${title}</div>
      <div class="db-meta">
        ${stat ? `<span class="db-stat">${stat}</span>` : ''}
        ${hasMore ? `<span class="db-chevron">▼</span>` : ''}
      </div>
    </button>
  `;
}

function moreHint(text) {
  return `<button class="db-more-hint" type="button">${escapeHtml(text)} <span class="mh-arrow">▼</span></button>`;
}

// ── Box 1: 오늘의 일정 (헤드라인 1개 + 나머지 펼치기) ──
function renderEventsBox(dayEvents) {
  if (!dayEvents.length) {
    return `
      <section class="day-box">
        ${dbHead('📅 오늘의 일정', '', false)}
        <div class="db-empty">큰 이벤트 없는 평범한 날이에요</div>
      </section>
    `;
  }

  const sorted = dayEvents.slice().sort((a, b) => eventPriority(b) - eventPriority(a));
  const top = sorted[0];
  const rest = sorted.slice(1);

  const counts = { positive: 0, negative: 0, earnings: 0, schedule: 0 };
  dayEvents.forEach((e) => {
    counts[classifyEvent(e)]++;
  });
  const statParts = [];
  if (counts.positive) statParts.push(`호재 ${counts.positive}`);
  if (counts.negative) statParts.push(`악재 ${counts.negative}`);
  if (counts.earnings) statParts.push(`실적 ${counts.earnings}`);
  if (counts.schedule) statParts.push(`일정 ${counts.schedule}`);
  const stat = statParts.join(' · ');

  const groups = groupEvents(rest);
  const order = [
    { key: 'positive', label: '🟢 호재' },
    { key: 'negative', label: '🔴 악재' },
    { key: 'earnings', label: '⭐ 실적' },
    { key: 'schedule', label: '📅 일정' },
  ].filter((g) => groups[g.key]?.length);

  const hasMore = rest.length > 0;

  return `
    <section class="day-box ${hasMore ? 'collapsible' : ''}" data-box="events">
      ${dbHead('📅 오늘의 일정', stat, hasMore)}
      <div class="db-headline">
        <div class="db-headline-label">⭐ 가장 주목할 이벤트</div>
        ${renderEventTile(top, 0)}
        ${hasMore ? moreHint(`외 ${rest.length}건 더보기`) : ''}
      </div>
      ${hasMore ? `
        <div class="db-content">
          ${order.map((g) => `
            <div class="db-group">
              <div class="dbg-label">
                <span>${g.label}</span>
                <span class="dbg-count">${groups[g.key].length}</span>
              </div>
              <div class="event-tiles">
                ${groups[g.key].map(renderEventTile).join('')}
              </div>
            </div>
          `).join('')}
        </div>
      ` : ''}
    </section>
  `;
}

// ── Box 2: 오늘의 핵심 뉴스 (헤드라인 1개 + 한국/미국 탭) ──
function renderNewsBox(report) {
  if (!report?.news?.length) return '';

  const news = report.news;
  const top = news[0];
  const rest = news.slice(1);
  const us = rest.filter((n) => newsCountry(n) === 'us');
  const kr = rest.filter((n) => newsCountry(n) === 'kr');

  const item = (n) => `
    <div class="news-item ${n.impact || 'neutral'}">
      <div class="ni-bar"></div>
      <div class="ni-body">
        <div class="ni-headline">${escapeHtml(n.headline)}</div>
        ${n.summary ? `<div class="ni-summary">${escapeHtml(n.summary)}</div>` : ''}
        ${(n.sources && n.sources.length) ? `
          <div class="ni-sources">${n.sources.map((s) => escapeHtml(s.name || '')).filter(Boolean).join(' · ')}</div>
        ` : ''}
      </div>
    </div>
  `;

  const hasMore = rest.length > 0;
  const defaultTab = us.length >= kr.length ? 'us' : 'kr';

  return `
    <section class="day-box ${hasMore ? 'collapsible' : ''}" data-box="news">
      ${dbHead('📰 오늘의 핵심 뉴스', `${news.length}건`, hasMore)}
      <div class="db-headline">
        <div class="db-headline-label">📌 톱 헤드라인</div>
        ${item(top)}
        ${hasMore ? moreHint(`외 ${rest.length}건 더보기`) : ''}
      </div>
      ${hasMore ? `
        <div class="db-content">
          <div class="news-tabs">
            <button class="ntab ${defaultTab === 'us' ? 'active' : ''}" data-tab="us">🇺🇸 미국 ${us.length}</button>
            <button class="ntab ${defaultTab === 'kr' ? 'active' : ''}" data-tab="kr">🇰🇷 한국 ${kr.length}</button>
          </div>
          <div class="news-list ${defaultTab === 'us' ? '' : 'hidden'}" data-tab-content="us">
            ${us.length ? us.map(item).join('') : '<div class="db-empty">미국 뉴스 없음</div>'}
          </div>
          <div class="news-list ${defaultTab === 'kr' ? '' : 'hidden'}" data-tab-content="kr">
            ${kr.length ? kr.map(item).join('') : '<div class="db-empty">한국 뉴스 없음</div>'}
          </div>
        </div>
      ` : ''}
    </section>
  `;
}

// ── Box 3: 내 포트폴리오 (위험 종목 헤드라인 + 전체 펼치기) ──
function renderPortfolioBox() {
  const us = State.portfolio.us || [];
  const kr = State.portfolio.kr || [];
  const all = [
    ...us.map((s) => ({ ...s, _market: 'us' })),
    ...kr.map((s) => ({ ...s, _market: 'kr' })),
  ];

  if (!all.length) {
    return `
      <section class="day-box">
        ${dbHead('📊 내 포트폴리오', '', false)}
        <div class="db-empty">아직 등록된 종목이 없어요</div>
      </section>
    `;
  }

  // 위험도 분류
  const isRisky = (s) => s.signal === 'red' || (s.change1D ?? 0) <= -5;
  const isCaution = (s) => !isRisky(s) && (s.signal === 'yellow' || (s.change1D ?? 0) <= -3);

  const risky = all.filter(isRisky);
  const caution = all.filter(isCaution);

  const renderRow = (s, market) => {
    const change = s.change1D ?? s.change1W ?? 0;
    const color = change > 0 ? 'var(--positive)' : change < 0 ? 'var(--negative)' : 'var(--text-tertiary)';
    return `
      <div class="port-row" data-ticker="${escapeHtml(s.ticker)}" data-market="${market}">
        <span class="dot ${s.signal || 'gray'}"></span>
        <div class="pr-info">
          <div class="pr-ticker">${escapeHtml(s.ticker)}</div>
          <div class="pr-name">${escapeHtml(s.name || '')}</div>
        </div>
        <div class="pr-right">
          <div class="pr-price">${market === 'us' ? '$' : '₩'}${s.price ? s.price.toLocaleString() : '—'}</div>
          <div class="pr-change" style="color: ${color}">${pct(change)}</div>
        </div>
      </div>
    `;
  };

  // 헤드라인: 위험 → 주의 → 모두 안전
  let headlineHtml;
  if (risky.length) {
    headlineHtml = `
      <div class="db-headline risky">
        <div class="db-headline-label red">🔴 위험 — 점검 필요 ${risky.length}개</div>
        <div class="port-rows">${risky.map((s) => renderRow(s, s._market)).join('')}</div>
        ${moreHint(`나머지 ${all.length - risky.length}개 종목 보기`)}
      </div>
    `;
  } else if (caution.length) {
    headlineHtml = `
      <div class="db-headline caution">
        <div class="db-headline-label amber">🟡 주의 — 모니터링 필요 ${caution.length}개</div>
        <div class="port-rows">${caution.map((s) => renderRow(s, s._market)).join('')}</div>
        ${moreHint(`나머지 ${all.length - caution.length}개 종목 보기`)}
      </div>
    `;
  } else {
    headlineHtml = `
      <div class="db-headline safe">
        <div class="db-headline-label green">✅ 오늘 모두 안전</div>
        <div class="safe-banner">위험 신호 없음 · 전체 ${all.length}개 종목 정상</div>
        ${moreHint(`전체 ${all.length}개 종목 보기`)}
      </div>
    `;
  }

  const groupBySector = (list) => {
    const out = {};
    list.forEach((s) => {
      const sec = s.sector || '기타';
      out[sec] = out[sec] || [];
      out[sec].push(s);
    });
    return out;
  };

  const renderMarketBlock = (list, market, flag, label) => {
    if (!list.length) {
      return `
        <div class="port-block">
          <div class="pb-flag"><span>${flag} ${label}</span><span class="pb-count">0</span></div>
          <div class="db-empty">등록된 종목이 없어요</div>
        </div>
      `;
    }
    const bySector = groupBySector(list);
    const sectorKeys = Object.keys(bySector);
    return `
      <div class="port-block">
        <div class="pb-flag"><span>${flag} ${label}</span><span class="pb-count">${list.length}</span></div>
        ${sectorKeys.map((sec) => `
          <div class="port-sector">
            <div class="ps-label">
              <span>${escapeHtml(sec)}</span>
              <span class="ps-count">${bySector[sec].length}</span>
            </div>
            <div class="port-rows">
              ${bySector[sec].map((s) => renderRow(s, market)).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  };

  return `
    <section class="day-box collapsible" data-box="portfolio">
      ${dbHead('📊 내 포트폴리오', `미국 ${us.length} · 한국 ${kr.length}`, true)}
      ${headlineHtml}
      <div class="db-content">
        ${renderMarketBlock(us, 'us', '🇺🇸', '미국 주식')}
        ${renderMarketBlock(kr, 'kr', '🇰🇷', '한국 주식')}
      </div>
    </section>
  `;
}

// ── Box 4: 오늘의 학습 (용어 1개 헤드라인 + 나머지 펼치기) ──
function renderTermsBox(report) {
  if (!report?.terms?.length && !report?.tip) return '';

  const terms = report.terms || [];
  const top = terms[0];
  const rest = terms.slice(1);
  const hasMore = rest.length > 0 || !!report.tip;

  const renderTerm = (t) => `
    <div class="term-card-v2">
      <div class="tc-term">${escapeHtml(t.term)}</div>
      <div class="tc-def">${escapeHtml(t.definition || '')}</div>
      ${t.example ? `<div class="tc-ex">${escapeHtml(t.example)}</div>` : ''}
    </div>
  `;

  const stat = terms.length ? `${terms.length}개 용어` : '';

  return `
    <section class="day-box ${hasMore ? 'collapsible' : ''}" data-box="terms">
      ${dbHead('📚 오늘의 학습', stat, hasMore)}
      ${top ? `
        <div class="db-headline">
          <div class="db-headline-label">📖 오늘의 핵심 용어</div>
          ${renderTerm(top)}
          ${hasMore ? moreHint(`나머지 ${rest.length}개 용어${report.tip ? ' + 팁' : ''} 보기`) : ''}
        </div>
      ` : ''}
      ${hasMore ? `
        <div class="db-content">
          ${rest.length ? `
            <div class="terms-list">
              ${rest.map(renderTerm).join('')}
            </div>
          ` : ''}
          ${report.tip ? `<div class="tip-box-v2">💡 ${escapeHtml(report.tip)}</div>` : ''}
        </div>
      ` : ''}
    </section>
  `;
}

async function renderSelectedDayPanel() {
  const panel = $('#selectedDayPanel');
  if (!panel) return;

  const dayEvents = (State.calendarEvents[State.calMode] || {})[State.selectedDate] || [];

  // ── 부동산 모드 ──
  if (State.calMode === 'realestate') {
    panel.innerHTML = `
      <div class="day-panel">
        ${renderEventsBox(dayEvents)}
      </div>
    `;
    attachEventTileHandlers();
    return;
  }

  // ── 주식 모드: 4박스 ──
  const report = await loadReport(State.selectedDate);

  panel.innerHTML = `
    <div class="day-panel">
      ${renderEventsBox(dayEvents)}
      ${renderNewsBox(report)}
      ${renderPortfolioBox()}
      ${renderTermsBox(report)}
    </div>
  `;

  attachBoxCollapseHandlers();
  attachEventTileHandlers();
  attachNewsTabHandlers();
  attachPortfolioRowHandlers();
}

// 박스 헤더 / "더보기" 힌트 클릭 → 펼침/접힘 토글
function attachBoxCollapseHandlers() {
  $$('.day-box.collapsible').forEach((box) => {
    const toggle = (e) => {
      e?.stopPropagation();
      box.classList.toggle('expanded');
    };
    const head = $('.db-head-btn', box);
    if (head) head.addEventListener('click', toggle);
    $$('.db-more-hint', box).forEach((h) => h.addEventListener('click', toggle));
  });
}

function attachEventTileHandlers() {
  $$('.etile.has-more').forEach((tile) => {
    tile.addEventListener('click', () => tile.classList.toggle('expanded'));
  });
  // 종목별 영향 행 클릭 → 종목 상세 (이벤트 펼침은 막음)
  $$('.si-row').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const ticker = btn.dataset.ticker;
      const market = btn.dataset.market;
      if (ticker && market) openStockDetail(ticker, market);
    });
  });
}

function attachNewsTabHandlers() {
  $$('.day-box').forEach((box) => {
    const tabs = $$('.ntab', box);
    if (!tabs.length) return;
    const lists = $$('[data-tab-content]', box);
    tabs.forEach((btn) => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        tabs.forEach((b) => b.classList.toggle('active', b === btn));
        lists.forEach((l) => l.classList.toggle('hidden', l.dataset.tabContent !== tab));
      });
    });
  });
}

function attachPortfolioRowHandlers() {
  $$('.port-row').forEach((row) => {
    row.addEventListener('click', () => {
      openStockDetail(row.dataset.ticker, row.dataset.market);
    });
  });
}

async function loadReport(dateStr) {
  if (State.reportCache[dateStr]) return State.reportCache[dateStr];
  const r = await loadJSON(`data/reports/${dateStr}.json`);
  if (r) State.reportCache[dateStr] = r;
  return r;
}

// ------------- 보고서 모달 (전체 보기) -------------
async function openReportModal(dateStr) {
  const report = await loadReport(dateStr);
  if (!report) return;

  const html = `
    <div class="report-detail">
      <div class="meta-row">${formatKoreanDate(dateStr)} · ${report.session ? report.session + '회차' : ''}</div>
      <h2>${escapeHtml(report.title)}</h2>

      ${report.terms?.length ? `
        <h3>📚 오늘의 학습</h3>
        ${report.terms.map((t) => `
          <div class="term-card">
            <div class="term">${escapeHtml(t.term)}</div>
            <div class="def">${escapeHtml(t.definition)}</div>
            <div class="ex">${escapeHtml(t.example)}</div>
          </div>
        `).join('')}
        ${report.tip ? `<div class="tip-box">💡 ${escapeHtml(report.tip)}</div>` : ''}
      ` : ''}

      ${report.marketSummary?.length ? `
        <h3>📊 시장 한눈에</h3>
        <table class="market-summary-table">
          ${report.marketSummary.map((m) => `
            <tr>
              <td>${escapeHtml(m.label)}</td>
              <td class="value">${escapeHtml(m.value)}</td>
              <td class="change" style="color: ${m.trend === 'up' ? 'var(--positive)' : m.trend === 'down' ? 'var(--negative)' : 'var(--text-tertiary)'}">${escapeHtml(m.change)}</td>
            </tr>
          `).join('')}
        </table>
      ` : ''}

      ${report.news?.length ? `
        <h3>📰 오늘의 핵심 뉴스</h3>
        ${report.news.map((n) => `
          <div class="news-detail ${n.impact || 'neutral'}">
            <div class="h">${escapeHtml(n.headline)}</div>
            <div class="s">${escapeHtml(n.summary || '')}</div>
            <div class="e">${escapeHtml(n.explain || '')}</div>
            <div class="sources">
              ${(n.sources || []).map((s) => `<a href="${escapeHtml(s.url)}" target="_blank" rel="noopener">· ${escapeHtml(s.name)}</a>`).join('')}
            </div>
          </div>
        `).join('')}
      ` : ''}

      ${report.upcoming?.length ? `
        <h3>🎯 다가오는 일정</h3>
        <div class="upcoming-list">
          ${report.upcoming.map((u) => `
            <div class="item">
              <span class="date">${escapeHtml(u.date.slice(5))}</span>
              <span class="label">${escapeHtml(u.label)}</span>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <div style="height: 20px;"></div>
      <button class="btn" onclick="closeModal()">닫기</button>
    </div>
  `;

  showModal(html);
}

function showModal(html) {
  $('#modalContent').innerHTML = html;
  $('#modalOverlay').classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  $('#modalOverlay').classList.remove('show');
  document.body.style.overflow = '';
}

$('#modalOverlay').addEventListener('click', (e) => {
  if (e.target === $('#modalOverlay')) closeModal();
});

window.closeModal = closeModal;

// ------------- 포트폴리오 탭 -------------
function renderPortfolio(app) {
  app.innerHTML = `
    <header class="app-header">
      <div class="meta">내 보유 종목</div>
      <h1>포트폴리오</h1>
    </header>

    <div class="portfolio-section">
      <h2>
        <span>🇺🇸 미국 주식 <span class="count">${State.portfolio.us.length}</span></span>
        <button class="add-btn" id="addUsStock">+ 추가</button>
      </h2>
      <div id="usList">${renderHoldings(State.portfolio.us, 'us')}</div>
    </div>

    <div class="portfolio-section">
      <h2>
        <span>🇰🇷 한국 주식 <span class="count">${State.portfolio.kr.length}</span></span>
        <button class="add-btn" id="addKrStock">+ 추가</button>
      </h2>
      <div id="krList">${
        State.portfolio.kr.length
          ? renderHoldings(State.portfolio.kr, 'kr')
          : `<div class="empty-state">아직 등록된 종목이 없어요.<br/>+ 추가 버튼으로 종목을 등록하세요</div>`
      }</div>
    </div>
  `;

  $('#addUsStock').addEventListener('click', () => openAddStockModal('us'));
  $('#addKrStock').addEventListener('click', () => openAddStockModal('kr'));

  $$('.holding-menu-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const ticker = btn.dataset.ticker;
      const market = btn.dataset.market;
      openHoldingActions(ticker, market);
    });
  });

  // 종목 카드 클릭 시 상세 보기
  $$('.holding-item[data-action="open-detail"]').forEach((el) => {
    el.addEventListener('click', () => {
      const ticker = el.dataset.ticker;
      const market = el.dataset.market;
      openStockDetail(ticker, market);
    });
  });
}

function renderHoldings(items, market) {
  if (!items.length) {
    return `<div class="empty-state">아직 등록된 종목이 없어요.<br/>+ 추가 버튼으로 종목을 등록하세요</div>`;
  }
  return items.map((it) => {
    const change = it.change1W ?? 0;
    const changeColor = change > 0 ? 'var(--positive)' : change < 0 ? 'var(--negative)' : 'var(--text-tertiary)';
    return `
      <div class="holding-item" data-ticker="${escapeHtml(it.ticker)}" data-market="${market}" data-action="open-detail">
        <div class="left">
          <span class="dot ${it.signal || 'gray'}"></span>
          <div class="info">
            <div class="ticker">${escapeHtml(it.ticker)}</div>
            <div class="name">${escapeHtml(it.name || '')}${it.note ? ' · ' + escapeHtml(it.note) : ''}</div>
          </div>
        </div>
        <div class="right">
          <div class="price">${market === 'us' ? '$' : '₩'}${it.price ? it.price.toLocaleString() : '—'}</div>
          <div class="change" style="color: ${changeColor}">${pct(change)} 1주</div>
        </div>
        <button class="holding-menu-btn" data-ticker="${escapeHtml(it.ticker)}" data-market="${market}">⋯</button>
      </div>
    `;
  }).join('');
}

// ------------- 종목 상세 모달 -------------
function findHolding(ticker, market) {
  const list = State.portfolio[market] || [];
  return list.find((it) => it.ticker === ticker);
}

function openStockDetail(ticker, market) {
  const it = findHolding(ticker, market);
  if (!it) return;

  const change1D = it.change1D ?? 0;
  const change1W = it.change1W ?? 0;
  const change1M = it.change1M ?? 0;
  const changeYTD = it.changeYTD ?? 0;

  const trendColorOf = (v) => v > 0 ? 'var(--positive)' : v < 0 ? 'var(--negative)' : 'var(--text-tertiary)';
  const symbol = market === 'us' ? '$' : '₩';
  const price = it.price ? it.price.toLocaleString() : '—';

  const html = `
    <div class="stock-detail">
      <div class="stock-head">
        <div class="row-between">
          <div>
            <div class="t-ticker">${escapeHtml(it.ticker)} <span class="dot ${it.signal || 'gray'}" style="display:inline-block; vertical-align:middle; margin-left:4px;"></span></div>
            <div class="t-name">${escapeHtml(it.name || '')} · ${escapeHtml(it.sector || '')}</div>
          </div>
          <div class="t-price-block">
            <div class="t-price">${symbol}${price}</div>
            <div class="t-1d" style="color: ${trendColorOf(change1D)}">${pct(change1D)} 오늘</div>
          </div>
        </div>

        <div class="period-grid">
          <div class="period-cell">
            <div class="l">1주</div>
            <div class="v" style="color: ${trendColorOf(change1W)}">${pct(change1W)}</div>
          </div>
          <div class="period-cell">
            <div class="l">1개월</div>
            <div class="v" style="color: ${trendColorOf(change1M)}">${pct(change1M)}</div>
          </div>
          <div class="period-cell">
            <div class="l">YTD</div>
            <div class="v" style="color: ${trendColorOf(changeYTD)}">${pct(changeYTD)}</div>
          </div>
          <div class="period-cell">
            <div class="l">베타</div>
            <div class="v">${(it.beta ?? 1).toFixed(2)}</div>
          </div>
        </div>

        <div style="margin-top: 10px;">
          <canvas id="stockDetailChart" style="width: 100%; height: 100px;" role="img" aria-label="${escapeHtml(it.ticker)} 1개월 차트"></canvas>
        </div>
      </div>

      ${it.simpleExplain ? `
        <div class="simple-explain">
          <span class="label">💡 한 줄로 말하면</span>
          ${escapeHtml(it.simpleExplain)}
        </div>
      ` : ''}

      ${it.todayWhy ? `
        <div class="sd-card">
          <div class="sd-card-title">📊 오늘 왜 움직였나?</div>
          <div class="why-box" style="border:none; background: transparent; padding: 0;">${escapeHtml(it.todayWhy)}</div>
        </div>
      ` : ''}

      ${it.outlook ? `
        <div class="sd-card">
          <div class="sd-card-title">🎯 전문가 분석</div>
          <div class="consensus-box">
            <div class="left-block">
              <span class="label">컨센서스</span>
              <span class="rating-pill rating-${(it.outlook.rating || 'hold').toLowerCase().split(' ')[0]}">${escapeHtml(it.outlook.rating || '—')}</span>
            </div>
            <div class="left-block" style="text-align: right; align-items: flex-end;">
              <span class="label">목표가</span>
              <span class="target-price">${symbol}${it.outlook.targetPrice ? it.outlook.targetPrice.toLocaleString() : '—'}</span>
              ${it.outlook.targetPrice && it.price ? (() => {
                const upside = ((it.outlook.targetPrice - it.price) / it.price) * 100;
                const cls = upside < 0 ? 'upside neg' : 'upside';
                const sign = upside > 0 ? '+' : '';
                return `<span class="${cls}">${sign}${upside.toFixed(0)}% 가능성</span>`;
              })() : ''}
            </div>
          </div>

          ${(it.outlook.bull && it.outlook.bull.length) || (it.outlook.bear && it.outlook.bear.length) ? `
            <div class="bull-bear-grid">
              ${it.outlook.bull && it.outlook.bull.length ? `
                <div class="bull-card">
                  <div class="head">▲ 강세 의견 (오를 거란 이유)</div>
                  <ul>${it.outlook.bull.map((b) => `<li>${escapeHtml(b)}</li>`).join('')}</ul>
                </div>
              ` : ''}
              ${it.outlook.bear && it.outlook.bear.length ? `
                <div class="bear-card">
                  <div class="head">▼ 약세 의견 (떨어질 거란 이유)</div>
                  <ul>${it.outlook.bear.map((b) => `<li>${escapeHtml(b)}</li>`).join('')}</ul>
                </div>
              ` : ''}
            </div>
          ` : ''}

          ${it.outlook.summary ? `
            <div style="margin-top: 10px; padding-top: 10px; border-top: 0.5px solid var(--border); font-size: 12px; color: var(--text-secondary); line-height: 1.6;">
              ${escapeHtml(it.outlook.summary)}
            </div>
          ` : ''}
        </div>
      ` : ''}

      ${(it.keyDates && it.keyDates.length) ? `
        <div class="sd-card">
          <div class="sd-card-title">📅 주요 일정</div>
          ${it.keyDates.map((k) => `
            <div class="key-date" style="background: transparent; padding: 6px 0; margin: 0;">
              <span class="kd-date">${escapeHtml(k.date.slice(5))}</span>
              <span class="kd-event">${escapeHtml(k.event)}</span>
            </div>
          `).join('')}
        </div>
      ` : ''}

      ${(it.recentNews && it.recentNews.length) ? `
        <div class="sd-card">
          <div class="sd-card-title">📰 최근 뉴스</div>
          ${it.recentNews.map((n) => `
            <div class="stock-news" style="background: transparent; padding: 8px 0; margin: 0; border-bottom: 0.5px solid var(--border);">
              <div class="sn-h">${escapeHtml(n.headline)}</div>
              <div class="sn-meta">
                ${n.url ? `<a href="${escapeHtml(n.url)}" target="_blank" rel="noopener">· ${escapeHtml(n.source || '출처')}</a>` : `<span>· ${escapeHtml(n.source || '출처')}</span>`}
                <span class="sn-date">· ${escapeHtml(n.date || '')}</span>
              </div>
            </div>
          `).join('')}
        </div>
      ` : ''}

      <div class="sd-card">
        <div class="sd-card-title">📝 내 메모</div>
        <textarea id="stockMemo" class="memo-input" placeholder="이 종목에 대한 메모...">${escapeHtml(it.userMemo || '')}</textarea>
      </div>

      <div class="modal-actions" style="margin-top: 16px;">
        <button class="btn" onclick="closeModal()">닫기</button>
        <button class="btn primary" id="saveMemoBtn">메모 저장</button>
      </div>
    </div>
  `;

  showModal(html);

  // 차트 그리기
  setTimeout(() => {
    const canvas = document.getElementById('stockDetailChart');
    if (!canvas || !window.Chart) return;
    const seed = hashString(it.ticker);
    const points = generateMockChart(20, change1M, seed);
    const change = change1M;
    new Chart(canvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: points.map((_, i) => i),
        datasets: [{
          data: points,
          borderColor: change > 0 ? '#4ADE80' : change < 0 ? '#EF4444' : '#9CA3B5',
          backgroundColor: change > 0 ? 'rgba(74, 222, 128, 0.12)' : change < 0 ? 'rgba(239, 68, 68, 0.12)' : 'rgba(156, 163, 181, 0.1)',
          borderWidth: 1.5,
          tension: 0.3,
          pointRadius: 0,
          fill: true,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
        scales: { x: { display: false }, y: { display: false } },
        animation: { duration: 400 },
      },
    });
  }, 50);

  // 메모 저장
  const saveBtn = document.getElementById('saveMemoBtn');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      const memo = document.getElementById('stockMemo')?.value || '';
      it.userMemo = memo.trim();
      localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(State.portfolio));
      closeModal();
    });
  }
}

function openAddStockModal(market) {
  const isUs = market === 'us';
  const html = `
    <h2>${isUs ? '🇺🇸 미국' : '🇰🇷 한국'} 주식 추가</h2>
    <div class="field">
      <label>티커 ${isUs ? '(예: AAPL, TSLA)' : '(예: 005930)'}</label>
      <input type="text" id="newTicker" autocomplete="off" autocapitalize="characters" placeholder="${isUs ? 'AAPL' : '005930'}" />
    </div>
    <div class="field">
      <label>종목명</label>
      <input type="text" id="newName" autocomplete="off" placeholder="${isUs ? '애플' : '삼성전자'}" />
    </div>
    <div class="field">
      <label>섹터 (선택)</label>
      <select id="newSector">
        <option value="">선택 안 함</option>
        ${isUs ? `
          <option value="빅테크">빅테크</option>
          <option value="반도체">반도체</option>
          <option value="AI 인프라">AI 인프라</option>
          <option value="AI 전력">AI 전력</option>
          <option value="에너지">에너지</option>
          <option value="금융">금융</option>
          <option value="헬스케어">헬스케어</option>
          <option value="소비재">소비재</option>
          <option value="ETF">ETF</option>
        ` : `
          <option value="반도체">반도체</option>
          <option value="자동차">자동차</option>
          <option value="2차전지">2차전지</option>
          <option value="바이오">바이오</option>
          <option value="금융">금융</option>
          <option value="에너지">에너지</option>
          <option value="ETF">ETF</option>
        `}
      </select>
    </div>
    <div class="field">
      <label>메모 (선택)</label>
      <input type="text" id="newNote" autocomplete="off" placeholder="관심 사유, 매수 이유 등" />
    </div>
    <div class="modal-actions">
      <button class="btn" onclick="closeModal()">취소</button>
      <button class="btn primary" id="confirmAdd">추가</button>
    </div>
  `;
  showModal(html);

  $('#confirmAdd').addEventListener('click', () => {
    const ticker = $('#newTicker').value.trim().toUpperCase();
    const name = $('#newName').value.trim();
    const sector = $('#newSector').value;
    const note = $('#newNote').value.trim();
    if (!ticker || !name) {
      alert('티커와 종목명은 필수입니다');
      return;
    }
    State.portfolio[market] = State.portfolio[market] || [];
    State.portfolio[market].push({
      ticker, name, sector, note,
      price: 0, change1W: 0, change1M: 0, changeYTD: 0, beta: 1.0, signal: 'gray',
    });
    localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(State.portfolio));
    closeModal();
    render();
  });
}

function openHoldingActions(ticker, market) {
  const html = `
    <h2>${escapeHtml(ticker)}</h2>
    <div style="margin-bottom: 16px; color: var(--text-tertiary); font-size: 13px;">이 종목으로 무엇을 하시겠어요?</div>
    <button class="btn" id="actEditNote" style="margin-bottom: 8px; width: 100%;">메모 수정</button>
    <button class="btn" id="actMoveToOther" style="margin-bottom: 8px; width: 100%;">${market === 'us' ? '한국' : '미국'} 주식으로 이동</button>
    <button class="btn" id="actDelete" style="margin-bottom: 16px; width: 100%; color: var(--negative);">삭제</button>
    <button class="btn" onclick="closeModal()" style="width: 100%;">닫기</button>
  `;
  showModal(html);

  $('#actDelete').addEventListener('click', () => {
    if (!confirm(`${ticker}을(를) 포트폴리오에서 삭제할까요?`)) return;
    State.portfolio[market] = State.portfolio[market].filter((it) => it.ticker !== ticker);
    localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(State.portfolio));
    closeModal();
    render();
  });

  $('#actMoveToOther').addEventListener('click', () => {
    const other = market === 'us' ? 'kr' : 'us';
    const item = State.portfolio[market].find((it) => it.ticker === ticker);
    if (!item) return;
    State.portfolio[market] = State.portfolio[market].filter((it) => it.ticker !== ticker);
    State.portfolio[other] = State.portfolio[other] || [];
    State.portfolio[other].push(item);
    localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(State.portfolio));
    closeModal();
    render();
  });

  $('#actEditNote').addEventListener('click', () => {
    const item = State.portfolio[market].find((it) => it.ticker === ticker);
    if (!item) return;
    const next = prompt('메모', item.note || '');
    if (next !== null) {
      item.note = next.trim();
      localStorage.setItem(STORAGE_KEYS.portfolio, JSON.stringify(State.portfolio));
    }
    closeModal();
    render();
  });
}

// ------------- 차트 탭 -------------
function renderCharts(app) {
  const us = State.portfolio.us;
  app.innerHTML = `
    <header class="app-header">
      <div class="meta">최근 1개월</div>
      <h1>차트</h1>
    </header>

    <div class="section-title" style="padding: 14px 20px 6px;">
      🇺🇸 미국 주식 (${us.length})
    </div>
    <div class="chart-grid" id="usCharts"></div>

    <div class="section-title" style="padding: 18px 20px 6px;">
      🇰🇷 한국 주식 (${State.portfolio.kr.length})
    </div>
    <div class="chart-grid" id="krCharts">${
      State.portfolio.kr.length
        ? ''
        : `<div class="empty-state" style="grid-column: 1 / -1;">한국 주식이 등록되면 여기 차트가 표시돼요</div>`
    }</div>
  `;

  setTimeout(() => {
    us.forEach((it, i) => renderThumbChart('us-' + i, it));
    State.portfolio.kr.forEach((it, i) => renderThumbChart('kr-' + i, it));

    // 차트 썸네일 클릭 시 상세 모달
    $$('.chart-thumb[data-ticker]').forEach((el) => {
      el.addEventListener('click', () => {
        openStockDetail(el.dataset.ticker, el.dataset.market);
      });
    });
  }, 50);
}

function renderThumbChart(id, item) {
  const containerId = id.startsWith('us-') ? 'usCharts' : 'krCharts';
  const container = document.getElementById(containerId);
  if (!container) return;

  const div = document.createElement('div');
  div.className = 'chart-thumb';
  div.dataset.ticker = item.ticker;
  div.dataset.market = id.startsWith('us-') ? 'us' : 'kr';
  const change = item.change1M ?? 0;
  const changeColor = change > 0 ? 'var(--positive)' : change < 0 ? 'var(--negative)' : 'var(--text-tertiary)';

  div.innerHTML = `
    <div class="head">
      <div class="ticker">${escapeHtml(item.ticker)}</div>
      <div class="change" style="color: ${changeColor}">${pct(change)}</div>
    </div>
    <canvas id="chart-${id}" role="img" aria-label="${escapeHtml(item.ticker)} 1개월 차트"></canvas>
    <div class="price">$${item.price ? item.price.toLocaleString() : '—'}</div>
  `;
  container.appendChild(div);

  // 가짜 시세 데이터 생성 (시드: ticker 해시)
  const seed = hashString(item.ticker);
  const points = generateMockChart(20, item.change1M ?? 0, seed);

  const ctx = document.getElementById('chart-' + id).getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: points.map((_, i) => i),
      datasets: [{
        data: points,
        borderColor: change > 0 ? '#4ADE80' : change < 0 ? '#EF4444' : '#9CA3B5',
        backgroundColor: change > 0 ? 'rgba(74, 222, 128, 0.12)' : change < 0 ? 'rgba(239, 68, 68, 0.12)' : 'rgba(156, 163, 181, 0.1)',
        borderWidth: 1.5,
        tension: 0.3,
        pointRadius: 0,
        fill: true,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false }, tooltip: { enabled: false } },
      scales: { x: { display: false }, y: { display: false } },
      animation: { duration: 400 },
    },
  });
}

function hashString(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

function generateMockChart(n, totalChangePct, seed) {
  const start = 100;
  const end = 100 * (1 + totalChangePct / 100);
  const arr = [];
  let v = start;
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    const target = start + (end - start) * t;
    // Pseudo-random walk
    seed = (seed * 1103515245 + 12345) & 0x7fffffff;
    const noise = ((seed % 1000) / 1000 - 0.5) * Math.abs(end - start) * 0.3;
    v = target + noise;
    arr.push(v);
  }
  return arr;
}

// ------------- 부동산 탭 -------------
function renderRealEstate(app) {
  const re = State.realEstate || { categories: {} };
  app.innerHTML = `
    <header class="app-header">
      <div class="meta">청약 · 대출 · 정책</div>
      <h1>부동산</h1>
    </header>

    <div class="section">
      ${Object.entries(re.categories).map(([key, cat]) => `
        <div class="realestate-cat">
          <div class="head">
            <div>
              <div class="title">${escapeHtml(cat.title)}</div>
              <div class="desc">${escapeHtml(cat.description)}</div>
            </div>
          </div>
          ${(cat.items || []).length === 0
            ? `<div class="empty">아직 등록된 정보가 없어요</div>`
            : (cat.items || []).map((it) => `
              <div class="card">
                <div style="font-size: 13px; font-weight: 500; margin-bottom: 4px;">${escapeHtml(it.title)}</div>
                <div style="font-size: 11px; color: var(--text-tertiary);">${escapeHtml(it.date || '')} ${it.summary ? ' · ' + escapeHtml(it.summary) : ''}</div>
              </div>
            `).join('')}
          <button class="add-here" data-cat="${key}">+ 정보 추가</button>
        </div>
      `).join('')}
    </div>
  `;

  $$('.add-here').forEach((btn) => {
    btn.addEventListener('click', () => openAddRealEstateModal(btn.dataset.cat));
  });
}

function openAddRealEstateModal(catKey) {
  const cat = State.realEstate.categories[catKey];
  const html = `
    <h2>${escapeHtml(cat.title)} 추가</h2>
    <div class="field">
      <label>제목</label>
      <input type="text" id="reTitle" placeholder="${catKey === 'subscription' ? '예: 강남구 OO아파트 1순위' : '제목'}" />
    </div>
    <div class="field">
      <label>날짜 (YYYY-MM-DD)</label>
      <input type="date" id="reDate" value="${State.todayDate}" />
    </div>
    <div class="field">
      <label>요약 (선택)</label>
      <input type="text" id="reSummary" placeholder="간단한 메모" />
    </div>
    <div class="modal-actions">
      <button class="btn" onclick="closeModal()">취소</button>
      <button class="btn primary" id="confirmReAdd">추가</button>
    </div>
  `;
  showModal(html);

  $('#confirmReAdd').addEventListener('click', () => {
    const title = $('#reTitle').value.trim();
    const date = $('#reDate').value;
    const summary = $('#reSummary').value.trim();
    if (!title) { alert('제목은 필수입니다'); return; }

    cat.items = cat.items || [];
    cat.items.push({ title, date, summary });

    // 캘린더에도 점 추가
    if (date) {
      State.calendarEvents.realestate = State.calendarEvents.realestate || {};
      State.calendarEvents.realestate[date] = State.calendarEvents.realestate[date] || [];
      State.calendarEvents.realestate[date].push({
        type: catKey, label: title, color: 'blue'
      });
    }

    localStorage.setItem(STORAGE_KEYS.realEstate, JSON.stringify(State.realEstate));
    closeModal();
    render();
  });
}

// ------------- 아카이브 탭 -------------
function renderArchive(app) {
  const reports = State.reportsIndex.slice().reverse();
  app.innerHTML = `
    <header class="app-header">
      <div class="meta">과거 보고서</div>
      <h1>아카이브</h1>
    </header>

    <div class="section">
      ${reports.length === 0
        ? `<div class="placeholder">
            <div class="ico">📁</div>
            <div>아직 보고서가 없어요</div>
            <div style="margin-top:4px; font-size:11px;">매일 오전 7:37에 자동 생성됩니다</div>
          </div>`
        : reports.map((r) => `
          <div class="archive-item" data-date="${r.date}">
            <div class="date">${formatKoreanDate(r.date)}</div>
            <div class="title">${escapeHtml(r.title)}</div>
            <div class="summary">${escapeHtml(r.summary || '')}</div>
          </div>
        `).join('')}
    </div>
  `;

  $$('.archive-item').forEach((el) => {
    el.addEventListener('click', () => openReportModal(el.dataset.date));
  });
}

// ------------- 시작 -------------
init();
