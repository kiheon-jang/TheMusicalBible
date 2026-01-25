#!/usr/bin/env python3
"""
The Musical Bible (TMB) - 썸네일 자동 생성 스크립트
영상에서 중간 프레임을 추출하고 텍스트 오버레이를 추가합니다.
"""

import sys
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import json

def extract_frame(video_path: str, output_path: str, timestamp: str = "00:00:15") -> bool:
    """
    영상에서 특정 시점의 프레임을 추출합니다.
    
    Args:
        video_path: 입력 영상 경로
        output_path: 출력 이미지 경로
        timestamp: 추출할 시점 (HH:MM:SS 형식)
    
    Returns:
        성공 여부
    """
    try:
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-ss', timestamp,
            '-vf', 'scale=1280:720',
            '-vframes', '1',
            '-y',  # 덮어쓰기
            output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: 프레임 추출 실패: {e.stderr}", file=sys.stderr)
        return False

def add_text_overlay(image_path: str, output_path: str, metadata: dict) -> bool:
    """
    이미지에 텍스트 오버레이를 추가합니다.
    
    Args:
        image_path: 입력 이미지 경로
        output_path: 출력 이미지 경로
        metadata: 메타데이터 딕셔너리
            - book_name: 책 이름 (예: "창세기")
            - chapter: 장 번호
            - verse: 절 번호
            - emotion: 감정 (예: "fear", "hope")
            - character: 캐릭터 이름 (예: "abraham")
    
    Returns:
        성공 여부
    """
    try:
        # 이미지 열기
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # 폰트 설정 (시스템 기본 폰트 사용)
        try:
            # macOS/Linux
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 60)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
        except:
            try:
                # Linux alternative
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                # 기본 폰트 (폰트 파일을 찾을 수 없는 경우)
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
        
        # 제목 텍스트 (verses_range 우선, 없으면 chapter:verse)
        verses_range = metadata.get('verses_range', '')
        if verses_range:
            title = f"{metadata.get('book_name', '')} {verses_range}"
        else:
            title = f"{metadata.get('book_name', '')} {metadata.get('chapter', '')}:{metadata.get('verse', '')}"
        
        # 감정 이모지 매핑
        emotion_emoji = {
            'fear': '😨',
            'hope': '✨',
            'joy': '😊',
            'sorrow': '😢',
            'awe': '🙏',
            'anger': '😠',
            'resolve': '💪',
            'compassion': '❤️',
            'curiosity': '🤔',
            'struggle': '⚔️',
            'acceptance': '🙌'
        }
        emotion = metadata.get('emotion', '')
        emoji = emotion_emoji.get(emotion, '🎬')
        
        # 텍스트 위치 계산 (중앙 정렬)
        img_width, img_height = img.size
        
        # 배경 박스 그리기 (반투명)
        box_padding = 20
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        
        box_x = (img_width - title_width) // 2 - box_padding
        box_y = img_height - 200 - box_padding
        box_width = title_width + box_padding * 2
        box_height = title_height + 100 + box_padding * 2
        
        # 반투명 배경
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [box_x, box_y, box_x + box_width, box_y + box_height],
            fill=(0, 0, 0, 180)  # 반투명 검은색
        )
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # 제목 텍스트 그리기
        title_x = (img_width - title_width) // 2
        title_y = img_height - 180
        draw.text((title_x, title_y), title, fill="white", font=title_font)
        
        # 감정 이모지 + 캐릭터 이름
        if metadata.get('character'):
            character_name = metadata.get('character', '').capitalize()
            subtitle = f"{emoji} {character_name}"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (img_width - subtitle_width) // 2
            subtitle_y = img_height - 120
            draw.text((subtitle_x, subtitle_y), subtitle, fill="gold", font=subtitle_font)
        
        # 저장
        img.save(output_path, quality=95)
        return True
        
    except Exception as e:
        print(f"ERROR: 썸네일 생성 실패: {e}", file=sys.stderr)
        return False

def main():
    """
    메인 함수
    사용법: python generate_thumbnail.py <video_path> <output_path> <metadata_json>
    """
    if len(sys.argv) < 4:
        print("사용법: python generate_thumbnail.py <video_path> <output_path> <metadata_json>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2]
    metadata_json = sys.argv[3]
    
    # 메타데이터 파싱
    try:
        metadata = json.loads(metadata_json)
    except json.JSONDecodeError:
        print("ERROR: 메타데이터 JSON 파싱 실패", file=sys.stderr)
        sys.exit(1)
    
    # 중간 프레임 추출
    temp_frame_path = output_path.replace('.jpg', '_temp.jpg')
    if not extract_frame(video_path, temp_frame_path):
        sys.exit(1)
    
    # 텍스트 오버레이 추가
    if not add_text_overlay(temp_frame_path, output_path, metadata):
        sys.exit(1)
    
    # 임시 파일 삭제
    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)
    
    print(f"SUCCESS: 썸네일 생성 완료: {output_path}")

if __name__ == "__main__":
    main()
