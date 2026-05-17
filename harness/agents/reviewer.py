import json

from tools.claude import run_claude


# fmt: off
def reviewer_agent(task, files):
    prompt = f"""
너는 구현 결과를 검토하는 Reviewer이다.

변경 사항이 Task 요구사항과 Acceptance Criteria를 정확히 만족하는지 검증한다.


Task:
{json.dumps(task, ensure_ascii=False, indent=2)}

Changed Files:
{json.dumps(files, ensure_ascii=False, indent=2)}


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
- "기능/로직/의도 불일치"할 경우 failed한다.
- 모호한 경우 이유를 명확히 설명한다.
- 각 문제에 대한 수정 방향을 포함한다.
- 추측 기반 판단은 금지한다.
- failed인 경우 최소 하나 이상의 issues를 포함한다.
- **file path는 프로젝트 루트 기준 상대 경로로 제공한다.**
- 프로젝트 루트는 app/ 디렉토리이다.


반환 형식:
{{
  "task_id": "",
  "result": "passed | failed",
  "issues": [
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
