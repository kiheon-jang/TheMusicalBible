# 스토리 프롬프트 저장 시 "데이터가 아예 없다" 해결

## 0. "스토리 3개 조회"에서 "1 item, No fields" 나올 때

**PostgreSQL: 스토리 3개 조회 (순차)** 노드가 **Success, Input 1 item, No fields** 로 나오면,  
SELECT 결과가 **0건**이라는 뜻입니다. n8n이 빈 결과를 "항목 1개, 필드 없음"으로 표시하는 경우입니다.

### 원인 후보

1. **pending 스토리가 없음**  
   `story_units`에 `status = 'pending'`인 행이 하나도 없음.
2. **book_order와 매칭 안 됨**  
   조회 쿼리가 `story_units`와 `book_order`를 `book_name = book_name_korean`으로 JOIN하므로,  
   `book_order`가 비어 있거나 `book_name_korean`이 `story_units.book_name`과 맞지 않으면 0건.

### 확인 및 조치

```bash
# 1) story_units 전체 개수
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM story_units;"

# 2) pending 개수
psql "$DATABASE_URL" -c "SELECT id, title, status FROM story_units WHERE status = 'pending';"

# 3) book_order 존재 여부
psql "$DATABASE_URL" -c "SELECT book_name_korean FROM book_order LIMIT 5;"
```

- **pending이 0건이면**  
  - 이미 처리된 스토리를 다시 돌리려면:  
    `UPDATE story_units SET status = 'pending' WHERE id IN (1,2,3);` (원하는 id로)
  - 새 스토리를 넣으려면:  
    `python3 scripts/analyze_story_units.py --test` 등으로 스토리 생성 후,  
    해당 행의 `status`가 `pending`인지 확인.
- **book_order가 비어 있으면**  
  - `database/book_order.sql` 적용 여부 확인 후,  
  - `psql "$DATABASE_URL" -f database/book_order.sql` 로 데이터 넣기.

---

## 1. pending 스토리가 있는지 확인

워크플로우는 **`status = 'pending'`** 인 `story_units` 행만 조회합니다.  
해당 행이 없으면 조회 결과가 0건이라 이후 단계가 실행되지 않고, DB에 저장되는 데이터도 없습니다.

```bash
# PostgreSQL에서 확인
psql "$DATABASE_URL" -c "SELECT id, title, status FROM story_units WHERE status = 'pending';"
```

- **0건이면**: pending 상태 스토리를 먼저 넣어야 합니다.
  - 예: `analyze_story_units.py`로 스토리 생성 후, 필요 시 `UPDATE story_units SET status = 'pending' WHERE ...` 로 상태 변경
- **1건 이상이면**: 조회는 정상이므로 아래 2번으로 진행합니다.

## 2. 디버그 노드 로그 확인

워크플로우에 **"디버그: 스토리 저장 전"** Code 노드가 있습니다.  
워크플로우 실행 후 n8n 실행 로그(또는 해당 노드 출력)에서 다음을 확인하세요.

- `[디버그] story_id:`  
  - 숫자가 나오면 정상.  
  - `undefined` / `null` 이면 `story_id`가 전달되지 않은 것이므로, **"Claude 요청 본문 준비"** 입력 데이터에 `id`(또는 `story_id`)가 포함되는지 확인합니다.
- `[디버그] narrative_structure 존재:`  
  - `true` 이면 Claude 응답 파싱은 된 것입니다.
- `[디버그] 오류: story_id가 없습니다`  
  - 이 메시지가 보이면, **PostgreSQL 쿼리 생성** 노드에서 `story_id` 부재로 에러를 던지도록 되어 있으므로, 그 전 단계(스토리 프롬프트 파싱 / Claude 요청 본문 준비)에서 `id` 전달 여부를 점검해야 합니다.

## 3. 적용한 수정 사항

- **스토리 프롬프트 파싱**: `story_id`를 `original.id ?? original.story_id` 로 설정해, 둘 중 하나라도 있으면 사용합니다.
- **PostgreSQL 쿼리 생성**: `story_id`를 정수로 변환하고, 없거나 유효하지 않으면 에러를 발생시켜 원인 파악이 쉽도록 했습니다.
- **디버그 노드**: "스토리 프롬프트 파싱" 바로 다음에 "디버그: 스토리 저장 전"을 두어, 저장 직전 `story_id`와 필수 필드를 로그로 확인할 수 있게 했습니다.

워크플로우를 다시 import한 뒤 실행하고, 위 순서대로 확인해 보세요.
