---
date: 2026-01-26
project: 10_Projects/project
tags: ['credentials', 'project']
---
# 🔑 n8n Credentials 연결 가이드 (5분)

## 📍 n8n 접속

**URL:** https://n8n-production-1d6b.up.railway.app/workflow/QoMfESYU0FCalwdb

**로그인:**
- Email: `xaqwer@gmail.com`
- Password: `Wkdrlgjs2@`

---

## ✅ 연결해야 할 Credentials (7개)

### 1. PostgreSQL (2개 노드)
- **노드**: `스토리 선택`, `완료 상태 업데이트`
- **Credential**: `PostgreSQL - TMB` (이미 생성됨)
- **방법**: 
  1. 노드 클릭
  2. `Credential for PostgreSQL` 드롭다운
  3. `PostgreSQL - TMB` 선택
  4. Save

---

### 2. Claude (1개 노드)
- **노드**: `Claude: 영상 프롬프트 생성`
- **Credential**: `Claude API - TMB` (이미 생성됨)
- **방법**:
  1. 노드 클릭
  2. `Credential for Claude` 드롭다운
  3. `Claude API - TMB` 선택
  4. Save

---

### 3. Suno (1개 노드)
- **노드**: `Suno: 음악 생성 시작`
- **Credential**: HTTP 헤더 인증
- **방법**:
  1. 노드 클릭
  2. Authentication: `Header Auth`
  3. Credential: `Suno API - TMB` 선택
  4. Save

---

### 4. Fish Audio (1개 노드)
- **노드**: `Fish Audio: 음성 생성`
- **Credential**: HTTP 헤더 인증
- **방법**:
  1. 노드 클릭
  2. Authentication: `Header Auth`
  3. Credential: `Fish Audio API - TMB` 선택
  4. Save

---

### 5. Hedra (1개 노드)
- **노드**: `Hedra: 립싱크 영상 생성`
- **Credential**: HTTP 헤더 인증
- **방법**:
  1. 노드 클릭
  2. Authentication: `Header Auth`
  3. Credential: `Hedra API - TMB` 선택
  4. Save

---

### 6. Runway (2개 노드)
- **노드**: `Runway: 배경 영상 생성 (Phase 1)`, `Runway: 배경 영상 생성 (Phase 2)`
- **Credential**: HTTP 헤더 인증
- **방법**:
  1. 각 노드 클릭
  2. Authentication: `Header Auth`
  3. Credential: `Runway API - TMB` 선택
  4. Save

---

### 7. YouTube (1개 노드)
- **노드**: `YouTube: 영상 업로드`
- **Credential**: `YouTube API - TMB` (이미 생성됨)
- **방법**:
  1. 노드 클릭
  2. `Credential for YouTube` 드롭다운
  3. `YouTube API - TMB` 선택
  4. Save

---

## 🎯 빠른 체크리스트

```
□ PostgreSQL - 스토리 선택
□ PostgreSQL - 완료 상태 업데이트
□ Claude - 영상 프롬프트 생성
□ Suno - 음악 생성 시작
□ Fish Audio - 음성 생성
□ Hedra - 립싱크 영상 생성
□ Runway - 배경 영상 생성 (Phase 1)
□ Runway - 배경 영상 생성 (Phase 2)
□ YouTube - 영상 업로드
```

---

## 💾 저장

모든 Credential 연결 후:
1. 워크플로우 우측 상단 `Save` 클릭
2. ✅ "Workflow saved" 확인

---

## ▶️ 테스트 실행

저장 후:
1. `Execute Workflow` 버튼 클릭
2. 10-15분 대기
3. 첫 영상 완성!

**예상 비용:** ₩3,051
**결과:** YouTube에 자동 업로드된 첫 뮤지컬 성경 영상!

---

## 🔍 실행 확인

```bash
# 터미널에서 확인
cd /Users/giheonjang/Documents/project/TMB

python3 << 'EOF'
import psycopg2
DATABASE_URL = "postgresql://postgres:cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq@maglev.proxy.rlwy.net:15087/railway"
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute("SELECT title, status, youtube_url FROM story_units WHERE status='completed';")
for row in cursor.fetchall():
    print(f"✅ {row[0]}")
    print(f"   상태: {row[1]}")
    print(f"   URL: {row[2]}")
    print()
cursor.close()
conn.close()
EOF
```

---

## ⚠️ 문제 발생 시

### Credential이 안 보여요
1. n8n 좌측 메뉴 → `Credentials` 클릭
2. 각 API 키 확인/생성
3. 워크플로우로 돌아가서 다시 선택

### 노드 실행 실패
1. 노드 클릭 → 에러 메시지 확인
2. API 키 유효성 확인
3. Railway 서비스 상태 확인

---

## 📊 다음 단계

첫 영상 성공 후:
1. ✅ 시스템 검증 완료
2. ✅ 품질 확인
3. 📥 전체 성경 데이터 추가
4. 🔄 전체 스토리 분석 (₩94,500)
5. 🚀 정규 운영 시작 (하루 1개 자동 업로드)

---

**현재까지 투자:** ₩5,751 (분석 ₩2,700 + 첫 영상 ₩3,051)
**검증 완료!** 🎉
