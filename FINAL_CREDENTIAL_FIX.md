---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 🔧 Credential 연결 문제 해결 (최종)

## 📊 문제 원인

```
여러 개의 중복된 Anthropic credential이 생성되어
잘못된 ID가 연결됨:

❌ Anthropic account 3 (ID: MLUKBLVTiBwYuO9d) - 존재하지 않음!
✅ Anthropic account (올바른 것) - 연결 필요!
```

---

## 🎯 해결 방법 (30초!)

### Step 1: 강력 새로고침
- Mac: **Cmd + Shift + R**
- Windows: **Ctrl + Shift + R**

### Step 2: Credentials 페이지 정리
1. 좌측 메뉴 → **Credentials** 클릭
2. 중복된 Anthropic credentials 확인
3. 가장 최근에 만든 **하나만 남기고** 나머지 삭제

### Step 3: 워크플로우에서 연결
1. 워크플로우로 돌아가기
2. **Claude** 노드 더블클릭
   - Credential 드롭다운 → 남은 Anthropic credential 선택
3. **PostgreSQL** 노드들 더블클릭 (2개)
   - Credential 드롭다운 → Railway PostgreSQL 선택
4. 우측 상단 **Save** 클릭

### Step 4: 실행!
- **Execute Workflow** 클릭
- 10-20초 대기
- ✅ 성공!

---

## 💡 또는 간단한 방법

제가 지금 브라우저 자동화로 시도하겠습니다!
