from pathlib import Path

from tools.claude import run_claude


# fmt: off
def run_task_decomposer_agent(project_dir: Path):
    prompt = f"""
너는 작업을 실행 가능한 단위로 분해하는 Task Decomposer이다.

설계 문서를 기반으로 실제 실행 가능한 task 목록으로 분해한다.

Plan Document:
{str(project_dir / "01_plan.json")}


역할:
- 설계 문서를 읽고 작업을 작은 단위로 분리한다.
- task 간 dependency를 정의한다.
- 안전한 실행 순서대로 정렬한다.
- 각 task별 관련 파일을 연결한다.
- 실행 가능한 수준까지 task를 구체화한다.

규칙:
- 각 task는 하나의 명확한 목적을 가진 논리적 변경 단위여야 한다.
- 각 task는 여러 파일을 포함할 수 있다.
- task는 코드 또는 설정 파일의 변경이 발생하는 작업만 포함한다.
- 실행 명령(npm install, npm run dev, build, typecheck 등)은 task에 포함하지 않는다.
- 하나의 task 내의 모든 변경은 하나의 목적을 위해 존재해야 한다.
- task는 가능한 한 독립적이어야 한다.
- dependency cycle을 만들지 않는다.
- dependency는 "실행 순서상 반드시 필요한 경우만" 정의한다.
- 모든 task에 dependency를 강제하지 않는다.
- task는 "하나의 파일 변경"이 아니라 "하나의 기능/환경 설정 단위"여야 한다.
- task는 최소 2~5개의 파일 변경을 포함하는 수준으로 묶는다.
- target의 목표가 누락 없이 반영되도록 한다.
- 구현 명세는 가이드로 사용할 수 있도록 구체적으로 작성한다.
- 모든 Task id는 다음 형식을 따른다:
  t{{숫자}}_{{설명}}
  예:
  t1_initialize_project
  t2_setup_typescript

파일 생성 규칙:
- 반드시 tasks.json 파일을 생성한다.
- 기존 tasks.json 파일이 있다면 overwrite한다.
- tasks.json 외의 다른 파일은 생성하지 않는다.
- 모든 결과는 JSON 내부에 포함한다.
- JSON 형식을 반드시 유지한다.
- 추가 질문 없이 즉시 작업을 수행한다.

파일 저장 경로:
{str(project_dir / "02_tasks.json")}

파일 형식:
{{
  "tasks": [
    {{
      "id": "",
      "description": "",
      "dependencies": [],
      "related_files": [],
      "implementation_details": [],
      "acceptance_criteria": []
    }}
  ]
}}


"""

    return run_claude(prompt)
