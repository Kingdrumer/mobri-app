// 포트폴리오 데일리 PWA — 메인 앱 로직

const STORAGE_KEYS = {
  portfolio: 'pwa.portfolio.v1',
  selectedDate: 'pwa.selectedDate.v1',
  calMode: 'pwa.calMode.v1',
  realEstate: 'pwa.realEstate.v1',
  realEstateFilter: 'pwa.realEstateFilter.v1',
};

// ── 부동산 맞춤설정 기본값 ──
const DEFAULT_RE_FILTER = {
  // 본인 상황
  housing: null,             // 부모님댁 | 월세 | 전세 | 기숙사 | 자가
  household: [],             // 1인_청년, 1인_일반, 신혼, 예비_신혼, 신생아, 다자녀, 한부모, 고령자
  age: null,                 // ~24 | 25-29 | 30-34 | 35-39 | 40-64 | 65+
  householdHead: null,       // 세대주 | 세대원
  supportType: null,         // 일반 | 수급자 | 차상위 | 한부모 | 보호종료청년 | 국가유공자
  // 가족 상황
  marriageDuration: null,    // 미혼 | 예비 | 1년이내 | 1-3년 | 3-5년 | 5-7년 | 7년초과
  children: null,            // 없음 | 신생아 | 1명 | 2명 | 3명이상
  dependents: null,          // 1명(본인만) | 2명 | 3명 | 4명 | 5명이상
  childPlan: null,           // 임신중 | 출산예정 | 계획있음 | 계획없음
  // 자격 / 재정
  housingNoneYears: null,    // 보유 | 미만3년 | 3-5년 | 5-10년 | 10-15년 | 15년이상
  income: null,              // 50%이하 | 70%이하 | 100%이하 | 120%이하 | 120%초과 | 모름
  savingsAccount: null,      // 없음 | 6개월미만 | 6개월-2년 | 2년이상
  savingsCount: null,        // 12회미만 | 12-24회 | 24-60회 | 60회이상
  budget: null,              // 1천이하 | 1천-5천 | 5천-1억 | 1억-3억 | 3억이상
  // 선호
  region: [],
  type: [],
  alerts: ['new', 'deadline_3'],
};

// 맞춤설정 옵션 메타 (UI에 표시할 라벨)
// 라벨은 칩에 짧게, 자세한 설명은 RE_GROUP_HINTS 에 따로
const RE_FILTER_OPTIONS = {
  housing:           [['parent','부모님 댁'],['monthly','자취 월세'],['jeonse','자취 전세'],['dorm','기숙사 (학교·회사)'],['own','자가 (내 명의)']],
  household:         [['1인_청년','1인 청년 (19~39세)'],['1인_일반','1인 일반 (40세+)'],['예비_신혼','예비 신혼'],['신혼','신혼부부 (혼인 7년 이내)'],['신생아','신생아 가구 (2년 내 출산)'],['다자녀','다자녀 (미성년 2명+)'],['한부모','한부모'],['고령자','고령자 (65세+)']],
  age:               [['~24','~24세'],['25-29','25-29세'],['30-34','30-34세'],['35-39','35-39세'],['40-64','40-64세'],['65+','65세+']],
  householdHead:     [['세대주','세대주 (등본 대표)'],['세대원','세대원 (부모 등본에 포함)']],
  supportType:       [['일반','일반 (해당없음)'],['수급자','수급자 (기초생활)'],['차상위','차상위 (수급 바로 위)'],['한부모','한부모 (지원법 대상)'],['보호종료청년','보호종료청년 (시설 퇴소 5년 내)'],['국가유공자','국가유공자 (본인·유족)']],
  marriageDuration:  [['미혼','미혼'],['예비','예비 (혼인신고 전)'],['1년이내','1년 이내'],['1-3년','1~3년'],['3-5년','3~5년'],['5-7년','5~7년'],['7년초과','7년 초과']],
  children:          [['없음','없음'],['신생아','신생아 (출산 2년 내)'],['1명','미성년 1명'],['2명','미성년 2명'],['3명이상','미성년 3명+']],
  dependents:        [['1명','본인만 (1명)'],['2명','2명 (예: 본인+배우자)'],['3명','3명 (예: 부부+자녀1)'],['4명','4명 (예: 부부+자녀2)'],['5명이상','5명 이상']],
  childPlan:         [['계획없음','계획 없음'],['계획있음','계획 있음'],['임신중','임신 중'],['출산예정','출산 예정 (2년 내)']],
  housingNoneYears:  [['보유','주택 보유 (현재 있음)'],['미만3년','3년 미만'],['3-5년','3~5년'],['5-10년','5~10년 (가점↑)'],['10-15년','10~15년 (가점↑↑)'],['15년이상','15년 이상 (만점)']],
  income:            [['50%이하','50% 이하 (예: 3인 월 360만↓)'],['70%이하','70% 이하 (월 500만↓)'],['100%이하','100% 이하 (월 720만↓)'],['120%이하','120% 이하 (월 860만↓)'],['120%초과','120% 초과'],['모름','모름']],
  savingsAccount:    [['없음','없음'],['6개월미만','6개월 미만'],['6개월-2년','6개월~2년'],['2년이상','2년 이상 (수도권 1순위)']],
  savingsCount:      [['12회미만','12회 미만'],['12-24회','12~24회 (1~2년)'],['24-60회','24~60회 (2~5년)'],['60회이상','60회 이상 (5년+, 생애최초 자격)']],
  budget:            [['1천이하','1천만 이하'],['1천-5천','1천~5천만'],['5천-1억','5천~1억'],['1억-3억','1억~3억'],['3억이상','3억 이상']],
  region:            [['서울','서울'],['경기','경기'],['인천','인천'],['부산','부산'],['대구','대구'],['광주','광주'],['전국','전국']],
  type:              [['매입임대','매입임대 (LH가 산 빌라)'],['행복주택','행복주택 (새로 지은 임대)'],['전세임대','전세임대 (LH가 대신 계약)'],['장기전세','장기전세 (10~20년, 미리내집)'],['공공분양','공공분양 (살 수 있는 분양)'],['신혼희망타운','신혼희망타운 (신혼 전용 분양)']],
  alerts:            [['new','신규 공고'],['deadline_3','마감 D-3'],['winner','당첨자 발표']],
};

// 그룹 아래에 표시할 💡 도움말 (긴 안내)
const RE_GROUP_HINTS = {
  household:        '한 사람이 여러 카테고리에 해당될 수 있어요. 예: 신혼+신생아 → 둘 다 선택',
  supportType:      '"수급자/차상위/한부모"는 임대주택에서 1순위(가점 최고)예요. 행정복지센터에서 본인 자격 확인 가능합니다.',
  marriageDuration: '"신혼부부 7년 이내" 기준은 청약·임대 모두 동일해요. 7년 넘으면 일반공급으로 분류됩니다.',
  housingNoneYears: '본인+배우자 합산 무주택 기간이에요. 부모님과 같이 살아도 본인 명의 집 없으면 무주택.',
  income:           '도시근로자 월평균소득 기준. 부부 모두 일하면 합산 금액으로 계산해요. 예시는 3인 가구 기준 대략값입니다.',
  savingsAccount:   '청약통장(주택청약종합저축) 가입 후 경과 기간. 수도권 공공분양 1순위는 2년+ 가입 필요.',
  savingsCount:     '매달 입금한 횟수. 생애최초 특별공급은 보통 60회 이상 납입해야 자격이 생겨요.',
  childPlan:        '임신·출산 계획이 있으면 신혼희망타운·미리내집 가점에 영향을 줍니다.',
  dependents:       '주민등록표상 같이 사는 가족 수 (본인 포함). 청약 가점에 영향.',
  householdHead:    '세대주는 등본의 대표자. 부모님 집 등본에 같이 있으면 보통 세대원이에요.',
};

// 필터 라벨 한국어 매핑
const RE_FILTER_LABELS = {
  housing: '거주 형태', household: '가구 형태', age: '연령',
  householdHead: '세대주 여부', supportType: '지원자격',
  marriageDuration: '혼인 기간', children: '자녀 (미성년)',
  dependents: '부양가족 수', childPlan: '자녀 계획',
  housingNoneYears: '무주택 기간', income: '소득 (도시근로자 %)',
  savingsAccount: '청약통장 가입기간', savingsCount: '청약 납입회수',
  budget: '자금 (보증금 가용)',
  region: '관심 지역', type: '주거 유형', alerts: '알림',
};

// 섹션 그룹 (UI 그룹화용)
const RE_FILTER_SECTIONS = [
  { title: '👤 본인 상황', keys: ['housing', 'household', 'age', 'householdHead', 'supportType'] },
  { title: '👨‍👩‍👧 가족 상황', keys: ['marriageDuration', 'children', 'dependents', 'childPlan'] },
  { title: '🏠 자격·재정', keys: ['housingNoneYears', 'income', 'savingsAccount', 'savingsCount', 'budget'] },
  { title: '🎯 선호 (필터링)', keys: ['region', 'type', 'alerts'] },
];

// 다중선택(multi) 키 셋
const RE_MULTI_KEYS = new Set(['household', 'region', 'type', 'alerts']);

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
  realEstateFilter: { ...DEFAULT_RE_FILTER },
  reportsIndex: [],
  reportCache: {},
  charts: {},
};

// 부동산 맞춤설정 로드 (localStorage)
function loadRealEstateFilter() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.realEstateFilter);
    if (raw) {
      State.realEstateFilter = { ...DEFAULT_RE_FILTER, ...JSON.parse(raw) };
    }
  } catch (e) { /* ignore */ }
}

function saveRealEstateFilter() {
  try {
    localStorage.setItem(STORAGE_KEYS.realEstateFilter, JSON.stringify(State.realEstateFilter));
  } catch (e) { /* ignore */ }
}

// 맞춤설정이 비어있는지 (초기 상태) 판단
function isFilterEmpty() {
  const f = State.realEstateFilter;
  const singles = ['housing','age','income','savingsAccount','budget','householdHead','supportType','marriageDuration','children','dependents','childPlan','housingNoneYears','savingsCount'];
  const arrays = ['household','region','type'];
  const anySingle = singles.some(k => !!f[k]);
  const anyArr = arrays.some(k => (f[k] || []).length > 0);
  return !anySingle && !anyArr;
}

// 맞춤설정 요약 배지 텍스트 (예: "1인 청년 · 서울 · 매입임대")
function filterSummaryBadge() {
  const f = State.realEstateFilter;
  const parts = [];
  if (f.household?.length) {
    const hh = RE_FILTER_OPTIONS.household.find(o => o[0] === f.household[0]);
    if (hh) parts.push(hh[1]);
  }
  if (f.region?.length) parts.push(f.region.slice(0, 2).join('·'));
  if (f.type?.length) parts.push(f.type[0]);
  return parts.slice(0, 3).join(' · ') || '설정 안함';
}

// ── 공고 순위 판별 ──
// 사용자 필터에 기반해 해당 공고에서 몇 순위로 신청 가능한지 판단
// 반환: { rank, label, hint, confidence: 'high'|'low' } 또는 null
function computeUserPriority(notice, filter) {
  if (!notice?.priorityRules?.length) return null;
  // 필터에서 의미있는 입력이 거의 없으면 신뢰도 낮음
  const hasMinimal = !!(filter.household?.length || filter.supportType || filter.children || filter.marriageDuration || filter.housingNoneYears);
  if (!hasMinimal) {
    return { rank: '미확정', label: '맞춤설정에 가구·자녀·지원자격 입력 필요', hint: '🎯 내 맞춤 설정에서 정보를 채워주세요', confidence: 'low' };
  }
  for (const rule of notice.priorityRules) {
    if (matchPriorityRule(rule.match || {}, filter)) {
      return {
        rank: rule.rank,
        label: rule.label,
        hint: rule.hint || '',
        confidence: 'high',
      };
    }
  }
  // 어떤 규칙에도 매치 안 됨 — 자격 미충족 가능성
  return { rank: '자격 미충족', label: '현재 입력 기준으로는 해당 없음', hint: '맞춤설정을 점검해 보세요', confidence: 'low' };
}

// 한 규칙의 match 조건이 사용자 필터에 통과하는지
function matchPriorityRule(match, filter) {
  // $or: 하위 조건들 중 하나라도 통과하면 OK
  if (match.$or && Array.isArray(match.$or)) {
    return match.$or.some(sub => matchPriorityRule(sub, filter));
  }
  // household — 교집합 있어야
  if (match.household?.length) {
    const userHH = filter.household || [];
    if (!userHH.some(h => match.household.includes(h))) return false;
  }
  // 단일값 필드들 — 리스트에 사용자 값이 있어야
  const singleFields = [
    'supportType', 'children', 'income', 'savingsAccount', 'savingsCount',
    'marriageDuration', 'housingNoneYears', 'dependents', 'childPlan', 'householdHead',
  ];
  for (const f of singleFields) {
    if (match[f]?.length) {
      if (!filter[f] || !match[f].includes(filter[f])) return false;
    }
  }
  // ageGroup: '청년' → 사용자 age가 청년 범위인지
  if (match.ageGroup === '청년') {
    if (!filter.age || !['~24','25-29','30-34','35-39'].includes(filter.age)) return false;
  }
  if (match.ageGroup === '고령') {
    if (filter.age !== '65+') return false;
  }
  return true;
}

