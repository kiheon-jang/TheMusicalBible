# 🔑 n8n Credentials 연결 체크리스트 (5분)

## ✅ 완료 상황

```
스토리 분석: ✅ 완료 (14개 스토리 생성)
워크플로우: ✅ 임포트 완료
Credentials: ⏳ 연결 대기중
```

---

## 📍 연결 방법 (매우 간단!)

### URL
https://n8n-production-1d6b.up.railway.app/workflow/QoMfESYU0FCalwdb

### 로그인
- Email: `xaqwer@gmail.com`
- Password: `Wkdrlgjs2@`

---

## 🎯 연결할 Credentials (9개 노드)

### 1. PostgreSQL (2개 노드)

**노드 이름:**
- `PostgreSQL: 스토리 3개 조회 (순차)`
- `PostgreSQL: 스토리 프롬프트 저장`

**연결 방법:**
1. 노드 더블클릭
2. 우측 패널에서 `Credential for PostgreSQL` 드롭다운 클릭
3. `PostgreSQL - TMB` 선택 (또는 새로 만들기)
4. Save

**Credential 정보 (새로 만드는 경우):**
```
Host: maglev.proxy.rlwy.net
Port: 15087
Database: railway
User: postgres
Password: cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq
```

---

### 2. Claude (1개 노드)

**노드 이름:**
- `Claude: 스토리 프롬프트 생성`

**연결 방법:**
1. 노드 더블클릭
2. `Credential for HTTP Request` 드롭다운
3. `Claude API - TMB` 선택 (또는 새로 만들기)

**Credential 정보 (Header Auth):**
```
Name: x-api-key
Value: (API_KEYS.txt 또는 환경변수 CLAUDE_API_KEY 사용)
```

---

### 3. Suno (1개 노드)

**노드 이름:**
- `Suno: 음악 생성 시작`

**연결 방법:**
1. 노드 더블클릭
2. `Authentication`: `Header Auth` 선택
3. Credential 드롭다운에서 `Suno API - TMB` 선택

**Credential 정보 (Header Auth):**
```
Name: Authorization
Value: Bearer <Suno Cookie>
```

---

### 4. Fish Audio (1개 노드)

**노드 이름:**
- `Fish Audio: 음성 생성`

**연결 방법:**
1. 노드 더블클릭
2. `Authentication`: `Header Auth`
3. Credential: `Fish Audio API - TMB`

**Credential 정보:**
```
Name: Authorization
Value: Bearer 8024d34fa5b84ee59b74bc5440fd9922
```

---

### 5. Hedra (1개 노드)

**노드 이름:**
- `Hedra: 립싱크 영상 생성`

**연결 방법:**
1. 노드 더블클릭
2. `Authentication`: `Header Auth`
3. Credential: `Hedra API - TMB`

**Credential 정보:**
```
Name: X-API-Key
Value: sk_hedra_H9RoTOX6ZvWtnctjIJ0ThjIA1gTWGa9F8Onc9EZFpupYkTiZaVzCCDZGJ51OMCvq
```

---

### 6. Runway (2개 노드)

**노드 이름:**
- `Runway: 배경 영상 생성 (Phase 1)`
- `Runway: 배경 영상 생성 (Phase 2)`

**연결 방법:**
1. 각 노드 더블클릭
2. `Authentication`: `Header Auth`
3. Credential: `Runway API - TMB`

**Credential 정보:**
```
Name: Authorization
Value: Bearer key_251946556723bdf0b9794eb0296b8f0be1407a79073afd64642b3b454cf653c04d4b9af33116e05c493e9401174d4ed25ba1ce690c51c451a934cd4fb2a62332
```

---

### 7. YouTube (1개 노드)

**노드 이름:**
- `YouTube: 영상 업로드`

**연결 방법:**
1. 노드 더블클릭
2. `Authentication`: `OAuth2`
3. Credential: `YouTube API - TMB`

**Credential 정보 (OAuth2):**
```
Client ID: 1053902423625-6dlr4lgb58e20d0nteaq16ufrnaj7hq0.apps.googleusercontent.com
Client Secret: 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
```

---

## 💡 빠른 팁

### Credentials 이미 있는 경우
- 드롭다운에서 선택만 하면 됨 (10초!)

### Credentials 없는 경우
1. 좌측 메뉴 → `Credentials` 클릭
2. `+ Add Credential` 클릭
3. 타입 선택 (PostgreSQL, Header Auth, OAuth2)
4. 위의 정보 입력
5. Save

---

## ✅ 연결 확인 체크리스트

```
□ PostgreSQL: 스토리 3개 조회 (순차)
□ PostgreSQL: 스토리 프롬프트 저장
□ Claude: 스토리 프롬프트 생성
□ Suno: 음악 생성 시작
□ Fish Audio: 음성 생성
□ Hedra: 립싱크 영상 생성
□ Runway: 배경 영상 (Phase 1)
□ Runway: 배경 영상 (Phase 2)
□ YouTube: 영상 업로드
```

---

## 🚀 다음 단계

### 1. 워크플로우 저장
우측 상단 `Save` 클릭

### 2. 첫 영상 테스트
`Execute Workflow` 버튼 클릭!

**예상 시간:** 10-15분
**예상 비용:** ₩3,051
**결과:** YouTube에 자동 업로드!

---

## 📊 현재 준비 상황

```
✅ 스토리 분석 완료: 14개
✅ PostgreSQL: 792개 구절
✅ 워크플로우: 임포트 완료
✅ n8n: 실행 준비 완료
⏳ Credentials: 연결만 하면 끝!
```

**5분 투자 → 첫 뮤지컬 성경 영상 완성!** 🎉
