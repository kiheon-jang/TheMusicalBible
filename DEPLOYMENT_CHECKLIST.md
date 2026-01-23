# The Musical Bible (TMB) - 배포 체크리스트

## ✅ 완료된 작업

- [x] 프로젝트 구조 생성
- [x] SQLite 데이터베이스 스키마 작성
- [x] 샘플 성경 데이터 스크립트 작성
- [x] FFmpeg 영상 합성 스크립트 작성
- [x] Python 썸네일 생성 스크립트 작성
- [x] n8n 워크플로우 3개 작성 (Morning Batch, Evening Generation, Daily Monitoring)
- [x] Railway Dockerfile 작성
- [x] 설정 가이드 작성

## 📋 배포 전 체크리스트

### 1. Railway 프로젝트 확인

현재 n8n URL: `https://n8n-production-1d6b.up.railway.app`

이 URL이 이미 존재하므로, 다음을 확인하세요:

- [ ] Railway 대시보드에서 해당 프로젝트 확인
- [ ] 서비스 상태 확인 (Running)
- [ ] 환경 변수 확인

### 2. 데이터베이스 초기화

Railway 터미널에서 실행:

```bash
# 데이터베이스 디렉토리 생성
mkdir -p /data/database

# 스키마 생성
sqlite3 /data/database/scripture.db < /data/database/init.sql

# 샘플 데이터 입력
sqlite3 /data/database/scripture.db < /data/database/seed_data.sql
```

또는 n8n 워크플로우에서 SQLite 노드를 사용하여 직접 실행할 수 있습니다.

### 3. API Credentials 설정

n8n 대시보드 (`https://n8n-production-1d6b.up.railway.app`)에서:

- [ ] Claude API Credential 추가
- [ ] Hedra Pro API Credential 추가
- [ ] Suno Pro API Credential 추가
- [ ] Fish Audio API Credential 추가
- [ ] Runway API Credential 추가
- [ ] YouTube OAuth2 Credential 추가
- [ ] Google Sheets OAuth2 Credential 추가 (선택)

### 4. 워크플로우 임포트

n8n에서:

- [ ] `workflows/morning_batch.json` 임포트
- [ ] `workflows/evening_generation.json` 임포트
- [ ] `workflows/daily_monitoring.json` 임포트

각 워크플로우에서:

- [ ] SQLite Credential 연결
- [ ] 각 API Credential 연결
- [ ] 경로 및 설정 확인

### 5. 스크립트 배포

Railway에서:

- [ ] `scripts/ffmpeg_compose.sh` 파일 업로드
- [ ] `scripts/generate_thumbnail.py` 파일 업로드
- [ ] 실행 권한 부여: `chmod +x scripts/*.sh scripts/*.py`

### 6. 테스트 실행

각 워크플로우를 수동으로 실행하여 테스트:

- [ ] Morning Batch: SQLite 조회 → Claude API 호출
- [ ] Evening Generation: 전체 파이프라인 테스트 (비용 발생 주의)
- [ ] Daily Monitoring: YouTube Analytics 수집

### 7. 자동화 활성화

- [ ] Morning Batch: Active ON, Schedule `0 2 * * *`
- [ ] Evening Generation: Active ON, Schedule `0 14 * * *`
- [ ] Daily Monitoring: Active ON, Schedule `0 10 * * *`

## 🔧 Railway 특정 설정

### 환경 변수 확인

Railway 대시보드에서 다음 환경 변수가 설정되어 있는지 확인:

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=[설정한 비밀번호]
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n-production-1d6b.up.railway.app
DB_SQLITE_PATH=/data/database/scripture.db
```

### 볼륨 마운트 확인

- [ ] `/data` 볼륨이 마운트되어 있는지 확인
- [ ] 데이터베이스 파일이 영구 저장되는지 확인

### FFmpeg 및 Python 확인

Railway 터미널에서:

```bash
ffmpeg -version  # FFmpeg 설치 확인
python3 --version  # Python 버전 확인
pip3 list | grep Pillow  # Pillow 설치 확인
```

## 📝 다음 단계

1. **성경 데이터 확장**
   - `database/seed_data.sql`에 더 많은 구절 추가
   - 최소 1,000개 구절 목표

2. **캐릭터 Identity Anchor 이미지**
   - DALL-E 3로 각 캐릭터 이미지 생성
   - S3 또는 로컬에 저장
   - `character_voices` 테이블에 경로 업데이트

3. **음성 품질 테스트**
   - Fish Audio에서 각 캐릭터별 음성 테스트
   - voice_id 확인 및 저장

4. **YouTube 채널 설정**
   - 채널 설명 작성
   - 썸네일 템플릿 생성
   - 플레이리스트 생성

5. **모니터링 대시보드**
   - Google Sheets 또는 다른 도구로 통계 시각화
   - 일일/주간 리포트 자동 생성

## ⚠️ 주의사항

1. **비용 관리**
   - Evening Generation 워크플로우는 실제 API 호출을 하므로 비용 발생
   - 테스트 시에는 1개 에피소드만 생성
   - 예비비 9.5만 원은 재시도 및 복구용

2. **API Rate Limit**
   - 각 API별 Rate Limit 확인
   - 월 50개 목표에 맞는 구독 플랜 확인

3. **데이터 백업**
   - SQLite 데이터베이스 정기 백업
   - Railway 볼륨 스냅샷 설정

4. **보안**
   - API 키는 n8n Credentials에만 저장
   - 환경 변수에 민감 정보 저장 금지
   - n8n 접속 비밀번호 강력하게 설정

## 🆘 문제 해결

### n8n 접속 불가
- Railway 로그 확인
- 환경 변수 `N8N_HOST=0.0.0.0` 확인
- 포트 `5678` 확인

### SQLite 오류
- 데이터베이스 파일 경로 확인
- 파일 권한 확인: `chmod 666 /data/database/scripture.db`
- 볼륨 마운트 확인

### API 호출 실패
- Credentials에서 API 키 확인
- Rate Limit 확인
- 네트워크 연결 확인

### FFmpeg 오류
- FFmpeg 설치 확인
- 스크립트 실행 권한 확인
- 파일 경로 확인

## 📞 지원

문제 발생 시:
1. Railway 로그 확인
2. n8n 실행 이력 확인
3. SQLite 데이터베이스 직접 조회
4. 각 API 문서 참조

**배포 성공을 기원합니다!** 🎬✨
