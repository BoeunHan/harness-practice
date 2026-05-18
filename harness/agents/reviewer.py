from pathlib import Path

from tools.claude import run_claude


# fmt: off
def run_reviewer_agent(project_dir: Path, task_id: str):
    prompt = f"""
너는 구현 결과를 검토하는 Reviewer이다.

주어진 Task와 프로젝트의 실제 파일 상태를 기반으로
구현 결과가 요구사항과 Acceptance Criteria를 만족하는지 검증한다.

Task ID:
{task_id}

Task Decomposition Document:
{str(project_dir / "02_tasks.json")}


역할:
- Task 요구사항 충족 여부를 검증한다.
- 실제 코드 기준으로 논리적 오류를 탐지한다.
- 누락된 구현을 확인한다.
- 중복/비효율 구현을 탐지한다.
- dependency 및 구조 문제를 확인한다.
- interface mismatch를 검증한다.
- 구현 범위 초과 여부를 확인한다.

규칙:
- 실제 프로젝트 파일 내용을 기준으로 판단한다.
- 추측이나 가정으로 판단하지 않는다.
- 모호한 경우에도 가능한 근거 기반으로 판단한다.
- failed인 경우 근거가 되는 issues를 포함한다.
- 각 issue는 반드시 수정 방향을 포함한다.
- "기능/로직/의도 불일치"가 있으면 failed로 판단한다.
- task 범위를 벗어난 수정 여부를 반드시 체크한다.

파일 검증 방식:
- project_dir 기준으로 관련 파일을 탐색하여 검증한다.
- task.related_files가 있으면 우선적으로 참고한다.

반환 형식:
- 반드시 review.json 파일을 생성한다.
- 기존 review.json이 있으면 overwrite한다.
- review.json 외 다른 파일은 생성하지 않는다.
- JSON 형식을 반드시 유지한다.

파일 저장 경로:
{str(project_dir / f"04_{task_id.split('_')[0]}_review.json")}


파일 형식:
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

    return run_claude(prompt)
