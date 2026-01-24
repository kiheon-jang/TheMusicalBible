#!/bin/bash
# FFmpeg 3단계 시네마틱 합성 스크립트
# The Musical Bible (TMB) - 30초 3단계 구조 영상 생성

# 입력 파라미터
EPISODE_ID=$1
SCRIPTURE_TEXT=$2   # 성경 구절 텍스트 (자막용)
BOOK_INFO=$3        # 책 정보 (예: "창세기 22:1")
HEDRA_VIDEO=$4      # Hedra 립싱크 영상 (URL 또는 로컬)
VOICE_AUDIO=$5      # Fish Audio 음성 (URL 또는 로컬)
MUSIC_AUDIO=$6      # Suno 배경음악 (URL 또는 로컬)
RUNWAY_VIDEO=$7     # Runway 배경 영상 (선택, URL 또는 로컬)
OUTPUT_DIR=$8       # 출력 디렉토리

# Phase 시간 설정 (초)
PHASE1_END=8
PHASE2_END=18
PHASE3_END=30

# 기본값 설정
if [ -z "$OUTPUT_DIR" ]; then
  OUTPUT_DIR="./output"
fi

mkdir -p "$OUTPUT_DIR"
mkdir -p "${OUTPUT_DIR}/temp"

# 중간 파일 경로
PHASE1_VIDEO="${OUTPUT_DIR}/temp/${EPISODE_ID}_phase1.mp4"
PHASE2_VIDEO="${OUTPUT_DIR}/temp/${EPISODE_ID}_phase2.mp4"
PHASE3_VIDEO="${OUTPUT_DIR}/temp/${EPISODE_ID}_phase3.mp4"
PHASE_CONCAT="${OUTPUT_DIR}/temp/${EPISODE_ID}_concat.mp4"
MIXED_AUDIO="${OUTPUT_DIR}/temp/${EPISODE_ID}_audio_mixed.mp3"
FINAL_VIDEO="${OUTPUT_DIR}/${EPISODE_ID}_final.mp4"

echo "=== 3단계 시네마틱 합성 시작: ${EPISODE_ID} ==="

