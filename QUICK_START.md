---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# ⚡ 5분 빠른 시작 가이드

> 지금 당장 첫 번째 음악을 생성하는 방법!

---

## 🎯 목표: 5분 안에 첫 AI 음악 생성!

---

## Step 1: Suno 쿠키 가져오기 (2분)

### 방법
```
1. https://suno.com/ 접속 → 로그인
   (Pro 구독 필요: $10/월)

2. F12 (개발자 도구)

3. Application 탭 → Cookies → https://suno.com

4. 전체 Cookie 문자열 복사
   (예: "__session=abc123...")
```

---

## Step 2: Railway에 쿠키 설정 (2분)

### 방법
```
1. https://railway.app/ 접속

2. "The Musical Bible" 프로젝트 클릭

3. "suno-api" 서비스 클릭

4. "Variables" 탭 클릭

5. SUNO_COOKIE 값 업데이트:
   [복사한 쿠키 붙여넣기]

6. ✓ 버튼 클릭 (자동 저장)

7. 2분 대기 (재배포)
```

---

## Step 3: 첫 음악 생성! (1분)

### 방법
```
터미널에서 실행:

curl -X POST https://suno-api-production-ac35.up.railway.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "cinematic orchestral epic biblical instrumental 30 seconds",
    "make_instrumental": true,
    "wait_audio": false
  }'

결과:
{
  "id": "abc-123-def",
  "status": "processing"
}

3분 후 상태 확인:
curl https://suno-api-production-ac35.up.railway.app/api/get/abc-123-def

완료 시:
{
  "id": "abc-123-def",
  "status": "complete",
  "audio_url": "https://..."
}
```

---

## 🎉 완료!

첫 번째 AI 음악이 생성되었습니다!

---

## 🚀 다음 단계

### n8n으로 자동화하기
```
1. https://n8n-production-1d6b.up.railway.app 접속
   Email: xaqwer@gmail.com
   Password: Wkdrlgjs2@

2. Workflows → Import from File
   파일: workflows/suno_with_polling.json

3. Execute Workflow → 자동으로 음악 생성!
```

---

## 💡 프롬프트 예시

### 드라마틱한 음악
```json
{
  "prompt": "dramatic orchestral tension building epic cinematic 30 seconds instrumental"
}
```

### 평화로운 음악
```json
{
  "prompt": "peaceful serene gentle piano strings calm biblical 30 seconds instrumental"
}
```

### 웅장한 음악
```json
{
  "prompt": "majestic grand epic choir orchestral powerful biblical 30 seconds instrumental"
}
```

---

**⚡ 5분 만에 첫 AI 음악 생성 완료!**

더 자세한 내용은 `HOW_TO_USE.md`를 참고하세요!
