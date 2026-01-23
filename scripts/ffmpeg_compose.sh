#!/bin/bash
# FFmpeg 영상 합성 스크립트
# The Musical Bible (TMB) - 30초 최종 영상 생성

# 입력 파라미터
EPISODE_ID=$1
HEDRA_VIDEO=$2      # Hedra에서 생성된 5초 영상
VOICE_AUDIO=$3      # Fish Audio에서 생성된 음성
MUSIC_AUDIO=$4      # Suno에서 생성된 배경음악
RUNWAY_VIDEO=$5     # Runway 배경 영상 (선택사항)
OUTPUT_DIR=$6       # 출력 디렉토리

# 기본값 설정
if [ -z "$OUTPUT_DIR" ]; then
  OUTPUT_DIR="./output"
fi

mkdir -p "$OUTPUT_DIR"

# 중간 파일 경로
STRETCHED_VIDEO="${OUTPUT_DIR}/${EPISODE_ID}_stretched.mp4"
MIXED_AUDIO="${OUTPUT_DIR}/${EPISODE_ID}_audio_mixed.mp3"
FINAL_VIDEO="${OUTPUT_DIR}/${EPISODE_ID}_final.mp4"

echo "=== FFmpeg 합성 시작: ${EPISODE_ID} ==="

# Step 1: 비디오 속도 조절 (5초 → 30초)
# setpts=6.0*PTS: 속도를 1/6로 줄임
echo "Step 1: 비디오 속도 조절 (5초 → 30초)..."
if [ -n "$RUNWAY_VIDEO" ] && [ -f "$RUNWAY_VIDEO" ]; then
  # Runway 배경 영상이 있는 경우: Hedra 영상과 합성
  ffmpeg -i "$HEDRA_VIDEO" -i "$RUNWAY_VIDEO" \
    -filter_complex "[0:v]scale=1920:1080,setpts=6.0*PTS[v0];[1:v]scale=1920:1080,setpts=6.0*PTS[v1];[v0][v1]blend=all_mode=overlay:all_opacity=0.3[v]" \
    -map "[v]" \
    -c:v libx264 -crf 18 -preset medium \
    -t 30 \
    "$STRETCHED_VIDEO" -y
else
  # Runway 배경 영상이 없는 경우: Hedra 영상만 사용
  ffmpeg -i "$HEDRA_VIDEO" \
    -filter:v "scale=1920:1080,setpts=6.0*PTS" \
    -c:v libx264 -crf 18 -preset medium \
    -t 30 \
    "$STRETCHED_VIDEO" -y
fi

if [ $? -ne 0 ]; then
  echo "ERROR: Step 1 실패"
  exit 1
fi

# Step 2: 음성 + 배경음악 믹싱
# 음성: 100% 볼륨, 배경음악: 30% 볼륨
echo "Step 2: 음성 + 배경음악 믹싱..."
ffmpeg -i "$VOICE_AUDIO" -i "$MUSIC_AUDIO" \
  -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.3,aloop=loop=-1:size=2e+09[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=2[out]" \
  -map "[out]" \
  -c:a aac -b:a 192k -ar 44100 \
  -t 30 \
  "$MIXED_AUDIO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: Step 2 실패"
  exit 1
fi

# Step 3: 영상 + 오디오 최종 합성
echo "Step 3: 영상 + 오디오 최종 합성..."
ffmpeg -i "$STRETCHED_VIDEO" -i "$MIXED_AUDIO" \
  -c:v copy \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  -t 30 \
  "$FINAL_VIDEO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: Step 3 실패"
  exit 1
fi

# 최종 영상 정보 출력
echo "=== 합성 완료 ==="
echo "최종 영상: $FINAL_VIDEO"
ffprobe -v quiet -print_format json -show_format -show_streams "$FINAL_VIDEO" | jq -r '.format.duration, .streams[0].width, .streams[0].height'

# 중간 파일 정리 (선택사항)
# rm -f "$STRETCHED_VIDEO" "$MIXED_AUDIO"

echo "=== FFmpeg 합성 완료 ==="
