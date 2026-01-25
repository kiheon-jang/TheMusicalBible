# Video Processor API

The Musical Bible - FFmpeg 영상 합성 및 썸네일 생성 API 서버

## Railway 배포 방법

### 방법 1: Railway 웹 UI (권장)

1. [Railway.app](https://railway.app)에 로그인
2. 프로젝트 선택 (The Musical Bible)
3. **"New Service"** 클릭
4. **"GitHub Repo"** 선택
5. 저장소: `kiheon-jang/TheMusicalBible`
6. **Root Directory**: `video-processor-api` 설정
7. **Deploy** 클릭

### 방법 2: Railway CLI

```bash
cd video-processor-api
railway login
railway link
railway up
```

## 환경 변수

필요 없음 (기본값 사용)

## API 엔드포인트

### POST /api/compose
FFmpeg 영상 합성

**Request:**
```json
{
  "episode_id": "story_1_1234567890",
  "hedra_url": "https://...",
  "fish_url": "https://...",
  "suno_url": "https://...",
  "runway_url": "https://...",
  "scripture_text": "창세기 1:1",
  "book_info": "창세기 1:1-3",
  "output_dir": "/tmp/tmb_output"
}
```

**Response:**
```json
{
  "success": true,
  "video_path": "/tmp/tmb_output/story_1_1234567890_final.mp4",
  "episode_id": "story_1_1234567890",
  "output_dir": "/tmp/tmb_output"
}
```

### POST /api/thumbnail
썸네일 생성

**Request:**
```json
{
  "video_path": "/tmp/tmb_output/story_1_1234567890_final.mp4",
  "output_path": "/tmp/tmb_output/story_1_1234567890_thumbnail.jpg",
  "metadata": {
    "book_name": "창세기",
    "verses_range": "1:1-3",
    "emotion": "reverent",
    "character": "god"
  }
}
```

**Response:**
```json
{
  "success": true,
  "thumbnail_path": "/tmp/tmb_output/story_1_1234567890_thumbnail.jpg"
}
```

### GET /health
헬스 체크

## n8n 워크플로우 설정

배포 후 Railway에서 제공하는 URL을 n8n 환경 변수에 설정:

```
VIDEO_PROCESSOR_API_URL=https://video-processor-production-xxxx.up.railway.app
```

또는 워크플로우에서 직접 URL 수정:
- `FFmpeg: 영상 합성 (API)` 노드의 URL 필드
- `Python: 썸네일 생성 (API)` 노드의 URL 필드
