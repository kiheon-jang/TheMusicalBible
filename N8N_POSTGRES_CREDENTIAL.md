---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# n8n에서 Credential 만드는 방법

---

## A. Claude (Anthropic API) – "Credentials not found" 해결

**노드:** `Claude: 스토리 프롬프트 생성`

### 1. Credential 추가
1. n8n 왼쪽 **Settings** → **Credentials**
2. **Add Credential** 클릭
3. 검색창에 **Anthropic** 입력 후 **Anthropic API** 선택

### 2. 입력
- **Credential Name**: `Claude API` (원하는 이름 가능)
- **API Key**: `API_KEYS.txt`의 **## Claude API** 아래에 있는 키 전체 복사  
  (예: `sk-ant-api03-...` 로 시작하는 문자열)

### 3. Save 후 노드에 연결
1. **Workflows** → **Complete Pipeline - 스토리 단위** 열기
2. **Claude: 스토리 프롬프트 생성** 노드 더블클릭
3. **Credential to connect with** → 방금 만든 **Claude API** 선택
4. **Save** → 워크플로우 저장

---

## B. PostgreSQL (Railway)

**노드:** `PostgreSQL: 스토리 3개 조회 (순차)` 등 세 개

### 1단계: Credentials 메뉴 열기

1. n8n 로그인 후 **왼쪽 사이드바** 맨 아래 **Settings(설정)** 클릭  
2. 왼쪽에서 **Credentials** 클릭  
3. **Add Credential** 버튼 클릭  

(또는 상단 메뉴에서 **Credentials**가 있으면 그걸로 들어가도 됩니다.)

---

## 2단계: Postgres 선택

1. 검색창에 **postgres** 입력  
2. **Postgres** (또는 **PostgreSQL**) 선택  

---

## 3단계: 연결 정보 입력

아래 값을 **그대로** 입력합니다. (Railway PostgreSQL 연결 정보)

| 항목 | 입력할 값 |
|------|-----------|
| **Credential Name** | `Railway PostgreSQL` (원하면 다른 이름도 가능) |
| **Host** | `maglev.proxy.rlwy.net` |
| **Database** | `railway` |
| **User** | `postgres` |
| **Password** | (아래 비밀번호) |
| **Port** | `15087` |
| **SSL** | 필요하면 **Enable** (Railway는 보통 SSL 지원) |

**Password** 값: 프로젝트 루트의 `API_KEYS.txt` 파일에서 **## PostgreSQL** 아래 **Password:** 뒤에 적힌 값을 복사해 넣으면 됩니다.

---

## 4단계: 저장

1. **Save** 버튼 클릭  
2. Credential 목록에 `Railway PostgreSQL`이 보이면 완료  

---

## 5단계: 워크플로우 노드에 연결

1. **Workflows** → **Complete Pipeline - 스토리 단위** 워크플로우 열기  
2. 아래 세 노드를 **한 번씩** 더블클릭해서 열기:
   - **PostgreSQL: 스토리 3개 조회 (순차)**
   - **PostgreSQL: 스토리 프롬프트 저장**
   - **PostgreSQL: 최종 업데이트**  
3. 각 노드에서 **Credential to connect with** (또는 **연결할 Credential**) 드롭다운 클릭  
4. 방금 만든 **Railway PostgreSQL** 선택  
5. **Save**  
6. 워크플로우 **저장** 버튼 클릭  

---

---

## C. "Needs first setup" 해결 – Runway / Fish Audio / Hedra (Header Auth)

이 세 개는 **Header Auth** 타입이라, Credential을 열어 **Header 이름 + 값**만 채우면 됩니다.

### Runway API
1. **Runway API** Credential 더블클릭
2. **Header Auth** 섹션:
   - **Name**: `Authorization` (또는 `X-API-Key`)
   - **Value**: `API_KEYS.txt`의 **## Runway API** 아래 키  
     (예: `key_251946556723bdf0b9794eb0296b8f0be...` 전체)
3. **Save**

### Fish Audio API
1. **Fish Audio API** Credential 더블클릭
2. **Header Auth**:
   - **Name**: `Authorization` (또는 `X-API-Key`)
   - **Value**: `API_KEYS.txt`의 **## Fish Audio API** 아래 키  
     (예: `8024d34fa5b84ee59b74bc5440fd9922`)
3. **Save**

### Hedra API
1. **Hedra API** Credential 더블클릭
2. **Header Auth**:
   - **Name**: `X-API-Key` (Hedra는 보통 이 이름)
   - **Value**: `API_KEYS.txt`의 **## Hedra API** 아래 키  
     (예: `sk_hedra_H9RoTOX6ZvWtnctjIJ0ThjIA1gTWGa9F8Onc9EZFpupYkTiZaVzCCDZGJ51OMCvq`)
3. **Save**

---

## D. YouTube Data API (Google OAuth2) – "Needs first setup"

1. **YouTube Data API** Credential 더블클릭
2. **Sign in with Google** (또는 **Connect my account**) 클릭
3. 브라우저에서 Google 계정 로그인 → YouTube 권한 승인
4. n8n으로 돌아오면 연결 완료 → **Save**

(Client ID / Client Secret은 이미 들어가 있으면 건드리지 않아도 됩니다. `API_KEYS.txt`의 YouTube 섹션과 같으면 OK.)

---

## 요약

- **설정 완료로 보면 되는 것:** Anthropic, Railway PostgreSQL  
- **한 번 더 설정해야 하는 것:**  
  - **Runway / Fish Audio / Hedra** → Credential 열어서 Header **Name** + **Value**에 `API_KEYS.txt` 값 입력 후 Save  
  - **YouTube Data API** → Credential에서 **Sign in with Google** 눌러서 로그인·승인 후 Save