// 순위 표시용 배지 정보
function getPriorityBadge(priority) {
  if (!priority) return null;
  if (priority.rank === '1순위' || priority.rank === '우선공급') {
    return { icon: '🥇', cls: 'pri-1', text: priority.rank };
  }
  if (priority.rank === '2순위') return { icon: '🥈', cls: 'pri-2', text: '2순위' };
  if (priority.rank === '3순위') return { icon: '🥉', cls: 'pri-3', text: '3순위' };
  if (priority.rank === '일반공급') return { icon: '📋', cls: 'pri-2', text: '일반공급' };
  if (priority.rank === '별도배정') return { icon: '✨', cls: 'pri-2', text: '별도배정' };
  if (priority.rank?.startsWith('특별공급')) return { icon: '⭐', cls: 'pri-1', text: priority.rank };
  if (priority.rank === '신청불가') return { icon: '🚫', cls: 'pri-no', text: '신청불가' };
  if (priority.rank === '자격 미충족') return { icon: '⚠️', cls: 'pri-no', text: '자격검토 필요' };
  if (priority.rank === '미확정') return { icon: '❓', cls: 'pri-unk', text: '설정 필요' };
  return { icon: '📌', cls: 'pri-unk', text: priority.rank };
}

// 공고가 사용자 필터에 매칭되는지 판단 (0~100 점수)
function matchNoticeToFilter(notice, filter) {
  if (!notice) return 0;
  let score = 0; let total = 0;

  // 지역 (가중치 3)
  if (filter.region?.length) {
    total += 3;
    const ok = filter.region.includes('전국') || notice.region?.some(r => filter.region.includes(r) || r === '전국');
    if (ok) score += 3;
  }
  // 가구 형태 (가중치 3)
  if (filter.household?.length) {
    total += 3;
    const ok = notice.household?.some(h => filter.household.includes(h));
    if (ok) score += 3;
  }
  // 주거 유형 (가중치 2)
  if (filter.type?.length) {
    total += 2;
    const ok = filter.type.includes(notice.type);
    if (ok) score += 2;
  }
  // 연령 (가중치 2)
  if (filter.age && notice.ageRange) {
    total += 2;
    const ageMap = { '~24': 22, '25-29': 27, '30-34': 32, '35-39': 37, '40-64': 50, '65+': 70 };
    const userAge = ageMap[filter.age];
    const [min, max] = notice.ageRange;
    if (userAge >= min && userAge <= max) score += 2;
  }
  if (total === 0) return 100; // 필터 안 했으면 전체 통과
  return Math.round((score / total) * 100);
}

// 공고 → 캘린더 이벤트로 변환 (접수기간 매일 + 시작·마감일은 강조)
function noticesToCalendarEvents(notices, filter) {
  const events = {};
  if (!notices) return events;
  const today = TODAY_KST;

  notices.forEach((n) => {
    if (!n.applicationStart) return;
    const score = matchNoticeToFilter(n, filter);
    if (score < 50) return; // 매칭 50% 미만은 캘린더에서 제외

    // 시작일 · 마감일에만 점 표시 (너무 많으면 캘린더 더러워짐)
    const dates = new Set();
    if (n.applicationStart) dates.add(n.applicationStart);
    if (n.applicationEnd && n.applicationEnd !== n.applicationStart) dates.add(n.applicationEnd);

    dates.forEach((date) => {
      const isStart = date === n.applicationStart;
      const isEnd = date === n.applicationEnd;
      const isClosingSoon = isEnd && date >= today;
      const isDday = date === today && isEnd;

      events[date] = events[date] || [];
      events[date].push({
        type: 'subscription',
        label: `${isDday ? '⏰ ' : isStart ? '📋 ' : '⏳ '}${n.shortTitle || n.title}`,
        color: isDday ? 'red' : isStart ? 'blue' : 'amber',
        time: isStart ? '접수 시작' : isDday ? 'D-day 마감' : '마감일',
        title: n.title,
        description: `${n.agency} · ${n.type} · ${n.supplyCount ? n.supplyCount + '세대 · ' : ''}${(n.region || []).join('·')}`,
        impact: (n.highlights || []).join(' / '),
        noticeId: n.id,
        agency: n.agency,
        matchScore: score,
      });
    });
  });

  return events;
}

// 진행 중인 공고 리스트 (마감 임박 순 정렬)
function filteredOpenNotices() {
  const notices = State.realEstate?.notices || [];
  const today = TODAY_KST;
  return notices
    .filter(n => {
      // 종료된 공고 제외
      if (n.applicationEnd && n.applicationEnd < today) return false;
      return true;
    })
    .map(n => ({ ...n, _matchScore: matchNoticeToFilter(n, State.realEstateFilter) }))
    .filter(n => n._matchScore >= 50)
    .sort((a, b) => {
      // 1) 오늘 마감 (closing-today) 최우선
      if (a.status === 'closing-today' && b.status !== 'closing-today') return -1;
      if (b.status === 'closing-today' && a.status !== 'closing-today') return 1;
      // 2) 마감일 빠른 순 (rolling은 뒤로)
      const aEnd = a.rolling ? '9999-12-31' : (a.applicationEnd || '9999-12-31');
      const bEnd = b.rolling ? '9999-12-31' : (b.applicationEnd || '9999-12-31');
      if (aEnd !== bEnd) return aEnd.localeCompare(bEnd);
      // 3) 매칭 점수 높은 순
      return b._matchScore - a._matchScore;
    });
}

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

// 긴 본문에 자동 단락 분리 — 문장 끝(. ? !) 다음 공백을 두 줄 띄움으로
function paraBreak(text) {
  if (!text) return text;
  // 이미 명시적 \n\n 있으면 그대로 유지
  if (text.includes('\n\n')) return text;
  // 한 줄 짧은 텍스트는 그대로
  if (text.length < 60) return text;
  return text.replace(/([.!?]) (?=[가-힣A-Z🟢🔴🟡⚪])/g, '$1\n\n');
}

// 뉴스 헤드라인의 선두 컬러 이모지를 제거하면서 톤 자동 감지
// 데이터에 ⚪🟢🔴🟡🟠🔵 prefix가 있으면 그걸로 impact 결정
function parseNewsHeadline(headline, explicitImpact) {
  if (!headline) return { headline: '', impact: explicitImpact || 'neutral' };
  const m = headline.match(/^([🟢🔴🟡🟠⚪🔵])\s*/u);
  if (!m) return { headline, impact: explicitImpact || 'neutral' };
  const emojiMap = {
    '🟢': 'positive',
    '🔴': 'negative',
    '🟡': 'warning',
    '🟠': 'warning',
    '⚪': 'neutral',
    '🔵': 'neutral',
  };
  const detected = emojiMap[m[1]];
  return {
    headline: headline.slice(m[0].length),
    // 명시적 impact 있으면 그쪽 우선, 없으면 이모지에서 추출
    impact: explicitImpact || detected || 'neutral',
  };
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

    // 부동산 공고를 캘린더 이벤트로 변환 (사용자 맞춤설정 반영)
    if (State.realEstate?.notices) {
      State.calendarEvents.realestate = noticesToCalendarEvents(
        State.realEstate.notices,
        State.realEstateFilter
      );
    }

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

// KST 기준 현재 시각 정보
function getKSTNow() {
  const fmt = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Seoul',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });
  const parts = fmt.formatToParts(new Date());
  const weekday = parts.find((p) => p.type === 'weekday').value;
  const hour = parseInt(parts.find((p) => p.type === 'hour').value, 10);
  const minute = parseInt(parts.find((p) => p.type === 'minute').value, 10);
  const map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  return { dayOfWeek: map[weekday], hour, minute, totalMinutes: hour * 60 + minute };
}

// 시장 상태 + 다음 데이터 갱신 시점 (KST)
// 갱신 스케줄: 평일 08:00, 22:30 KST (portfolio.json 직접 갱신)
function getMarketStatus() {
  const now = getKSTNow();
  const T_0800 = 8 * 60;
  const T_2230 = 22 * 60 + 30;

  // 토(6), 일(0) — 미국 시장 휴장
  if (now.dayOfWeek === 0 || now.dayOfWeek === 6) {
    return {
      isWeekend: true,
      isMarketOpen: false,
      tone: 'weekend',
      label: '주말 휴장 중',
      nextUpdate: '월요일 08:00 KST',
    };
  }

  // 평일
  let nextUpdate;
  if (now.totalMinutes < T_0800) {
    nextUpdate = '오늘 08:00 KST';
  } else if (now.totalMinutes < T_2230) {
    nextUpdate = '오늘 22:30 KST';
  } else {
    nextUpdate = (now.dayOfWeek === 5) ? '월요일 08:00 KST' : '내일 08:00 KST';
  }

  // 미국 정규장 시간(KST 22:30~익일 05:00)
  const isMarketOpen = (now.totalMinutes >= T_2230) || (now.totalMinutes < 5 * 60 && now.dayOfWeek !== 1);

  return {
    isWeekend: false,
    isMarketOpen,
    tone: isMarketOpen ? 'live' : 'pre',
    label: isMarketOpen ? '정규장 진행 중' : '평일 휴장 중',
    nextUpdate,
  };
}

function updateLastUpdatedDisplay() {
  const els = document.querySelectorAll('.last-updated-text');
  const bars = document.querySelectorAll('.refresh-bar');
  if (!els.length) return;

  const ts = State.portfolio?.lastUpdated;
  const status = getMarketStatus();

  // refresh-bar 톤 클래스
  bars.forEach((b) => {
    b.classList.remove('weekend', 'live', 'pre');
    b.classList.add(status.tone);
  });

  let html;
  if (!ts) {
    html = `<span class="lu-status">갱신 중...</span>`;
  } else {
    const ago = formatTimeAgo(new Date(ts));
    const stale = (Date.now() - new Date(ts).getTime()) > 24 * 60 * 60 * 1000;
    html = `
      <span class="lu-status">${escapeHtml(status.label)}</span>
      <span class="lu-sep">·</span>
      <span class="lu-ago ${stale ? 'stale' : ''}">${escapeHtml(ago)} 갱신</span>
      <span class="lu-next">다음: ${escapeHtml(status.nextUpdate)}</span>
    `;
  }
  els.forEach((el) => { el.innerHTML = html; });
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

  // 부동산 데이터는 항상 서버 최신본 우선 (스키마 v2 마이그레이션 위해)
  // — userMemos만 localStorage에서 보존
  const fetchedRealEstate = await loadJSON('data/real-estate.json');
  const savedRealEstateRaw = localStorage.getItem(STORAGE_KEYS.realEstate);
  let savedUserMemos = [];
  if (savedRealEstateRaw) {
    try {
      const parsed = JSON.parse(savedRealEstateRaw);
      savedUserMemos = parsed.userMemos || [];
      // 구버전 schema (categories.memo.items)도 회수
      if (!savedUserMemos.length && parsed.categories?.memo?.items?.length) {
        savedUserMemos = parsed.categories.memo.items;
      }
    } catch (e) {}
  }
  State.realEstate = fetchedRealEstate || { notices: [], userMemos: [] };
  if (savedUserMemos.length) State.realEstate.userMemos = savedUserMemos;

  // 부동산 맞춤설정 로드
  loadRealEstateFilter();

  const calEvents = await loadJSON('data/calendar-events.json');
  if (calEvents) State.calendarEvents = calEvents;

  // 부동산 공고를 캘린더 이벤트로 변환
  if (State.realEstate?.notices) {
    State.calendarEvents.realestate = noticesToCalendarEvents(
      State.realEstate.notices,
      State.realEstateFilter
    );
  }

  const reportsIdx = await loadJSON('data/reports/index.json');
  if (reportsIdx) State.reportsIndex = reportsIdx.reports || [];

  const savedMode = localStorage.getItem(STORAGE_KEYS.calMode);
  if (savedMode) State.calMode = savedMode;

  const savedDate = localStorage.getItem(STORAGE_KEYS.selectedDate);
  if (savedDate) State.selectedDate = savedDate;

  setupTabs();
  render();
  initDaySheetGestures();
  startAutoRefresh();
}

// ------------- 탭 라우팅 -------------
function setupTabs() {
  $$('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      State.tab = btn.dataset.tab;
      $$('.tab-btn').forEach((b) => b.classList.toggle('active', b === btn));
      closeDaySheet();   // 바텀시트가 열려 있으면 닫고 탭 전환
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

    ${State.calMode === 'realestate' ? renderCustomFilterBar() : ''}

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

  // 부동산 맞춤설정 작은줄 클릭 → 바텀시트 열기
  $('#reCustomBar')?.addEventListener('click', openRealEstateFilterSheet);

  renderCalendarGrid();
  renderSelectedDayPanel();
}

// ── 부동산 맞춤설정 작은줄 ──
function renderCustomFilterBar() {
  const isEmpty = isFilterEmpty();
  const summary = isEmpty ? '👋 5초만에 설정하기' : filterSummaryBadge();
  const cls = isEmpty ? 're-custom-bar is-empty' : 're-custom-bar';
  return `
    <button class="${cls}" id="reCustomBar" type="button">
      <span class="left">
        <span class="icon">🎯</span>
        <span class="label">내 맞춤 설정</span>
        <span class="badge">${escapeHtml(summary)}</span>
      </span>
      <span class="arrow">›</span>
    </button>
  `;
}

// ── 부동산 맞춤설정 바텀시트 모달 ──
function openRealEstateFilterSheet() {
  // 임시 상태 (저장 전까지 누적)
  let temp = JSON.parse(JSON.stringify(State.realEstateFilter));

  const renderGroup = (key, multi) => {
    const opts = RE_FILTER_OPTIONS[key];
    const hint = RE_GROUP_HINTS[key];
    return `
      <div class="qgroup">
        <div class="qtitle">
          ${escapeHtml(RE_FILTER_LABELS[key])}
          ${multi ? '<span class="qhint">중복 선택</span>' : ''}
        </div>
        <div class="qopts" data-key="${key}" data-multi="${multi}">
          ${opts.map(([v, label]) => {
            const isSel = multi
              ? (temp[key] || []).includes(v)
              : temp[key] === v;
            return `<button type="button" class="qopt ${isSel ? 'on' : ''}" data-val="${v}">${escapeHtml(label)}</button>`;
          }).join('')}
        </div>
        ${hint ? `<div class="qgroup-hint">💡 ${escapeHtml(hint)}</div>` : ''}
      </div>
    `;
  };

  const matchedCount = () => {
    const notices = State.realEstate?.notices || [];
    return notices.filter(n => matchNoticeToFilter(n, temp) >= 50).length;
  };

  const html = `
    <div class="re-filter-sheet">
      <div class="rfs-head">
        <div>
          <div class="rfs-title">🎯 내 맞춤 설정</div>
          <div class="rfs-sub">선택한 조건에 맞는 공고만 캘린더에 보여드려요</div>
        </div>
        <button class="rfs-reset" id="rfsReset" type="button">초기화</button>
      </div>
      <div class="rfs-body" id="rfsBody">
        ${RE_FILTER_SECTIONS.map(section => `
          <div class="qsection-head">${section.title}</div>
          ${section.keys.map(k => renderGroup(k, RE_MULTI_KEYS.has(k))).join('')}
        `).join('')}
      </div>
      <div class="rfs-footer">
        <button class="rfs-save" id="rfsSave" type="button">맞춤 설정 저장 <span id="rfsCount">(${matchedCount()}개 공고 매칭)</span></button>
      </div>
    </div>
  `;
  showModal(html);

  // 옵션 칩 클릭 핸들러
  $$('.qopt', $('#rfsBody')).forEach((btn) => {
    btn.addEventListener('click', () => {
      const group = btn.closest('.qopts');
      const key = group.dataset.key;
      const multi = group.dataset.multi === 'true';
      const val = btn.dataset.val;
      if (multi) {
        const arr = temp[key] || [];
        const idx = arr.indexOf(val);
        if (idx === -1) arr.push(val); else arr.splice(idx, 1);
        temp[key] = arr;
        btn.classList.toggle('on');
      } else {
        // 단일선택: 같은 값 누르면 해제, 다른 값이면 변경
        if (temp[key] === val) {
          temp[key] = null;
          btn.classList.remove('on');
        } else {
          temp[key] = val;
          $$('.qopt', group).forEach(b => b.classList.toggle('on', b === btn));
        }
      }
      // 매칭 카운트 갱신
      const cnt = $('#rfsCount');
      if (cnt) cnt.textContent = `(${matchedCount()}개 공고 매칭)`;
    });
  });

  // 초기화 버튼
  $('#rfsReset')?.addEventListener('click', () => {
    temp = JSON.parse(JSON.stringify(DEFAULT_RE_FILTER));
    closeModal();
    setTimeout(openRealEstateFilterSheet, 50);
  });

  // 저장 버튼
  $('#rfsSave')?.addEventListener('click', () => {
    State.realEstateFilter = temp;
    saveRealEstateFilter();
    // 캘린더 이벤트 재생성
    if (State.realEstate?.notices) {
      State.calendarEvents.realestate = noticesToCalendarEvents(
        State.realEstate.notices,
        State.realEstateFilter
      );
    }
    closeModal();
    render();
  });
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
    el.addEventListener('click', async () => {
      const date = el.dataset.date;
      if (!date) return;
      State.selectedDate = date;
      localStorage.setItem(STORAGE_KEYS.selectedDate, date);
      // 다른 달이면 그 달로 이동 후 캘린더만 다시 그림 (전체 render 안 함)
      const d = new Date(date);
      if (d.getMonth() !== State.currentMonth.getMonth() || d.getFullYear() !== State.currentMonth.getFullYear()) {
        State.currentMonth = new Date(d.getFullYear(), d.getMonth(), 1);
        render();
      } else {
        // 같은 달이면 셀 강조만 다시 처리
        $$('.cal-day', grid).forEach((c) => {
          c.classList.toggle('selected', c.dataset.date === date && !c.classList.contains('today'));
        });
        // 선택 날짜 라벨 갱신
        const monthInfo = $('.calendar-nav .month');
        if (monthInfo) monthInfo.textContent = formatKoreanDate(date);
      }
      // 시트 내용 채우고 슬라이드 업
      await renderSelectedDayPanel();
      openDaySheet();
    });
  });
}

