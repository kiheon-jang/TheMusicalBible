#!/usr/bin/env python3
"""
The Musical Bible - Video Processing API
FFmpeg 영상 합성 및 썸네일 생성을 HTTP API로 제공
"""

import os
import subprocess
import json
import tempfile
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="TMB Video Processor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 작업 디렉토리
WORK_DIR = Path("/tmp/tmb_video_processor")
WORK_DIR.mkdir(exist_ok=True)

class ComposeRequest(BaseModel):
    episode_id: str
    hedra_url: str
    fish_url: str
    suno_url: str
    runway_url: str = ""
    scripture_text: str = ""
    book_info: str = ""
    output_dir: str = "/tmp/tmb_output"

class ThumbnailRequest(BaseModel):
    video_path: str
    output_path: str
    metadata: dict

def download_file(url: str, output_path: str) -> bool:
    """URL에서 파일 다운로드"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"ERROR: 다운로드 실패 {url}: {e}")
        return False

@app.post("/api/compose")
async def compose_video(request: ComposeRequest):
    """FFmpeg 영상 합성"""
    try:
        output_dir = Path(request.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        temp_dir = output_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        # 파일 다운로드
        hedra_path = temp_dir / f"{request.episode_id}_hedra.mp4"
        fish_path = temp_dir / f"{request.episode_id}_voice.mp3"
        suno_path = temp_dir / f"{request.episode_id}_music.mp3"
        runway_path = temp_dir / f"{request.episode_id}_runway.mp4" if request.runway_url else None
        
        print(f"다운로드 시작: {request.episode_id}")
        
        if not download_file(request.hedra_url, str(hedra_path)):
            raise HTTPException(status_code=400, detail="Hedra 영상 다운로드 실패")
        if not download_file(request.fish_url, str(fish_path)):
            raise HTTPException(status_code=400, detail="Fish Audio 다운로드 실패")
        if not download_file(request.suno_url, str(suno_path)):
            raise HTTPException(status_code=400, detail="Suno 음악 다운로드 실패")
        if request.runway_url and runway_path:
            download_file(request.runway_url, str(runway_path))
        
        # FFmpeg 스크립트 실행
        script_path = Path("/data/scripts/ffmpeg_compose.sh")
        if not script_path.exists():
            script_path = Path("./scripts/ffmpeg_compose.sh")
        
        cmd = [
            "bash", str(script_path),
            request.episode_id,
            str(hedra_path),
            str(fish_path),
            str(suno_path),
            request.runway_url or "",
            str(output_dir)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(output_dir)
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"FFmpeg 실행 실패: {result.stderr}"
            )
        
        final_video = output_dir / f"{request.episode_id}_final.mp4"
        
        if not final_video.exists():
            raise HTTPException(status_code=500, detail="최종 영상 생성 실패")
        
        return {
            "success": True,
            "video_path": str(final_video),
            "video_url": f"/api/download/{request.episode_id}_final.mp4"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"영상 합성 실패: {str(e)}")

@app.post("/api/thumbnail")
async def generate_thumbnail(request: ThumbnailRequest):
    """썸네일 생성"""
    try:
        script_path = Path("/data/scripts/generate_thumbnail.py")
        if not script_path.exists():
            script_path = Path("./scripts/generate_thumbnail.py")
        
        metadata_json = json.dumps(request.metadata)
        
        cmd = [
            "python3", str(script_path),
            request.video_path,
            request.output_path,
            metadata_json
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"썸네일 생성 실패: {result.stderr}"
            )
        
        if not Path(request.output_path).exists():
            raise HTTPException(status_code=500, detail="썸네일 파일 생성 실패")
        
        return {
            "success": True,
            "thumbnail_path": request.output_path,
            "thumbnail_url": f"/api/download/{Path(request.output_path).name}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"썸네일 생성 실패: {str(e)}")

@app.get("/health")
async def health():
    """헬스 체크"""
    return {"status": "ok", "ffmpeg": shutil.which("ffmpeg") is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
