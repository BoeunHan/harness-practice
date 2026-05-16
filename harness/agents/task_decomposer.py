from tools.claude import run_claude


# fmt: off
def task_decomposer_agent(plan: dict) -> dict:
    prompt = f"""
너는 작업을 실행 가능한 단위로 분해하는 Task Decomposer Agent이다.
설계 문서를 기반으로 실제 실행 가능한 task 목록으로 분해한다.

Plan:
{plan}

역할:
- 작업을 작은 단위로 분리한다.
- task 간 dependency를 정의한다.
- 안전한 실행 순서대로 정렬한다.
- 각 task별 관련 파일을 연결한다.

규칙:
- 각 task는 하나의 명확한 목적을 가진 논리적 변경 단위여야 한다.
- 각 task는 여러 파일을 포함할 수 있다.
- 하나의 task 내의 모든 변경은 하나의 목적을 위해 존재해야 한다.
- task는 가능한 한 독립적이어야 한다.
- dependency cycle을 만들지 않는다.
- 지나치게 거대한 task를 만들지 않는다.
- 실행 가능한 수준까지 구체화한다.
- 결과는 JSON 형식으로 반환한다.

반환 형식:
{{
  "tasks": [
    {{
      "id": "",
      "description": "",
      "dependencies": [],
      "related_files": [],
      "acceptance_criteria": []
    }}
  ],
}}

"""

    return run_claude(prompt)
