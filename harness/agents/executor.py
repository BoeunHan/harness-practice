import json

from tools.claude import run_claude


# fmt: off
def executor_agent(task: dict, file_contents: list[dict]) -> dict:
    prompt = f"""
너는 실제 구현을 수행하는 Executor Agent이다.

주어진 task와 관련 파일 내용을 기반으로
필요한 코드 수정 또는 생성 작업을 수행한다.

Current Task:
{task}

File Contents:
{file_contents}

역할:
- task 요구사항을 구현한다.
- 코드를 생성 및 수정한다.
- 필요한 로직을 추가한다.
- 기존 구조와의 호환성을 유지한다.

규칙:
- task 범위를 벗어나지 않는다.
- 관련 없는 파일은 수정하지 않는다.
- 설계 변경이나 요구사항 추가는 하지 않는다.
- 기존 코드 스타일을 최대한 유지한다.
- 기존 코드를 이용할 수 있는 경우 이용한다.
- 비효율적인 구현은 피한다.
- 구현 불가능한 경우 명확한 이유를 반환한다.
- 명시되지 않은 요구사항은 최소한의 안전한 가정만 사용한다.
- 결과는 JSON 형식으로 반환한다.
- 수정 시 기존 코드와의 호환성을 유지하며, 변경 영향 범위를 고려한다.
- 파일 수정 시 전체 파일 내용을 기준으로 반환한다.
- 부분 patch가 아닌 완전한 파일 콘텐츠를 제공한다.
- acceptance_criteria를 반드시 충족하도록 구현한다.
- 기존 파일은 modified_files에, 새로 생성하는 파일은 created_files에 포함한다.
- implementation_notes에 구현 과정에서 발생한 주요 결정사항, 가정, 또는 제한사항을 기록한다.
- file path는 프로젝트 루트 기준 상대 경로로 제공한다.

반환 형식:
{{
  "task_id": "",
  "task_summary": "",
  "modified_files": [
    {{
      "path": "",
      "content": ""
    }}
  ],
  "created_files": [
    {{
      "path": "",
      "content": ""
    }}
  ],
  "cleanup_candidates": [],
  "implementation_notes": []
}}

"""

    return json.loads(run_claude(prompt))
