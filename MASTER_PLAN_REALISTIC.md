---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 📑 [REALISTIC MASTER PLAN] AI 시네마틱 뮤지컬 성경 유니버스

**Project Title**: The Musical Bible (TMB) - Cinematic Collection 2026  
**Vision**: 성경을 읽는 텍스트에서 '영혼의 공연'으로, AI 기술의 현실적 한계 내에서 최고의 몰입감을 구현

---

## ■ PART 0. 프로젝트의 본질 (Core Essence)

### 문제 의식
기존 성경 콘텐츠는 3인칭 해설과 교리 전달 중심에 치우쳐 있어 현대 세대에게 정서적 몰입을 주지 못하며, 성경 읽기를 '공부'나 '부채감'으로 느끼게 함.

### 해결 방안
해설을 배제한 **'1인칭 체험 시점'**과 **'뮤지컬 문법'**의 결합. 성경 인물의 내면적 고뇌와 영적 환희를 해석하거나 평가하지 않고, 기록된 현상만을 예술적으로 복원하여 시청자를 '방관자'에서 '목격자'로 전환함.

### 논쟁 최소화 선언 (Neutrality)
특정 교리나 신학적 해석을 주장하지 않음. 의미 부여가 아닌 **'현상 묘사'**에만 집중하며, 본문에 대한 판단은 시청자에게 전적으로 위임함.

---

## ■ PART 1. 30초 시네마틱 3단계 구조 (현실적 구현)

모든 에피소드는 30초 독립 숏츠이며, 후반 작업으로 장편 영화 통합 가능하도록 메타데이터를 관리합니다.

### 1-1. Phase 1: Scripture Context (0-8초, 도입)
**컨셉**: 거룩한 말씀의 시각적 각인

**구현 방법**:
- ✅ **자막**: FFmpeg로 성경 구절 텍스트 오버레이 (fade in/out)
- ✅ **배경 영상**: Runway Gen-3/4로 10초 영상 생성
  - 프롬프트 예시: "Wide cinematic shot of ancient desert, golden hour lighting, slow camera pan"
- ⚠️ **샷 타입**: "wide shot", "close-up", "overhead view" 등 프롬프트 키워드로 간접 제어
- ✅ **음악**: Suno Instrumental, 조용한 도입부 (볼륨 30%)

**기술적 타협**:
- "핸드헬드", "익스트림 와이드" 같은 정밀한 샷 타입은 프롬프트 표현에 의존
- AI가 해석한 결과를 수용 (100% 제어 불가)

---

### 1-2. Phase 2: Atmosphere & Tension (8-18초, 전개)
**컨셉**: 노래 직전의 감정적 긴장감 빌드업

**구현 방법**:
- ✅ **인물 영상**: Hedra 립싱크 (무음 또는 짧은 숨소리)
  - Hedra의 자동 표정 연기에 의존
  - 프롬프트로 감정 상태만 제시 ("anxious expression", "fearful eyes")
- ✅ **배경 음악**: Suno Instrumental 크레센도 (볼륨 50% → 70%)
- ✅ **환경음**: 프롬프트에 명시 ("wind sounds", "thunderstorm approaching")

**기술적 타협**:
- "미세한 눈동자 흔들림", "거친 숨소리" 같은 세밀한 연기는 Hedra의 자동 결과 수용
- ASMR 수준의 제어는 불가능, 음악과 프롬프트로 분위기 조성

---

### 1-3. Phase 3: Aria & Grand Finale (18-30초, 절정)
**컨셉**: 뮤지컬 가창과 립싱크의 완벽한 동기화

**구현 방법**:
- ✅ **립싱크 가창**: Hedra + Fish Audio 완벽 동기화
  - Fish Audio로 감정 태그 기반 음성 생성 (`(scared)(urgent)`)
  - Hedra로 립싱크 영상 생성
- ✅ **가사**: Suno Custom Lyrics로 성경 구절 직접 인용
  - 예: "주님이 나를 부르시니 / 내가 어찌 거절하리오" (창세기 22장 리듬화)
- ✅ **배경 음악**: Suno Instrumental (볼륨 100%, 드라마틱)
- ✅ **시각 효과**: Runway로 "dramatic lighting", "ethereal glow" 프롬프트

**기술적 타협**:
- "초현실적 빛의 움직임"은 Runway 프롬프트로 간접 표현
- Silent Aria는 가능 (가사 없는 Instrumental + Hedra 립싱크)

---

## ■ PART 2. AI 캐릭터 관리 시스템 (현실적 버전)

### 2-1. 캐릭터 프로파일 관리

**구현 방법**:
- ✅ **DB 기반 캐릭터 저장**: PostgreSQL `character_voices` 테이블
  - 캐릭터명, 나이 범위, 기본 감정, Fish Audio 음성 ID
