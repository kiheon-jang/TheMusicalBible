#!/bin/bash
# The Musical Bible - 스토리 모드 자동 설치 스크립트
# 이 스크립트 하나로 모든 설정 완료!

set -e  # 에러 시 중단

echo "=================================================="
echo "📖 The Musical Bible - 스토리 모드 전환"
echo "=================================================="

# 환경 변수 확인
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL 환경 변수가 설정되지 않았습니다"
    echo "   Railway 대시보드에서 PostgreSQL 연결 문자열을 복사하세요"
    echo ""
    echo "   설정 방법:"
    echo "   export DATABASE_URL='postgresql://user:pass@host:port/railway'"
    exit 1
fi

if [ -z "$CLAUDE_API_KEY" ]; then
    echo "❌ CLAUDE_API_KEY 환경 변수가 설정되지 않았습니다"
    echo ""
    echo "   설정 방법:"
    echo "   export CLAUDE_API_KEY='sk-ant-...'"
    exit 1
fi

echo ""
echo "✅ 환경 변수 확인 완료"
echo ""

# Step 1: DB 스키마 생성
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Step 1/4: 스토리 단위 DB 스키마 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

psql "$DATABASE_URL" < database/story_units_schema.sql

if [ $? -eq 0 ]; then
    echo "✅ story_units 테이블 생성 완료"
else
    echo "❌ DB 스키마 생성 실패"
    exit 1
fi

echo ""

# Step 2: Python 패키지 확인
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Step 2/4: Python 패키지 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

pip install -q anthropic psycopg2-binary requests

echo "✅ 필요한 패키지 설치 완료"
echo ""

# Step 3: 테스트 분석 (창세기 1-5장)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Step 3/4: 테스트 분석 (창세기 1-5장)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 scripts/analyze_story_units.py --test

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 스토리 분석 완료"
else
    echo "❌ 스토리 분석 실패"
    exit 1
fi

echo ""

# Step 4: 결과 확인
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Step 4/4: 결과 확인"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

psql "$DATABASE_URL" -c "
SELECT 
    id, 
    book_name, 
    verses_range, 
    title, 
    verse_count, 
    estimated_duration_sec 
FROM story_units 
ORDER BY id 
LIMIT 10;
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 통계
TOTAL_STORIES=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM story_units;")
TOTAL_VERSES=$(psql "$DATABASE_URL" -t -c "SELECT SUM(verse_count) FROM story_units;")
AVG_DURATION=$(psql "$DATABASE_URL" -t -c "SELECT ROUND(AVG(estimated_duration_sec)) FROM story_units;")

echo ""
echo "📊 통계:"
echo "  - 총 스토리: $TOTAL_STORIES 개"
echo "  - 총 구절: $TOTAL_VERSES 개"
echo "  - 평균 길이: $AVG_DURATION 초"
echo ""

# 다음 단계 안내
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 설치 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 다음 단계:"
echo ""
echo "1. n8n 워크플로우 임포트:"
echo "   - Railway n8n 대시보드 열기"
echo "   - 'Import' 클릭"
echo "   - workflows/complete_pipeline_story.json 선택"
echo "   - Credentials 연결"
echo ""
echo "2. 추가 분석 (선택):"
echo "   # 창세기 전체"
echo "   python3 scripts/analyze_story_units.py --genesis"
echo ""
echo "   # 전체 성경 (비용: ~\$70)"
echo "   python3 scripts/analyze_story_units.py --all"
echo ""
echo "3. 테스트 실행:"
echo "   - n8n에서 'Execute Workflow' 클릭"
echo "   - 첫 스토리 영상 생성 확인"
echo ""
echo "=================================================="