# 함수: URL인지 확인하고 다운로드
download_if_url() {
  local input=$1
  local output=$2
  
  if [[ $input =~ ^https?:// ]]; then
    echo "다운로드 중: $input"
    curl -sL "$input" -o "$output"
    if [ $? -ne 0 ]; then
      echo "ERROR: 다운로드 실패: $input"
      return 1
    fi
    echo "$output"
  else
    echo "$input"
  fi
}

# 파일 다운로드
echo "Step 0: 파일 준비 중..."
HEDRA_LOCAL=$(download_if_url "$HEDRA_VIDEO" "${OUTPUT_DIR}/temp/${EPISODE_ID}_hedra.mp4")
VOICE_LOCAL=$(download_if_url "$VOICE_AUDIO" "${OUTPUT_DIR}/temp/${EPISODE_ID}_voice.mp3")
MUSIC_LOCAL=$(download_if_url "$MUSIC_AUDIO" "${OUTPUT_DIR}/temp/${EPISODE_ID}_music.mp3")

if [ -n "$RUNWAY_VIDEO" ]; then
  RUNWAY_LOCAL=$(download_if_url "$RUNWAY_VIDEO" "${OUTPUT_DIR}/temp/${EPISODE_ID}_runway.mp4")
fi

# 파일 존재 확인
if [ ! -f "$HEDRA_LOCAL" ]; then
  echo "ERROR: Hedra 영상 없음"
  exit 1
fi

if [ ! -f "$VOICE_LOCAL" ]; then
  echo "ERROR: 음성 파일 없음"
  exit 1
fi

if [ ! -f "$MUSIC_LOCAL" ]; then
  echo "ERROR: 음악 파일 없음"
  exit 1
fi

# ==============================================
# Phase 1: Scripture Context (0-8초)
# - Runway 배경 영상 (또는 Hedra)
# - 성경 구절 자막 (fade in/out)
# - 배경음악 30% 볼륨
# ==============================================
echo "=== Phase 1: Scripture Context (0-8초) ==="

if [ -n "$RUNWAY_LOCAL" ] && [ -f "$RUNWAY_LOCAL" ]; then
  VIDEO_SOURCE="$RUNWAY_LOCAL"
else
  VIDEO_SOURCE="$HEDRA_LOCAL"
fi

# 자막 텍스트 파일 생성
SUBTITLE_FILE="${OUTPUT_DIR}/temp/${EPISODE_ID}_subtitle.srt"
cat > "$SUBTITLE_FILE" << EOF
1
00:00:01,000 --> 00:00:07,000
${BOOK_INFO}

2
00:00:02,000 --> 00:00:07,000
${SCRIPTURE_TEXT}
EOF

# Phase 1 영상 생성 (자막 오버레이)
ffmpeg -i "$VIDEO_SOURCE" \
  -vf "subtitles=${SUBTITLE_FILE}:force_style='FontName=NanumGothic,FontSize=28,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Alignment=2,MarginV=50'" \
  -c:v libx264 -crf 18 -preset medium \
  -t $PHASE1_END \
  -an \
  "$PHASE1_VIDEO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: Phase 1 영상 생성 실패"
  exit 1
fi

# ==============================================
# Phase 2: Atmosphere & Tension (8-18초)
# - Hedra 인물 영상 (무음 또는 짧은 숨소리)
# - 배경음악 50% → 70% 크레센도
# ==============================================
echo "=== Phase 2: Atmosphere & Tension (8-18초) ==="

ffmpeg -i "$HEDRA_LOCAL" \
  -ss 0 -t 10 \
  -c:v libx264 -crf 18 -preset medium \
  -an \
  "$PHASE2_VIDEO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: Phase 2 영상 생성 실패"
  exit 1
fi

# ==============================================
# Phase 3: Aria & Grand Finale (18-30초)
# - Hedra 립싱크 영상
# - Fish Audio 음성 100%
# - 배경음악 100% 풀볼륨
# ==============================================
echo "=== Phase 3: Aria & Grand Finale (18-30초) ==="

ffmpeg -i "$HEDRA_LOCAL" \
  -ss 0 -t 12 \
  -c:v libx264 -crf 18 -preset medium \
  -an \
  "$PHASE3_VIDEO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: Phase 3 영상 생성 실패"
  exit 1
fi

# ==============================================
# 영상 결합 (Phase 1 + 2 + 3)
# ==============================================
echo "=== 영상 결합 중 ==="

# concat 파일 리스트 생성
CONCAT_LIST="${OUTPUT_DIR}/temp/${EPISODE_ID}_list.txt"
cat > "$CONCAT_LIST" << EOF
file '${PHASE1_VIDEO}'
file '${PHASE2_VIDEO}'
file '${PHASE3_VIDEO}'
EOF

ffmpeg -f concat -safe 0 -i "$CONCAT_LIST" \
  -c:v copy \
  "$PHASE_CONCAT" -y

if [ $? -ne 0 ]; then
  echo "ERROR: 영상 결합 실패"
  exit 1
fi

# ==============================================
# 오디오 믹싱 (3단계 볼륨 조절)
# Phase 1: 음악 30%
# Phase 2: 음악 50% → 70% (페이드인)
# Phase 3: 음성 100% + 음악 100%
# ==============================================
echo "=== 오디오 믹싱 (3단계 볼륨) ==="

ffmpeg -i "$MUSIC_LOCAL" -i "$VOICE_LOCAL" \
  -filter_complex "
    [0:a]volume=0.3:eval=frame:enable='between(t,0,${PHASE1_END})'[music_phase1];
    [0:a]volume='0.5+(t-${PHASE1_END})/(${PHASE2_END}-${PHASE1_END})*0.2':eval=frame:enable='between(t,${PHASE1_END},${PHASE2_END})'[music_phase2];
    [0:a]volume=1.0:eval=frame:enable='gte(t,${PHASE2_END})'[music_phase3];
    [music_phase1][music_phase2][music_phase3]concat=n=3:v=0:a=1[music];
    [1:a]adelay=${PHASE2_END}000|${PHASE2_END}000[voice];
    [music][voice]amix=inputs=2:duration=first:dropout_transition=2[out]
  " \
  -map "[out]" \
  -c:a aac -b:a 192k -ar 44100 \
  -t $PHASE3_END \
  "$MIXED_AUDIO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: 오디오 믹싱 실패"
  exit 1
fi

# ==============================================
# 최종 합성 (영상 + 오디오)
# ==============================================
echo "=== 최종 합성 중 ==="

ffmpeg -i "$PHASE_CONCAT" -i "$MIXED_AUDIO" \
  -c:v copy \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  "$FINAL_VIDEO" -y

if [ $? -ne 0 ]; then
  echo "ERROR: 최종 합성 실패"
  exit 1
fi

# ==============================================
# 완료 및 정리
# ==============================================
echo "=== 합성 완료 ==="
echo "최종 영상: $FINAL_VIDEO"

# 영상 정보 출력
if command -v ffprobe &> /dev/null; then
  echo "영상 정보:"
  ffprobe -v quiet -show_entries format=duration:stream=width,height -of default=noprint_wrappers=1 "$FINAL_VIDEO"
fi

# 임시 파일 정리
echo "임시 파일 정리 중..."
rm -rf "${OUTPUT_DIR}/temp"

echo "=== 3단계 시네마틱 합성 완료! ==="
