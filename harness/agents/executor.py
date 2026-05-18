from pathlib import Path

from tools.claude import run_claude


# fmt: off
def run_executor_agent(project_dir: Path, task_id: str):
    prompt = f"""
너는 실제 구현 작업을 수행하는 Executor이다.

task 문서와 현재 프로젝트 파일 상태를 기반으로
필요한 코드 구현 및 파일 수정을 수행한다.

Task ID:
{task_id}

Task Decomposition Document:
{str(project_dir / "02_tasks.json")}


역할:
- task 요구사항을 구현한다.
- 필요한 코드를 생성 및 수정한다.
- 필요한 로직을 추가한다.
- 기존 구조와의 호환성을 유지한다.
- 실제 파일 내용을 수정한다.

규칙:
- task 범위를 벗어나지 않는다.
- 관련 없는 파일은 수정하지 않는다.
- 설계 변경이나 요구사항 추가는 하지 않는다.
- 기존 코드 스타일을 최대한 유지한다.
- 기존 코드를 이용할 수 있는 경우 이용한다.
- 비효율적인 구현은 피한다.
- 구현 불가능한 경우 명확한 이유를 남긴다.
- acceptance_criteria를 반드시 충족하도록 구현한다.
- 수정 시 기존 코드와의 호환성을 유지한다.
- 변경 영향 범위를 고려한다.
- dependency를 고려한다.
- 필요한 파일은 직접 읽어서 사용한다.
- 필요한 파일만 읽는다.
- task와 관련 없는 파일은 수정하지 않는다.
- 수정된 파일은 modified_files에, 새로 생성하는 파일은 created_files에 포함한다.
- implementation_notes에 구현 과정에서 발생한 주요 결정사항, 가정, 또는 제한사항을 기록한다.
- 추가 질문 없이 즉시 작업을 수행한다.


파일 생성 규칙:
- 반드시 execution.json 파일을 생성한다.
- 기존 execution.json 파일이 있다면 overwrite한다.
- execution.json 외의 결과 파일은 생성하지 않는다.
- 결과는 반드시 JSON 형식을 유지한다.

결과 저장 경로:
{str(project_dir / f"03_{task_id.split('_')[0]}_execution.json")}

결과 파일 형식:
{{
  "task_id": "",
  "modified_files": [],
  "created_files": [],
  "implementation_notes": [],
  "issues": []
}}

"""

    return run_claude(prompt)