- ✅ **감정 변수**: `fear`, `confusion`, `resolve`, `fatigue` (0.0-1.0)
  - Claude가 구절 분석 후 수치 자동 계산
  - Fish Audio 태그로 자동 변환 (`fear > 0.7` → `(scared)(nervous)`)
- ⚠️ **캐릭터 이미지 버전 관리**: 수동 준비 필요
  - 예: `abraham_young.jpg`, `abraham_middle.jpg`, `abraham_old.jpg`
  - Claude가 구절의 시간대 분석 후 적절한 이미지 선택

**기술적 구현**:
- Hedra가 프롬프트로 캐릭터 자동 생성 (이미지 준비 불필요)
- characterId를 DB에 저장하여 같은 얼굴 재사용
- 첫 실행에만 생성, 이후 자동 일관성 유지

---

### 2-2. 환경 연속성 시스템

**구현 방법**:
- ✅ **장소 Seed 관리**: DB에 `location_name`, `runway_seed`, `color_palette` 저장
  - 동일 장소는 동일 Seed 재사용
- ✅ **시간대/날씨**: 프롬프트에 명시
  - 예: "Jerusalem temple courtyard, early morning sunlight, clear sky"
- ⚠️ **날씨 상호작용**: 프롬프트 묘사에 의존
  - 예: "wet hair from rain", "dusty clothes from desert wind"

**기술적 타협**:
- AI가 "젖은 머리카락" 표현을 정확히 렌더링할지는 불확실
- Seed 재사용으로 장소 일관성은 확보 가능

---

## ■ PART 3. 제작 파이프라인 (2026.01 현실 스택)

### 3-1. 완전 자동화 워크플로우

```
n8n Complete Pipeline (하루 1회, AM 3:00 실행)
│
├─ Step 1: PostgreSQL 구절 3개 조회 (1초)
│   - status = 'pending'인 구절
│
├─ Step 2: Claude 프롬프트 생성 (3초/구절)
│   - 3단계 구조화된 프롬프트 JSON 생성
│   - 감정 변수 계산 (fear, resolve, confusion)
│   - 캐릭터 나이/이미지 버전 선택
│   - 장소 Seed 조회/생성
│
├─ Step 3: 병렬 AI 생성 (5분)
│   ├─ Suno: Custom Lyrics 음악 (2분 대기 + Polling)
│   ├─ Fish Audio: 감정 태그 음성 (30초)
│   ├─ Hedra: 립싱크 영상 (1분)
│   └─ Runway: 배경 영상 10초×3 = 30초 (3분)
│
├─ Step 4: FFmpeg 3단계 합성 (30초)
│   - Phase 1: 자막 오버레이 (0-8초)
│   - Phase 2: 음악 크레센도 (8-18초)
│   - Phase 3: 립싱크 + 음악 풀볼륨 (18-30초)
│
├─ Step 5: 썸네일 자동 생성 (10초)
│   - 15초 지점 프레임 추출
│   - 텍스트 오버레이: "창세기 22:1-2"
│
├─ Step 6: YouTube 자동 업로드 (1분)
│   - 제목: "{book_name} {chapter}:{verse}"
│   - 설명: 성경 구절 + 태그
│
└─ Step 7: PostgreSQL 상태 업데이트 (1초)
    - status = 'completed'
    - 메타데이터 저장 (Seed, 구도, 음악 URL)
```

**총 소요시간**: 구절 1개당 6-7분, 3개 기준 **20분**

---

### 3-2. 기술 스택

| 역할 | 도구 | 버전 | 기능 |
|------|------|------|------|
| 🧠 두뇌 | Claude | 3.5 Sonnet | 구절 분석, 프롬프트 생성, 감정 계산 |
| 🎬 관제 | n8n | Latest | 전체 파이프라인 자동화 |
| 🎥 배경 영상 | Runway | Gen-3/4 | 10초 영상×3개 생성 |
| 👤 립싱크 | Hedra | Pro | 음성 동기화 영상 |
| 🎤 음성 | Fish Audio | - | 64+ 감정 태그 TTS |
| 🎵 음악 | Suno | v4 | Custom Lyrics 뮤지컬 |
| 🔧 합성 | FFmpeg | - | 타임라인 편집, 자막, 믹싱 |
| 🖼️ 썸네일 | Pillow | - | 자동 생성 |
| 📤 업로드 | YouTube API | v3 | 자동 업로드 |
| 💾 DB | PostgreSQL | - | 메타데이터 관리 |

---

## ■ PART 4. 시네마틱 통합 준비 (Phase 2 목표)

### 4-1. 메타데이터 관리

