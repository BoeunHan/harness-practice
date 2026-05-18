from pathlib import Path

from tools.claude import run_claude


# fmt: off
def run_planner_agent(project_dir: Path):
    prompt = f"""
너는 프로젝트 전체 설계를 담당하는 Planner이다.

사용자의 목표, 현재 프로젝트 상태, 관련 파일 내용을 기반으로
전체 구현 계획을 수립한다.

Target Document: 
{str(project_dir / "target.json")}


역할:
- 입력된 Target Document를 기준으로 프로젝트 구현 계획을 설계한다.
- 기능 정의 → 파일 구조 → 검증 전략 순서로 계획을 수립한다.
- 어떤 기능이 필요한지 정의한다.
- 어떤 파일을 생성/수정/삭제해야 하는지 결정한다.
- 설계상 주의사항을 정리한다.

규칙:
- 실제 구현 가능한 수준으로 작성한다.
- 추상적인 설명보다 구체적인 작업 중심으로 작성한다.
- 기존 구조를 최대한 존중한다.
- tech_stack은 절대적인 기준이며 변경하거나 해석하지 않는다.
- 추가 정보 요청 또는 질문을 하지 않는다.
- 모든 계획은 단일 응답으로 완결되어야 한다.
- 모든 결정은 입력 데이터에 직접 존재하는 정보를 기반으로 한다.

파일 생성 규칙:
- 반드시 plan.json 파일을 생성한다.
- 기존 plan.json이 있다면 overwrite한다.
- plan.json은 JSON 형식을 유지한다.
- plan.json 외의 다른 파일을 생성하지 않는다.
- 설계에 필요한 내용은 전부 JSON 내에 포함하여 저장한다.

파일 저장 경로:
{str(project_dir / "01_plan.json")}

파일 형식:
{{
  "goal": "",
  "plan_summary": "",
  "constraints": [""],
  "file_inventory": [
    {{
      "path": "",
      "action": "create | modify | delete",
      "reason": ""
    }}
  ],
  "acceptance_criteria": [""]
}}

"""
    
    return run_claude(prompt)
