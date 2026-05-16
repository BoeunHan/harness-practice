import json

from tools.claude import run_claude


# fmt: off
def reviewer_agent(task, files):
    prompt = f"""
너는 구현 결과를 검토하는 Reviewer이다.

변경 사항이 Task 요구사항과 Acceptance Criteria를 정확히 만족하는지 검증한다.


Task:
{task}

Changed Files:
{files}


역할:
- 요구사항 충족 여부를 확인한다.
- 논리적 오류를 탐지한다.
- 누락된 구현을 확인한다.
- 중복 구현이나 비효율적인 구현을 확인한다.
- dependency 문제를 탐지한다.
- 테스트 필요 여부를 판단한다.

규칙:
- 실제 task 목표 기준으로 평가한다.
- 구현 범위 초과 여부도 확인한다.
- "기능/로직/의도 불일치"할 경우 reject한다.
- 모호한 경우 이유를 명확히 설명한다.
- 각 문제에 대한 수정 방향을 포함한다.
- 추측 기반 판단은 금지한다.
- rejected인 경우 최소 하나 이상의 retry_issues를 포함한다.
- 결과는 반드시 JSON 형식으로 반환한다.
- JSON 외의 다른 설명은 포함하지 않는다.
- 설명이 필요한 경우 JSON 내 적절한 위치에 포함한다.

반환 형식:
{{
  "task_id": "",
  "result": "approved | rejected",
  "retry_issues": [
    {{
      "type": "logic | missing_feature | dependency | performance | duplication | interface_mismatch",
      "file": "",
      "description": "",
      "expected_behavior": "",
      "actual_behavior": "",
      "fix_suggestion": ""
    }}
  ],
  "positive_notes": []
}}

"""

    return json.loads(run_claude(prompt))