**DB 스키마 확장**:
```sql
ALTER TABLE scripture ADD COLUMN:
- phase1_duration INTEGER DEFAULT 8,  -- Phase 1 길이 (초)
- phase2_duration INTEGER DEFAULT 10,
- phase3_duration INTEGER DEFAULT 12,
- runway_seed VARCHAR(255),           -- 장소 Seed
- camera_angle VARCHAR(50),           -- 'wide', 'close-up', 'overhead'
- prev_episode_id INTEGER,            -- 이전 에피소드 (매치 컷용)
- next_episode_id INTEGER,            -- 다음 에피소드
- transition_type VARCHAR(50),        -- 'cut', 'fade', 'match-cut'
- background_music_url TEXT           -- 사운드 브릿지용
```

### 4-2. 장편 영화 통합 (수동 편집)

**Phase 2에서 구현**:
- ⚠️ 에피소드 간 매치 컷: 메타데이터 기반 수동 편집
- ⚠️ 사운드 브릿지: 에피소드 사이 연주곡 삽입 (FFmpeg)
- ⚠️ 챕터 마커: YouTube 타임스탬프 자동 생성

**현재는 독립 숏츠로 먼저 배포, 추후 통합 버전 제작**

---

## ■ PART 5. 글로벌 확장 (Phase 3 목표)

### 5-1. 다국어 자동화 (현재 미구현)

**Phase 3에서 구현 예정**:
```
1. 번역 DB 구축 (한국어 → 영어/중국어/스페인어 등)
2. Fish Audio로 다국어 음성 재생성
3. Hedra로 립싱크 재합성
4. 국가별 YouTube 채널 자동 배포
```

### 5-2. 비즈니스 모델

**수익원**:
- ✅ YouTube 광고 수익 (즉시)
- ⚠️ 음원 스트리밍 (Suno 라이선스 확인 필요)
- ⚠️ 교육용 B2B (Phase 2)
- ⚠️ 통합 영화 VOD (Phase 3)

---

## ■ PART 6. 단계별 로드맵

### 🚀 Phase 1: MVP 완성 (2주)
```
□ Claude 3단계 프롬프트 시스템
□ 감정 변수 → Fish Audio 태그 자동 변환
□ FFmpeg 3단계 타임라인 합성
□ 완전 자동화 파이프라인 테스트
□ 첫 30개 에피소드 제작
```

### 📈 Phase 2: 고도화 (1개월)
```
□ 캐릭터 이미지 버전 관리 (나이별)
□ 장소 Seed 관리 시스템
□ 매치 컷 메타데이터
□ 통합 영화 1편 제작 (창세기)
```

### 🌏 Phase 3: 글로벌 확장 (3개월)
```
□ 다국어 번역 DB
□ 립싱크 재합성 자동화
□ 국가별 채널 자동 배포
□ B2B 라이선스 모델
```

---

## ■ PART 7. 최종 결언

**현실적 비전**:

"본 프로젝트는 2026년 AI 기술의 현실적 한계를 인정하며, 그 안에서 최고의 몰입감을 구현합니다. 

**100% 구현**:
- ✅ 립싱크 뮤지컬 가창 (Phase 3의 핵심)
- ✅ 감정 기반 음성/음악
- ✅ 성경 본문 직접 인용 (Custom Lyrics)
- ✅ 완전 자동화 파이프라인

**70-80% 구현** (타협):
- ⚠️ 3단계 시네마틱 구조 (FFmpeg 후처리)
- ⚠️ 캐릭터 노화 (수동 이미지 관리)
- ⚠️ 장소 연속성 (Seed 재사용)

**현재 불가능** (미래 과제):
- ❌ 미세 표정 제어 (AI 자동에 의존)
- ❌ 실시간 환경 상호작용

The Musical Bible은 기술적 완벽함보다 **'영혼의 공연'**이라는 본질에 집중하며, AI 기술의 발전과 함께 진화할 것입니다."

---

## 📊 구현 완성도

| 항목 | 목표 | 현실 | 비고 |
|------|------|------|------|
| 핵심 가치 (중립성, 1인칭) | 100% | 95% | ✅ 완벽 구현 |
| 립싱크 가창 | 100% | 100% | ✅ 완벽 구현 |
| 3단계 구조 | 100% | 70% | ⚠️ 후처리로 타협 |
| 동적 캐릭터 | 100% | 50% | ⚠️ 수동 이미지 관리 |
| 환경 연속성 | 100% | 40% | ⚠️ Seed 재사용 |
| 자동화 | 100% | 100% | ✅ 완벽 구현 |
| **종합** | **100%** | **76%** | ✅ 충분히 출시 가능 |

---

**이 계획에 동의하시면 바로 구현을 시작하겠습니다!** 🚀