// 바텀 시트 열기/닫기
function openDaySheet() {
  const sheet = $('#daySheet');
  const backdrop = $('#daySheetBackdrop');
  if (!sheet) return;
  sheet.classList.add('open');
  backdrop?.classList.add('open');
  document.body.classList.add('sheet-open');
}

function closeDaySheet() {
  const sheet = $('#daySheet');
  const backdrop = $('#daySheetBackdrop');
  if (!sheet) return;
  sheet.classList.remove('open');
  backdrop?.classList.remove('open');
  document.body.classList.remove('sheet-open');
  // 시트 닫을 때 컨텐츠는 위로 스크롤 리셋
  setTimeout(() => {
    const content = $('#selectedDayPanel');
    if (content) content.scrollTop = 0;
  }, 300);
}

// 시트 드래그 다운으로 닫기 — 핸들 + 컨텐츠 상단 모두에서 인식 + 속도 감지 + 낮은 임계값
let _sheetInitDone = false;
function initDaySheetGestures() {
  if (_sheetInitDone) return;
  _sheetInitDone = true;
  const sheet = $('#daySheet');
  const handleArea = $('#dsHandleArea');
  const content = $('#selectedDayPanel');
  const backdrop = $('#daySheetBackdrop');
  const closeBtn = $('#dsCloseBtn');
  if (!sheet || !handleArea) return;

  let startY = null;
  let startTime = 0;
  let currentDelta = 0;
  let activeFrom = null; // 'handle' | 'content'

  const CLOSE_THRESHOLD = 60;     // 60px 끌면 닫기 (이전 100 → 완화)
  const FAST_CLOSE_THRESHOLD = 20; // 빠르게 끌면 20px만 끌어도 닫기
  const FAST_VELOCITY = 0.35;      // px/ms — 빠른 플릭 기준

  const onStart = (clientY, from) => {
    // content에서 시작했으면 스크롤이 맨 위에 있을 때만 닫기 제스처 시작
    if (from === 'content' && content && content.scrollTop > 0) return;
    startY = clientY;
    startTime = Date.now();
    currentDelta = 0;
    activeFrom = from;
    sheet.style.transition = 'none';
  };

  const onMove = (clientY) => {
    if (startY === null) return;
    const delta = clientY - startY;
    if (delta > 0) {
      currentDelta = delta;
      sheet.style.transform = `translateY(${delta}px)`;
      if (backdrop) backdrop.style.opacity = String(Math.max(0, 1 - delta / 400));
    } else if (delta < -5 && activeFrom === 'content') {
      // content에서 위로 스크롤하려고 한 거면 제스처 취소 (스크롤 양보)
      sheet.style.transform = '';
      if (backdrop) backdrop.style.opacity = '';
      startY = null;
      currentDelta = 0;
      activeFrom = null;
    }
  };

  const onEnd = () => {
    if (startY === null) return;
    sheet.style.transition = '';
    sheet.style.transform = '';
    if (backdrop) backdrop.style.opacity = '';
    const dt = Date.now() - startTime;
    const velocity = currentDelta / Math.max(dt, 1);
    const shouldClose =
      currentDelta > CLOSE_THRESHOLD ||
      (currentDelta > FAST_CLOSE_THRESHOLD && velocity > FAST_VELOCITY);
    if (shouldClose) closeDaySheet();
    startY = null;
    currentDelta = 0;
    activeFrom = null;
  };

  const bindTouch = (el, from) => {
    el.addEventListener('touchstart', (e) => onStart(e.touches[0].clientY, from), { passive: true });
    el.addEventListener('touchmove',  (e) => onMove(e.touches[0].clientY),  { passive: true });
    el.addEventListener('touchend',   onEnd);
    el.addEventListener('touchcancel', onEnd);
  };

  bindTouch(handleArea, 'handle');
  if (content) bindTouch(content, 'content');

  // 마우스 드래그(데스크톱) — 핸들에서만
  handleArea.addEventListener('mousedown', (e) => {
    onStart(e.clientY, 'handle');
    const move = (ev) => onMove(ev.clientY);
    const up = () => {
      onEnd();
      document.removeEventListener('mousemove', move);
      document.removeEventListener('mouseup', up);
    };
    document.addEventListener('mousemove', move);
    document.addEventListener('mouseup', up);
  });

  // 핸들 단순 탭(클릭) — 드래그 안 했을 때만 닫기
  handleArea.addEventListener('click', () => {
    if (currentDelta < 5) closeDaySheet();
  });

  // 명시적 X 닫기 버튼
  closeBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    closeDaySheet();
  });

  // 백드롭 탭
  backdrop?.addEventListener('click', closeDaySheet);

  // ESC 키 (데스크톱)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sheet.classList.contains('open')) closeDaySheet();
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

  const rows = impacts.map((it) => {
    const tone = it.tone || 'neutral';
    const market = (State.portfolio.us || []).some((s) => s.ticker === it.ticker) ? 'us'
                : (State.portfolio.kr || []).some((s) => s.ticker === it.ticker) ? 'kr'
                : null;
    const heldCls = market ? '' : 'not-held';
    return `
      <button class="si-row ${tone} ${heldCls}" type="button" data-ticker="${escapeHtml(it.ticker)}" ${market ? `data-market="${market}"` : ''}>
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
  const isNotice = !!ev.noticeId;
  const hasMore = !!(ev.impact || ev.ourImpact || (ev.stockImpacts && ev.stockImpacts.length) || isNotice);
  const desc = ev.description || (ev.title && ev.title !== ev.label ? ev.title : '');
  const stockImpactsHtml = renderStockImpacts(ev.stockImpacts);
  const agencyChip = ev.agency ? `<span class="etile-agency ag-${ev.agency.toLowerCase()}">${escapeHtml(ev.agency)}</span>` : '';
  const matchChip = ev.matchScore !== undefined ? `<span class="etile-match">매칭 ${ev.matchScore}%</span>` : '';

  return `
    <div class="etile color-${colorClass} ${hasMore ? 'has-more' : ''}" data-idx="${idx}">
      <div class="etile-body">
        <div class="etile-meta">
          <span class="etile-badge">${meta.icon} ${escapeHtml(meta.kind)}</span>
          ${agencyChip}
          ${matchChip}
          ${ev.time ? `<span class="etile-time">${escapeHtml(ev.time)}</span>` : ''}
        </div>
        <div class="etile-title">${escapeHtml(ev.label || ev.title || '')}</div>
        ${desc ? `<div class="etile-desc">${escapeHtml(desc)}</div>` : ''}

        ${hasMore ? `
          <div class="etile-more">
            ${ev.impact ? `
              <div class="erow">
                <div class="erow-label">💡 자세히</div>
                <div class="erow-text">${escapeHtml(paraBreak(ev.impact))}</div>
              </div>
            ` : ''}
            ${(ev.ourImpact || stockImpactsHtml) ? `
              <div class="erow">
                <div class="erow-label">📌 내 종목엔</div>
                ${ev.ourImpact ? `<div class="erow-text">${escapeHtml(paraBreak(ev.ourImpact))}</div>` : ''}
                ${stockImpactsHtml}
              </div>
            ` : ''}
            ${isNotice ? `
              <button class="etile-detail-btn" type="button" data-notice-id="${escapeHtml(ev.noticeId)}">📋 공고 상세 보기</button>
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
// Lucide 라인 아이콘 (stroke-width 1.6, 모노톤 미니멀)
const DB_ICONS = {
  terms: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>`,
  events: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>`,
  news: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5M10 6h8v4h-8z"/></svg>`,
  signals: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/><path d="M5 3v4M19 17v4M3 5h4M17 19h4"/></svg>`,
  portfolio: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>`,
};

function dbHead(category, title, stat, hasMore) {
  const icon = DB_ICONS[category] || '';
  // C-Plan: chevron은 항상 렌더, .day-box:not(.collapsible) 인 경우만 CSS에서 숨김
  return `
    <button class="db-head-btn" type="button">
      <div class="db-title">
        ${icon ? `<span class="db-title-icon">${icon}</span>` : ''}
        <span class="db-title-text">${escapeHtml(title)}</span>
      </div>
      <div class="db-meta">
        ${stat ? `<span class="db-stat">${escapeHtml(stat)}</span>` : ''}
        <span class="db-chevron" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </span>
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
      <section class="day-box collapsible" data-box="events">
        ${dbHead('events', '오늘의 일정', '이벤트 없음', false)}
        <div class="db-content"><div class="db-empty">큰 이벤트 없는 평범한 날이에요</div></div>
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
    <section class="day-box collapsible" data-box="events">
      ${dbHead('events', '오늘의 일정', stat, hasMore)}
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

// 뉴스 카테고리 자동 분류 (data에 category 필드 있으면 우선)
function detectNewsCategory(n) {
  if (n.category) return n.category;
  const text = ((n.headline || '') + ' ' + (n.summary || '') + ' ' + (n.explain || '')).toLowerCase();
  if (/(fed|fomc|금리|cpi|pce|pmi|nfp|연준|중앙은행|파월|워시|기준금리|통화정책|관세)/i.test(text)) return '정책·금리';
  if (/(이란|중동|호르무즈|러시아|우크라|중국|북한|지정학|유가|wti|opec|전쟁|군사|트럼프)/i.test(text)) return '글로벌·지정학';
  if (/(amd|nvda|nvidia|tsm|googl?|alphabet|meta|amzn|amazon|msft|aapl|apple|tsla|tesla|avgo|broadcom|micron|\bmu\b|mrvl|marvell|sndk|sandisk|dell|lite|lumentum|cls|celestica|crdo|credo|tln|talen|실적|어닝|어닝서프라이즈|분석가|컨센서스|가이던스|상향|하향)/i.test(text)) return '개별 종목';
  if (/(코스피|kospi|nikkei|니케이|항셍|상해|섹터|industrial)/i.test(text)) return '아시아 증시';
  if (/(s&p|sp500|나스닥|nasdaq|다우|dow|vix|러셀|미증시|월스트리트|사상최고|신고가|반도체 섹터|성장주|기술주)/i.test(text)) return '미국 증시';
  return '기타';
}

// 뉴스 지역 분류 (kr | global)
//  - 아시아 증시 카테고리는 기본 국내(한국 관점, 사용자 위치 기준)
//  - 미국 증시·정책·금리는 국제
//  - 개별 종목·글로벌·지정학은 본문에서 한국 키워드 감지하여 분류
function detectNewsRegion(n) {
  const cat = n.category || detectNewsCategory(n);
  if (cat === '아시아 증시') return 'kr';
  if (cat === '미국 증시' || cat === '정책·금리') return 'global';
  const text = ((n.headline || '') + ' ' + (n.summary || '') + ' ' + (n.oneLineSummary || '') + ' ' + (n.ourImpact || '')).toLowerCase();
  if (/(한국|코스피|kospi|원화|sk하이닉스|삼성전자|네이버|카카오|현대차|lg|기아|포스코|한국은행|kosdaq|코스닥)/i.test(text)) return 'kr';
  return 'global';
}

// ── Box 2: 오늘의 핵심 뉴스 (국내/국제 탭 → 카테고리별 그룹, 카테고리당 최대 2개) ──
function renderNewsBox(report) {
  if (!report?.news?.length) return '';

  const news = report.news;
  const LIMIT_PER_CAT = 2;
  const order = ['미국 증시', '아시아 증시', '개별 종목', '정책·금리', '글로벌·지정학', '기타'];

  // 지역별로 먼저 나누고, 그 안에서 카테고리별 그룹 (카테고리당 최대 2)
  const regions = {
    kr: { grouped: {}, all: [] },
    global: { grouped: {}, all: [] },
  };
  news.forEach((n) => {
    const region = detectNewsRegion(n);
    const cat = detectNewsCategory(n);
    regions[region].grouped[cat] = regions[region].grouped[cat] || [];
    if (regions[region].grouped[cat].length < LIMIT_PER_CAT) {
      regions[region].grouped[cat].push(n);
      regions[region].all.push(n);
    }
  });
  const krCount = regions.kr.all.length;
  const globalCount = regions.global.all.length;
  const totalCount = krCount + globalCount;

  const item = (n) => {
    const parsed = parseNewsHeadline(n.headline, n.impact);
    // 새 구조: oneLineSummary(한 줄로) → summary(자세히, 토글) → ourImpact(내 종목엔)
    // 하위호환: oneLineSummary 없으면 summary를 그대로 표시 (옛 보고서)
    const hasOneLine = !!(n.oneLineSummary && n.oneLineSummary.trim());
    const hasSummary = !!(n.summary && n.summary.trim());
    const hasOurImpact = !!(n.ourImpact && n.ourImpact.trim());
    const showDetailToggle = hasOneLine && hasSummary && n.oneLineSummary !== n.summary;
    return `
      <div class="news-item ${parsed.impact}">
        <div class="ni-bar"></div>
        <div class="ni-body">
          <div class="ni-headline">${escapeHtml(parsed.headline)}</div>
          ${hasOneLine ? `
            <div class="ni-oneline">${escapeHtml(paraBreak(n.oneLineSummary))}</div>
          ` : (hasSummary ? `
            <div class="ni-summary">${escapeHtml(paraBreak(n.summary))}</div>
          ` : '')}
          ${showDetailToggle ? `
            <details class="ni-detail">
              <summary>📰 자세히 보기</summary>
              <div class="ni-summary">${escapeHtml(paraBreak(n.summary))}</div>
            </details>
          ` : ''}
          ${hasOurImpact ? `
            <div class="ni-ourimpact"><span class="ni-label">👉 내 종목엔</span> ${escapeHtml(paraBreak(n.ourImpact))}</div>
          ` : ''}
          ${(n.sources && n.sources.length) ? `
            <div class="ni-sources">${n.sources.map((s) => escapeHtml(s.name || '')).filter(Boolean).join(' · ')}</div>
          ` : ''}
        </div>
      </div>
    `;
  };

  // 각 지역 내부 렌더: 헤드라인 1개 + 나머지 카테고리별 그룹
  const renderRegion = (regKey) => {
    const r = regions[regKey];
    if (!r.all.length) {
      return `<div class="region-empty">${regKey === 'kr' ? '오늘 국내 관련 뉴스가 없어요.' : '오늘 국제 관련 뉴스가 없어요.'}</div>`;
    }
    const cats = order.filter((k) => r.grouped[k]?.length);
    const top = r.all[0];
    const topCat = detectNewsCategory(top);
    const restGrouped = {};
    cats.forEach((cat) => { restGrouped[cat] = r.grouped[cat].filter((n) => n !== top); });
    const restCats = cats.filter((cat) => restGrouped[cat].length > 0);
    const restCount = restCats.reduce((sum, cat) => sum + restGrouped[cat].length, 0);
    return `
      <div class="db-headline">
        <div class="db-headline-label">&lt;${escapeHtml(topCat)}&gt; 톱 헤드라인</div>
        ${item(top)}
        ${restCount ? moreHint(`외 ${restCount}건 카테고리별 보기`) : ''}
      </div>
      ${restCount ? `
        <div class="db-content">
          ${restCats.map((cat) => `
            <div class="news-cat">
              <div class="news-cat-label">&lt;${escapeHtml(cat)}&gt;</div>
              <div class="news-list">${restGrouped[cat].map(item).join('')}</div>
            </div>
          `).join('')}
        </div>
      ` : ''}
    `;
  };

  // 더보기 토글 가능 여부: 어느 한쪽 지역이라도 헤드라인 외 1건 이상 더 있으면 ON
  const hasMore = (krCount > 1) || (globalCount > 1);
  // 기본 활성 탭: 컨텐츠 있는 쪽 우선, 둘 다 있으면 국내 (사용자가 한국에 있음)
  const defaultTab = krCount > 0 ? 'kr' : 'global';

  return `
    <section class="day-box collapsible" data-box="news">
      ${dbHead('news', '오늘의 핵심 뉴스', `${totalCount}건`, hasMore)}
      <div class="news-region-tabs">
        <button class="ntab ${defaultTab === 'kr' ? 'active' : ''}" data-tab="kr" ${krCount === 0 ? 'disabled' : ''}>🇰🇷 국내 <span class="ntab-count">${krCount}</span></button>
        <button class="ntab ${defaultTab === 'global' ? 'active' : ''}" data-tab="global" ${globalCount === 0 ? 'disabled' : ''}>🌐 국제 <span class="ntab-count">${globalCount}</span></button>
      </div>
      <div data-tab-content="kr" class="news-region-pane ${defaultTab === 'kr' ? '' : 'hidden'}">
        ${renderRegion('kr')}
      </div>
      <div data-tab-content="global" class="news-region-pane ${defaultTab === 'global' ? '' : 'hidden'}">
        ${renderRegion('global')}
      </div>
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
      <section class="day-box collapsible" data-box="portfolio">
        ${dbHead('portfolio', '내 포트폴리오', '종목 없음', false)}
        <div class="db-content"><div class="db-empty">아직 등록된 종목이 없어요</div></div>
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
          <div class="pr-ticker">
            ${escapeHtml(s.ticker)}
            ${s.dataQualityNote ? `<span class="data-warning" title="${escapeHtml(s.dataQualityNote)}">⚠</span>` : ''}
          </div>
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
      ${dbHead('portfolio', '내 포트폴리오', `미국 ${us.length} · 한국 ${kr.length}`, true)}
      ${headlineHtml}
      <div class="db-content">
        ${renderMarketBlock(us, 'us', '🇺🇸', '미국 주식')}
        ${renderMarketBlock(kr, 'kr', '🇰🇷', '한국 주식')}
      </div>
    </section>
  `;
}

// ── 주식 용어 사전 — 그날 이벤트·뉴스에서 자동 추출용 ──
const GLOSSARY = [
  { term: 'Fed', def: '미국 중앙은행 (Federal Reserve System)', example: '금리 결정 + 통화 정책 관리. 시장이 가장 주시하는 기관.' },
  { term: 'FOMC', def: '미국 연방공개시장위원회 — Fed 안에서 금리를 결정하는 회의', example: '연 8회 열리며 결과가 시장을 크게 흔든다.' },
  { term: '금리', def: '은행이 돈을 빌려줄 때 받는 이자율', example: '금리가 오르면 빚을 많이 쓰는 회사에 부담.' },
  { term: '베타', def: '시장 평균 대비 흔들리는 정도', example: '베타 2 = 시장이 1% 빠지면 그 종목은 2% 빠질 수 있음.' },
  { term: '컨센서스', def: '시장(분석가 평균) 예상치', example: '월가 분석가 30명의 평균 매출·EPS 예상.' },
  { term: 'EBITDA', def: '본업으로 번 돈 (이자·세금·감가상각 차감 전 영업이익)', example: '회사 본질적인 수익성을 보는 지표.' },
  { term: '시간외 거래', def: '미국 정규장(KST 22:30~05:00) 마감 후 추가 거래 시간', example: '실적 발표 직후 큰 변동이 자주 발생.' },
  { term: '어닝 서프라이즈', def: '시장 예상보다 훨씬 좋은 실적', example: 'EPS·매출이 컨센서스를 큰 폭 상회.' },
  { term: '가이던스', def: '회사가 시장에 제시하는 향후 매출·이익 예상치', example: '가이던스 상향 = 회사가 더 자신 있다는 신호.' },
  { term: '파운드리', def: '반도체 위탁 생산 (남의 칩 설계를 받아서 만들어주는 사업)', example: 'TSMC가 대표적. 애플·NVDA·AMD 칩을 모두 생산.' },
  { term: 'TPU', def: '구글이 자체 개발한 AI 칩', example: 'NVDA의 GPU와 경쟁하는 자리.' },
  { term: '인터커넥트', def: '서버 사이를 잇는 고속 통신 부품', example: 'AVGO·MRVL의 핵심 사업 영역.' },
  { term: '비둘기파', def: '금리 인하·통화 완화에 우호적인 입장', example: '비둘기파 발언 → 성장주 호재.' },
  { term: '매파', def: '금리 인상·통화 긴축에 우호적인 입장', example: '매파 발언 → 성장주 부담.' },
  { term: '백로그', def: '이미 수주했지만 아직 매출로 잡히지 않은 주문', example: 'GOOG 클라우드 백로그 460B$ = 향후 매출 가능성.' },
  { term: 'PMI', def: '제조업/서비스업 경기 지수 (50 기준)', example: '50 이상 = 경기 활발, 미만 = 위축.' },
  { term: 'ISM', def: '미국 공급관리자협회 — PMI를 발표하는 기관', example: 'ISM 제조업·ISM 서비스업 두 가지가 핵심.' },
  { term: 'NFP', def: '미국 비농업 신규 고용 (월간 일자리 수 발표)', example: '시장이 가장 주시하는 고용 지표.' },
  { term: 'PCE', def: 'Fed가 가장 신뢰하는 미국 물가 지표', example: '적정 수준 2%, 높을수록 인플레.' },
  { term: 'CPI', def: '소비자물가지수 (미국 인플레 측정)', example: 'PCE보다 자주 발표되어 시장이 민감.' },
  { term: 'VIX', def: '시장 변동성 지수 (공포 지수)', example: '20 이하 안정, 30 이상 불안.' },
  { term: 'WTI', def: '서부텍사스산 원유 — 미국 대표 유가', example: '유가가 오르면 인플레 압력 ↑.' },
  { term: '프리마켓', def: '미국 정규장 직전 거래 시간 (KST 17:00~22:30)', example: '실적 영향이 미리 반영되는 시간.' },
  { term: '신고가', def: '사상 최고가 갱신', example: '강한 상승 흐름 신호.' },
  { term: '분할매수', def: '한 번에 사지 않고 시간을 두고 나눠서 매수', example: '평균 단가를 안정적으로 만드는 전략.' },
  { term: 'YoY', def: '전년 동기 대비 (Year over Year)', example: '매출 +57% YoY = 1년 전보다 57% 성장.' },
  { term: 'EPS', def: '주당 순이익 (Earnings Per Share)', example: '순이익을 발행 주식 수로 나눈 값.' },
  { term: 'CapEx', def: '설비 투자 (장비·시설에 쓰는 돈)', example: '메타 145B$ CapEx = AI 인프라에 1,450억$ 투입.' },
  { term: '빅테크', def: '미국 대형 기술 기업 (GOOG·META·AMZN·MSFT 등)', example: 'AI·클라우드 시대 핵심 그룹.' },
  { term: 'AI 인프라', def: 'AI 학습·서비스에 필요한 서버·전력·통신 시설', example: 'DELL·LITE·CLS·CRDO 등이 해당.' },
  { term: 'GPU', def: '그래픽 처리 장치 — AI 학습에 핵심 부품', example: 'NVDA가 절대 강자, AMD가 경쟁 시작.' },
  { term: 'ASIC', def: '특정 용도에 맞춤 설계된 반도체', example: 'AVGO·MRVL이 빅테크에 맞춤 칩 공급.' },
  { term: '인플레', def: '물가 상승 (Inflation)', example: '월급 그대로인데 물건값 오르면 실질 구매력 하락.' },
  { term: '인플레이션', def: '물가 상승 (Inflation)', example: '월급 그대로인데 물건값 오르면 실질 구매력 하락.' },
  { term: '디플레', def: '물가 하락 (Deflation)', example: '오히려 경기 침체 신호.' },
  { term: '컨퍼런스 콜', def: '실적 발표 후 분석가·투자자와 회사 경영진의 전화 회의', example: '추가 가이던스·정보가 여기서 나옴.' },
  { term: '단위노동비용', def: '기업이 한 단위 생산하는 데 드는 인건비', example: '오르면 인플레 압력, 내리면 완화.' },
  { term: '실업청구건수', def: '주간 신규 실업수당 신청 수', example: '많아지면 고용 둔화 신호.' },
  { term: '신호등', def: 'Mobri의 종목 위험도 표시 — 🟢 안전 / 🟡 주의 / 🔴 위험', example: '베타·최근 변동성·신호를 종합해서 판단.' },
  { term: '모멘텀', def: '주가가 한 방향으로 계속 움직이는 힘', example: '상승 모멘텀 = 추세 지속, 약화되면 조정 가능.' },
  { term: '광통신', def: '빛으로 데이터를 전송하는 기술', example: 'LITE가 데이터센터 광통신 부품을 만듦.' },
  { term: '클라우드', def: '인터넷으로 빌려 쓰는 컴퓨팅·저장 자원', example: 'AWS(아마존)·구글 클라우드·애저(MS) 3대 강자.' },
];

function extractTodayTerms(events, news) {
  const texts = [];
  (events || []).forEach((e) => {
    [e.label, e.title, e.description, e.impact, e.ourImpact].forEach((t) => t && texts.push(t));
    (e.stockImpacts || []).forEach((s) => s.text && texts.push(s.text));
  });
  (news || []).forEach((n) => {
    [n.headline, n.summary, n.explain].forEach((t) => t && texts.push(t));
  });
  const all = texts.join(' ');
  if (!all) return [];

  const found = [];
  const seen = new Set();
  GLOSSARY.forEach((g) => {
    if (seen.has(g.term)) return;
    let pattern;
    if (/^[A-Za-z]+$/.test(g.term)) {
      pattern = new RegExp('\\b' + g.term + '\\b', 'g');
    } else {
      pattern = new RegExp(g.term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    }
    const count = (all.match(pattern) || []).length;
    if (count > 0) {
      found.push({ ...g, count });
      seen.add(g.term);
    }
  });
  return found.sort((a, b) => b.count - a.count);
}

// ── Box 1: 오늘의 학습 (그날 이벤트·뉴스에서 자동 추출, 최대 5개) ──
const TERMS_LIMIT = 5;

function renderTermsBox(report, dayEvents) {
  const auto = extractTodayTerms(dayEvents, report?.news);

  // 큐레이션된 용어는 자동 추출 결과를 보강(example을 더 풍부하게)하는 데만 사용
  const curatedMap = new Map();
  (report?.terms || []).forEach((t) => {
    curatedMap.set((t.term || '').toLowerCase(), t);
  });

  // 오늘 본문에 등장한 용어만, 큐레이션이 있으면 example 보강 — 빈도순 상위 5개
  const enriched = auto.slice(0, TERMS_LIMIT).map((t) => {
    const c = curatedMap.get(t.term.toLowerCase());
    return {
      term: t.term,
      definition: c?.definition || t.def,
      example: c?.example || t.example,
      count: t.count,
    };
  });

  // 등장 용어가 0개면 큐레이션 fallback (얘도 5개로 제한)
  const allTerms = enriched.length > 0
    ? enriched
    : (report?.terms || []).slice(0, TERMS_LIMIT).map((t) => ({ ...t }));

  if (!allTerms.length && !report?.tip) return '';

  const renderTerm = (t) => `
    <div class="term-card-v2">
      <div class="tc-term">
        <span>${escapeHtml(t.term)}</span>
        ${t.count ? `<span class="tc-count">오늘 ${t.count}회 언급</span>` : ''}
      </div>
      <div class="tc-def">${escapeHtml(paraBreak(t.definition || t.def || ''))}</div>
      ${t.example ? `<div class="tc-ex">${escapeHtml(t.example)}</div>` : ''}
    </div>
  `;

  const top = allTerms[0];
  const rest = allTerms.slice(1);
  const hasMore = rest.length > 0 || !!report?.tip;
  const stat = allTerms.length ? `${allTerms.length}개 용어` : '';

  return `
    <section class="day-box collapsible" data-box="terms">
      ${dbHead('terms', '오늘의 학습', stat, hasMore)}
      ${top ? `
        <div class="db-headline">
          <div class="db-headline-label">📖 오늘 등장한 용어</div>
          ${renderTerm(top)}
          ${hasMore ? moreHint(`나머지 ${rest.length}개 용어${report?.tip ? ' + 팁' : ''} 보기`) : ''}
        </div>
      ` : ''}
      ${hasMore ? `
        <div class="db-content">
          ${rest.length ? `
            <div class="terms-list">
              ${rest.map(renderTerm).join('')}
            </div>
          ` : ''}
          ${report?.tip ? `<div class="tip-box-v2">💡 ${escapeHtml(report.tip)}</div>` : ''}
        </div>
      ` : ''}
    </section>
  `;
}

// 시트 상단에 보일 날짜 라벨 (드래그 핸들 옆)
function dayPanelHeader() {
  return `
    <div class="ds-date-label">${formatKoreanDate(State.selectedDate)}</div>
  `;
}

async function renderSelectedDayPanel() {
  const panel = $('#selectedDayPanel');
  if (!panel) return;

  const dayEvents = (State.calendarEvents[State.calMode] || {})[State.selectedDate] || [];

  // ── 부동산 모드 ──
  if (State.calMode === 'realestate') {
    panel.innerHTML = `
      ${dayPanelHeader()}
      <div class="day-panel">
        ${renderEventsBox(dayEvents)}
      </div>
    `;
    attachBoxCollapseHandlers();
    attachEventTileHandlers();
    return;
  }

  // ── 주식 모드: 4박스 ──
  const report = await loadReport(State.selectedDate);

  panel.innerHTML = `
    ${dayPanelHeader()}
    <div class="day-panel">
      ${renderTermsBox(report, dayEvents)}
      ${renderEventsBox(dayEvents)}
      ${renderNewsBox(report)}
      ${renderSignalsBox(report)}
      ${renderPortfolioBox()}
    </div>
  `;

  attachBoxCollapseHandlers();
  attachEventTileHandlers();
  attachPortfolioRowHandlers();
  attachNewsTabHandlers();
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
  // 공고 상세 보기 버튼 (펼침 토글은 막음)
  $$('.etile-detail-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      openNoticeDetail(btn.dataset.noticeId);
    });
  });
}

// ── 공고 상세 모달 ──
function openNoticeDetail(noticeId) {
  const notice = (State.realEstate?.notices || []).find(n => n.id === noticeId);
  if (!notice) return;

  const today = TODAY_KST;
  const dDay = (() => {
    if (!notice.applicationEnd || notice.rolling) return null;
    const diff = Math.floor((new Date(notice.applicationEnd) - new Date(today)) / 86400000);
    if (diff < 0) return '마감';
    if (diff === 0) return 'D-day';
    return `D-${diff}`;
  })();

  const score = matchNoticeToFilter(notice, State.realEstateFilter);
  const priority = computeUserPriority(notice, State.realEstateFilter);
  const priBadge = getPriorityBadge(priority);

  const html = `
    <div class="notice-detail">
      <div class="nd-head">
        <div class="nd-chips">
          <span class="nd-agency ag-${notice.agency.toLowerCase()}">${escapeHtml(notice.agency)}</span>
          <span class="nd-type">${escapeHtml(notice.type)}</span>
          ${dDay ? `<span class="nd-dday ${dDay === 'D-day' ? 'urgent' : ''}">${dDay}</span>` : ''}
          ${notice.rolling ? `<span class="nd-rolling">수시모집</span>` : ''}
          ${priBadge ? `<span class="nd-priority ${priBadge.cls}">${priBadge.icon} ${escapeHtml(priBadge.text)}</span>` : ''}
        </div>
        <h2>${escapeHtml(notice.title)}</h2>
        ${score < 100 ? `<div class="nd-match-bar"><span class="nd-match-fill" style="width:${score}%"></span><span class="nd-match-text">내 조건 매칭 ${score}%</span></div>` : ''}
      </div>

      ${notice.priorityRules?.length ? `
        <div class="nd-priority-section">
          <div class="nd-section-title">📊 내 순위 분석</div>
          ${priority ? `
            <div class="nd-pri-result ${priBadge?.cls || ''}">
              <div class="nd-pri-rank">${priBadge?.icon || ''} ${escapeHtml(priority.rank)}</div>
              <div class="nd-pri-label">${escapeHtml(priority.label)}</div>
              ${priority.hint ? `<div class="nd-pri-hint">💡 ${escapeHtml(priority.hint)}</div>` : ''}
              ${priority.confidence === 'low' ? `<div class="nd-pri-warn">⚠ 맞춤설정 정보가 부족해 정확도가 낮습니다. 🎯 내 맞춤 설정에서 추가 입력해 주세요.</div>` : ''}
            </div>
          ` : ''}
          <div class="nd-pri-rules">
            <div class="nd-pri-rules-title">전체 순위 기준</div>
            ${notice.priorityRules.map(rule => `
              <div class="nd-pri-rule">
                <span class="nd-pri-rule-rank">${escapeHtml(rule.rank)}</span>
                <span class="nd-pri-rule-label">${escapeHtml(rule.label)}</span>
              </div>
            `).join('')}
          </div>
        </div>
      ` : ''}

      <div class="nd-info-grid">
        <div class="nd-info-row">
          <span class="nd-info-label">📅 접수기간</span>
          <span class="nd-info-val">
            ${notice.applicationStart ? formatKoreanDate(notice.applicationStart) : '—'}
            ${notice.applicationEnd && notice.applicationEnd !== notice.applicationStart ? ' ~ ' + formatKoreanDate(notice.applicationEnd) : ''}
            ${notice.rolling ? ' (수시)' : ''}
          </span>
        </div>
        ${notice.announcementDate ? `
          <div class="nd-info-row">
            <span class="nd-info-label">📢 공고일</span>
            <span class="nd-info-val">${formatKoreanDate(notice.announcementDate)}</span>
          </div>
        ` : ''}
        ${notice.supplyCount ? `
          <div class="nd-info-row">
            <span class="nd-info-label">🏠 공급세대</span>
            <span class="nd-info-val">${notice.supplyCount.toLocaleString()}세대</span>
          </div>
        ` : ''}
        ${notice.region?.length ? `
          <div class="nd-info-row">
            <span class="nd-info-label">📍 지역</span>
            <span class="nd-info-val">${notice.region.join(' · ')}</span>
          </div>
        ` : ''}
        ${notice.districts?.length ? `
          <div class="nd-info-row">
            <span class="nd-info-label">🗺 세부지역</span>
            <span class="nd-info-val">${notice.districts.join(', ')}</span>
          </div>
        ` : ''}
        ${notice.ageRange ? `
          <div class="nd-info-row">
            <span class="nd-info-label">👤 연령</span>
            <span class="nd-info-val">만 ${notice.ageRange[0]}~${notice.ageRange[1]}세</span>
          </div>
        ` : ''}
        ${notice.maritalRequired ? `
          <div class="nd-info-row">
            <span class="nd-info-label">💑 혼인</span>
            <span class="nd-info-val">혼인 ${notice.marriedYears || 7}년 이내 (예비신혼 포함)</span>
          </div>
        ` : ''}
        ${notice.maritalForbidden ? `
          <div class="nd-info-row">
            <span class="nd-info-label">💑 결혼상태</span>
            <span class="nd-info-val">미혼만 가능</span>
          </div>
        ` : ''}
        ${notice.applyMethod ? `
          <div class="nd-info-row">
            <span class="nd-info-label">📝 신청방법</span>
            <span class="nd-info-val">${escapeHtml(notice.applyMethod)}</span>
          </div>
        ` : ''}
      </div>

      ${notice.highlights?.length ? `
        <div class="nd-highlights">
          <div class="nd-section-title">✨ 특징</div>
          <ul>${notice.highlights.map(h => `<li>${escapeHtml(h)}</li>`).join('')}</ul>
        </div>
      ` : ''}

      ${notice.uncertain ? `
        <div class="nd-warning">⚠️ 일부 정보는 공고문 원본에서 최종 확인하세요.</div>
      ` : ''}

      <div class="modal-actions">
        <button class="btn" onclick="closeModal()">닫기</button>
        ${notice.url ? `<a class="btn primary" href="${escapeHtml(notice.url)}" target="_blank" rel="noopener">🔗 공고문 원본 열기</a>` : ''}
      </div>
    </div>
  `;
  showModal(html);
}
window.openNoticeDetail = openNoticeDetail;

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
        ${report.news.map((n) => {
          const hasOneLine = !!(n.oneLineSummary && n.oneLineSummary.trim());
          const hasSummary = !!(n.summary && n.summary.trim());
          const hasOurImpact = !!(n.ourImpact && n.ourImpact.trim());
          const showDetailToggle = hasOneLine && hasSummary && n.oneLineSummary !== n.summary;
          return `
          <div class="news-detail ${n.impact || 'neutral'}">
            ${n.category ? `<div class="cat">&lt;${escapeHtml(n.category)}&gt;</div>` : ''}
            <div class="h">${escapeHtml(n.headline || '')}</div>
            ${hasOneLine ? `
              <div class="oneline">${escapeHtml(paraBreak(n.oneLineSummary))}</div>
            ` : (hasSummary ? `
              <div class="s">${escapeHtml(paraBreak(n.summary))}</div>
            ` : '')}
            ${showDetailToggle ? `
              <details class="detail">
                <summary>📰 자세히 보기</summary>
                <div class="s">${escapeHtml(paraBreak(n.summary))}</div>
              </details>
            ` : ''}
            ${hasOurImpact ? `
              <div class="ourimpact"><span class="label">👉 내 종목엔</span> ${escapeHtml(paraBreak(n.ourImpact))}</div>
            ` : ''}
            ${n.explain ? `<div class="e">${escapeHtml(n.explain)}</div>` : ''}
            <div class="sources">
              ${(n.sources || []).map((s) => `<a href="${escapeHtml(s.url || '')}" target="_blank" rel="noopener">· ${escapeHtml(s.name || '')}</a>`).join('')}
            </div>
          </div>
          `;
        }).join('')}
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

    <div class="refresh-bar">
      <div class="last-updated">
        <span class="live-dot"></span>
        <span class="last-updated-text">갱신 중...</span>
      </div>
      <button class="refresh-btn" id="refreshBtnPort">
        <span class="ico">↻</span>
        <span>새로고침</span>
      </button>
    </div>

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

  $('#refreshBtnPort')?.addEventListener('click', async () => {
    const btn = $('#refreshBtnPort');
    btn.classList.add('refreshing');
    await refreshAllData();
    btn.classList.remove('refreshing');
  });

  // 갱신 시간 즉시 + 1분마다
  updateLastUpdatedDisplay();
  if (window._timeAgoTimer) clearInterval(window._timeAgoTimer);
  window._timeAgoTimer = setInterval(updateLastUpdatedDisplay, 60000);

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
            <div class="ticker">
              ${escapeHtml(it.ticker)}
              ${it.dataQualityNote ? `<span class="data-warning" title="${escapeHtml(it.dataQualityNote)}">⚠</span>` : ''}
            </div>
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
  const symbol = market === 'us' ? '$' : '';
  const priceUnit = market === 'kr' ? '원' : '';
  const price = it.price ? it.price.toLocaleString() : '—';
  const chartImgUrl = naverChartUrl(it.ticker, market);
  const chartFallbacks = naverChartFallbackChain(it.ticker, market);
  const chartOnerrorAttr = chartFallbacks.length
    ? `onerror="if(this.dataset.fbi===undefined)this.dataset.fbi='0';else this.dataset.fbi=String(parseInt(this.dataset.fbi)+1);const fbs=${JSON.stringify(chartFallbacks).replace(/"/g, '&quot;')};const i=parseInt(this.dataset.fbi);if(i<fbs.length){this.src=fbs[i];}else{this.onerror=null;this.style.display='none';this.parentElement.classList.add('chart-img-failed');}"`
    : `onerror="this.onerror=null;this.style.display='none';this.parentElement.classList.add('chart-img-failed');"`;

  const html = `
    <div class="stock-detail">
      <div class="stock-head">
        <div class="row-between">
          <div>
            <div class="t-ticker">${escapeHtml(it.ticker)} <span class="dot ${it.signal || 'gray'}" style="display:inline-block; vertical-align:middle; margin-left:4px;"></span></div>
            <div class="t-name">${escapeHtml(it.name || '')} · ${escapeHtml(it.sector || '')}</div>
          </div>
          <div class="t-price-block">
            <div class="t-price">${symbol}${price}${priceUnit}</div>
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

        <div class="stock-detail-chart-wrap">
          <img class="stock-detail-chart" src="${chartImgUrl}" alt="${escapeHtml(it.ticker)} 3개월 차트" loading="lazy" ${chartOnerrorAttr}>
          <div class="chart-img-fail-msg">차트 불러오기 실패</div>
          <div class="chart-period-tag">최근 3개월 · 네이버 금융</div>
        </div>
      </div>

      ${it.dataQualityNote ? `
        <div class="data-quality-banner">
          <span class="dq-icon">⚠</span>
          <div class="dq-body">
            <div class="dq-title">데이터 정확도 경고</div>
            <div class="dq-text">${escapeHtml(it.dataQualityNote)}</div>
          </div>
        </div>
      ` : ''}

      ${(it.priceSourcedFrom && it.priceSourcedFrom.length) ? `
        <div class="price-sources">출처: ${it.priceSourcedFrom.map((s) => escapeHtml(s)).join(' · ')}</div>
      ` : ''}

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

      ${it.outlookEasy ? `
        <div class="sd-card sd-card-outlook">
          <div class="sd-card-title">🔮 앞으로 어떻게 될까? <span class="sd-card-sub">(쉬운 설명)</span></div>
          <div class="sd-outlook-easy">${escapeHtml(paraBreak(it.outlookEasy))}</div>
        </div>
      ` : ''}

      ${it.company ? `
        <div class="sd-card">
          <div class="sd-card-title">🏢 회사 정보</div>
          <div class="sd-company">
            ${it.company.business ? `<div class="sd-co-row"><span class="sd-co-lbl">사업</span><span class="sd-co-val">${escapeHtml(it.company.business)}</span></div>` : ''}
            ${it.company.ceo ? `<div class="sd-co-row"><span class="sd-co-lbl">대표</span><span class="sd-co-val">${escapeHtml(it.company.ceo)}</span></div>` : ''}
            ${it.company.hq ? `<div class="sd-co-row"><span class="sd-co-lbl">본사</span><span class="sd-co-val">${escapeHtml(it.company.hq)}</span></div>` : ''}
            ${it.company.employees ? `<div class="sd-co-row"><span class="sd-co-lbl">직원</span><span class="sd-co-val">${escapeHtml(it.company.employees)}</span></div>` : ''}
            ${it.company.homepage ? `<div class="sd-co-row"><span class="sd-co-lbl">홈페이지</span><span class="sd-co-val"><a href="${escapeHtml(it.company.homepage)}" target="_blank" rel="noopener">${escapeHtml(it.company.homepage)}</a></span></div>` : ''}
            ${it.company.ceoSource ? `<div class="sd-co-source">출처: ${escapeHtml(it.company.ceoSource)}</div>` : ''}
          </div>
        </div>
      ` : ''}

      ${(it.recentNews && it.recentNews.length) ? `
        <div class="sd-card">
          <div class="sd-card-title">📰 최근 뉴스 <span class="sd-card-sub">(매일 08:00 갱신)</span></div>
          ${it.recentNews.map((n) => `
            <div class="stock-news" style="background: transparent; padding: 8px 0; margin: 0; border-bottom: 0.5px solid var(--border);">
              <div class="sn-h">${escapeHtml(n.headline)}</div>
              ${n.easySummary ? `<div class="sn-easy">💬 ${escapeHtml(n.easySummary)}</div>` : ''}
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
      <div class="meta">최근 3개월 · 네이버 금융 실시간</div>
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

// 네이버 금융 종목별 suffix 매핑 — 정확히 알려진 케이스
// '' = base ticker (no suffix), '.K' = NYSE/AMEX 일부, '.O' = NASDAQ 기본
const NAVER_SUFFIX_OVERRIDE = {
  // NYSE — base ticker
  'TSM': '', 'CLS': '', 'NU': '', 'BABA': '',
  // NYSE — .K suffix
  'DELL': '.K', 'ORCL': '.K',
};

// 종목 차트 이미지 URL — 네이버 금융 3개월 영역 차트
function naverChartUrl(ticker, market) {
  const bucket = Math.floor(Date.now() / 600000); // 10분 단위 캐시 무효화
  if (market === 'kr') {
    return `https://ssl.pstatic.net/imgfinance/chart/mobile/area/month3/${ticker}_end.png?t=${bucket}`;
  }
  // 미국: 매핑에 명시된 suffix → 없으면 NASDAQ 기본 .O
  const suffix = ticker in NAVER_SUFFIX_OVERRIDE ? NAVER_SUFFIX_OVERRIDE[ticker] : '.O';
  return `https://ssl.pstatic.net/imgfinance/chart/mobile/world/item/area/month3/${ticker}${suffix}_end.png?t=${bucket}`;
}

// 폴백 체인 — 첫 URL이 404일 때 시도할 대안들
function naverChartFallbackChain(ticker, market) {
  if (market === 'kr') return [];
  const primary = ticker in NAVER_SUFFIX_OVERRIDE ? NAVER_SUFFIX_OVERRIDE[ticker] : '.O';
  const candidates = ['.O', '', '.K', '.N'];
  return candidates
    .filter((s) => s !== primary)
    .map((s) => `https://ssl.pstatic.net/imgfinance/chart/mobile/world/item/area/month3/${ticker}${s}_end.png`);
}

// 가격 포맷 — 시장에 맞게 통화 단위
function fmtStockPrice(price, market) {
  if (price == null) return '—';
  if (market === 'kr') return `${price.toLocaleString()}원`;
  return `$${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function renderThumbChart(id, item) {
  const containerId = id.startsWith('us-') ? 'usCharts' : 'krCharts';
  const container = document.getElementById(containerId);
  if (!container) return;

  const market = id.startsWith('us-') ? 'us' : 'kr';
  const div = document.createElement('div');
  div.className = 'chart-thumb';
  div.dataset.ticker = item.ticker;
  div.dataset.market = market;
  const change = item.change1M ?? 0;
  const changeColor = change > 0 ? 'var(--positive)' : change < 0 ? 'var(--negative)' : 'var(--text-tertiary)';

  const chartUrl = naverChartUrl(item.ticker, market);
  const fallbacks = naverChartFallbackChain(item.ticker, market);
  const onerrorAttr = fallbacks.length
    ? `onerror="if(this.dataset.fbi===undefined)this.dataset.fbi='0';else this.dataset.fbi=String(parseInt(this.dataset.fbi)+1);const fbs=${JSON.stringify(fallbacks)};const i=parseInt(this.dataset.fbi);if(i<fbs.length){this.src=fbs[i];}else{this.onerror=null;this.style.display='none';this.parentElement.classList.add('chart-img-failed');}"`
    : `onerror="this.onerror=null;this.style.display='none';this.parentElement.classList.add('chart-img-failed');"`;

  div.innerHTML = `
    <div class="head">
      <div class="ticker">${escapeHtml(item.ticker)}</div>
      <div class="change" style="color: ${changeColor}">${pct(change)}</div>
    </div>
    <div class="chart-img-wrap">
      <img class="chart-img" src="${chartUrl}" alt="${escapeHtml(item.ticker)} 3개월 차트" loading="lazy" ${onerrorAttr}>
      <div class="chart-img-fail-msg">차트 불러오기 실패</div>
    </div>
    <div class="price">${fmtStockPrice(item.price, market)}</div>
  `;
  container.appendChild(div);
}

// ------------- 부동산 탭 (캘린더 위주 개편) -------------
function renderRealEstate(app) {
  const re = State.realEstate || { notices: [], userMemos: [] };
  const today = TODAY_KST;

  // 마감 임박 순으로 정렬된 매칭 공고
  const matchedNotices = filteredOpenNotices();
  const memos = re.userMemos || [];

  // D-day 카운트
  const dDayCount = matchedNotices.filter(n => n.applicationEnd === today && !n.rolling).length;
  const upcomingCount = matchedNotices.filter(n => n.applicationStart > today).length;
  const openCount = matchedNotices.filter(n => {
    return (!n.applicationStart || n.applicationStart <= today) &&
           (!n.applicationEnd || n.applicationEnd >= today);
  }).length;

  app.innerHTML = `
    <header class="app-header">
      <div class="meta">청약 · 임대 · 전세임대</div>
      <h1>부동산 공고</h1>
    </header>

    ${renderCustomFilterBar()}

    <div class="re-stats">
      <div class="re-stat ${dDayCount ? 'urgent' : ''}">
        <div class="re-stat-num">${dDayCount}</div>
        <div class="re-stat-label">⏰ 오늘 마감</div>
      </div>
      <div class="re-stat">
        <div class="re-stat-num">${openCount}</div>
        <div class="re-stat-label">📋 접수 중</div>
      </div>
      <div class="re-stat">
        <div class="re-stat-num">${upcomingCount}</div>
        <div class="re-stat-label">🔜 곧 시작</div>
      </div>
    </div>

    <div class="section">
      <div class="re-list-head">
        <div class="re-list-title">📌 진행 중인 공고 <span class="re-list-count">${matchedNotices.length}건</span></div>
        <div class="re-list-sort">마감 임박순</div>
      </div>

      ${matchedNotices.length === 0 ? `
        <div class="re-empty">
          <div class="re-empty-icon">🔍</div>
          <div class="re-empty-title">조건에 맞는 공고가 없어요</div>
          <div class="re-empty-sub">맞춤 설정을 다시 조정해보세요</div>
        </div>
      ` : matchedNotices.map(n => renderNoticeCard(n, today)).join('')}
    </div>

    <div class="section">
      <div class="re-list-head">
        <div class="re-list-title">📝 내 메모 <span class="re-list-count">${memos.length}건</span></div>
        <button class="re-add-memo-btn" id="reAddMemoBtn">+ 메모 추가</button>
      </div>
      ${memos.length === 0 ? `
        <div class="re-empty subtle">
          <div class="re-empty-sub">관심 매물·공고를 직접 메모해두세요</div>
        </div>
      ` : memos.map((m, i) => `
        <div class="card re-memo-card" data-idx="${i}">
          <div style="font-size: 13px; font-weight: 500; margin-bottom: 4px;">${escapeHtml(m.title)}</div>
          <div style="font-size: 11px; color: var(--text-tertiary);">${escapeHtml(m.date || '')} ${m.summary ? ' · ' + escapeHtml(m.summary) : ''}</div>
        </div>
      `).join('')}
    </div>

    <div class="re-tip">
      💡 더 자세한 월간 캘린더 뷰는 <b>캘린더 탭 → 부동산 토글</b>에서 보세요
    </div>
  `;

  // 맞춤설정 작은줄
  $('#reCustomBar')?.addEventListener('click', openRealEstateFilterSheet);

  // 공고 카드 클릭 → 상세 모달
  $$('.notice-card').forEach((card) => {
    card.addEventListener('click', () => openNoticeDetail(card.dataset.noticeId));
  });

  // 메모 추가
  $('#reAddMemoBtn')?.addEventListener('click', openAddMemoModal);
}

// 진행 중 공고 카드
function renderNoticeCard(n, today) {
  const dDay = (() => {
    if (n.rolling) return { text: '수시', cls: 'rolling' };
    if (!n.applicationEnd) return null;
    const diff = Math.floor((new Date(n.applicationEnd) - new Date(today)) / 86400000);
    if (diff < 0) return null;
    if (diff === 0) return { text: 'D-day', cls: 'dday' };
    if (diff <= 3) return { text: `D-${diff}`, cls: 'soon' };
    return { text: `D-${diff}`, cls: '' };
  })();

  const isUpcoming = n.applicationStart > today;
  const score = matchNoticeToFilter(n, State.realEstateFilter);
  const priority = computeUserPriority(n, State.realEstateFilter);
  const priBadge = getPriorityBadge(priority);

  return `
    <div class="card notice-card" data-notice-id="${escapeHtml(n.id)}">
      <div class="nc-top">
        <span class="nc-agency ag-${n.agency.toLowerCase()}">${escapeHtml(n.agency)}</span>
        <span class="nc-type">${escapeHtml(n.type)}</span>
        ${dDay ? `<span class="nc-dday ${dDay.cls}">${escapeHtml(dDay.text)}</span>` : ''}
        ${isUpcoming ? `<span class="nc-upcoming">곧 시작</span>` : ''}
        ${priBadge ? `<span class="nc-priority ${priBadge.cls}">${priBadge.icon} ${escapeHtml(priBadge.text)}</span>` : ''}
        ${score < 100 && score >= 50 ? `<span class="nc-match">매칭 ${score}%</span>` : ''}
      </div>
      <div class="nc-title">${escapeHtml(n.shortTitle || n.title)}</div>
      <div class="nc-meta">
        📅 ${n.applicationStart ? formatShortDate(n.applicationStart) : '—'}${n.applicationEnd && n.applicationEnd !== n.applicationStart ? ' ~ ' + formatShortDate(n.applicationEnd) : ''}${n.rolling ? ' (수시)' : ''}
        ${n.supplyCount ? ` · 🏠 ${n.supplyCount.toLocaleString()}세대` : ''}
        ${n.region?.length ? ` · 📍 ${n.region.join('·')}` : ''}
      </div>
      ${priority && priority.confidence === 'high' && priority.label ? `<div class="nc-pri-detail">→ ${escapeHtml(priority.label)}</div>` : ''}
      ${n.highlights?.length ? `<div class="nc-highlight">${escapeHtml(n.highlights[0])}</div>` : ''}
    </div>
  `;
}

// 메모 추가 모달
function openAddMemoModal() {
  const html = `
    <h2>📝 메모 추가</h2>
    <div class="field">
      <label>제목</label>
      <input type="text" id="memoTitle" placeholder="예: 강남구 OO아파트 1순위" />
    </div>
    <div class="field">
      <label>날짜</label>
      <input type="date" id="memoDate" value="${State.todayDate}" />
    </div>
    <div class="field">
      <label>요약 (선택)</label>
      <input type="text" id="memoSummary" placeholder="간단한 메모" />
    </div>
    <div class="modal-actions">
      <button class="btn" onclick="closeModal()">취소</button>
      <button class="btn primary" id="confirmMemoAdd">추가</button>
    </div>
  `;
  showModal(html);

  $('#confirmMemoAdd').addEventListener('click', () => {
    const title = $('#memoTitle').value.trim();
    const date = $('#memoDate').value;
    const summary = $('#memoSummary').value.trim();
    if (!title) { alert('제목은 필수입니다'); return; }

    State.realEstate.userMemos = State.realEstate.userMemos || [];
    State.realEstate.userMemos.unshift({ title, date, summary, createdAt: new Date().toISOString() });

    localStorage.setItem(STORAGE_KEYS.realEstate, JSON.stringify(State.realEstate));
    closeModal();
    render();
  });
}

// 짧은 날짜 포맷 (5/6)
function formatShortDate(dateStr) {
  if (!dateStr) return '';
  const parts = dateStr.split('-');
  if (parts.length !== 3) return dateStr;
  return `${parseInt(parts[1])}/${parseInt(parts[2])}`;
}

// ── Box 5: 🎯 오늘의 추천 (캘린더 바텀시트 내부) ──
function renderSignalsBox(report) {
  const signals = report?.signals;
  if (!signals) return '';
  const kr = signals.kr || [];
  const us = signals.us || [];
  const krFlow = signals.krForeignFlow;
  const newListings = signals.newListings || null;
  const newKr = newListings?.kr || [];
  const newUs = newListings?.us || [];
  if (!kr.length && !us.length && !newKr.length && !newUs.length) return '';

  const defaultTab = kr.length ? 'kr' : 'us';
  const totalCount = kr.length + us.length;

  // 🌍 외국인 동향 패널 (국내 탭에만) — 그룹핑된 간단 카드 뷰
  const renderForeignFlow = () => {
    if (!krFlow || !krFlow.rows?.length) return '';

    const fmtShares = (n) => {
      const sign = n >= 0 ? '+' : '';
      const abs = Math.abs(n);
      if (abs >= 10000) return `${sign}${(n / 10000).toFixed(1)}만 주`;
      return `${sign}${n.toLocaleString()}주`;
    };

    // 종목별 한 줄 요약 작성
    const summarize = (r) => {
      const last = r.dailyNetBuy[r.dailyNetBuy.length - 1];
      const lastStr = fmtShares(last.shares);
      const totalStr = fmtShares(r.netBuy5d);
      if (r.trendTone === 'positive') {
        return `어제 ${lastStr} 매수로 돌아섰어요 (5일 합계 ${totalStr})`;
      }
      if (r.trendTone === 'negative') {
        // 연속 매도일수
        const seq = [];
        for (let i = r.dailyNetBuy.length - 1; i >= 0; i--) {
          if (r.dailyNetBuy[i].shares < 0) seq.push(i);
          else break;
        }
        const n = seq.length;
        if (n >= 2) return `${n}일 연속 매도 중 (5일 합계 ${totalStr})`;
        return `어제 ${lastStr} 매도 (5일 합계 ${totalStr})`;
      }
      return `5일 합계 ${totalStr} — 거의 중립`;
    };

    // 그룹: 매수 전환/매수 (positive) vs 매도 (negative) vs 중립
    const buying = krFlow.rows.filter((r) => r.trendTone === 'positive');
    const selling = krFlow.rows.filter((r) => r.trendTone === 'negative');
    const neutral = krFlow.rows.filter((r) => r.trendTone === 'neutral');

    // 한 줄 결론 자동 생성
    const conclusion = (() => {
      if (buying.length >= 3 && selling.length <= 1) {
        return `${buying.length}종목이 매수로 돌아섰어요 — 외국인이 다시 사기 시작하는 분위기`;
      }
      if (selling.length >= 3 && buying.length <= 1) {
        return `${selling.length}종목 매도세 지속 — 외국인이 신중하게 빠지는 중`;
      }
      if (buying.length >= 2 && selling.length >= 2) {
        return `${buying.length}종목 매수 / ${selling.length}종목 매도 — 외국인이 종목을 골라가며 사고팔고 있어요`;
      }
      return `매수 ${buying.length} · 매도 ${selling.length} · 중립 ${neutral.length}`;
    })();

    const renderStockLine = (r) => {
      const reason = r.flowReason || {};
      const hasReason = reason.summary || reason.detail;
      return `
        <div class="fflow-stock">
          <div class="fflow-stock-head">
            <span class="fflow-stock-name">${escapeHtml(r.name)}</span>
            <span class="fflow-stock-hold">외국인 ${r.foreignHoldRatio != null ? r.foreignHoldRatio.toFixed(1) + '%' : '—'} 보유</span>
          </div>
          <div class="fflow-stock-line">${escapeHtml(summarize(r))}</div>
          ${hasReason ? `
            <div class="fflow-reason">
              <div class="fflow-reason-summary">💡 ${escapeHtml(reason.summary || '')}</div>
              ${reason.detail ? `
                <details class="fflow-reason-detail">
                  <summary>왜 그런지 자세히 보기</summary>
                  <div class="fflow-reason-text">${escapeHtml(paraBreak(reason.detail))}</div>
                  ${(reason.sources && reason.sources.length) ? `
                    <div class="fflow-reason-sources">
                      출처: ${reason.sources.map((s) => s.url
                        ? `<a href="${escapeHtml(s.url)}" target="_blank" rel="noopener">${escapeHtml(s.name)}</a>`
                        : escapeHtml(s.name)).join(' · ')}
                    </div>
                  ` : ''}
                </details>
              ` : ''}
            </div>
          ` : ''}
        </div>
      `;
    };

    return `
      <details class="fflow-panel" open>
        <summary class="fflow-head">
          <span class="fflow-title">🌍 외국인은 어떻게 움직이고 있을까?</span>
          <span class="fflow-sub">국내 5종목, 최근 5거래일 (${escapeHtml(krFlow.asOf)} 기준)</span>
        </summary>
        <div class="fflow-body">
          <div class="fflow-conclusion">💬 ${escapeHtml(conclusion)}</div>

          ${buying.length ? `
            <div class="fflow-group fflow-group-buy">
              <div class="fflow-group-title">🟢 사기 시작했어요 (${buying.length})</div>
              ${buying.map(renderStockLine).join('')}
            </div>
          ` : ''}

          ${selling.length ? `
            <div class="fflow-group fflow-group-sell">
              <div class="fflow-group-title">🔴 계속 팔고 있어요 (${selling.length})</div>
              ${selling.map(renderStockLine).join('')}
            </div>
          ` : ''}

          ${neutral.length ? `
            <div class="fflow-group fflow-group-neutral">
              <div class="fflow-group-title">⚪ 거의 중립 (${neutral.length})</div>
              ${neutral.map(renderStockLine).join('')}
            </div>
          ` : ''}

          <details class="fflow-raw">
            <summary>📊 5일 일별 매매 자세히 보기</summary>
            <div class="fflow-raw-body">
              ${krFlow.rows.map((r) => `
                <div class="fflow-raw-row">
                  <div class="fflow-raw-name">${escapeHtml(r.name)}</div>
                  <div class="fflow-raw-daily">
                    ${r.dailyNetBuy.map((d) => `
                      <span class="fflow-day ${d.shares >= 0 ? 'pos' : 'neg'}">
                        <span class="fflow-day-date">${escapeHtml(d.date)}</span>
                        <span class="fflow-day-val">${fmtShares(d.shares)}</span>
                      </span>
                    `).join('')}
                  </div>
                </div>
              `).join('')}
            </div>
          </details>

          ${krFlow.sources?.length ? `
            <div class="fflow-sources">
              출처: ${krFlow.sources.map((s) => escapeHtml(s.name)).join(' · ')}
            </div>
          ` : ''}
        </div>
      </details>
    `;
  };

  return `
    <section class="day-box collapsible" data-box="signals">
      ${dbHead('signals', '오늘의 추천', `국내 ${kr.length} · 미국 ${us.length}`, true)}
      <div class="db-headline">
        <div class="sig-mini-note">📌 ${signalCardBrief(kr[0] || us[0])}</div>
        ${moreHint(`외 ${totalCount - 1}건 자세히 보기`)}
      </div>
      <div class="db-content">
        <div class="sig-disclaimer">정보·분석 제공이며 매수 추천이 아닙니다. 투자 판단·책임은 본인에게 있어요.</div>
        <div class="sig-region-tabs">
          <button class="ntab ${defaultTab === 'kr' ? 'active' : ''}" data-tab="kr-sig" ${kr.length === 0 ? 'disabled' : ''}>🇰🇷 국내 <span class="ntab-count">${kr.length}</span></button>
          <button class="ntab ${defaultTab === 'us' ? 'active' : ''}" data-tab="us-sig" ${us.length === 0 ? 'disabled' : ''}>🇺🇸 미국 <span class="ntab-count">${us.length}</span></button>
        </div>
        <div data-tab-content="kr-sig" class="sig-list ${defaultTab === 'kr' ? '' : 'hidden'}">
          ${renderForeignFlow()}
          ${kr.map(signalCard).join('') || '<div class="region-empty">국내 추천이 없어요.</div>'}
        </div>
        <div data-tab-content="us-sig" class="sig-list ${defaultTab === 'us' ? '' : 'hidden'}">
          ${us.map(signalCard).join('') || '<div class="region-empty">미국 추천이 없어요.</div>'}
        </div>

        ${(newKr.length || newUs.length) ? `
          <div class="new-listings-section">
            <div class="new-listings-head">
              <span class="new-listings-title">🆕 신규 상장주 (IPO)</span>
              <span class="new-listings-sub">상장한 지 얼마 안 된 종목 · 변동이 매우 큰 종목이라 신중히 보세요</span>
            </div>
            ${newKr.length ? `
              <div class="new-listings-region">
                <div class="new-listings-region-title">🇰🇷 국내 (${newKr.length})</div>
                ${newKr.map(signalCard).join('')}
              </div>
            ` : ''}
            ${newUs.length ? `
              <div class="new-listings-region">
                <div class="new-listings-region-title">🇺🇸 미국 (${newUs.length})</div>
                ${newUs.map(signalCard).join('')}
              </div>
            ` : ''}
          </div>
        ` : ''}
      </div>
    </section>
  `;
}

// 카드 1줄짜리 미니 (박스 collapsed 시 헤드라인용)
function signalCardBrief(s) {
  if (!s) return '';
  const ticker = escapeHtml(s.ticker || '');
  const name = escapeHtml(s.name || '');
  const cat = escapeHtml(s.category || '주목');
  return `<strong>${ticker} ${name}</strong> · <span class="sig-mini-cat">${cat}</span>`;
}

// 시그널 카드 한 장 — 간략 모드 default, 클릭하면 4-블록 펼침
function signalCard(s) {
  const catColor = {
    '관련주': 'rel',
    '성장주': 'growth',
    '이슈주': 'issue',
    '실적기대': 'earn',
  }[s.category] || 'neutral';

  const priceStr = s.currentPrice != null
    ? (typeof s.currentPrice === 'number'
        ? (s.market && /KOSPI|KOSDAQ/i.test(s.market) ? s.currentPrice.toLocaleString() + '원' : '$' + s.currentPrice.toLocaleString())
        : String(s.currentPrice))
    : '';
  const changeStr = (s.change1D != null)
    ? `<span class="sig-change ${s.change1D >= 0 ? 'pos' : 'neg'}">${pct(s.change1D)}</span>`
    : '';

  const hasDetail = s.financials || s.comparable || s.risk || s.horizon || s.outlook || s.outlookEasy || s.company || s.financialStatements || (s.relatedStocks && s.relatedStocks.length);

  return `
    <div class="sig-card cat-${catColor}" data-sig-card>
      <div class="sig-card-top">
        <div class="sig-id">
          <div class="sig-badges">
            <span class="sig-cat-badge cat-${catColor}">${escapeHtml(s.category || '주목')}</span>
            ${s.listedAt ? `<span class="sig-ipo-badge">🆕 ${escapeHtml(s.listedAt)} 상장</span>` : ''}
          </div>
          <div class="sig-name-row">
            <span class="sig-ticker">${escapeHtml(s.ticker || '')}</span>
            <span class="sig-name">${escapeHtml(s.name || '')}</span>
          </div>
        </div>
        <div class="sig-meta">
          ${s.market ? `<span class="sig-market">${escapeHtml(s.market)}</span>` : ''}
          ${priceStr ? `<span class="sig-price">${escapeHtml(priceStr)}</span>` : ''}
          ${changeStr}
        </div>
      </div>
      ${s.thesis ? `
        <div class="sig-why">
          <div class="sig-why-label">💡 왜 추천하나요?</div>
          <div class="sig-thesis">${escapeHtml(paraBreak(s.thesis))}</div>
        </div>
      ` : ''}
      ${hasDetail ? `
        <details class="sig-detail">
          <summary><span class="sig-detail-label">📋 자세히 보기</span></summary>
          <div class="sig-blocks">
            ${s.company ? `
              <div class="sig-block sig-block-company">
                <span class="sig-block-lbl">🏢 회사 정보</span>
                <div class="sig-block-val">
                  ${s.company.business ? `<div class="sig-co-row"><span class="sig-co-lbl">사업</span><span class="sig-co-val">${escapeHtml(s.company.business)}</span></div>` : ''}
                  ${s.company.ceo ? `<div class="sig-co-row"><span class="sig-co-lbl">대표</span><span class="sig-co-val">${escapeHtml(s.company.ceo)}</span></div>` : ''}
                  ${s.company.hq ? `<div class="sig-co-row"><span class="sig-co-lbl">본사</span><span class="sig-co-val">${escapeHtml(s.company.hq)}</span></div>` : ''}
                  ${s.company.employees ? `<div class="sig-co-row"><span class="sig-co-lbl">직원</span><span class="sig-co-val">${escapeHtml(s.company.employees)}</span></div>` : ''}
                  ${s.company.homepage ? `<div class="sig-co-row"><span class="sig-co-lbl">홈페이지</span><span class="sig-co-val"><a href="${escapeHtml(s.company.homepage)}" target="_blank" rel="noopener">${escapeHtml(s.company.homepage)}</a></span></div>` : ''}
                  ${s.company.ceoSource ? `<div class="sig-co-source">출처: ${escapeHtml(s.company.ceoSource)}</div>` : ''}
                </div>
              </div>
            ` : ''}
            ${s.financials ? `<div class="sig-block"><span class="sig-block-lbl">💰 재무</span><span class="sig-block-val">${escapeHtml(s.financials)}</span></div>` : ''}
            ${s.financialStatements && s.financialStatements.annual?.length ? `
              <div class="sig-block sig-block-fs">
                <span class="sig-block-lbl">📊 재무재표 (연간)</span>
                <div class="sig-block-val">
                  ${s.financialStatementsEasy ? `<div class="sig-fs-easy">💬 ${escapeHtml(paraBreak(s.financialStatementsEasy))}</div>` : ''}
                  <details class="sig-fs-detail">
                    <summary>📊 연간 매출·영업이익 표 보기</summary>
                    <div class="sig-fs-table">
                      <div class="sig-fs-row sig-fs-row-head">
                        <span class="sig-fs-year">연도</span>
                        <span class="sig-fs-val">매출</span>
                        <span class="sig-fs-val">영업이익</span>
                        <span class="sig-fs-margin">마진</span>
                      </div>
                      ${s.financialStatements.annual.map((r) => `
                        <div class="sig-fs-row ${r.isConsensus ? 'sig-fs-row-est' : ''}">
                          <span class="sig-fs-year">${escapeHtml(r.period)}${r.isConsensus ? ' (추정)' : ''}</span>
                          <span class="sig-fs-val">${escapeHtml(r.salesFmt)}</span>
                          <span class="sig-fs-val ${r.operatingIncome < 0 ? 'neg' : 'pos'}">${escapeHtml(r.operatingIncomeFmt)}</span>
                          <span class="sig-fs-margin ${r.operatingMargin != null && r.operatingMargin < 0 ? 'neg' : ''}">${r.operatingMargin != null ? r.operatingMargin.toFixed(1) + '%' : '—'}</span>
                        </div>
                      `).join('')}
                    </div>
                    <div class="sig-fs-note">단위: ${escapeHtml(s.financialStatements.unit)} · 출처: ${(s.financialStatements.sources || []).map((src) => escapeHtml(src.name)).join(' · ')}</div>
                  </details>
                </div>
              </div>
            ` : ''}
            ${s.comparable ? `<div class="sig-block"><span class="sig-block-lbl">📊 과거 사례</span><span class="sig-block-val">${escapeHtml(s.comparable)}</span></div>` : ''}
            ${(s.outlookEasy || s.outlook) ? `
              <div class="sig-block sig-block-outlook">
                <span class="sig-block-lbl">🔮 앞으로 전망</span>
                <div class="sig-block-val">
                  ${s.outlookEasy ? `<div class="sig-outlook-easy">💬 ${escapeHtml(paraBreak(s.outlookEasy))}</div>` : ''}
                  ${s.outlook ? `
                    <details class="sig-outlook-detail">
                      <summary>📊 분석가·숫자로 자세히 보기</summary>
                      <div class="sig-outlook-tech">${escapeHtml(paraBreak(s.outlook))}</div>
                    </details>
                  ` : ''}
                </div>
              </div>
            ` : ''}
            ${s.risk ? `<div class="sig-block"><span class="sig-block-lbl">⚠️ 리스크</span><span class="sig-block-val">${escapeHtml(s.risk)}</span></div>` : ''}
            ${s.horizon ? `<div class="sig-block"><span class="sig-block-lbl">⏱️ 예상 기간</span><span class="sig-block-val">${escapeHtml(s.horizon)}</span></div>` : ''}
            ${(s.relatedStocks && s.relatedStocks.length) ? `
              <div class="sig-block sig-block-related">
                <span class="sig-block-lbl">🔗 같이 볼 종목</span>
                <div class="sig-block-val">
                  <div class="sig-related-list">
                    ${s.relatedStocks.map((r) => {
                      const isKr = /^A?\d+$/.test(r.code);
                      const unit = isKr ? '원' : '$';
                      const priceStr = r.currentPrice
                        ? (isKr ? `${r.currentPrice}${unit}` : `${unit}${r.currentPrice}`)
                        : '—';
                      const changeCls = r.change1D == null ? '' : (r.change1D >= 0 ? 'pos' : 'neg');
                      const changeStr = r.change1D == null ? '' : pct(r.change1D);
                      return `
                        <div class="sig-related-item">
                          <div class="sig-related-head">
                            <span class="sig-related-name">${escapeHtml(r.name)}</span>
                            <span class="sig-related-price">${escapeHtml(priceStr)}
                              ${changeStr ? `<span class="sig-related-change ${changeCls}">${changeStr}</span>` : ''}
                            </span>
                          </div>
                          <div class="sig-related-relation">${escapeHtml(r.relation)}</div>
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>
              </div>
            ` : ''}
          </div>
          ${(s.sources && s.sources.length) ? `
            <div class="sig-sources">
              ${s.sources.map((src) => src.url
                ? `<a href="${escapeHtml(src.url)}" target="_blank" rel="noopener">${escapeHtml(src.name || '출처')}</a>`
                : `<span>${escapeHtml(src.name || '')}</span>`).join(' · ')}
            </div>
          ` : ''}
        </details>
      ` : ''}
    </div>
  `;
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
